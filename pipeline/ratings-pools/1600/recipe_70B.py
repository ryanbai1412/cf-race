"""Source-attested text grammar and exact minimum contiguous message count."""
import itertools
import random
import re


IDS = ('70B',)
SEMANTICS = {
    '70B': 'n2..255; second-line ASCII text1..10000 follows the original BNF: '
           'nonempty letter-only words, single spaces, nonempty sentences ending '
           'in .?!, and single spaces between sentences. Messages preserve sentence '
           'order and cannot split sentences; only a space at a message boundary '
           'is omitted. The unique minimum count (or Impossible) follows longest '
           'feasible prefix packing; exhaustive cut enumeration independently checks it. '
           'Upstream needs the omitted BNF restored and 104 corrected to 10^4.',
}
_SENTENCE = r'[A-Za-z]+(?: [A-Za-z]+)*[.!?]'
_TEXT = re.compile(_SENTENCE + r'(?: ' + _SENTENCE + r')*')


def _require_id(pid):
    if pid != '70B':
        raise ValueError('unknown problem: ' + str(pid))


def parse(pid, text):
    _require_id(pid)
    if not isinstance(text, str):
        raise ValueError('input must be text')
    lines = text.splitlines()
    if len(lines) != 2 or not re.fullmatch(r'[ \t]*[0-9]+[ \t]*', lines[0]):
        raise ValueError('expected integer line and single text line')
    n = int(lines[0])
    message = lines[1]
    if not 2 <= n <= 255 or not 1 <= len(message) <= 10000:
        raise ValueError('message capacity/text length constraints')
    if not _TEXT.fullmatch(message):
        raise ValueError('original TEXT/SENTENCE/WORD grammar violation')
    return n, message


def answer(pid, data):
    _require_id(pid)
    n, text = data
    count = used = start = 0
    for i, c in enumerate(text):
        if c not in '.?!':
            continue
        length = i - start + 1
        if length > n:
            return 'Impossible'
        if not used or used + 1 + length > n:
            count += 1
            used = length
        else:
            used += 1 + length
        start = i + 2
    return count


def brute(pid, data):
    """Enumerate every subset of sentence-boundary cuts on small texts."""
    _require_id(pid)
    n, text = data
    ends = [i + 1 for i, c in enumerate(text) if c in '.?!']
    if len(ends) > 10:
        raise ValueError('cut enumeration is limited to ten sentences')
    best = len(ends) + 1
    for mask in range(1 << (len(ends) - 1)):
        cuts = [end for i, end in enumerate(ends[:-1]) if mask & (1 << i)]
        cuts.append(len(text))
        start = 0
        valid = True
        for end in cuts:
            if len(text[start:end]) > n:
                valid = False
                break
            start = end + 1
        if valid:
            best = min(best, len(cuts))
    return 'Impossible' if best > len(ends) else best


def brute_checks():
    count = 0
    for size in range(1, 7):
        for sentences in itertools.product(('a.', 'Bb?', 'C d!'), repeat=size):
            text = ' '.join(sentences)
            for n in range(2, 19):
                data = parse('70B', f'{n}\n{text}\n')
                assert answer('70B', data) == brute('70B', data), data
                count += 1
    rng = random.Random(70001600)
    for _ in range(300):
        sentences = []
        for _ in range(rng.randint(1, 8)):
            words = [''.join(rng.choice('abCD') for _ in range(rng.randint(1, 12)))
                     for _ in range(rng.randint(1, 5))]
            sentences.append(' '.join(words) + rng.choice('.?!'))
        data = parse('70B', f'{rng.randint(2, 80)}\n' + ' '.join(sentences) + '\n')
        assert answer('70B', data) == brute('70B', data), data
        count += 1
    return {'70B': count}


