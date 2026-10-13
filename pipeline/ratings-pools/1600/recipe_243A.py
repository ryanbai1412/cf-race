"""The Brand New Function (243A): distinct ORs over all contiguous subarrays."""
import itertools
import random
import re


IDS = ('243A',)
SEMANTICS = {
    '243A': 'n1..100000 on line one, exactly n single-space-separated integers0..1000000 on line two '
            '(10^5/10^6 attested from public English statement superscripts). Output the unique count of distinct '
            'f(l,r)=a_l|...|a_r over all 1<=l<=r<=n. Oracle keeps the at most21 distinct ORs of subarrays ending at '
            'each index; independent references recompute every interval OR from scratch and track last bit positions.',
}

MAX_N = 100000
MAX_A = 1000000
_LINE_ONE = re.compile(r'(?:0|[1-9][0-9]*)')
_LINE_TWO = re.compile(r'(?:0|[1-9][0-9]*)(?: (?:0|[1-9][0-9]*))*')


def _require_id(pid):
    if pid not in IDS:
        raise ValueError(f'unsupported problem {pid}')


def parse(pid, text):
    _require_id(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    body = text.replace('\r\n', '\n')
    if '\r' in body:
        raise ValueError('carriage return outside CRLF terminator')
    if body.endswith('\n'):
        body = body[:-1]
    lines = body.split('\n')
    if len(lines) != 2:
        raise ValueError('expected exactly two lines')
    if not _LINE_ONE.fullmatch(lines[0]) or not _LINE_TWO.fullmatch(lines[1]):
        raise ValueError('line layout/token format')
    n = int(lines[0])
    values = tuple(int(token) for token in lines[1].split(' '))
    if not 1 <= n <= MAX_N:
        raise ValueError('n out of range')
    if len(values) != n:
        raise ValueError('sequence arity')
    if any(v > MAX_A for v in values):
        raise ValueError('element out of range')
    return values


def answer(pid, data):
    _require_id(pid)
    seen = set()
    ending = set()
    for value in data:
        ending = {value | previous for previous in ending}
        ending.add(value)
        seen |= ending
    return len(seen)


def _brute_answer(values):
    seen = set()
    for left in range(len(values)):
        for right in range(left, len(values)):
            total = 0
            for index in range(left, right + 1):
                total |= values[index]
            seen.add(total)
    return len(seen)


def _last_bit_answer(values):
    last = [-1] * 20
    seen = set()
    for index, value in enumerate(values):
        for bit in range(20):
            if value >> bit & 1:
                last[bit] = index
        seen.add(value)
        positions = sorted({p for p in last if 0 <= p < index}, reverse=True)
        total = value
        for position in positions:
            total |= sum(1 << bit for bit in range(20) if last[bit] == position)
            seen.add(total)
    return len(seen)


def _text(values):
    return f'{len(values)}\n' + ' '.join(map(str, values)) + '\n'


def extras(pid):
    _require_id(pid)
    rng = random.Random(2431600)
    cases = []
    seen = set()

    def add(values, reason, category):
        text = _text(values)
        if text in seen:
            return
        seen.add(text)
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n',
                      'reason': reason, 'category': category})

    for value in (0, 1, 2, 524288, 999999, MAX_A):
        add([value], 'minimum n with single extreme/representative value', 'boundary')
    add([0, 0], 'all-zero pair has the single value 0', 'boundary')
    add([MAX_A, MAX_A], 'repeated maximum value', 'boundary')
    add([MAX_A, 0], 'maximum then zero', 'boundary')
    add([0, MAX_A, 0], 'zero both sides of maximum', 'boundary')
    add([1, 2, 4], 'non-contiguous OR 5 must not be counted (cumulative-set bug)', 'boundary')
    add([1, 0, 4], 'zero between disjoint bits; 1|4 only via the interval through 0', 'boundary')
    add([4, 1, 2, 4], 'repeated bit after middle values', 'boundary')
    add([1, 2, 1, 2], 'alternating values; subarray ORs collapse to {1,2,3}', 'boundary')
    add([3, 1, 2], 'later elements subsumed by first', 'boundary')
    add([1 << b for b in range(20)], 'all twenty bits as powers of two, maximal distinct contiguous ORs', 'boundary')
    add([1 << b for b in reversed(range(20))], 'descending powers of two', 'boundary')
    add([2 ** 20 - 1 - (1 << b) for b in range(20) if 2 ** 20 - 1 - (1 << b) <= MAX_A],
        'complements of single bits below 2^20 within range', 'boundary')
    add([524288, 475712, 524288 | 1], 'bit 19 values near 10^6', 'boundary')
    add([MAX_A, 1, 2, 4, 8], 'maximum first absorbs only some low bits (10^6 = 0b11110100001001000000)', 'boundary')
    add([0, 1, 0, 2, 0, 4], 'zeros interleaved with powers of two', 'boundary')
    add([5, 5, 5, 5, 5], 'constant sequence counts once', 'boundary')
    add([1, 2, 3, 4, 5, 6, 7, 8], 'consecutive small integers', 'boundary')
    add([7, 0, 0, 0, 0, 0, 0, 7], 'distant equal values with zeros between', 'boundary')
    add([1, 2], 'two-element: answer 3 with ordered pair', 'boundary')
    add([2, 1, 0, 0], 'element i not equal to index i (index-insertion bug)', 'boundary')
    add([6, 3, 5, 0], 'answer equals none of n, n+1 or len(set(a))+1 shortcuts', 'boundary')

    for n in range(2, 7):
        add([1 << ((i * 7) % 20) for i in range(n)], 'spread powers of two', 'adversarial')
    for _ in range(60):
        n = rng.randint(1, 12)
        add([rng.randint(0, 15) for _ in range(n)], 'fixed-seed small random values 0..15', 'adversarial')
    for _ in range(30):
        n = rng.randint(5, 60)
        add([rng.choice([0, 1 << rng.randrange(20)]) for _ in range(n)],
            'fixed-seed sparse single-bit values exercising contiguity', 'adversarial')
    for _ in range(30):
        n = rng.randint(10, 300)
        add([rng.randint(0, MAX_A) for _ in range(n)], 'fixed-seed random full-range values', 'adversarial')
    for _ in range(10):
        n = rng.randint(20, 300)
        add([sum(1 << b for b in rng.sample(range(20), 2)) & MAX_A or 1 for _ in range(n)],
            'fixed-seed two-bit values, many partial unions', 'adversarial')

    powers = [1 << b for b in range(20)]
    add([MAX_A] * MAX_N, 'maximum n, every element maximum', 'maxSize')
    add([0] * MAX_N, 'maximum n, every element zero', 'maxSize')
    add([powers[i % 20] for i in range(MAX_N)], 'maximum n cycling all powers of two (quadratic per-left loops TLE)', 'maxSize')
    add([powers[i % 20] if i % 3 else 0 for i in range(MAX_N)], 'maximum n powers with periodic zeros', 'maxSize')
    add([rng.randint(0, MAX_A) for _ in range(MAX_N)], 'maximum n fixed-seed random full range', 'maxSize')
    add([1 << rng.randrange(20) for _ in range(MAX_N)], 'maximum n fixed-seed random single bits', 'maxSize')
    add([MAX_A - (i % 1000) for i in range(MAX_N)], 'maximum n values just below 10^6', 'maxSize')
    add([(i * 7919) % (MAX_A + 1) for i in range(MAX_N)], 'maximum n arithmetic progression mod 10^6+1', 'maxSize')
    return cases


def review(pid, tests, samples):
    _require_id(pid)
    failures = []
    for name, pair in itertools.chain(tests, samples):
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'oracle output differs from supplied bytes',
                                 'expected': expected, 'actual': pair['output'].split()})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def brute_checks():
    count = 0

    def check(values, reference):
        nonlocal count
        expected = reference(values)
        actual = answer('243A', values)
        if actual != expected:
            raise AssertionError((values, expected, actual))
        count += 1

    for n in range(1, 5):
        for values in itertools.product(range(8), repeat=n):
            check(values, _brute_answer)
    for values in itertools.product((0, 1, 2, 4, 8, 16), repeat=5):
        check(values, _brute_answer)
    rng = random.Random(2431601)
    for _ in range(600):
        n = rng.randint(1, 40)
        mask = rng.choice((7, 63, 1023, MAX_A))
        check(tuple(min(MAX_A, rng.randint(0, mask)) for _ in range(n)), _brute_answer)
    for case in extras('243A'):
        values = parse('243A', case['input'])
        reference = _brute_answer if len(values) <= 300 else _last_bit_answer
        if int(case['output']) != reference(values):
            raise AssertionError(case['reason'])
        count += 1
    return {'243A': count}
