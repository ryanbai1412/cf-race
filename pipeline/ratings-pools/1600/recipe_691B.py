"""691B s-palindrome: mirror-table oracle, line-strict parser, exhaustive and generative cross-checks."""
import itertools
import random
import re
import string

IDS = ('691B',)
SEMANTICS = {
    '691B': 'One line holding s, 1<=|s|<=1000 English letters. TAK iff for every i the pair (s[i], s[n-1-i]) is a '
            'vertical-axis mirror pair in the statement image (espresso.codeforces.com/baf8111c...png): self-mirror '
            'AHIMOoTUVvWwXxY, cross pairs b<->d and p<->q; everything else NIE. Image-derived table agrees with all '
            '12 selected CF-OK sources and all 160 available official/sample pairs, which pin every visually '
            'ambiguous letter (m, n, u, i, l, s, S, Z, N, y ...). Unique literal TAK/NIE output. Oracle checks pairs '
            'with a mirror dict; the brute compares against a position-indexed mirror alphabet transcribed '
            'independently and against exhaustive generation of all s-palindromes from their first halves.',
}

SELF = frozenset('AHIMOoTUVvWwXxY')
CROSS = {'b': 'd', 'd': 'b', 'p': 'q', 'q': 'p'}
MIRROR = {**{c: c for c in SELF}, **CROSS}
LETTERS = string.ascii_letters
LINE = re.compile(r'[A-Za-z]{1,1000}(\r?\n)?')


def parse(pid, text):
    if pid != '691B':
        raise ValueError('unknown problem ' + pid)
    if not LINE.fullmatch(text):
        raise ValueError('expected exactly one line of 1..1000 English letters')
    return text.rstrip('\r\n')


