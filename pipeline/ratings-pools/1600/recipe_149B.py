"""149B author recipe; qualification and external-source validation are separate."""
from functools import lru_cache
import itertools
import random
import re


IDS = ('149B',)
ALPHABET = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
SEMANTICS = {
    '149B': 'Public English 149B: one a:b line, each part 1..5 digits 0..9/A..Z '
            '(values 0..35), leading zeroes allowed; integer radix >=2 with no '
            'upper cap, each digit <radix, hour 0..23 and minute 0..59. Unique '
            'increasing base tokens, or 0 for none / -1 for infinitely many. '
            'Horner evaluation checks bases through 59; any nonconstant part '
            'is at least its base. Constant valid parts give infinitely many '
            'bases. Independent inverse clock-value encoding cross-checks this.',
}


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def parse(pid, text):
    _require_pid(pid)
    lines = text.splitlines()
    if len(lines) != 1 or not re.fullmatch(r'[0-9A-Z]{1,5}:[0-9A-Z]{1,5}', lines[0]):
        raise ValueError('expected one a:b line with two 1..5-character uppercase digit strings')
    return tuple(lines[0].split(':'))


def _value(digits, base):
    value = 0
    for digit in digits:
        value = value * base + digit
    return value


def answer(pid, data):
    _require_pid(pid)
    hours, minutes = (tuple(ALPHABET.index(c) for c in word) for word in data)
    constants = all(digit == 0 for digit in hours[:-1] + minutes[:-1])
    if constants:
        return (-1,) if hours[-1] < 24 and minutes[-1] < 60 else (0,)
    minimum = max(2, max(hours + minutes) + 1)
    bases = tuple(base for base in range(minimum, 60)
                  if _value(hours, base) < 24 and _value(minutes, base) < 60)
    return bases or (0,)


def extras(pid):
    _require_pid(pid)
    cases = []
    seen = set()

    def add(clock, reason, category='adversarial'):
        if clock in seen:
            return
        seen.add(clock)
        text = clock + '\n'
        output = ' '.join(map(str, answer(pid, parse(pid, text)))) + '\n'
        cases.append({'input': text, 'output': output, 'reason': reason, 'category': category})

    fixed = [
        ('0:0', 'minimum component lengths; infinitely many bases', 'boundary'),
        ('0:1', 'single digits must never produce base 1', 'boundary'),
        ('1:0', 'minimum base is 2 even when max digit is 1', 'boundary'),
        ('00000:00000', 'both components at length 5; all zeroes', 'maxSize'),
        ('0000N:0000Z', 'both length 5; constant hour 23 and minute 35', 'maxSize'),
        ('0000O:0000Z', 'both length 5; constant hour 24 is impossible', 'maxSize'),
        ('ZZZZZ:ZZZZZ', 'both length 5; largest symbols cannot denote a clock', 'maxSize'),
        ('00000:00010', 'both length 5; finite bases 2..59 despite leading zeroes', 'maxSize'),
        ('11111:11111', 'both length 5; even binary hours exceed 23', 'maxSize'),
        ('10101:11111', 'both length 5; binary hour 21/minute 31', 'maxSize'),
        ('0:10000', 'five-digit minute 16 in base 2; base 3 already exceeds 59', 'boundary'),
        ('10000:0', 'five-digit hour 16 in base 2; base 3 already exceeds 23', 'boundary'),
        ('0:10', 'finite bases extend past 36 through 59', 'boundary'),
        ('10:0', 'hour upper limit stops at base 23', 'boundary'),
        ('0:11', 'minute 59 at base 58; base 59 is excluded', 'boundary'),
        ('11:0', 'hour 23 at base 22; base 23 is excluded', 'boundary'),
        ('0:20', 'minute 58 at base 29; minute 60 is excluded', 'boundary'),
        ('20:0', 'hour 22 at base 11; hour 24 is excluded', 'boundary'),
        ('0:1N', 'minimum base 24 gives minute 47; maximum base 36 gives 59', 'boundary'),
        ('0:1O', 'minimum base 25 gives minute 49; maximum base 35 gives 59', 'boundary'),
        ('0:1T', 'minimum base 30 gives minute 59; exactly one base', 'boundary'),
        ('0:1U', 'minimum base 31 gives minute 61; no base', 'boundary'),
        ('0:1Z', 'large minute symbol disqualifies every base', 'boundary'),
        ('1B:0', 'minimum base 12 gives hour 23; exactly one base', 'boundary'),
        ('1C:0', 'minimum base 13 gives hour 25; no base', 'boundary'),
        ('22:00', 'digit 2 requires base 3, not base 2', 'adversarial'),
        ('11:20', 'sample finite base interval', 'boundary'),
        ('2A:13', 'sample with no legal radix', 'boundary'),
        ('000B:00001', 'sample infinite bases after removing leading zeroes', 'boundary'),
        ('0001:0010', 'leading zeroes do not make a nonconstant minute constant', 'adversarial'),
        ('00O:00000', 'constant does not imply valid hour', 'adversarial'),
        ('00N:000Z', 'letter mapping N=23 and Z=35', 'adversarial'),
        ('00002:00130', 'minute polynomial limits otherwise constant hours', 'adversarial'),
        ('01B:4A', 'two polynomials intersect in one legal base', 'adversarial'),
        ('27:0070', 'leading zeroes preserve a singleton finite base', 'adversarial'),
    ]
    for clock, reason, category in fixed:
        add(clock, reason, category)
    for digit in ALPHABET:
        add(digit + ':0', 'every single hour symbol: 0..N valid; O..Z impossible', 'boundary')
        add('0:' + digit, 'every single minute symbol remains valid at all sufficiently large bases', 'boundary')
    for digit in ALPHABET[:12]:
        add('0:1' + digit, 'finite minute interval extends beyond base 36; increasing complete output')
    rng = random.Random(1600149)
    for _ in range(35):
        parts = [''.join(rng.choice('012') for _ in range(rng.randint(1, 3))) for _ in range(2)]
        add(':'.join(parts), 'fixed-seed small polynomial: carry thresholds and base/digit admissibility')
    while len(cases) < 160:
        parts = [''.join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 5))) for _ in range(2)]
        add(':'.join(parts), 'fixed-seed full alphabet, asymmetric lengths and impossible clock values')
    return cases


