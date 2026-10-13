"""260B source-attested date-frequency recipe; not a qualification or audit."""
from collections import Counter
from datetime import date, timedelta
import itertools
import random
import re


IDS = ('260B',)
SEMANTICS = {
    '260B': 'One line of ASCII digits/hyphens, 1..100000 characters; a unique '
            'positive-frequency most common valid dd-mm-yyyy substring exists. '
            'Years2013..2015 are non-leap; overlaps count. Original English HTML '
            'attests10^5, not105. Lookahead counts every start, then Gregorian '
            'month bounds filter; independent brute enumerates all1095 calendar '
            'dates and searches each literal at every overlapping occurrence.',
}
_CANDIDATE = re.compile(r'(?=([0-9]{2}-[0-9]{2}-201[345]))')
_MONTH_DAYS = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _pid(pid):
    if pid != '260B':
        raise ValueError('unsupported problem ID')


def _counts(word):
    counts = Counter()
    for match in _CANDIDATE.finditer(word):
        token = match.group(1)
        day, month = int(token[:2]), int(token[3:5])
        if 1 <= month <= 12 and 1 <= day <= _MONTH_DAYS[month]:
            counts[token] += 1
    return counts


def _winner(counts):
    if not counts:
        raise ValueError('no correct date: existence guarantee violated')
    maximum = max(counts.values())
    winners = [token for token, count in counts.items() if count == maximum]
    if len(winners) != 1:
        raise ValueError('tied correct dates: uniqueness guarantee violated')
    return winners[0]


def parse(pid, text):
    _pid(pid)
    lines = text.splitlines()
    if len(lines) != 1:
        raise ValueError('prophesy must occupy exactly one line')
    word = lines[0]
    if not 1 <= len(word) <= 100000 or re.fullmatch(r'[0-9-]+', word) is None:
        raise ValueError('prophesy length/ASCII alphabet')
    if text not in (word, word + '\n', word + '\r\n'):
        raise ValueError('prophesy line ending')
    _winner(_counts(word))
    return word


def answer(pid, data):
    _pid(pid)
    return [_winner(_counts(data))]


def _calendar_dates():
    current, end = date(2013, 1, 1), date(2016, 1, 1)
    tokens = []
    while current < end:
        tokens.append(f'{current.day:02d}-{current.month:02d}-{current.year:04d}')
        current += timedelta(days=1)
    return tuple(tokens)


_DATES = _calendar_dates()


def _brute_counts(word):
    counts = {}
    for token in _DATES:
        count, start = 0, 0
        while True:
            found = word.find(token, start)
            if found < 0:
                break
            count += 1
            start = found + 1
        if count:
            counts[token] = count
    return counts


def brute(pid, data):
    _pid(pid)
    counts = _brute_counts(data)
    if not counts:
        raise ValueError('no correct calendar date')
    ranked = sorted((count, token) for token, count in counts.items())
    if len(ranked) > 1 and ranked[-2][0] == ranked[-1][0]:
        raise ValueError('calendar date frequency tie')
    return [ranked[-1][1]]


