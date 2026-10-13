"""Hometask (154A / 155C): minimum deletions removing adjacent forbidden letter pairs."""
import itertools
import random
import re
import string


IDS = ('154A',)
SEMANTICS = {
    '154A': 'Line 1: nonempty lowercase s, |s|<=10^5 (exponent attested from public English statement). Line 2: integer k 0..13. Next k lines: two different lowercase letters, every letter in at most one pair; pairs are unordered. '
            'Unique integer: minimum deletions so no forbidden pair is adjacent. Oracle: for every maximal run consisting only of the two letters of one pair, delete the rarer letter (min of the two counts); runs are independent because other letters are never worth deleting. '
            'Independently checked by exhaustive kept-subsequence enumeration and a separate last-kept-letter dynamic program.',
}

MAX_LENGTH = 100000
WORD = re.compile(r'[a-z]+')
COUNT = re.compile(r'0|[1-9][0-9]*')


def parse(pid, text):
    if pid not in IDS:
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) < 2:
        raise ValueError('hometask line layout')
    s, count = lines[0], lines[1]
    if not WORD.fullmatch(s) or len(s) > MAX_LENGTH:
        raise ValueError('sentence constraints')
    if not COUNT.fullmatch(count) or not 0 <= int(count) <= 13:
        raise ValueError('pair count constraints')
    k = int(count)
    if len(lines) != 2 + k:
        raise ValueError('hometask line layout')
    pairs = lines[2:]
    if any(len(p) != 2 or not WORD.fullmatch(p) or p[0] == p[1] for p in pairs):
        raise ValueError('pair constraints')
    letters = ''.join(pairs)
    if len(set(letters)) != len(letters):
        raise ValueError('letter repeated across pairs')
    return s, tuple(pairs)


def answer(pid, data):
    s, pairs = data
    partner = {}
    for a, b in pairs:
        partner[a], partner[b] = b, a
    total, i, n = 0, 0, len(s)
    while i < n:
        c = s[i]
        if c not in partner:
            i += 1
            continue
        group = (c, partner[c])
        first = second = 0
        while i < n and s[i] in group:
            if s[i] == c:
                first += 1
            else:
                second += 1
            i += 1
        total += min(first, second)
    return total


def forbidden(pairs):
    return {frozenset(p) for p in pairs}


def exhaustive(data):
    s, pairs = data
    bad = forbidden(pairs)
    n = len(s)
    for removed in range(n + 1):
        for gone in itertools.combinations(range(n), removed):
            gone = set(gone)
            kept = [c for i, c in enumerate(s) if i not in gone]
            if all(frozenset((x, y)) not in bad for x, y in zip(kept, kept[1:])):
                return removed
    raise AssertionError('removing every letter is always valid')


def last_kept_dp(data):
    s, pairs = data
    bad = forbidden(pairs)
    best = {None: 0}
    for c in s:
        keep = max(v + 1 for last, v in best.items() if last is None or frozenset((last, c)) not in bad)
        if keep > best.get(c, -1):
            best[c] = keep
    return len(s) - max(best.values())


def render(s, pairs):
    return s + '\n' + str(len(pairs)) + '\n' + ''.join(p + '\n' for p in pairs)


def random_pairs(rng, alphabet, k):
    letters = rng.sample(alphabet, 2 * k)
    return [letters[2 * i] + letters[2 * i + 1] for i in range(k)]