def _encode_clock_value(value, base):
    if value == 0:
        return '0'
    digits = []
    while value:
        value, remainder = divmod(value, base)
        if remainder >= len(ALPHABET):
            return None
        digits.append(ALPHABET[remainder])
    return ''.join(reversed(digits))


@lru_cache(maxsize=None)
def _clock_spellings(base, limit):
    return frozenset(_encode_clock_value(value, base) for value in range(limit)) - {None}


def _inverse_reference(data):
    hours, minutes = (word.lstrip('0') or '0' for word in data)
    if hours in _clock_spellings(60, 24) and minutes in _clock_spellings(60, 60):
        return (-1,)
    bases = tuple(base for base in range(2, 60)
                  if hours in _clock_spellings(base, 24) and minutes in _clock_spellings(base, 60))
    return bases or (0,)


def brute_checks():
    count = 0

    def check(data):
        nonlocal count
        actual = answer('149B', data)
        expected = _inverse_reference(data)
        if actual != expected:
            raise AssertionError((data, actual, expected))
        count += 1

    small = [''.join(digits) for n in range(1, 4) for digits in itertools.product('012', repeat=n)]
    for data in itertools.product(small, repeat=2):
        check(data)
    for data in itertools.product(ALPHABET, repeat=2):
        check(data)
    binary = [''.join(digits) for n in range(1, 6) for digits in itertools.product('01', repeat=n)]
    for data in itertools.product(binary, repeat=2):
        check(data)
    rng = random.Random(1491600)
    for _ in range(200):
        check(tuple(''.join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 5))) for _ in range(2)))
    for _ in range(200):
        base = rng.randint(2, 59)
        parts = []
        for limit in (24, 60):
            spellings = sorted(word for word in _clock_spellings(base, limit) if len(word) <= 5)
            word = rng.choice(spellings)
            parts.append('0' * rng.randint(0, 5 - len(word)) + word)
        check(tuple(parts))
    for pair in extras('149B'):
        check(parse('149B', pair['input']))
    return {'149B': count}


def review(pid, tests, samples):
    _require_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = list(map(str, answer(pid, parse(pid, pair['input']))))
            actual = pair['output'].split()
            if actual != expected:
                failures.append({'test': name, 'reason': 'independent oracle disagreement',
                                 'expected': expected, 'actual': actual})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
