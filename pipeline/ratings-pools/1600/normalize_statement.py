"""Restore externally attested exponent markup, retaining exact original source bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import digest, manifest, read_json, write_json


REPAIRS = {
    '235A': ('≤ 106)', '≤ 10<sup>6</sup>)', '10^{6}'),
    '322B': ('≤ 109)', '≤ 10<sup>9</sup>)', '10^{9}'),
    '11B': ('- 109 ≤ x ≤ 109)', '- 10<sup>9</sup> ≤ x ≤ 10<sup>9</sup>)', '10<sup class="upper-index">9</sup>'),
    '40B': ('≤ 109)', '≤ 10<sup>9</sup>)', '10<sup class="upper-index">9</sup>'),
}

MULTI_REPAIRS = {
    '922C': [('≤ 1018)', '≤ 10<sup>18</sup>)', 1)],
    '599C': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '777C': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '898E': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '165C': [('≤ 106)', '≤ 10<sup>6</sup>)', 1), ('106 characters.', '10<sup>6</sup> characters.', 1)],
    '348A': [('≤ 105)', '≤ 10<sup>5</sup>)', 1), ('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '86A': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '373B': [('≤ 1016)', '≤ 10<sup>16</sup>)', 2), ('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '495B': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '597A': [('≤ 1018;', '≤ 10<sup>18</sup>;', 1),
             ('- 1018 ≤ a ≤ b ≤ 1018)', '- 10<sup>18</sup> ≤ a ≤ b ≤ 10<sup>18</sup>)', 1)],
}


def repair_spec(pid):
    if pid in REPAIRS:
        old, new, attestation = REPAIRS[pid]
        return [(old, new, 1)], [attestation]
    repairs = MULTI_REPAIRS[pid]
    exponents = {value for _, new, _ in repairs for value in re.findall(r'<sup>(\d+)</sup>', new)}
    return repairs, [f'10<sup class="upper-index">{value}</sup>' for value in sorted(exponents)]


def normalize(pid):
    repairs, attestations = repair_spec(pid)
    package = BASE / 'packages' / pid
    state = BASE / 'state' / pid / 'generate.json'
    generated = read_json(state)
    if generated['packageHash'] != digest(manifest(package)):
        raise ValueError('changed package before documented normalization')
    source_path = BASE / 'statement-sources' / (pid + '.json')
    source = read_json(source_path)
    if (source['id'] != pid or source['content']['locale'] != 'en'
            or any(value not in source['content']['formatI'] for value in attestations)):
        raise ValueError('original English constraint attestation absent')
    statement = package / 'statement.html'
    original = statement.read_bytes()
    text = original.decode('utf-8')
    if all(text.count(new) == count and old not in text for old, new, count in repairs):
        return {'id': pid, 'status': 'already-normalized'}
    if any(text.count(old) != count or new in text for old, new, count in repairs):
        raise ValueError('ambiguous or absent exponent-loss match')
    preserved = BASE / 'statement-sources' / (pid + '.original.html')
    if preserved.exists() and preserved.read_bytes() != original:
        raise ValueError('original statement preservation mismatch')
    preserved.write_bytes(original)
    normalized = text
    for old, new, _ in repairs:
        normalized = normalized.replace(old, new)
    statement.write_text(normalized, encoding='utf-8')
    provenance = read_json(package / 'provenance.json')
    provenance['statementNormalization'] = {
        'reason': 'Pinned source flattened an exponent. Only its rendered exponent markup was restored from independently public original English statement; source row and all test bytes are unchanged.',
        'originalSha256': hashlib.sha256(original).hexdigest(),
        'normalizedSha256': hashlib.sha256(statement.read_bytes()).hexdigest(),
        'originalPath': 'statement-sources/' + preserved.name,
        'attestationPath': 'statement-sources/' + source_path.name,
        'attestationSha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'sourceUrl': source['sourceUrl'],
        'replacements': [{'from': old, 'to': new, 'occurrences': count} for old, new, count in repairs],
    }
    write_json(package / 'provenance.json', provenance)
    generated['files'] = manifest(package)
    generated['packageHash'] = digest(generated['files'])
    write_json(state, generated)
    return {'id': pid, 'status': 'normalized-reexecution-required', 'packageHash': generated['packageHash']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', choices=tuple(REPAIRS) + tuple(MULTI_REPAIRS), required=True)
    args = parser.parse_args()
    for pid in args.ids:
        print(json.dumps(normalize(pid), sort_keys=True), flush=True)
