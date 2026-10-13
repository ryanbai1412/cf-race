"""Exact longest-alternating-subsequence-after-one-flip suite for 603A."""
import itertools
import random
import re


IDS = ('603A',)
SEMANTICS = {
    '603A': 'n1..100000 on line1, binary string of exactly n chars on line2. Flip exactly one nonempty substring; output the unique integer maximum longest alternating subsequence. LAS equals block count, and each prefix-boundary flip changes it by at most one, so the answer is min(n, blocks+2). Exhaustive all-flip enumeration with subsequence/DP LAS independently checks small strings.',
}

COUNT = re.compile(r'[1-9][0-9]*')
BITS = re.compile(r'[01]+')


def parse(pid, text):
    if pid != '603A':
        raise ValueError('unknown problem')
    lines = text.strip().splitlines()
    if len(lines) != 2 or [len(line.split()) for line in lines] != [1, 1]:
        raise ValueError('line layout')
    count, bits = lines[0].strip(), lines[1].strip()
    if not COUNT.fullmatch(count) or not BITS.fullmatch(bits):
        raise ValueError('token format')
    n = int(count)
    if not 1 <= n <= 100000 or len(bits) != n:
        raise ValueError('length constraints')
    return bits


def answer(pid, bits):
    blocks = 1 + sum(a != b for a, b in zip(bits, bits[1:]))
    return min(len(bits), blocks + 2)


def las_dp(bits):
    end = [0, 0]
    for c in bits:
        d = int(c)
        end[d] = max(end[d], end[1 - d] + 1)
    return max(end)


def las_subsets(bits):
    best = 0
    for mask in range(1, 1 << len(bits)):
        chosen = [bits[i] for i in range(len(bits)) if mask >> i & 1]
        if len(chosen) > best and all(a != b for a, b in zip(chosen, chosen[1:])):
            best = len(chosen)
    return best


def flipped(bits, lo, hi):
    return bits[:lo] + bits[lo:hi].translate(str.maketrans('01', '10')) + bits[hi:]


def brute(pid, bits, las=las_dp):
    n = len(bits)
    return max(las(flipped(bits, lo, hi)) for lo in range(n) for hi in range(lo + 1, n + 1))


def flip_dp(bits):
    neg = -1
    best = {(0, None): 0}
    for c in bits:
        nxt = {}
        for (phase, last), length in best.items():
            for p in ((0, 1) if phase == 0 else (1, 2) if phase == 1 else (2,)):
                d = int(c) ^ (p == 1)
                for state, value in (((p, last), length), ((p, d), length + 1) if last != d else ((p, last), neg)):
                    if nxt.get(state, neg) < value:
                        nxt[state] = value
        best = nxt
    return max(value for (phase, _), value in best.items() if phase)


def extras(pid):
    rng = random.Random(16006030)
    cases = []
    seen = set()

    def add(bits, reason, category='adversarial'):
        text = f'{len(bits)}\n{bits}\n'
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for n in range(1, 4):
        for bits in itertools.product('01', repeat=n):
            add(''.join(bits), 'every string with n<=3; answer always n, kills max(LAS+2,n)', 'boundary')
    for bits in ('0000', '1111', '0011', '0110', '1001', '0100', '0010', '00100', '01110', '010010', '0001', '1000'):
        add(bits, 'small runs: single triple, two doubles, interior/edge double', 'boundary')
    alt = ('01' * 50000)
    adversarial = [
        ('000', 'single run of three gives +2 (not +1)'),
        ('0001010', 'run of three at the start only'),
        ('0101000', 'run of three at the end only, missed by i<n-3 window scan'),
        ('01001010', 'exactly one interior double gives +1'),
        ('0101100101', 'two separated interior doubles give +2'),
        ('00101011', 'doubles at both string ends give +2'),
        ('001010', 'single leading double gives +1'),
        ('010100', 'single trailing double gives +1'),
        ('00100', 'two nonadjacent length-2 runs give +2'),
        ('0011', 'adjacent length-2 runs give +2 to n'),
        ('0100110', 'two adjacent interior doubles'),
        ('0000000', 'one long run answers 3'),
        ('00011', 'n - doubles formula overshoots'),
        ('1101', 'leading double with first character one'),
        ('10110', 'interior double with first character one'),
        ('0110110', 'two separated length-2 runs of ones'),
        ('000111', 'two runs of three'),
        ('0' * 4 + '1' * 4, 'two long runs'),
        ('01' * 10 + '0', 'odd alternating, flip keeps n'),
        ('01' * 10 + '1', 'alternating with trailing double'),
    ]
    for bits, reason in adversarial:
        add(bits, reason)
        add(bits.translate(str.maketrans('01', '10')), reason + ' (complemented)')
        add(bits[::-1], reason + ' (reversed)')
    for size in (1, 99999, 100000):
        for bits in ('0' * size, '1' * size, alt[:size], alt[1:] + '0'):
            add(bits[:size], f'n={size} all-equal/alternating extremes', 'maxSize' if size > 1 else 'boundary')
    seam = alt[:50000] + alt[49999:99998]
    add(seam + seam[-1], 'maximum n with doubles at a seam and the end', 'maxSize')
    add(alt[:50000] + alt[49999:99999], 'maximum n with exactly one interior double', 'maxSize')
    add('00' + alt[1:99999], 'maximum n with exactly one leading double', 'maxSize')
    add(alt[:99999] + alt[99998], 'maximum n with exactly one trailing double', 'maxSize')
    add('000' + alt[1:99998], 'maximum n with a single triple at the start', 'maxSize')
    add(''.join(rng.choice('01') for _ in range(100000)), 'maximum n uniform random', 'maxSize')
    add(''.join('0' * 2 + '1' * 2 for _ in range(25000)), 'maximum n all length-2 runs', 'maxSize')
    for _ in range(80):
        n = rng.randint(4, 40)
        mode = rng.randrange(3)
        if mode == 0:
            bits = ''.join(rng.choice('01') for _ in range(n))
        else:
            chars = list(alt[rng.randrange(2):][:n])
            for _ in range(mode):
                i = rng.randrange(n)
                chars[i] = chars[i - 1] if i else chars[1]
            bits = ''.join(chars)
        add(bits, 'fixed-seed random/near-alternating string')
    return cases


def brute_checks():
    counts = {'603A': 0}

    def check(bits, las):
        expected = brute('603A', bits, las)
        assert answer('603A', bits) == expected, (bits, answer('603A', bits), expected)
        counts['603A'] += 1
    for n in range(1, 9):
        for bits in itertools.product('01', repeat=n):
            check(''.join(bits), las_subsets)
    for n in range(9, 13):
        for bits in itertools.product('01', repeat=n):
            check(''.join(bits), las_dp)
    rng = random.Random(16006031)
    for _ in range(300):
        check(''.join(rng.choice('01') for _ in range(rng.randint(13, 40))), las_dp)
    for case in extras('603A'):
        bits = parse('603A', case['input'])
        assert flip_dp(bits) == int(case['output']), bits[:50]
        counts['603A'] += 1
    return counts


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'independent oracle disagreement', 'expected': [expected], 'actual': pair['output'].split()[:15]})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
