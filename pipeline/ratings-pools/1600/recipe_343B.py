"""343B author recipe: adjacent equal crossings cancel with endpoints fixed."""
from functools import lru_cache
import itertools
import random
import re


IDS = ('343B',)
SEMANTICS = {
    '343B': 'Original English input: one line of 1..100000 plus/minus characters; '
            'stdio, no interaction or special checker. With both endpoints fixed, '
            'two consecutive crossings with the same upper wire cancel. A stack '
            'computes the reduced alternating word in O(n) time/space; uniquely '
            'print Yes iff it is empty, otherwise No. Exhaustive deletion searches '
            'and an independent oriented-crossing sum cross-check the oracle.',
}


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _require_pid(pid)
    if not isinstance(text, str) or re.fullmatch(r'[+-]{1,100000}(?:\r?\n)?', text) is None:
        raise ValueError('343B requires one line of 1..100000 plus/minus characters')
    return text.removesuffix('\n').removesuffix('\r')


def answer(pid, data):
    _require_pid(pid)
    stack = []
    for crossing in data:
        if stack and stack[-1] == crossing:
            stack.pop()
        else:
            stack.append(crossing)
    return ['No' if stack else 'Yes']


@lru_cache(maxsize=None)
def _deletion_search(word):
    if not word:
        return True
    return any(_deletion_search(word[:i] + word[i + 2:])
               for i in range(len(word) - 1) if word[i] == word[i + 1])


def _oriented_crossings(word):
    winding = sum((1 if crossing == '+' else -1) * (1 if i % 2 == 0 else -1)
                  for i, crossing in enumerate(word))
    return 'Yes' if len(word) % 2 == 0 and winding == 0 else 'No'


def extras(pid):
    _require_pid(pid)
    rng = random.Random(3431600)
    cases, seen = [], set()

    def add(word, reason, category='adversarial'):
        if word in seen:
            return False
        text = word + '\n'
        data = parse(pid, text)
        cases.append({'input': text, 'output': answer(pid, data)[0] + '\n',
                      'reason': reason, 'category': category})
        seen.add(word)
        return True

    for n in range(1, 6):
        for symbols in itertools.product('+-', repeat=n):
            add(''.join(symbols), 'exhaustive short crossing orders, including both minima',
                'boundary' if n <= 2 else 'adversarial')
    for word in ('+-++-+', '++--++', '+--+--', '++-++-', '+-+-++',
                 '+-+-+-', '++----++', '+-+--+-+'):
        add(word, 'nested/disjoint cancellations versus palindrome, run-parity, or endpoint shortcuts')
    for word in ('+' * 31, '+' * 32, '-' * 33, '-' * 64,
                 '+-' * 31, '-+' * 32, '+-' * 32 + '+',
                 '+-' * 16 + '-+' * 16, '+' * 63 + '-' * 64 + '+',
                 '++--' * 25):
        add(word, 'odd/even runs, irreducible alternation, and cancellation across long blocks', 'boundary')
    for word in ('+' * 100000, '-' * 100000, '+-' * 50000,
                 '+-' * 25000 + '-+' * 25000, '+-' * 49999 + '++',
                 '+-' * 49999 + '+'):
        add(word, 'legal maximum or one-below-maximum length; long stack or cascading cancellation',
            'maxSize' if len(word) == 100000 else 'boundary')
    added = 0
    while added < 64:
        word = ''.join(rng.choice('+-') for _ in range(rng.randint(6, 18)))
        added += add(word, 'fixed-seed small crossing order checked by exhaustive deletion search')
    while len(cases) < 168:
        word = ''.join(rng.choice('+-') for _ in range(rng.randint(19, 512)))
        add(word, 'fixed-seed medium crossing order checked by the oriented-crossing invariant')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    failures = []
    for name, pair in itertools.chain(tests, samples):
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != expected:
                failures.append({'test': name, 'reason': 'oracle output disagreement',
                                 'expected': expected, 'actual': pair['output'].split()})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def brute_checks():
    count = 0
    try:
        for n in range(1, 12):
            for symbols in itertools.product('+-', repeat=n):
                word = ''.join(symbols)
                expected = 'Yes' if _deletion_search(word) else 'No'
                assert answer('343B', word) == [expected], word
                count += 1
        rng = random.Random(3431601)
        for _ in range(256):
            word = ''.join(rng.choice('+-') for _ in range(rng.randint(12, 18)))
            expected = 'Yes' if _deletion_search(word) else 'No'
            assert answer('343B', word) == [expected], word
            count += 1
        for pair in extras('343B'):
            word = parse('343B', pair['input'])
            assert pair['output'].split() == [_oriented_crossings(word)], word
            count += 1
    finally:
        _deletion_search.cache_clear()
    return {'343B': count}
