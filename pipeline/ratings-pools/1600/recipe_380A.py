"""Source-attested exact prefix-copy sequence recipe; not a qualification."""
from bisect import bisect_left
import itertools
import random
import re


IDS = ('380A',)
LIMIT = 100000
SEMANTICS = {
    '380A': 'Public English 380/A: m,n,x,l in1..10^5,c in1..10^4; '
    'copy the first l existing elements c times, l<=current length. '
    'Queries are strictly increasing one-based positions within the final sequence. '
    'One operation per line and all queries on one line. Unique integer output tokens. '
    'Cache only the first10^5 elements and binary-search exact cumulative lengths; '
    'copied positions map into that cache. Literal expansion independently checks small programs.',
}


def _pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem')


def _numbers(line):
    tokens = line.split()
    if not tokens or any(re.fullmatch(r'[1-9][0-9]*', token) is None for token in tokens):
        raise ValueError('positive decimal integers required')
    return list(map(int, tokens))


def parse(pid, text):
    _pid(pid)
    lines = text.splitlines()
    if not lines:
        raise ValueError('empty input')
    header = _numbers(lines[0])
    if len(header) != 1 or not 1 <= header[0] <= LIMIT:
        raise ValueError('stage count')
    m = header[0]
    if len(lines) != m + 3:
        raise ValueError('stage/query line layout')
    operations = []
    length = 0
    for line in lines[1:m + 1]:
        op = _numbers(line)
        if op[0] == 1 and len(op) == 2 and 1 <= op[1] <= LIMIT:
            length += 1
        elif (op[0] == 2 and len(op) == 3 and
              1 <= op[1] <= min(length, LIMIT) and 1 <= op[2] <= 10000):
            length += op[1] * op[2]
        else:
            raise ValueError('operation arity/range or nonexistent prefix')
        operations.append(tuple(op))
    count = _numbers(lines[m + 1])
    if len(count) != 1 or not 1 <= count[0] <= LIMIT:
        raise ValueError('query count')
    queries = _numbers(lines[m + 2])
    if (len(queries) != count[0] or queries[-1] > length or
            any(a >= b for a, b in zip(queries, queries[1:]))):
        raise ValueError('query arity/range/order')
    return operations, queries


def answer(pid, data):
    _pid(pid)
    operations, queries = data
    prefix = []
    ends = []
    length = 0
    for op in operations:
        if op[0] == 1:
            if len(prefix) < LIMIT:
                prefix.append(op[1])
            length += 1
        else:
            _, size, copies = op
            take = min(size * copies, LIMIT - len(prefix))
            if take:
                block = prefix[:size]
                full, rest = divmod(take, size)
                prefix.extend(block * full)
                prefix.extend(block[:rest])
            length += size * copies
        ends.append(length)
    result = []
    for position in queries:
        stage = bisect_left(ends, position)
        op = operations[stage]
        if op[0] == 1:
            result.append(op[1])
        else:
            before = ends[stage - 1] if stage else 0
            result.append(prefix[(position - before - 1) % op[1]])
    return result


def _length(operations):
    return sum(1 if op[0] == 1 else op[1] * op[2] for op in operations)


def _text(operations, queries):
    return (str(len(operations)) + '\n' +
            ''.join(' '.join(map(str, op)) + '\n' for op in operations) +
            str(len(queries)) + '\n' + ' '.join(map(str, queries)) + '\n')


def _literal(operations):
    sequence = []
    for op in operations:
        if op[0] == 1:
            sequence.append(op[1])
        else:
            block = sequence[:op[1]]
            for _ in range(op[2]):
                sequence.extend(block)
    return sequence


def _backwards(operations, queries):
    result = []
    length = _length(operations)
    for query in queries:
        position, end = query, length
        for op in reversed(operations):
            before = end - (1 if op[0] == 1 else op[1] * op[2])
            if position > before:
                if op[0] == 1:
                    result.append(op[1])
                    break
                position = (position - before - 1) % op[1] + 1
            end = before
        else:
            raise AssertionError('unresolved position')
    return result


