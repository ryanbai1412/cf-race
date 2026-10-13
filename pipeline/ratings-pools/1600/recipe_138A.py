"""Literature Lesson recipe; author checks are not pool qualification."""
import itertools
import random
import re


IDS = ('138A',)
SEMANTICS = {
    '138A': 'n1..2500, k1..5; exactly 4n nonempty lowercase Latin lines, total length<=10000 (original English formatI: https://www.luogu.com.cn/problem/CF138A?lang=en, 10^{4}). Rhyme is equality of suffixes beginning at the kth vowel from the end; too few vowels never rhyme. Intersect stanza schemes, returning aaaa only when every stanza is pairwise rhyming. Two different pair schemes imply aaaa, so the required output is unique. Linear suffix oracle independently checked by longest-common-suffix pair comparisons.',
}
VOWELS = frozenset('aeiou')
SCHEMES = ('aabb', 'abab', 'abba')


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem id')


def parse(pid, text):
    _require_pid(pid)
    normalized = text.replace('\r\n', '\n')
    if '\r' in normalized:
        raise ValueError('invalid line ending')
    lines = normalized.split('\n')
    if lines[-1] == '':
        lines.pop()
    if not lines or len(lines[0].split()) != 2:
        raise ValueError('header arity')
    header = lines[0].split()
    if any(re.fullmatch(r'[0-9]+', value) is None for value in header):
        raise ValueError('header integers')
    n, k = map(int, header)
    if not 1 <= n <= 2500 or not 1 <= k <= 5:
        raise ValueError('header range')
    words = tuple(lines[1:])
    if len(words) != 4*n:
        raise ValueError('poem line layout')
    if any(re.fullmatch(r'[a-z]+', word) is None for word in words):
        raise ValueError('poem nonempty lowercase Latin lines')
    if sum(map(len, words)) > 10000:
        raise ValueError('poem total length')
    return k, words


def answer(pid, data):
    _require_pid(pid)
    k, words = data
    signatures = []
    for word in words:
        remaining = k
        for i in range(len(word)-1, -1, -1):
            remaining -= word[i] in VOWELS
            if remaining == 0:
                signatures.append(word[i:])
                break
        else:
            return 'NO'
    possible = set(SCHEMES)
    all_equal = True
    for offset in range(0, len(signatures), 4):
        a, b, c, d = signatures[offset:offset+4]
        all_equal &= a == b == c == d
        if not (a == b and c == d):
            possible.discard('aabb')
        if not (a == c and b == d):
            possible.discard('abab')
        if not (a == d and b == c):
            possible.discard('abba')
    if all_equal:
        return 'aaaa'
    return next((scheme for scheme in SCHEMES if scheme in possible), 'NO')


def _reference(data):
    k, words = data

    def rhyme(left, right):
        common_vowels = 0
        for a, b in zip(reversed(left), reversed(right)):
            if a != b:
                break
            common_vowels += a in 'aeiou'
        return common_vowels >= k

    pairs = {
        'aabb': ((0, 1), (2, 3)),
        'abab': ((0, 2), (1, 3)),
        'abba': ((0, 3), (1, 2)),
    }
    valid = [scheme for scheme, edges in pairs.items()
             if all(rhyme(words[start+i], words[start+j])
                    for start in range(0, len(words), 4) for i, j in edges)]
    if len(valid) == 3:
        return 'aaaa'
    if len(valid) == 1:
        return valid[0]
    if not valid:
        return 'NO'
    raise AssertionError('two schemes force all three')


def _poem(k, words):
    return f'{len(words)//4} {k}\n' + '\n'.join(words) + '\n'


