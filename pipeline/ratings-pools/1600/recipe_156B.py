"""Source-attested Suspects recipe; author checks do not qualify the problem."""
import itertools
import random
import re


IDS = ('156B',)
SEMANTICS = {
    '156B': 'Public English 156/B attests n1..100000, m0..n, exactly n '
            'signed answers, one per line, with targets1..n and at least one '
            'consistent criminal. For criminal c, truth count is total '
            'negative answers + positive[c] - negative[c]. Classify each '
            'answer over all consistent criminals; each output line is '
            'uniquely Truth, Lie, or Not defined. O(n) integer oracle; '
            'literal truth-table enumeration independently checks small inputs.'
}


def _check_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def _candidates(n, m, statements):
    balance = [0] * (n + 1)
    negatives = 0
    for value in statements:
        balance[abs(value)] += 1 if value > 0 else -1
        negatives += value < 0
    return {c for c in range(1, n + 1) if negatives + balance[c] == m}


def parse(pid, text):
    _check_pid(pid)
    lines = text.splitlines()
    if not lines or len(lines[0].split()) != 2:
        raise ValueError('expected n m on the first line')
    header = lines[0].split()
    if any(re.fullmatch(r'[0-9]+', word) is None for word in header):
        raise ValueError('nondecimal header')
    n, m = map(int, header)
    if not (1 <= n <= 100000 and 0 <= m <= n):
        raise ValueError('n/m constraints')
    if len(lines) != n + 1:
        raise ValueError('expected exactly n answer lines')
    statements = []
    for line in lines[1:]:
        word = line.strip()
        if re.fullmatch(r'[+-][0-9]+', word) is None:
            raise ValueError('expected one signed target per line')
        value = int(word)
        if not 1 <= abs(value) <= n:
            raise ValueError('target outside 1..n')
        statements.append(value)
    statements = tuple(statements)
    if not _candidates(n, m, statements):
        raise ValueError('no criminal consistent with exactly m truths')
    return n, m, statements


def answer(pid, data):
    _check_pid(pid)
    n, m, statements = data
    candidates = _candidates(n, m, statements)
    if not candidates:
        raise ValueError('no consistent criminal')
    result = []
    for value in statements:
        if abs(value) not in candidates:
            result.append('Lie' if value > 0 else 'Truth')
        elif len(candidates) > 1:
            result.append('Not defined')
        else:
            result.append('Truth' if value > 0 else 'Lie')
    return '\n'.join(result) + '\n'


def _brute(n, m, statements):
    scenarios = []
    for criminal in range(1, n + 1):
        truths = tuple(criminal == value if value > 0 else criminal != -value
                       for value in statements)
        if sum(truths) == m:
            scenarios.append(truths)
    if not scenarios:
        return None
    result = []
    for outcomes in zip(*scenarios):
        if all(outcomes):
            result.append('Truth')
        elif not any(outcomes):
            result.append('Lie')
        else:
            result.append('Not defined')
    return '\n'.join(result) + '\n'


def brute_checks():
    count = 0
    for n in range(1, 5):
        domain = tuple(range(-n, 0)) + tuple(range(1, n + 1))
        for statements in itertools.product(domain, repeat=n):
            for m in range(n + 1):
                expected = _brute(n, m, statements)
                if expected is not None:
                    assert answer('156B', (n, m, statements)) == expected
                    count += 1
    rng = random.Random(1561600)
    for _ in range(300):
        n = rng.randint(5, 40)
        statements = tuple(rng.choice((-1, 1)) * rng.randint(1, n)
                           for _ in range(n))
        criminal = rng.randint(1, n)
        m = sum(criminal == v if v > 0 else criminal != -v for v in statements)
        assert answer('156B', (n, m, statements)) == _brute(n, m, statements)
        count += 1
    return {'156B': count}


def extras(pid):
    _check_pid(pid)
    cases = []
    seen = set()

    def add(statements, m, reason, category='adversarial'):
        text = f'{len(statements)} {m}\n' + ''.join(f'{v:+d}\n' for v in statements)
        if text in seen:
            return
        data = parse(pid, text)
        output = answer(pid, data)
        if len(statements) <= 50:
            assert output == _brute(*data)
        seen.add(text)
        cases.append({'input': text, 'output': output,
                      'reason': reason, 'category': category})

    for n in (1, 2):
        domain = tuple(range(-n, 0)) + tuple(range(1, n + 1))
        for statements in itertools.product(domain, repeat=n):
            for m in range(n + 1):
                if _brute(n, m, statements) is not None:
                    add(statements, m, 'exhaustive minimum domains including m=0/n '
                        'and self-reference', 'boundary')
    fixed = [
        ((1, -2, -3), 3, 'unique criminal: innocent-target denials are Truth; '
         'selected WA 72577648 ignores that branch'),
        ((1, 1, -2), 3, 'repeated accusations count with multiplicity, not a set; '
         'selected WA 159445718 uses sets'),
        ((-1, -1, -1), 0, 'repeated denials and zero truths'),
        ((1, -1, 2, -2), 2, 'positive/negative cancellation leaves every criminal possible'),
        ((2, -3, 4, -1), 1, 'ambiguous suspects coexist with definite lies'),
        ((1, 2, 3), 1, 'all criminals possible: accusations individually ambiguous'),
        ((-1, -2, -3), 2, 'all criminals possible: self-denials individually ambiguous'),
        ((3, 3, 3), 0, 'two unmentioned suspects possible; no eligible accusation'),
        ((-3, -3, -3), 3, 'unmentioned criminals make every denial true'),
        ((-4, -3, -1, -3), 3, 'multiplicity removes a target from the candidate set'),
        ((5, 5, 5, 1, 1, 1), 3, 'exactly two candidates tied despite duplicate claims'),
        ((-6, -1, 5, 1, 6, 1), 3, 'all three output labels and both signs'),
    ]
    for statements, m, reason in fixed:
        add(statements, m, reason)
    add((100000,) * 100000, 100000,
        'maximum n and target; repeated accusation has a unique criminal', 'maxSize')
    add(tuple(-i for i in range(1, 100001)), 99999,
        'maximum n; every criminal possible, every self-denial ambiguous', 'maxSize')
    add((1, -1) * 50000, 50000,
        'maximum n; cancellation permits all targets including unmentioned ones', 'maxSize')
    add((1,) * 25000 + (-1,) * 25000 + (100000,) * 25000 + (-2,) * 25000, 50000,
        'maximum n; mixed candidate membership produces all three labels', 'maxSize')
    rng = random.Random(1561601)
    while len(cases) < 150:
        n = rng.randint(3, 50)
        statements = tuple(rng.choice((-1, 1)) * rng.randint(1, n)
                           for _ in range(n))
        criminal = rng.randint(1, n)
        m = sum(criminal == v if v > 0 else criminal != -v for v in statements)
        add(statements, m, 'fixed-seed small truth-table case with guaranteed feasible m')
    return cases


def review(pid, tests, samples):
    _check_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            data = parse(pid, pair['input'])
            expected = answer(pid, data).splitlines()
            actual = [line.strip() for line in pair['output'].splitlines()]
            if actual != expected:
                failures.append({'test': name, 'reason': 'oracle/output-line disagreement',
                                 'expected': expected[:15], 'actual': actual[:15]})
        except (ValueError, TypeError, KeyError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