def extras(pid):
    _require_id(pid)
    cases, seen = [], set()

    def add(n, text, reason, category='adversarial'):
        value = f'{n}\n{text}\n'
        if value not in seen:
            data = parse(pid, value)
            cases.append({'input': value, 'output': str(answer(pid, data)) + '\n',
                          'reason': reason, 'category': category})
            seen.add(value)

    for n, text, reason in (
        (2, 'a.', 'minimum capacity and shortest sentence, exact fit'),
        (2, 'Z?', 'uppercase letters and question terminator'),
        (2, 'b!', 'exclamation terminator'),
        (2, 'aa.', 'punctuation counts toward capacity; one character too long'),
        (2, 'a. b.', 'separator may be omitted only at a message boundary'),
        (4, 'a. b.', 'retained separator prevents packing two length-two sentences'),
        (5, 'a. b.', 'exact fit accepts equality rather than a strict inequality'),
        (8, 'a. b. c.', 'three sentences in one message, not one message per sentence'),
        (7, 'a. bb. c.', 'order prevents rearranging to combine first and last sentences'),
        (5, 'a b c.', 'words cannot be split into separate messages within a sentence'),
        (5, 'ab. c. d.', 'greedy prefix followed by a two-sentence exact fit'),
        (4, 'a. abc. b.', 'middle sentence exact fit starts without its preceding space'),
        (4, 'a. abcd. b.', 'an oversized middle sentence makes the entire text impossible'),
        (4, 'abcd. a. b.', 'oversized first sentence must not be ignored'),
        (4, 'a. b. abcd.', 'oversized last sentence must not be ignored'),
        (255, 'a.', 'one sentence is legal even with a very large capacity'),
        (19, 'Hello! Do you like fish? Why?', 'official sample exercises all three terminators'),
        (10, 'A B. Cd? e!', 'internal and inter-sentence spaces both count when retained'),
        (6, 'a. b! C?', 'punctuation-independent parsing and a nonempty final message'),
        (6, 'aa. bb. cc. dd.', 'total-length division is not sufficient for indivisible sentences'),
    ):
        add(n, text, reason, 'boundary' if n == 2 else 'adversarial')

    for n in (2, 3, 4, 5, 8, 16, 254, 255):
        add(n, 'A' * (n - 1) + '!', 'single sentence exactly at message capacity', 'boundary')
        add(n, 'A' * n + '?', 'single sentence exceeds capacity by exactly one', 'boundary')
        add(n, 'a. ' + 'B' * (n - 1) + '.',
            'full later sentence is legal after dropping only the boundary space', 'boundary')
        add(n, 'a. ' * 9 + 'Z!', 'many shortest sentences expose separator accounting')

    large = [
        (255, 'a' * 9999 + '.', 'maximum 10000-character single sentence is impossible'),
        (255, ' '.join(['a'] * 5000) + '?', 'maximum multiword sentence cannot be split'),
        (2, ' '.join(['a.'] * 3332 + ['bbb.']), 'maximum text with an oversized final sentence'),
        (255, ' '.join(['a.'] * 3332 + ['bbb.']), 'maximum text with many feasible shortest sentences'),
        (255, ' '.join(['A' * 254 + '!'] * 39 + ['b' * 15 + '?']),
         'maximum text with many full-capacity sentences and a shorter final sentence'),
        (2, ' '.join(['a.'] * 3333), 'maximum feasible sentence count at minimum capacity'),
    ]
    for n, text, reason in large:
        add(n, text, reason, 'maxSize')

    rng = random.Random(701600)
    while len(cases) < 150:
        n = rng.choice((2, 3, 4, 5, 8, 16, 50, 254, 255, rng.randint(2, 255)))
        sentences = []
        for _ in range(rng.randint(1, 10)):
            words = [''.join(rng.choice('abcXYZ') for _ in range(rng.randint(1, 30)))
                     for _ in range(rng.randint(1, 5))]
            sentences.append(' '.join(words) + rng.choice('.?!'))
        add(n, ' '.join(sentences), 'fixed-seed small mixed words, punctuation, and capacities')
    return cases


def review(pid, tests, samples):
    _require_id(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = str(answer(pid, parse(pid, pair['input'])))
            if pair['output'].split() != [expected]:
                raise ValueError('output differs from exact minimum message count')
        except (ValueError, TypeError, KeyError) as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