def extras(pid):
    _require_pid(pid)
    cases, seen = [], set()

    def add(k, words, reason, category='adversarial'):
        text = _poem(k, words)
        if text not in seen:
            seen.add(text)
            cases.append({'input': text, 'output': answer(pid, (k, words))+'\n',
                          'reason': reason, 'category': category})

    def stanza(scheme, k, x='x', y='y'):
        return [prefix + 'a'*k + (x if label == 'a' else y)
                for prefix, label in zip(('b', 'c', 'd', 'f'), scheme)]

    for k in range(1, 6):
        add(k, ['a'*k]*4, 'Minimum n and exact kth vowel; aaaa precedence.', 'boundary')
        for missing in range(4):
            words = ['a'*k]*4
            words[missing] = 'a'*(k-1) if k > 1 else 'b'
            add(k, words, f'Line {missing+1} has too few vowels; empty suffixes must not rhyme.')
        for scheme in (*SCHEMES, 'aaaa'):
            add(k, stanza(scheme, k), 'Different consonant prefixes are outside the rhyme suffix.')
        add(k, ['a'*k+'x', 'a'*k+'y', 'a'*k+'z', 'a'*k+'w'],
            'Same vowel sequence but different trailing consonants: not rhyming.')
        add(k, ['aeiou'+prefix+'a'*k+'z' for prefix in ('b', 'c', 'd', 'f')],
            'Extra vowels before the kth-from-end vowel do not belong to the suffix.')
    for k in (1, 2, 5):
        for first, second in itertools.permutations(SCHEMES, 2):
            add(k, stanza(first, k)+stanza(second, k, 's', 't'),
                'Each stanza rhymes, but their forced global schemes conflict.')
    for k in (1, 3, 5):
        for scheme in (*SCHEMES, 'aaaa'):
            add(k, stanza('aaaa', k)+stanza(scheme, k, 's', 't')+stanza('aaaa', k, 'v', 'w'),
                'aaaa is neutral; stanzas need not rhyme with other stanzas.')
    for k in (1, 2):
        add(k, ['commit', 'hermit', 'commit', 'hermit'],
            'Statement example changes rhyme when k changes.')
    add(1, ['b']*4, 'Identical vowelless lines cannot rhyme.')
    for scheme in (*SCHEMES, 'aaaa'):
        words = [('a' if label == 'a' else 'e') for label in scheme]*2500
        add(1, words, 'Maximum n=2500 and total length=10000.', 'maxSize')
    add(1, ['b']*10000, 'Maximum dimension with all vowels absent.', 'maxSize')
    add(1, list('aaee')*2499+list('aeae'), 'Only the last of 2500 stanzas conflicts.', 'maxSize')
    add(1, ['b'*2499+'a']*4, 'One stanza, total length=10000, longest common suffix.', 'maxSize')
    add(5, ['aeiou']*2000, 'k=5 and total length=10000; exactly five vowels per line.', 'maxSize')
    rng = random.Random(138)
    index = 0
    while len(cases) < 160:
        k, n = rng.randint(1, 5), rng.randint(1, 6)
        if index % 2:
            scheme = rng.choice((*SCHEMES, 'aaaa'))
            words = []
            for _ in range(n):
                x, y = rng.sample(('x', 'z', 's', 't', 'v'), 2)
                words.extend(stanza(rng.choice((scheme, 'aaaa')), k, x, y))
        else:
            words = [''.join(rng.choice('abcdeiouxyz') for _ in range(rng.randint(1, 20)))
                     for _ in range(4*n)]
        add(k, words, f'Fixed-seed small random poem {index}: global intersection and suffix scan.')
        index += 1
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                errors.append({'test': name, 'reason': 'exact oracle disagreement',
                               'expected': expected, 'actual': pair['output']})
        except ValueError as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors


def brute_checks():
    count = 0

    def check(data):
        nonlocal count
        got, expected = answer('138A', data), _reference(data)
        if got != expected:
            raise AssertionError((data, got, expected))
        count += 1

    words = [''.join(chars) for size in (1, 2) for chars in itertools.product('ab', repeat=size)]
    for stanza in itertools.product(words, repeat=4):
        for k in range(1, 6):
            check((k, stanza))
    stanzas = list(itertools.product(('a', 'e', 'b'), repeat=4))
    for first, second in itertools.product(stanzas, repeat=2):
        check((1, first+second))
    rng = random.Random(1380138)
    for _ in range(500):
        words = tuple(''.join(rng.choice('abcdefghijklmnopqrstuvwxyz')
                              for _ in range(rng.randint(1, 30)))
                      for _ in range(4*rng.randint(1, 4)))
        check((rng.randint(1, 5), words))
    for case in extras('138A'):
        check(parse('138A', case['input']))
    return {'138A': count}
