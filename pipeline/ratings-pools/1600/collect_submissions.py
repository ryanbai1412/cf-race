"""Read pinned public shards, selecting deterministic distinct supported sources."""
import argparse
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import sys

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pool_contract import digest, read_json, write_json
from pool_sandbox import kind
from pool_sources import PINS, download, provenance, sha_file, tree


def platform_gap(row):
    language = row.get('programmingLanguage') or ''
    code = row.get('source') or ''
    if language.startswith('MS C++'):
        return 'unsupported-MSVC-toolchain'
    if re.search(r'%[^"\n]*I64', code):
        return 'unsupported-Windows-CRT-format'
    if re.search(r'\bfreopen\s*\(', code):
        return 'source-file-io-without-online-judge-macro'
    return None


def choose(rows):
    selected, seen, identities, counts = [], set(), set(), Counter()
    for row in sorted(rows, key=lambda r: int(r['submission_id'])):
        sha = hashlib.sha256(row['source'].encode()).hexdigest()
        group = 'accepted' if row['verdict'] == 'OK' else 'incorrect'
        if sha in seen or row['submission_id'] in identities or counts[group] >= (12 if group == 'accepted' else 20):
            continue
        seen.add(sha)
        identities.add(row['submission_id'])
        counts[group] += 1
        selected.append(row)
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache', required=True)
    parser.add_argument('--base', default=str(Path(__file__).resolve().parent))
    args = parser.parse_args()
    base = Path(args.base)
    inv = read_json(base / 'inventory.json')
    ids = sorted(i['sourceId'] for i in inv['items'] if not i['exclusions'])
    source_ids = pa.array(ids)
    entries = [e for prefix in ('data', 'selected_accepted', 'selected_incorrect')
               for e in tree('open-r1/codeforces-submissions', prefix) if e['path'].endswith('.parquet')]
    def scan(entry):
        source = provenance('open-r1/codeforces-submissions', entry)
        root = base / 'submissions' / entry['lfs']['oid']
        marker = root / 'complete.json'
        if marker.exists():
            prior = read_json(marker)
            if prior['source'] == source and prior['problemIds'] == ids and prior.get('recipeHash') == sha_file(Path(__file__)):
                if all(sha_file(root / f) == sha for f, sha in prior['files'].items()):
                    print('resume', entry['path'], flush=True)
                    return prior
                raise ValueError('changed submission index')
        path = download('open-r1/codeforces-submissions', entry, args.cache)
        groups, counters, exclusions = defaultdict(list), defaultdict(Counter), defaultdict(list)
        for batch in pq.ParquetFile(path).iter_batches(batch_size=4096):
            selected = batch.filter(pc.is_in(batch.column(batch.schema.get_field_index('problem_id')), value_set=source_ids))
            for row in selected.to_pylist():
                pid = row['problem_id']
                counters[pid]['rows'] += 1
                if row.get('testset') != 'TESTS':
                    counters[pid]['excluded-nonfinal'] += 1
                elif kind(row.get('programmingLanguage') or '') is None:
                    counters[pid]['excluded-language'] += 1
                elif not row.get('source'):
                    counters[pid]['excluded-empty-source'] += 1
                elif platform_gap(row):
                    reason = platform_gap(row)
                    counters[pid]['excluded-' + reason] += 1
                    exclusions[pid].append({'submissionId': row['submission_id'], 'sourceHash': hashlib.sha256(row['source'].encode()).hexdigest(),
                                            'language': row['programmingLanguage'], 'verdict': row['verdict'], 'reason': reason, 'source': source})
                elif row['verdict'] not in ('OK', 'WRONG_ANSWER', 'TIME_LIMIT_EXCEEDED'):
                    counters[pid]['excluded-verdict-' + str(row['verdict'])] += 1
                else:
                    counters[pid]['eligible-' + row['verdict']] += 1
                    row['provenance'] = source
                    groups[pid].append(row)
            for pid in groups:
                groups[pid] = choose(groups[pid])
        hashes = {}
        for pid, rows in sorted(groups.items()):
            name = pid.replace('/', '') + '.json'
            write_json(root / name, rows)
            hashes[name] = sha_file(root / name)
        value = {'source': source, 'problemIds': ids, 'files': hashes, 'recipeHash': sha_file(Path(__file__)),
                 'platformExclusions': {pid: sorted(rows, key=lambda r: int(r['submissionId'])) for pid, rows in sorted(exclusions.items())},
                 'counts': {pid: dict(c) for pid, c in sorted(counters.items())},
                 'selection': 'lowest submission IDs; unique source hashes; supported TESTS OK/WA/TLE; cap12accepted20incorrect per shard'}
        write_json(marker, value)
        print('scanned', entry['path'], sum(c['rows'] for c in counters.values()), flush=True)
        return value
    with ThreadPoolExecutor(max_workers=4) as executor:
        markers = list(executor.map(scan, entries))
    combined, totals, platform_exclusions = defaultdict(list), defaultdict(Counter), defaultdict(list)
    for marker in markers:
        root = base / 'submissions' / marker['source']['sha256']
        for name in marker['files']:
            for row in read_json(root / name):
                combined[row['problem_id']].append(row)
        for pid, counts in marker['counts'].items():
            totals[pid].update(counts)
        for pid, rows in marker['platformExclusions'].items():
            platform_exclusions[pid].extend(rows)
    files, candidates = {}, []
    for pid in ids:
        rows = choose(combined[pid])
        name = pid.replace('/', '') + '.json'
        write_json(base / 'submissions' / 'selected' / name, rows)
        write_json(base / 'submissions' / 'platform-exclusions' / name, sorted(platform_exclusions[pid], key=lambda r: int(r['submissionId'])))
        files[name] = sha_file(base / 'submissions' / 'selected' / name)
        accepted = sum(r['verdict'] == 'OK' for r in rows)
        incorrect = len(rows) - accepted
        candidates.append({'id': pid.replace('/', ''), 'sourceId': pid, 'acceptedSelected': accepted,
                           'incorrectSelected': incorrect, 'counts': dict(totals[pid]),
                           'blockers': [] if min(accepted, incorrect) >= 5 else ['insufficient-supported-distinct-5/5-sources']})
    report = {'pins': PINS, 'inventoryHash': digest(inv), 'recipeHash': sha_file(Path(__file__)), 'sourceFiles': [m['source'] for m in markers],
              'scope': 'all36default-plus-both-selected-submission-shards', 'selection': 'lowest distinct supported final submission IDs; cap12accepted20incorrect',
              'platformPolicy': 'Unmodified GNU-compatible stdio sources only; MSVC, Windows CRT I64 formats and freopen source file IO excluded before execution, never repaired.',
              'files': files, 'candidates': candidates,
              'fiveFiveSourceEligible': sum(not c['blockers'] for c in candidates), 'validatedCount': 0}
    write_json(base / 'submission-report.json', report)
    print(json.dumps({'metadataCandidates': len(ids), 'fiveFiveSourceEligible': report['fiveFiveSourceEligible'], 'validatedCount': 0}), flush=True)


if __name__ == '__main__':
    main()