def extras(pid):
    rng = random.Random(16015400)
    cases, seen = [], set()

    def add(s, pairs, reason, category='adversarial'):
        text = render(s, pairs)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    letters = string.ascii_lowercase
    all_pairs = [letters[i] + letters[i + 1] for i in range(0, 26, 2)]
    add('a', [], 'minimum length, no pairs', 'boundary')
    add('z', all_pairs, 'minimum length with maximum k=13 pairs covering all letters', 'boundary')
    add('ab', ['ab'], 'minimum forbidden adjacency', 'boundary')
    add('ba', ['ab'], 'pair order reversed in sentence', 'boundary')
    add('ab', ['ba'], 'pair order reversed in pair line', 'boundary')
    add('aa', ['ab'], 'only one letter of the pair present', 'boundary')
    add('ab', [], 'k=0 with adjacent letters', 'boundary')
    add('ab', ['cd'], 'pair letters absent from sentence', 'boundary')
    add(letters, all_pairs, 'every adjacent letter pair forbidden', 'boundary')
    add(letters, [letters[i] + letters[25 - i] for i in range(13)], 'all 26 letters paired but none adjacent', 'boundary')
    add('a' * 26, all_pairs, 'single repeated letter with all pairs', 'boundary')

    add('abz', ['ab'], 'run ended by an unpaired letter as last segment (stale-segment reset)')
    add('baz', ['ab'], 'run ended by an unpaired letter, reversed')
    add('abzzzz', ['ab'], 'run ended by unpaired suffix')
    add('aab', ['ab'], 'unequal run counts: delete the single b, not half the run')
    add('aaab', ['ab'], 'run length4 needs one deletion')
    add('abbb', ['ab'], 'run length4 rare letter first')
    add('abba', ['ab'], 'equal counts split 2/2')
    add('aba', ['ab'], 'delete middle letter only')
    add('bab', ['ab'], 'delete middle letter only, reversed')
    add('ababab', ['ab'], 'alternating run')
    add('aabbaabb', ['ab'], 'blocks inside one run')
    add('abxab', ['ab'], 'unpaired letter separates two runs')
    add('aabbccdd', ['ab', 'cd'], 'two runs of different pairs touching')
    add('abcd', ['ab', 'cd'], 'adjacent runs of different pairs, each one deletion')
    add('acbd', ['ab', 'cd'], 'interleaved pairs never adjacent')
    add('abcabc', ['ab'], 'repeated run broken by c')
    add('abcabc', ['ab', 'cd'], 'c paired but partner absent')
    add('aaaaabbbbbaaaaa', ['ab'], 'one run, majority letter split around minority')
    add('bbbbbaaaaabbbbb', ['ab'], 'one run, minority in the middle')
    add('abababababababababab', ['ab'], 'long alternating run')
    add('abacaba', ['ab', 'cd'], 'separator letter belongs to another pair')
    add('codeforces', ['do', 'cs'], 'sample with a pair that never matters')
    add('cscscs', ['do', 'cs'], 'alternating second pair')
    add('ababa', ['ab'], 'sample one')
    add('aabaa', ['ab'], 'delete the single minority letter')
    add('abbaab', ['ab'], 'equal counts 3/3')
    add('ab' * 3 + 'c' + 'ba' * 2, ['ab'], 'two alternating runs of different lengths')
    add('aaaab' + 'xy' * 3, ['ab', 'xy'], 'runs of two pairs, unequal')
    add('xaaaaabx', ['ab'], 'run surrounded by unpaired letters')
    add('mbmbbbbbmbbbbmm', ['mb'], 'official-like dense block')

    big_pairs = list(all_pairs)
    rng.shuffle(big_pairs)
    add('ab' * 50000, ['ab'], 'maximum length alternating single run', 'maxSize')
    add('a' * 50000 + 'b' * 50000, ['ab'], 'maximum length two blocks', 'maxSize')
    add('a' * 99999 + 'b', ['ab'], 'maximum length single minority letter at end', 'maxSize')
    add('a' * MAX_LENGTH, all_pairs, 'maximum length repeated letter, k=13', 'maxSize')
    add(('ab' * 4 + 'c') * 11111 + 'a', ['ab'], 'maximum length many separated runs', 'maxSize')
    add(''.join(rng.choice(letters) for _ in range(MAX_LENGTH)), big_pairs, 'maximum length random letters, all 13 pairs', 'maxSize')
    add(''.join(rng.choice('abcd') for _ in range(MAX_LENGTH)), ['ab', 'cd'], 'maximum length dense two-pair alternation', 'maxSize')
    add(''.join(rng.choice('ab') * rng.randint(1, 9) for _ in range(30000))[:MAX_LENGTH].ljust(MAX_LENGTH, 'a'), ['ab'], 'maximum length random block run', 'maxSize')

    for _ in range(120):
        size = rng.randint(1, 8)
        alphabet = letters[:size]
        k = rng.randint(0, size // 2)
        s = ''.join(rng.choice(alphabet) for _ in range(rng.randint(1, 60)))
        add(s, random_pairs(rng, alphabet, k), 'fixed-seed small alphabet runs/separators', 'adversarial')
    return cases


def brute_checks():
    rng = random.Random(16015401)
    count = 0

    def check(data, exact):
        nonlocal count
        expected = answer('154A', data)
        assert expected == last_kept_dp(data), data
        count += 1
        if exact:
            assert expected == exhaustive(data), data
            count += 1

    pair_sets = [(), ('ab',), ('ba',), ('ac',), ('ab', 'cd'), ('ad', 'bc')]
    for n in range(1, 8):
        for word in itertools.product('abcd', repeat=n):
            if n > 6 and rng.randrange(8):
                continue
            for pairs in pair_sets:
                check((''.join(word), pairs), n <= 6)
    for _ in range(300):
        alphabet = string.ascii_lowercase[:rng.randint(2, 10)]
        k = rng.randint(0, len(alphabet) // 2)
        s = ''.join(rng.choice(alphabet) for _ in range(rng.randint(1, 400)))
        check((s, tuple(random_pairs(rng, alphabet, k))), False)
    return {'154A': count}


def review(pid, tests, samples):
    failures = []
    for name, pair in list(tests) + list(samples):
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
            continue
        if pair['output'].split() != [expected]:
            failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
    return failures
