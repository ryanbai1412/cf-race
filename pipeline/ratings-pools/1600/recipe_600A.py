"""1600/600A Extract Numbers: exact word split, integer classification and quoted output."""
import itertools
import random
import re

IDS = ('600A',)
SEMANTICS = {
    '600A': 'One line s, 1<=|s|<=10^5 (public statement 10<sup>5</sup>; row text flattened to 105), over . , ; digits and Latin letters. '
            'Words are maximal runs without , or ; so k separators give k+1 words, empty words included. '
            'A word is a number iff it is "0" or a nonzero digit followed by digits (no sign, dot or leading zero). '
            'Output line1: numbers joined by "," in order, quoted, or - if none; line2: all other words likewise. '
            'Unique output; lines contain no whitespace so token comparison equals line comparison. '
            'Checked against a character-level state machine and exhaustive small strings.',
}

ALPHABET = re.compile(r'[A-Za-z0-9.,;]{1,100000}')
NUMBER = re.compile(r'0|[1-9][0-9]*')
MAX_LEN = 100000


def parse(pid, text):
    if pid != '600A':
        raise ValueError('unknown problem ' + pid)
    lines = text.strip().splitlines()
    if len(lines) != 1:
        raise ValueError('expected exactly one line')
    s = lines[0]
    if not ALPHABET.fullmatch(s):
        raise ValueError('length/alphabet constraint violated')
    return s


def answer(pid, s):
    numbers, others = [], []
    for word in re.split('[,;]', s):
        (numbers if NUMBER.fullmatch(word) else others).append(word)
    return ['"' + ','.join(part) + '"' if part else '-' for part in (numbers, others)]


def brute(s):
    numbers = []
    others = []
    word = ''
    state = 'empty'
    for c in s + ';':
        if c in ',;':
            if state in ('zero', 'number'):
                numbers.append(word)
            else:
                others.append(word)
            word = ''
            state = 'empty'
            continue
        word += c
        if state == 'empty':
            state = 'zero' if c == '0' else 'number' if '1' <= c <= '9' else 'other'
        elif state == 'zero' or (state == 'number' and not '0' <= c <= '9'):
            state = 'other'
    first = '-' if not numbers else '"' + ','.join(numbers) + '"'
    second = '-' if not others else '"' + ','.join(others) + '"'
    return [first, second]


def render(output):
    return '\n'.join(output) + '\n'


def brute_checks():
    total = 0
    for length in range(1, 7):
        for chars in itertools.product('01a.,;', repeat=length):
            s = ''.join(chars)
            assert answer('600A', s) == brute(s), s
            total += 1
    rng = random.Random(600002)
    pool = '0123456789aZ.,;'
    for _ in range(3000):
        s = ''.join(rng.choice(pool) for _ in range(rng.randint(1, 40)))
        assert answer('600A', s) == brute(s), s
        total += 1
    for case in extras('600A'):
        s = parse('600A', case['input'])
        assert case['output'] == render(brute(s)), s[:50]
        total += 1
    return {'600A': total}


def _words_to_length(rng, length, word_maker):
    parts = []
    size = 0
    while True:
        word = word_maker()
        sep = rng.choice(',;')
        if size + len(word) + 1 > length:
            break
        parts.append(word + sep)
        size += len(word) + 1
    s = ''.join(parts)
    pad = length - len(s)
    if pad:
        s += ('1' + '0' * (pad - 1)) if pad < 4000 else 'x' * pad
    return s


