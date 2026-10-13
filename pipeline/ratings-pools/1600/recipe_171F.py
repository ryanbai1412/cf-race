"""Emirp index suite for the Caesar-enciphered April Fools problem 171F."""
from bisect import bisect_left
import random
import re


IDS = ('171F',)
SEMANTICS = {
    '171F': 'Statement is Caesar-shifted by 10 letters (q->a): one line with one integer d, 1<=d<=11184; output the d-th emirp, '
            'a prime whose decimal reversal is a different prime (palindromic primes excluded), as one integer. '
            'Exactly 11184 emirps lie below 10^6, so the 10^6 sieve covers every d and every reversal. '
            'Output is unique; independently checked over the whole input domain by trial-division enumeration.',
}
MAX_D = 11184
LIMIT = 10 ** 6
_EMIRPS = []


def parse(pid, text):
    if pid != '171F':
        raise ValueError('unknown problem')
    lines = text.splitlines()
    if len(lines) != 1:
        raise ValueError('emirp line layout')
    tokens = lines[0].split()
    if len(tokens) != 1 or not re.fullmatch(r'[1-9][0-9]*', tokens[0]):
        raise ValueError('emirp arity')
    d = int(tokens[0])
    if not 1 <= d <= MAX_D:
        raise ValueError('emirp index range')
    return d


def _emirps():
    if not _EMIRPS:
        sieve = bytearray([1]) * LIMIT
        sieve[0] = sieve[1] = 0
        for i in range(2, int(LIMIT ** 0.5) + 1):
            if sieve[i]:
                sieve[i * i::i] = bytearray(len(range(i * i, LIMIT, i)))
        for p in range(2, LIMIT):
            if sieve[p]:
                r = int(str(p)[::-1])
                if r != p and sieve[r]:
                    _EMIRPS.append(p)
    return _EMIRPS


def answer(pid, d):
    return _emirps()[d - 1]


def _is_prime_trial(n):
    if n < 2:
        return False
    if n % 2 == 0 or n % 3 == 0:
        return n in (2, 3)
    f = 5
    while f * f <= n:
        if n % f == 0 or n % (f + 2) == 0:
            return False
        f += 6
    return True


def _reverse_digits(n):
    r = 0
    while n:
        r, n = r * 10 + n % 10, n // 10
    return r


def brute_emirps(limit=LIMIT):
    found = []
    for n in range(2, limit):
        if _is_prime_trial(n):
            r = _reverse_digits(n)
            if r != n and _is_prime_trial(r):
                found.append(n)
    return found


def _palindromic_primes(limit=LIMIT):
    return [p for p in range(2, limit) if str(p) == str(p)[::-1] and _is_prime_trial(p)]


def _index_of_first_at_least(x):
    return bisect_left(_emirps(), x) + 1


def extras(pid):
    rng = random.Random(171006)
    cases = []
    seen = set()
    emirps = _emirps()

    def add(d, reason, category='adversarial'):
        if d in seen or not 1 <= d <= MAX_D:
            return
        seen.add(d)
        text = f'{d}\n'
        cases.append({'input': text, 'output': f'{answer(pid, parse(pid, text))}\n', 'reason': reason, 'category': category})

    for d in (1, 2, 3, 4, 5, 6, 7, 8):
        add(d, 'minimum indices: two-digit emirps 13..97 with palindrome 11 excluded', 'boundary')
    for d in range(MAX_D, MAX_D - 8, -1):
        add(d, 'maximum legal index 11184 and its neighbours near the 10^6 limit', 'maxSize')
    for bound in (100, 1000, 10000, 100000, 200000, 500000, 10 ** 6):
        k = _index_of_first_at_least(bound)
        add(k - 1, f'last emirp below {bound}: catches fixed search/sieve caps', 'boundary')
        add(k, f'first emirp at or above {bound}: catches fixed search/sieve caps', 'boundary')
    palindromic = [p for p in _palindromic_primes() if p > 11]
    for p in palindromic[:30] + palindromic[-10:]:
        add(_index_of_first_at_least(p), f'first emirp after palindromic prime {p}: catches missing reversal!=p check')
    for k, (e, nxt) in enumerate(zip(emirps, emirps[1:]), 1):
        if str(e)[0] != str(nxt)[0]:
            add(k, f'last emirp {e} before leading digit/length jump to {nxt}: no emirp starts with 2,4,5,6,8', 'boundary')
            add(k + 1, f'first emirp {nxt} after leading digit/length jump from {e}', 'boundary')
    while len(cases) < 150:
        add(rng.randint(1, MAX_D), 'fixed-seed random index', 'adversarial')
    return cases


def brute_checks():
    reference = brute_emirps()
    assert len(reference) == MAX_D, len(reference)
    count = 1
    for d in range(1, MAX_D + 1):
        assert answer('171F', d) == reference[d - 1], d
        count += 1
    palindromes = set(_palindromic_primes())
    assert not palindromes & set(reference)
    count += 1
    return {'171F': count}


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
