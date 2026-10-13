"""Bill Total Value: exact integer cents and canonical dotted formatting."""
import itertools
import random
import re


IDS = ('727B',)
SEMANTICS = {
    '727B': 'One ASCII bill line, length1..1000, alternating lowercase names1..10 '
            'and canonical positive prices1cent..10^6dollars (public English '
            'superscript attested). Dots group dollars by3; a final two-digit '
            'group is nonzero cents. Sum integer cents, retain repeated prices, '
            'and print the unique canonical price without .00. Independent '
            'small amount enumeration and group-based decoding cross-check the oracle.',
}

_ITEM = re.compile(r'([a-z]{1,10})([0-9.]+)')
_PRICE = re.compile(r'(?:0|[1-9][0-9]{0,2}(?:\.[0-9]{3})*)(?:\.(?!00)[0-9]{2})?')


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + pid)


def _price_cents(price):
    if len(price) >= 3 and price[-3] == '.':
        dollars, cents = price[:-3], int(price[-2:])
    else:
        dollars, cents = price, 0
    return int(dollars.replace('.', '')) * 100 + cents


def parse(pid, text):
    _require_pid(pid)
    if text.endswith('\r\n'):
        text = text[:-2]
    elif text.endswith('\n'):
        text = text[:-1]
    if not 1 <= len(text) <= 1000 or any(c.isspace() for c in text):
        raise ValueError('bill must occupy exactly one nonempty line of length1..1000')
    prices = []
    offset = 0
    while offset < len(text):
        item = _ITEM.match(text, offset)
        if item is None:
            raise ValueError('bill requires alternating lowercase names1..10 and prices')
        price = item[2]
        if _PRICE.fullmatch(price) is None:
            raise ValueError('noncanonical dollar grouping or cents')
        if not 1 <= _price_cents(price) <= 100000000:
            raise ValueError('price outside1cent..10^6dollars')
        prices.append(price)
        offset = item.end()
    return tuple(prices)


def _format(cents):
    dollars, fraction = divmod(cents, 100)
    digits = str(dollars)
    groups = []
    while digits:
        groups.append(digits[-3:])
        digits = digits[:-3]
    result = '.'.join(reversed(groups))
    return result + (f'.{fraction:02d}' if fraction else '')


def answer(pid, data):
    _require_pid(pid)
    return _format(sum(_price_cents(price) for price in data))


def _bill(amounts, names=None):
    if names is None:
        names = ['abc'[i % 3] for i in range(len(amounts))]
    return ''.join(name + _format(value) for name, value in zip(names, amounts)) + '\n'


def extras(pid):
    _require_pid(pid)
    rng = random.Random(1600727)
    cases = []

    def add(text, reason, category='adversarial'):
        result = answer(pid, parse(pid, text))
        cases.append({'input': text, 'output': result + '\n',
                      'reason': reason, 'category': category})

    singles = (1, 2, 5, 9, 10, 11, 50, 90, 99, 100, 101, 109, 110, 199,
               999, 1000, 9999, 10000, 99900, 99901, 99999, 100000, 100001,
               999900, 999999, 1000000, 1000001, 9999999, 10000000,
               99999999, 100000000)
    for value in singles:
        add(_bill([value]), 'cent minimum, integer/fraction distinction, grouping thresholds', 'boundary')
    for fraction in (1, 2, 9, 10, 11, 49, 50, 90, 99):
        for dollars in (0, 999, 999999):
            add(_bill([100 * dollars + fraction, 100 - fraction]),
                'exact cent carry must omit .00 and regroup dollars', 'boundary')
    for value in (1, 9, 10, 99, 100, 101, 1001, 9900, 100000, 999999,
                  99999999, 100000000):
        add(_bill([value] * 3, ['same'] * 3),
            'repeated equal prices are purchases, not a set (selected96146189)')
    for values in ([1, 1, 1], [10, 20], [100, 1, 1000], [100000, 101],
                   [100000000, 1, 99999999], [99] * 20):
        add(_bill(values), 'mixed dollar groups, final purchase, and accumulated cent carries')
    add('a1' * 500 + '\n', '1000-character bill with maximum500 purchases', 'maxSize')
    add('a1.000.000' * 100 + '\n',
        '1000characters,100 maximum prices; total cents exceed32-bit', 'maxSize')
    add('a0.01' * 200 + '\n', '1000characters of minimum prices and many carries', 'maxSize')
    add('a999.999.99' * 90 + 'a1.000.000\n',
        '1000characters with two kinds of dots and large nonzero remainder', 'maxSize')
    for _ in range(50):
        size = rng.randint(1, 15)
        values = [rng.randint(1, 99999) for _ in range(size)]
        names = [''.join(rng.choice('abcdefghijklmnopqrstuvwxyz')
                         for _ in range(rng.randint(1, 10))) for _ in range(size)]
        add(_bill(values, names), 'fixed-seed small exact-cent bills and name lengths')
    for _ in range(30):
        size = rng.randint(15, 40)
        values = [rng.randint(1, 100000000) for _ in range(size)]
        names = [''.join(rng.choice('abcdefghijklmnopqrstuvwxyz')
                         for _ in range(rng.randint(1, 10))) for _ in range(size)]
        add(_bill(values, names), 'fixed-seed large bills, varying last-price cents')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                raise ValueError('output differs from exact canonical bill total')
        except (ValueError, AssertionError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures


def _reference_format(cents):
    dollars, remainder = divmod(cents, 100)
    result = f'{dollars:,}'.replace(',', '.')
    return result if remainder == 0 else result + '.' + str(remainder).zfill(2)


def _reference_bill(text):
    dollars = cents = 0
    for word in re.split(r'[a-z]+', text.rstrip('\r\n')):
        if not word:
            continue
        groups = word.split('.')
        if len(groups) > 1 and len(groups[-1]) == 2:
            cents += int(groups.pop())
        whole = 0
        for group in groups:
            whole = 1000 * whole + int(group)
        dollars += whole
    return _reference_format(100 * dollars + cents)


def brute_checks():
    count = 0

    def check(amounts):
        nonlocal count
        text = ''.join('x' + _reference_format(value) for value in amounts) + '\n'
        assert answer('727B', parse('727B', text)) == _reference_format(sum(amounts))
        count += 1

    for cents in range(1, 1001):
        check([cents])
    domain = (1, 2, 9, 10, 11, 50, 90, 99, 100, 101, 109, 199,
              999, 1000, 99999, 100000, 100000000)
    for amounts in itertools.product(domain, repeat=2):
        check(amounts)
    for amounts in itertools.product((1, 9, 50, 99, 100), repeat=3):
        check(amounts)
    rng = random.Random(7271600)
    for _ in range(300):
        check([rng.randint(1, 100000000) for _ in range(rng.randint(1, 20))])
    for case in extras('727B'):
        assert answer('727B', parse('727B', case['input'])) == _reference_bill(case['input'])
        count += 1
    return {'727B': count}
