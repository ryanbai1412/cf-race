"""Restore externally attested exponent markup, retaining exact original source bytes."""
import argparse
import hashlib
import json
from pathlib import Path
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


def normalize(pid):
    old, new, attestation = REPAIRS[pid]
    package = BASE / 'packages' / pid
    state = BASE / 'state' / pid / 'generate.json'
    generated = read_json(state)
    if generated['packageHash'] != digest(manifest(package)):
        raise ValueError('changed package before documented normalization')
    source_path = BASE / 'statement-sources' / (pid + '.json')
    source = read_json(source_path)
    if source['id'] != pid or source['content']['locale'] != 'en' or attestation not in source['content']['formatI']:
        raise ValueError('original English constraint attestation absent')
    statement = package / 'statement.html'
    original = statement.read_bytes()
    text = original.decode('utf-8')
    if new in text:
        return {'id': pid, 'status': 'already-normalized'}
    if text.count(old) != 1:
        raise ValueError('ambiguous or absent exponent-loss match')
    preserved = BASE / 'statement-sources' / (pid + '.original.html')
    if preserved.exists() and preserved.read_bytes() != original:
        raise ValueError('original statement preservation mismatch')
    preserved.write_bytes(original)
    statement.write_text(text.replace(old, new), encoding='utf-8')
    provenance = read_json(package / 'provenance.json')
    provenance['statementNormalization'] = {
        'reason': 'Pinned source flattened an exponent. Only its rendered exponent markup was restored from independently public original English statement; source row and all test bytes are unchanged.',
        'originalSha256': hashlib.sha256(original).hexdigest(),
        'normalizedSha256': hashlib.sha256(statement.read_bytes()).hexdigest(),
        'originalPath': 'statement-sources/' + preserved.name,
        'attestationPath': 'statement-sources/' + source_path.name,
        'attestationSha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
        'sourceUrl': source['sourceUrl'],
        'replacement': {'from': old, 'to': new},
    }
    write_json(package / 'provenance.json', provenance)
    generated['files'] = manifest(package)
    generated['packageHash'] = digest(generated['files'])
    write_json(state, generated)
    return {'id': pid, 'status': 'normalized-reexecution-required', 'packageHash': generated['packageHash']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='+', choices=REPAIRS, required=True)
    args = parser.parse_args()
    for pid in args.ids:
        print(json.dumps(normalize(pid), sort_keys=True), flush=True)
