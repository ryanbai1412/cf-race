"""Deterministic, byte-complete owned-pool handoff without downloading shard archives."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import publication_gate


def sha(data):
    return hashlib.sha256(data).hexdigest()


def build(output, ids):
    paths = set(BASE.glob('*.py'))
    paths.update(BASE / name for name in ('inventory.json', 'api-problems.json',
                                        'submission-report.json', 'brute-report.json',
                                        'SIGNOFF-LEDGER.json', 'QUARANTINED-AUDITS.json'))
    paths.update(p for p in (BASE / 'audits').rglob('*') if p.is_file())
    paths.update(p for p in (BASE / 'evidence' / 'history').rglob('*') if p.is_file())
    paths.update(p for p in (BASE / 'audit-reports').rglob('*') if p.is_file())
    for pid in ids:
        paths.update((BASE / 'statement-sources').glob(f'{pid}*'))
        for category in ('packages', 'state'):
            paths.update(p for p in (BASE / category / pid).rglob('*') if p.is_file())
        for category in ('evidence', 'audits', 'semantic', 'coverage', 'extras', 'build-gaps', 'source-policies'):
            paths.update((BASE / category).glob(f'{pid}*.json'))
        for category in ('selected', 'platform-exclusions'):
            paths.add(BASE / 'submissions' / category / f'{pid}.json')
    contents = {}
    for path in sorted(paths):
        if path.is_symlink():
            raise ValueError('archive symlinks prohibited')
        if path.is_file() and not path.name.endswith('.partial'):
            contents['1600/' + path.relative_to(BASE).as_posix()] = path.read_bytes()
    manifest = {name: {'sha256': sha(data), 'bytes': len(data)} for name, data in contents.items()}
    validated = []
    for pid in ids:
        try:
            publication_gate(BASE / 'packages' / pid, BASE.parent, require_approval=False)
            validated.append(pid)
        except (OSError, ValueError, KeyError, RuntimeError):
            pass
    metadata = {'problemIds': sorted(ids), 'sourceCards': {
                    'statements': 'https://huggingface.co/datasets/open-r1/codeforces',
                    'submissions': 'https://huggingface.co/datasets/open-r1/codeforces-submissions'},
                'upstreamShards': 'Pinned shard URLs/checksums recorded in inventory and submission-report; shard binaries are not embedded.',
                'files': manifest, 'validatedCount': len(validated), 'validatedIds': sorted(validated),
                'notes': 'Archive contains current evidence and superseded diagnostics; archival completeness is not qualification.'}
    contents['1600/ARCHIVE-MANIFEST.json'] = (json.dumps(metadata, sort_keys=True, indent=2) + '\n').encode()
    with output.open('wb') as raw, gzip.GzipFile(fileobj=raw, filename='', mode='wb', mtime=0, compresslevel=1) as zipped, tarfile.open(fileobj=zipped, mode='w') as tar:
        for name, data in sorted(contents.items()):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = 0o644
            info.uid = info.gid = info.mtime = 0
            info.uname = info.gname = ''
            tar.addfile(info, io.BytesIO(data))
    provenance = {**metadata, 'archive': output.name, 'sha256': sha(output.read_bytes()), 'bytes': output.stat().st_size}
    output.with_name(output.name + '.provenance.json').write_text(json.dumps(provenance, sort_keys=True, indent=2) + '\n')
    with tarfile.open(output, 'r:gz') as tar:
        actual = {m.name: tar.extractfile(m).read() for m in tar.getmembers()}
    assert actual == contents
    return {'archive': str(output), 'sha256': provenance['sha256'], 'bytes': provenance['bytes'], 'fileCount': len(contents)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--ids', nargs='+')
    args = parser.parse_args()
    ids = args.ids or sorted(p.name for p in (BASE / 'packages').iterdir() if p.is_dir() and not p.name.endswith('.partial'))
    print(json.dumps(build(args.output, ids), sort_keys=True))
