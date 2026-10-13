"""Source-attested 59C recipe; author checks are not pool qualification."""
import itertools
import random
import re
import string

IDS = ('59C',)
SEMANTICS = {
    '59C': 'Public English statement: k=1..26; two lines k and a template of '
    '1..100 characters from the first k lowercase Latin letters or ?. Replace '
    'only ? to obtain a palindrome containing every allowed letter, choosing '
    'the unique lexicographic minimum, or IMPOSSIBLE. Mirror fixed letters; '
    'put missing letters in ascending order in the rightmost free mirror '
    'groups (including the center), filling earlier groups with a. Exhaustive '
    'literal full-string substitutions independently check small cases.',
}


def _check_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _check_pid(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    lines = [line.split() for line in text.splitlines()]
    if len(lines) != 2 or [len(line) for line in lines] != [1, 1]:
        raise ValueError('expected exactly two lines: k, then template')
    token, word = lines[0][0], lines[1][0]
    if not re.fullmatch(r'[0-9]+', token):
        raise ValueError('invalid integer token')
    k = int(token)
    if not 1 <= k <= 26:
        raise ValueError('k outside 1..26')
    if not 1 <= len(word) <= 100 or set(word) - set(string.ascii_lowercase[:k] + '?'):
        raise ValueError('invalid template length/alphabet')
    return k, word


def answer(pid, data):
    _check_pid(pid)
    k, word = data
    result = list(word)
    free = []
    present = set()
    for i in range((len(result) + 1) // 2):
        j = len(result) - 1 - i
        left, right = result[i], result[j]
        if left == right == '?':
            free.append((i, j))
        elif left != '?' and right != '?' and left != right:
            return ['IMPOSSIBLE']
        else:
            letter = right if left == '?' else left
            result[i] = result[j] = letter
            present.add(letter)
    missing = [c for c in string.ascii_lowercase[:k] if c not in present]
    if len(missing) > len(free):
        return ['IMPOSSIBLE']
    letters = ['a'] * (len(free) - len(missing)) + missing
    for (i, j), letter in zip(free, letters):
        result[i] = result[j] = letter
    return [''.join(result)]


def _literal_brute(k, word):
    alphabet = string.ascii_lowercase[:k]
    holes = [i for i, c in enumerate(word) if c == '?']
    best = None
    for replacements in itertools.product(alphabet, repeat=len(holes)):
        candidate = list(word)
        for i, letter in zip(holes, replacements):
            candidate[i] = letter
        candidate = ''.join(candidate)
        if candidate == candidate[::-1] and set(candidate) == set(alphabet):
            if best is None or candidate < best:
                best = candidate
    return best if best is not None else 'IMPOSSIBLE'


def brute_checks():
    count = 0
    for k in range(1, 4):
        for length in range(1, 7):
            for template in itertools.product(string.ascii_lowercase[:k] + '?', repeat=length):
                word = ''.join(template)
                expected = _literal_brute(k, word)
                assert answer('59C', (k, word)) == [expected], (k, word, expected)
                count += 1
    rng = random.Random(59001600)
    for _ in range(300):
        k = rng.randint(1, 5)
        word = ''.join(rng.choice(string.ascii_lowercase[:k] + '?')
                       for _ in range(rng.randint(1, 8)))
        if word.count('?') > 5:
            word = word.replace('?', 'a', word.count('?') - 5)
        expected = _literal_brute(k, word)
        assert answer('59C', (k, word)) == [expected], (k, word, expected)
        count += 1
    return {'59C': count}


def extras(pid):
    _check_pid(pid)
    cases = []
    seen = set()

    def add(k, word, reason, category='adversarial'):
        text = f'{k}\n{word}\n'
        if text in seen:
            return
        seen.add(text)
        data = parse(pid, text)
        cases.append({'input': text, 'output': answer(pid, data)[0] + '\n',
                      'reason': reason, 'category': category})

    for k, word in [(1, '?'), (1, 'a'), (1, '??'), (2, '?'), (2, 'a'),
                    (2, 'ab'), (2, 'aa'), (2, 'aba'), (2, 'abba'), (3, 'a?c')]:
        add(k, word, 'minimum sizes, fixed conflict, or absent required letter', 'boundary')
    for k, word in [(2, '???'), (2, '?a?'), (3, '??b??'), (3, '?b?b?'),
                    (3, 'abcba'), (3, 'ab?ba'), (2, '??????'), (3, '???????'),
                    (2, '?b?a'), (2, 'a??a'), (3, '?a????a?'), (3, 'ac??ca')]:
        add(k, word, 'center is one usable group; propagate fixed mirrors before '
            'coverage; reserve inner free groups to minimize the prefix')
    for k in range(1, 27):
        add(k, '?' * (2 * k - 1), 'odd minimum number of mirror groups to cover all k letters', 'boundary')
        add(k, '?' * (2 * k), 'even minimum number of mirror groups to cover all k letters', 'boundary')
        if k > 1:
            add(k, '?' * (2 * k - 2), 'one too few distinct mirror groups', 'boundary')
    for k, word in [(1, '?' * 100), (26, '?' * 100), (26, '?' * 99),
                    (26, 'abcdefghijklmnopqrstuvwxyz' + '?' * 74),
                    (26, 'z' + '?' * 98 + 'a'), (26, 'a' * 100),
                    (2, '?' * 49 + 'bb' + '?' * 49)]:
        add(k, word, 'legal maximum-length or adjacent odd-length template; '
            'slack, full alphabet, forced mirrors, conflict and missing coverage', 'maxSize')
    rng = random.Random(591600)
    while len(cases) < 135:
        k = rng.randint(1, 5)
        word = ''.join(rng.choice(string.ascii_lowercase[:k] + '?')
                       for _ in range(rng.randint(1, 9)))
        add(k, word, 'fixed-seed small arbitrary templates including impossible conflicts')
    while len(cases) < 160:
        k = rng.randint(1, 26)
        length = rng.randint(2 * k - 1, 98)
        groups = list(string.ascii_lowercase[:k])
        groups += [rng.choice(string.ascii_lowercase[:k])
                   for _ in range((length + 1) // 2 - k)]
        rng.shuffle(groups)
        half = ''.join(groups)
        palindrome = half + (half[:-1] if length % 2 else half)[::-1]
        word = ''.join('?' if rng.randrange(3) else c for c in palindrome)
        add(k, word, 'fixed-seed feasible templates masked from full-alphabet palindromes')
    return cases


def review(pid, tests, samples):
    _check_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            actual = pair['output'].split()
            if actual != expected:
                failures.append({'test': name, 'reason': 'oracle output differs from supplied bytes',
                                 'expected': expected, 'actual': actual})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
