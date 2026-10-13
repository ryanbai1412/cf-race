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
    '34D': [('≤ 5·104,', '≤ 5·10<sup>4</sup>,', 1)],
    '756B': [('≤ 105)', '≤ 10<sup>5</sup>)', 1), ('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '788A': [('≤ 105)', '≤ 10<sup>5</sup>)', 1), ('-109 ≤ ai ≤ 109)', '-10<sup>9</sup> ≤ ai ≤ 10<sup>9</sup>)', 1)],
    '209A': [('≤ 106)', '≤ 10<sup>6</sup>)', 1)],
    '337C': [('≤ 109;', '≤ 10<sup>9</sup>;', 1)],
    '343A': [('≤ 1018)', '≤ 10<sup>18</sup>)', 1)],
    '440B': [('exceed 109,', 'exceed 10<sup>9</sup>,', 1)],
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
    '244B': [('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '317A': [('- 1018 ≤ x, y, m ≤ 1018)', '- 10<sup>18</sup> ≤ x, y, m ≤ 10<sup>18</sup>)', 1)],
    '913C': [('≤ 109)', '≤ 10<sup>9</sup>)', 2), ('volume 2i - 1 liters', 'volume 2<sup>i - 1</sup> liters', 1)],
    '992B': [('≤ 109,', '≤ 10<sup>9</sup>,', 1), ('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '319A': [('2n members', '2<sup>n</sup> members', 2), ('0 to 2n - 1', '0 to 2<sup>n</sup> - 1', 1), ('(109 + 7)', '(10<sup>9</sup> + 7)', 2)],
    '23B': [('≤ 105)', '≤ 10<sup>5</sup>)', 2)],
    '71C': [('≤ 105)', '≤ 10<sup>5</sup>)', 1)],
    '246D': [('≤ 105)', '≤ 10<sup>5</sup>)', 2)],
    '407B': [('≤ 103)', '≤ 10<sup>3</sup>)', 1), ('(109 + 7)', '(10<sup>9</sup> + 7)', 1)],
    '525C': [('≤ 105)', '≤ 10<sup>5</sup>)', 1), ('≤ 106)', '≤ 10<sup>6</sup>)', 1)],
    '534C': [('≤ 2·105,', '≤ 2·10<sup>5</sup>,', 1), ('≤ 106)', '≤ 10<sup>6</sup>)', 1)],
    '476C': [('≤ 107)', '≤ 10<sup>7</sup>)', 1), ('(109 + 7)', '(10<sup>9</sup> + 7)', 2)],
    '735C': [('≤ 1018)', '≤ 10<sup>18</sup>)', 1)],
    '735D': [('≤ 2·109)', '≤ 2·10<sup>9</sup>)', 1)],
    '768B': [('&lt; 250,', '&lt; 2<sup>50</sup>,', 1), ('≤ 105,', '≤ 10<sup>5</sup>,', 1)],
    '817C': [('≤ 1018)', '≤ 10<sup>18</sup>)', 1)],
    '992C': [('≤ 1018)', '≤ 10<sup>18</sup>)', 1), ('modulo 109 + 7', 'modulo 10<sup>9</sup> + 7', 2)],
    '113A': [('does not exceed 105.', 'does not exceed 10<sup>5</sup>.', 1)],
    '150B': [('(109 + 7)', '(10<sup>9</sup> + 7)', 2)],
    '154A': [("The length of string s doesn't exceed 105.", "The length of string s doesn't exceed 10<sup>5</sup>.", 1)],
    '237C': [('≤ 106;', '≤ 10<sup>6</sup>;', 1)],
    '260B': [('105 characters.', '10<sup>5</sup> characters.', 1)],
    '272D': [('≤ 105)', '≤ 10<sup>5</sup>)', 1), ('≤ 109)', '≤ 10<sup>9</sup>)', 2), ('≤ 109 + 7)', '≤ 10<sup>9</sup> + 7)', 1)],
    '291C': [('≤ 105)', '≤ 10<sup>5</sup>)', 1)],
    '297B': [('≤ 105,', '≤ 10<sup>5</sup>,', 1), ('≤ 109)', '≤ 10<sup>9</sup>)', 1)],
    '333A': [('≤ 1017)', '≤ 10<sup>17</sup>)', 1)],
    '340C': [('(2 ≤ n ≤ 105)', '(2 ≤ n ≤ 10<sup>5</sup>)', 1), ('(1 ≤ ai ≤ 107)', '(1 ≤ ai ≤ 10<sup>7</sup>)', 1)],
    '364A': [('(0 ≤ a ≤ 109)', '(0 ≤ a ≤ 10<sup>9</sup>)', 1)],
}


def repair_spec(pid):
    if pid in REPAIRS:
        old, new, attestation = REPAIRS[pid]
        return [(old, new, 1)], [attestation]
    repairs = MULTI_REPAIRS[pid]
    powers = {power for _, new, _ in repairs for power in re.findall(r'(\d+)<sup>([^<]+)</sup>', new)}
    return repairs, [f'{base}<sup class="upper-index">{value}</sup>' for base, value in sorted(powers)]


def has_attestation(text, value):
    if value in text:
        return True
    power = re.fullmatch(r'(\d+)(?:<sup class="upper-index">([^<]+)</sup>|\^\{([^}]+)\})', value)
    if not power:
        return False
    base, html_power, tex_power = power.groups()
    exponent = html_power or tex_power
    if f'{base}^{{{exponent}}}' in text:
        return True
    return exponent.isdigit() and base + exponent.translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')) in text


def readable_sections(text):
    start = re.search(r'\noutput\n(?:standard output|stdout)\n', text)
    if not start:
        raise ValueError('readable statement body absent')
    body = text[start.end():]
    description, marker, rest = body.partition('\nInput\n')
    inputs, output_marker, rest = rest.partition('\nOutput\n')
    outputs, example_marker, _ = rest.partition('\nExamples\n')
    if not marker or not output_marker or not example_marker:
        raise ValueError('readable statement sections absent')
    return {'formatD': description.strip(), 'formatI': inputs.strip(), 'formatO': outputs.strip()}


def verify_attestations(source, repairs, attestations, captured=None):
    sections = readable_sections(captured) if captured is not None else source['content']
    if captured is not None and source.get('schemaVersion') == 2:
        if any(source['content'].get(key) != text for key, text in sections.items()):
            raise ValueError('public readable section extraction changed')
    if source['content']['locale'] != 'en':
        raise ValueError('original English constraint attestation absent')
    if captured is None and 'formatD' not in sections and 'formatO' not in sections:
        if any(not has_attestation(sections['formatI'], value) for value in attestations):
            raise ValueError('original English constraint attestation absent')
        return
    for old, new, _ in repairs:
        fields = ('formatI',) if any(s in old for s in ('≤', '&lt;', 'exceed', 'characters.')) else ('formatD', 'formatO')
        for base, exponent in re.findall(r'(\d+)<sup>([^<]+)</sup>', new):
            value = f'{base}<sup class="upper-index">{exponent}</sup>'
            if not any(has_attestation(sections.get(field, ''), value) for field in fields):
                raise ValueError('original English constraint attestation absent in required section')


def normalize(pid):
    repairs, attestations = repair_spec(pid)
    package = BASE / 'packages' / pid
    state = BASE / 'state' / pid / 'generate.json'
    generated = read_json(state)
    if generated['packageHash'] != digest(manifest(package)):
        raise ValueError('changed package before documented normalization')
    source_path = BASE / 'statement-sources' / (pid + '.json')
    source = read_json(source_path)
    captured_text = None
    if 'capturedTextSha256' in source:
        captured = (BASE / source['capturedTextPath']).read_bytes()
        captured_text = captured.decode('utf-8')
        recorded_text = source['content'].get('fullStatement', source['content']['formatI'])
        if (hashlib.sha256(captured).hexdigest() != source['capturedTextSha256']
                or captured_text.rstrip('\n') != recorded_text.rstrip('\n')):
            raise ValueError('public readable extraction attestation changed')
    if source['id'] != pid:
        raise ValueError('original English constraint attestation absent')
    verify_attestations(source, repairs, attestations, captured_text)
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