def extras(pid):
    rng = random.Random(600001)
    cases = []
    seen = set()

    def add(s, reason, category='adversarial'):
        text = s + '\n'
        if text in seen:
            return
        parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': render(answer(pid, s)), 'reason': reason, 'category': category})

    boundary = [
        ('0', 'single zero is a number; second line dash (sources treating leading 0 as invalid fail)'),
        ('00', 'double zero is not a number (int()==0 acceptance bug)'),
        ('000', 'triple zero is not a number'),
        ('01', 'leading zero non-number, minimal'),
        ('02', 'leading zero other than 01 (hard-coded "01" check)'),
        ('007', 'leading zeros before nonzero digit'),
        ('9', 'single nonzero digit'),
        ('10', 'trailing zero is fine'),
        (',', 'two empty words only: b is ","'),
        (';', 'semicolon only: two empty words'),
        (',,', 'three empty words'),
        (';;;;', 'five empty words'),
        ('.', 'single dot is a non-number word'),
        ('Z', 'uppercase letter word (isalpha lowercase-only scans)'),
        ('a', 'single lowercase word'),
        ('0,', 'zero then trailing empty word'),
        (',0', 'leading empty word then zero'),
        ('0;0', 'two zeros, b dash'),
        ('1,2', 'all numbers, b must be dash not ""'),
        ('a,b', 'no numbers, a must be dash not ""'),
        ('1,', 'trailing separator creates empty word in b: ""'),
        (',1', 'leading separator creates empty word in b'),
        (';1;', 'empty words on both sides'),
        ('0.', 'zero with dot not number'),
        ('.0', 'dot then zero not number'),
        ('1.0', 'decimal-looking word not number'),
        ('1e5', 'exponent-looking word not number'),
        ('0a', 'zero then letter'),
        ('a0', 'letter then zero'),
        ('1a', 'digit then letter'),
    ]
    for s, reason in boundary:
        add(s, reason, 'boundary')

    adversarial = [
        ('0,00,000,0', 'zero runs: only single zeros are numbers'),
        ('00;0;00', 'zero between double zeros'),
        ('01,02,03,0,10,20', 'leading-zero family vs real numbers'),
        ('0;a;0', 'zero mid-string and as last word'),
        ('a;0', 'zero only as last word (end-of-string branch)'),
        ('0;a', 'zero only as first word'),
        ('x,0,y', 'zero surrounded by non-numbers'),
        ('1;;2', 'internal empty word between numbers'),
        (';;1', 'leading empty words'),
        ('1;;', 'trailing empty words'),
        (',;,;,;', 'seven empty words, mixed separators'),
        ('A,B;C', 'uppercase words only'),
        ('aA1,1aA,1', 'mixed-case alnum vs number'),
        ('1.1;1..1;.1.', 'dot placements'),
        ('...,..,.', 'dots-only words'),
        ('1;2,3;4,5', 'alternating separators all numbers'),
        ('12345678901234567890', 'number exceeding 64-bit'),
        ('99999999999999999999999999999999999999', 'very large number (stoll overflow)'),
        ('4294967296,18446744073709551616', 'just above 32/64-bit unsigned'),
    ]
    for s, reason in adversarial:
        add(s, reason)
    add('0' * 4000, '4000 zeros: not a number', 'adversarial')
    add('1' + '0' * 3999, '4000-digit number (stays under CPython int-string 4300 limit)', 'adversarial')
    add('0' + '1' * 3999, '4000-digit leading-zero word', 'adversarial')

    tokens = ['0', '00', '01', '1', '10', '', 'a', 'Z', '.', '0.', '1.0', '007', '9', 'a0', '0a', '123']
    for _ in range(60):
        n = rng.randint(1, 12)
        s = rng.choice(',;').join(rng.choice(tokens) for _ in range(n))
        if not s:
            s = rng.choice(',;')
        add(s, 'fixed-seed mixed word list from numeric/leading-zero/empty/dot vocabulary')
    pool = '0123456789aZ.,;'
    for _ in range(30):
        add(''.join(rng.choice(pool) for _ in range(rng.randint(1, 30))), 'fixed-seed random characters over the full symbol classes')

    def numeric_word():
        r = rng.random()
        if r < 0.3:
            return '0'
        if r < 0.6:
            return str(rng.randint(1, 10 ** rng.randint(1, 18)))
        if r < 0.75:
            return '0' + str(rng.randint(0, 999))
        if r < 0.85:
            return ''
        return ''.join(rng.choice('abcXYZ.0123') for _ in range(rng.randint(1, 6)))

    add(_words_to_length(rng, MAX_LEN, numeric_word), 'max |s|=10^5 mixed words, many separators', 'maxSize')
    add(','.join(['0'] * 50000)[:MAX_LEN - 1] + ',', 'max length: 50000 zeros, trailing empty word', 'maxSize')
    add(';' * MAX_LEN, 'max length all separators: 100001 empty words, a dash', 'maxSize')
    add('a' * MAX_LEN, 'max length single non-number word', 'maxSize')
    add(','.join(['1'] * 50000)[:MAX_LEN - 1] + '2', 'max length all numbers, b dash', 'maxSize')
    add(_words_to_length(rng, MAX_LEN, lambda: '1' + '0' * rng.randint(100, 3999)), 'max length of long numbers <=4000 digits', 'maxSize')
    add(('0' * 3999 + ',') * 25, 'long zero-run words just under limits', 'maxSize')
    add(('9' * 4000 + ';') * 24 + '9' * 3976, 'large-number words near max length', 'maxSize')
    return cases


def review(pid, tests, samples):
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            s = parse(pid, pair['input'])
            expected = answer(pid, s)
            if brute(s) != expected:
                raise ValueError('oracle and state-machine reference disagree')
            if pair['output'].split() != expected or pair['output'].strip().splitlines() != expected:
                raise ValueError('output differs from independent oracle')
        except (ValueError, AssertionError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