def answer(pid, data):
    s = data
    n = len(s)
    return 'TAK' if all(MIRROR.get(s[i]) == s[n - 1 - i] for i in range((n + 1) // 2)) else 'NIE'


TABLE_UPPER = 'A......HI...M.O....TUVWXY.'
TABLE_LOWER = '.d.b..........oqp....vwx..'


def table_mirror(c):
    image = (TABLE_UPPER[ord(c) - 65] if c.isupper() else TABLE_LOWER[ord(c) - 97])
    return None if image == '.' else image


def brute(pid, data):
    reflected = []
    for c in reversed(data):
        image = table_mirror(c)
        if image is None:
            return 'NIE'
        reflected.append(image)
    return 'TAK' if ''.join(reflected) == data else 'NIE'


def all_s_palindromes(alphabet, n):
    images = [(c, table_mirror(c)) for c in alphabet if (table_mirror(c) or '.') in alphabet]
    centers = [c for c, image in images if image == c]
    found = set()
    for half in itertools.product(images, repeat=n // 2):
        left = ''.join(c for c, _ in half)
        right = ''.join(image for _, image in reversed(half))
        for middle in (centers if n % 2 else ['']):
            found.add(left + middle + right)
    return found


def brute_checks():
    count = 0
    for n in (1, 2, 3):
        palindromes = all_s_palindromes(LETTERS, n)
        for chars in itertools.product(LETTERS, repeat=n):
            s = ''.join(chars)
            expected = 'TAK' if s in palindromes else 'NIE'
            assert answer('691B', s) == expected == brute('691B', s), s
            count += 1
    alphabet = 'AbdmnpquwiS'
    for n in (4, 5):
        palindromes = all_s_palindromes(alphabet, n)
        for chars in itertools.product(alphabet, repeat=n):
            s = ''.join(chars)
            expected = 'TAK' if s in palindromes else 'NIE'
            assert answer('691B', s) == expected == brute('691B', s), s
            count += 1
    assert len(all_s_palindromes(LETTERS, 1)) == 15 and len(all_s_palindromes(LETTERS, 2)) == 19
    rng = random.Random(6910002)
    for _ in range(3000):
        n = rng.randint(1, 60)
        s = ''.join(rng.choice(LETTERS if rng.random() < 0.3 else 'AHIMOoTUVvWwXxYbdpqmnuiS') for _ in range(n))
        assert answer('691B', s) == brute('691B', s), s
        count += 1
    return {'691B': count}


def mirror_half(rng, length, centers=tuple(sorted(SELF))):
    half = [rng.choice(sorted(MIRROR)) for _ in range(length // 2)]
    middle = [rng.choice(centers)] if length % 2 else []
    return ''.join(half) + ''.join(middle) + ''.join(MIRROR[c] for c in reversed(half))


def extras(pid):
    if pid != '691B':
        raise ValueError('unknown problem ' + pid)
    rng = random.Random(6910001)
    cases = []
    seen = set()

    def add(s, reason, category='adversarial'):
        text = s + '\n'
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': answer(pid, parse(pid, text)) + '\n', 'reason': reason, 'category': category})

    for c in LETTERS:
        add(c, 'single letter: centre must be self-mirror (b/d/p/q and m/n/u/i are not)', 'boundary')
    for s in ('bd', 'db', 'pq', 'qp', 'bb', 'dd', 'pp', 'qq', 'AA', 'oo', 'BD', 'PQ', 'bp', 'dq', 'LJ', 'JL',
              'Pq', 'pQ', 'Bd', 'mm', 'nn', 'uu', 'ii', 'yy', 'NN', 'zz', 'SS'):
        add(s, 'length-2 pair: cross mirrors only lowercase b/d and p/q; equal letters need self-mirror', 'boundary')
    for s in ('AbA', 'odo', 'HpH', 'XqX', 'bod', 'dob', 'pOq', 'qxp', 'bAd', 'AmA', 'onO', 'xux', 'oio', 'WyW'):
        add(s, 'odd-length centre letter must itself be self-mirror; WA sources skip or mis-classify the centre')
    for s in ('oXXo', 'HAAH', 'bxxd', 'pood', 'bAAd', 'qMMp', 'WvvW', 'AAWW', 'AHHA', 'AH', 'AHA', 'HAeH', 'HeAH',
              'bbdd', 'bdbd', 'dbdb', 'pqpq', 'qqpp'):
        add(s, 'even-length TAK/NIE, self-mirror letters at unmatched positions, last pair before centre')
    for s in ('AmmA', 'mAm', 'nAn', 'uAu', 'iAi', 'NAN', 'yAy', 'LAJ', 'JAL', 'PAq', 'pAq', 'qAq', 'dAd'):
        add(s, 'letters selected WA sources wrongly accept (m, n, u, i, N, y, L/J, P, q:q)')
    add('A' * 1000, 'maximum length all self-mirror', 'maxSize')
    add('b' * 500 + 'd' * 500, 'maximum length cross pairs', 'maxSize')
    add('p' * 500 + 'q' * 500, 'maximum length p/q cross pairs', 'maxSize')
    add('A' * 999, 'maximum odd length, self-mirror centre', 'maxSize')
    add('A' * 499 + 'b' + 'A' * 499, 'maximum odd length, non-self-mirror centre', 'maxSize')
    add('b' * 1000, 'maximum length equal non-self-mirror letters', 'maxSize')
    add('m' * 1000, 'maximum length visually-ambiguous m', 'maxSize')
    add('z' * 1000, 'maximum length of z', 'maxSize')
    for _ in range(6):
        add(mirror_half(rng, 1000), 'maximum length random s-palindrome', 'maxSize')
    for _ in range(4):
        add(mirror_half(rng, 999), 'maximum odd length random s-palindrome', 'maxSize')
    for position in (0, 1, 499, 500, 998, 999):
        s = list(mirror_half(rng, 1000))
        s[position] = rng.choice([c for c in LETTERS if c != s[position] and c not in SELF])
        add(''.join(s), 'maximum length s-palindrome broken at position %d' % position, 'maxSize')
    s = list(mirror_half(rng, 999))
    s[499] = 'm'
    add(''.join(s), 'maximum odd length broken only at the centre', 'maxSize')
    add(''.join(rng.choice(LETTERS) for _ in range(1000)), 'maximum length random letters', 'maxSize')
    for _ in range(12):
        add(mirror_half(rng, rng.randint(2, 60)), 'fixed-seed random s-palindrome')
    for _ in range(12):
        s = list(mirror_half(rng, rng.randint(2, 60)))
        position = rng.randrange(len(s))
        s[position] = rng.choice([c for c in LETTERS if c != s[position]])
        add(''.join(s), 'fixed-seed s-palindrome with one perturbed letter')
    for _ in range(5):
        s = ''.join(rng.choice('bdpqmnuiAHOo') for _ in range(rng.randint(1, 12)))
        add(s + s[::-1], 'fixed-seed plain palindrome over mirror-confusable letters')
    return cases


def review(pid, tests, samples):
    failures = []
    for name, pair in list(tests) + list(samples):
        try:
            expected = answer(pid, parse(pid, pair['input']))
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if pair['output'].split() != [expected]:
            failures.append({'test': name, 'reason': 'independent oracle disagreement',
                             'expected': expected, 'actual': pair['output'].split()[:3]})
    return failures