def extras(pid):
    _pid(pid)
    rng = random.Random(3801600)
    result, seen = [], set()

    def add(operations, queries, reason, category='adversarial'):
        text = _text(operations, queries)
        if text not in seen:
            seen.add(text)
            values = answer(pid, parse(pid, text))
            result.append({'input': text, 'output': ' '.join(map(str, values)) + '\n',
                           'reason': reason, 'category': category})

    add([(1, 1)], [1], 'minimum stages, queries, and value', 'boundary')
    add([(1, LIMIT)], [1], 'maximum appended value', 'boundary')
    add([(1, 11), (1, 22), (1, 33), (2, 2, 3)], list(range(1, 10)),
        'prefix is not suffix; copy block starts after a nonaligned length')
    add([(1, 7), (1, 13), (1, 17), (2, 2, 2)], [4, 5, 6, 7],
        'subtract pre-stage length before modulo; each copy first/last position')
    add([(1, 9), (1, 8), (2, 1, 1)], [3],
        'single-element copy is not append of its length')
    add([(1, 41), (1, 73), (1, 29)], [2],
        'sparse queries are not the entire resulting sequence')
    add([(1, 99), (2, 1, 5), (1, 22), (2, 7, 4), (2, 19, 3)], [1, 6, 7, 8, 35, 36, 92],
        'prefix contains earlier copied blocks and a later appended value')
    add([(1, 3), (1, 5), (2, 2, 10000)], [1, 2, 3, 4, 20001, 20002],
        'maximum repetitions, exact copy-end residues', 'boundary')
    for size in range(1, 21):
        base = [(1, 100 + i) for i in range(size + 1)]
        ops = base + [(2, size, 2), (1, 99999), (2, size + 2, 3)]
        length = _length(ops)
        add(ops, list(range(1, length + 1)),
            'all positions across nonaligned copies, nested prefix, and append boundaries')
        add(ops, sorted({1, size + 1, size + 2, 2 * size + 1, 3 * size + 1, length}),
            'sparse prefix/copy boundaries and final position')
    while len(result) < 156:
        ops, length = [], 0
        for _ in range(rng.randint(1, 25)):
            if length == 0 or rng.random() < 0.48:
                ops.append((1, rng.randint(1, LIMIT)))
                length += 1
            else:
                size, copies = rng.randint(1, min(length, 50)), rng.randint(1, 5)
                ops.append((2, size, copies))
                length += size * copies
        queries = sorted(rng.sample(range(1, length + 1), rng.randint(1, min(length, 40))))
        add(ops, queries, 'fixed-seed small mixed stages and ordered sparse queries')
    add([(1, i) for i in range(1, LIMIT + 1)], list(range(1, LIMIT + 1)),
        'maximum100000 stages and queries; all appended values distinct', 'maxSize')
    ops = [(1, i * 97) for i in range(1, 18)] + [(2, 17, 10000)]
    ops += [(2, LIMIT, 10000)] * (LIMIT - len(ops))
    length = _length(ops)
    queries = [1 + i * (length - 1) // (LIMIT - 1) for i in range(LIMIT)]
    add(ops, queries, 'all four count/prefix/copy maxima; final length near10^14 and 64-bit queries', 'maxSize')
    ops = [(1, i) for i in range(1, LIMIT)] + [(2, LIMIT - 1, 2)]
    add(ops, list(range(99950, 100050)) + [199998, 199999, 299997],
        'cache cap crossed by a copy: first cached repeated element and last prefix index', 'maxSize')
    ops = [(1, i) for i in range(1, 99998)] + [(2, 99997, 1), (1, LIMIT), (2, LIMIT, 10000)]
    add(ops, [99997, 99998, 100000, 199994, 199995, 199996, 299995, _length(ops)],
        'maximum prefix length includes copied elements; late append lies outside cache', 'maxSize')
    return result


def review(pid, tests, samples):
    _pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            values = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != list(map(str, values)):
                raise ValueError('oracle output differs from supplied bytes')
        except (ValueError, IndexError, KeyError, TypeError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors


def brute_checks():
    assertions = 0

    def check(operations):
        nonlocal assertions
        sequence = _literal(operations)
        queries = list(range(1, len(sequence) + 1))
        observed = answer('380A', parse('380A', _text(operations, queries)))
        for expected, actual in zip(sequence, observed):
            if expected != actual:
                raise AssertionError((operations, expected, actual))
            assertions += 1
        if len(sequence) != len(observed):
            raise AssertionError('output arity')

    def enumerate_programs(operations, depth):
        if operations:
            check(operations)
        if depth == 4:
            return
        length = _length(operations)
        choices = [(1, 1), (1, 2)]
        choices += [(2, size, copies) for size, copies in itertools.product(range(1, length + 1), (1, 2))]
        for op in choices:
            enumerate_programs(operations + [op], depth + 1)

    enumerate_programs([], 0)
    rng = random.Random(380042)
    for _ in range(400):
        operations, length = [], 0
        for _ in range(rng.randint(1, 24)):
            if not length or rng.random() < 0.45:
                operations.append((1, rng.randint(1, LIMIT)))
                length += 1
            else:
                size, copies = rng.randint(1, min(length, 25)), rng.randint(1, 4)
                operations.append((2, size, copies))
                length += size * copies
        check(operations)
    return {'380A': assertions}