def extras(pid):
    _pid(pid)
    rng = random.Random(2601600)
    cases, seen = [], set()

    def add(word, reason, category='adversarial'):
        if word in seen:
            return
        data = parse(pid, word + '\n')
        cases.append({'input': word + '\n', 'output': answer(pid, data)[0] + '\n',
                      'reason': reason, 'category': category})
        seen.add(word)

    for token in ('01-01-2013', '31-12-2015', '28-02-2013', '28-02-2014',
                  '28-02-2015', '01-09-2014'):
        add(token, 'minimum legal length10; fixed-width leading zeroes/year bounds', 'boundary')
    for year in range(2013, 2016):
        for month in range(1, 13):
            token = f'{_MONTH_DAYS[month]:02d}-{month:02d}-{year}'
            add('000' + token + '999', 'last legal day in every month/year; no word boundaries', 'boundary')
    invalid = ('00-01-2013', '32-01-2013', '31-04-2013', '31-06-2014',
               '31-09-2015', '31-11-2013', '29-02-2013', '29-02-2014',
               '29-02-2015', '30-02-2014', '31-02-2015', '01-00-2013',
               '01-13-2014', '01-99-2015', '01-01-2012', '01-01-2016',
               '01-01-2023', '1-01-2013', '01-1-2013', '1-1-2013',
               '01--01-2013', '01012013', '01-01-02013', '01-01-201')
    for token in invalid:
        add('---'.join([token] * 5 + ['28-02-2015']),
            'repeated invalid day/month/year/width cannot beat one real date')
    for suffix in ('13', '14', '15'):
        for repetitions in (2, 3, 9):
            word = '21-12-20' + suffix + ('-12-20' + suffix) * repetitions
            add(word, 'winner starts inside previous year; overlapping matches must count')
    for prefix, suffix in (('7', ''), ('', '9'), ('9' * 100, '0' * 100),
                           ('-----', '-----'), ('0', '0')):
        add(prefix + '06-07-2014' + suffix, 'first/last sliding-window start, digit/hyphen padding')
    for first, second in (('01-01-2013', '31-12-2015'), ('31-12-2015', '01-01-2013'),
                          ('28-02-2014', '01-03-2013'), ('01-09-2015', '09-01-2015')):
        for reverse in (False, True):
            pieces = [first] * 3 + [second] * 4
            add('---'.join(pieces[::-1] if reverse else pieces),
                'frequency, not first/last/lexicographic/chronological date; lead by one')
    add('9' * 99990 + '31-12-2015', 'maximum100000; only valid date at final start', 'maxSize')
    add('01-01-2013' + '-' * 99990, 'maximum100000; only valid date at initial start', 'maxSize')
    add('13-12-2013' + '-12-2013' * 12498 + '-' * 6,
        'maximum100000;12499 overlapping copies, no non-overlap shortcut', 'maxSize')
    while len(cases) < 160:
        winner, rival = rng.sample(_DATES, 2)
        count = rng.randint(2, 8)
        pieces = [winner] * count + [rival] * rng.randint(1, count - 1)
        pieces += [rng.choice(invalid) for _ in range(rng.randint(0, 6))]
        rng.shuffle(pieces)
        noise = ''.join(rng.choice('0123456789-') for _ in range(rng.randint(0, 80)))
        word = noise + '---' + '---'.join(pieces) + '---' + noise[::-1]
        try:
            add(word, 'fixed-seed small date mixtures, invalid distractors, frequency lead and noise')
        except ValueError:
            continue
    return cases


def brute_checks():
    count = 0

    def check(word):
        nonlocal count
        fast, slow = _counts(word), _brute_counts(word)
        assert dict(fast) == slow, (word, fast, slow)
        if slow and list(slow.values()).count(max(slow.values())) == 1:
            assert answer('260B', word) == brute('260B', word)
            count += 1
        count += 1

    for token in _DATES:
        check(token)
    for day, month, year in itertools.product(range(33), range(14), range(2012, 2017)):
        token = f'{day:02d}-{month:02d}-{year}'
        check(token + '---' + token + '---28-02-2015')
    noise = [''.join(chars) for width in range(4)
             for chars in itertools.product('01-', repeat=width)]
    for prefix, suffix in itertools.product(noise, repeat=2):
        check(prefix + '01-01-2013' + suffix)
    blocks = ('13-12-2013', '01-01-2015', '29-02-2014', '00-01-2013', '2013', '-', '0')
    for width in range(1, 5):
        for pieces in itertools.product(blocks, repeat=width):
            check(''.join(pieces))
    rng = random.Random(26001600)
    for _ in range(300):
        check(''.join(rng.choice(blocks + _DATES) for _ in range(rng.randint(1, 12))))
    return {'260B': count}


def review(pid, tests, samples):
    _pid(pid)
    errors = []
    for name, pair in tests + samples:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            actual = pair['output'].split()
            if expected != actual:
                errors.append({'test': name, 'reason': 'independent oracle disagreement',
                               'expected': expected, 'actual': actual})
        except (ValueError, KeyError, TypeError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors
