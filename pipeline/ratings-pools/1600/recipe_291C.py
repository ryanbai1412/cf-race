"""Source-attested Network Mask recipe; not a qualification or audit."""
import itertools
import random
import re


IDS = ('291C',)
SEMANTICS = {
    '291C': 'Original English HTML attests 1<=k<=n<=10^5; n distinct canonical '
            'IPv4 addresses, one per line. Only /1..31 masks are legal. Choose '
            'the least prefix length yielding exactly k networks, else -1; '
            'therefore output is unique. Sorted adjacent XOR split depths give '
            'prefix counts; independent literal binary-prefix sets check them.',
}
_POSITIVE = re.compile(r'[1-9][0-9]*')
_OCTET = re.compile(r'0|[1-9][0-9]{0,2}')


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def _ip(value):
    return '.'.join(str((value >> shift) & 255) for shift in (24, 16, 8, 0))


def parse(pid, text):
    _require_pid(pid)
    lines = [line.split() for line in text.splitlines()]
    if not lines or len(lines[0]) != 2:
        raise ValueError('header must contain n and k on one line')
    if not all(_POSITIVE.fullmatch(token) for token in lines[0]):
        raise ValueError('n and k must be positive decimal integers')
    n, k = map(int, lines[0])
    if not 1 <= k <= n <= 100000:
        raise ValueError('require 1<=k<=n<=100000')
    if len(lines) != n + 1 or any(len(line) != 1 for line in lines[1:]):
        raise ValueError('require exactly n address lines, one IPv4 per line')
    addresses = []
    for line in lines[1:]:
        octets = line[0].split('.')
        if len(octets) != 4 or not all(_OCTET.fullmatch(octet) for octet in octets):
            raise ValueError('require four decimal octets without leading zeroes')
        values = list(map(int, octets))
        if any(value > 255 for value in values):
            raise ValueError('IPv4 octet outside 0..255')
        a, b, c, d = values
        addresses.append((a << 24) | (b << 16) | (c << 8) | d)
    if len(set(addresses)) != n:
        raise ValueError('IP addresses must be distinct')
    return k, addresses


def answer(pid, data):
    _require_pid(pid)
    k, addresses = data
    ordered = sorted(addresses)
    splits = [0] * 33
    for a, b in zip(ordered, ordered[1:]):
        splits[33 - (a ^ b).bit_length()] += 1
    networks = 1
    for prefix in range(1, 32):
        networks += splits[prefix]
        if networks == k:
            return _ip(((1 << prefix) - 1) << (32 - prefix))
        if networks > k:
            break
    return '-1'


def _brute(data):
    k, addresses = data
    binary = [format(value, '032b') for value in addresses]
    for prefix in range(1, 32):
        if len({word[:prefix] for word in binary}) == k:
            mask = '1' * prefix + '0' * (32 - prefix)
            return '.'.join(str(int(mask[i:i + 8], 2)) for i in range(0, 32, 8))
    return '-1'


def brute_checks():
    count = 0

    def check(data):
        nonlocal count
        actual, expected = answer('291C', data), _brute(data)
        assert actual == expected, (data, actual, expected)
        count += 1

    for shift in (0, 7, 8, 15, 16, 23, 24, 29):
        domain = [value << shift for value in range(8)]
        for size in range(1, 9):
            for addresses in itertools.combinations(domain, size):
                for k in range(1, size + 1):
                    check((k, addresses))
    for bit in range(32):
        for k in (1, 2):
            check((k, (0, 1 << bit)))
    rng = random.Random(29101600)
    for _ in range(400):
        n = rng.randint(1, 24)
        addresses = rng.sample(range(1 << 32), n)
        check((rng.randint(1, n), addresses))
    return {'291C': count}


def extras(pid):
    _require_pid(pid)
    rng = random.Random(1600291)
    cases, seen = [], set()

    def add(addresses, k, reason, category='adversarial'):
        text = f'{len(addresses)} {k}\n' + ''.join(_ip(value) + '\n' for value in addresses)
        if text in seen:
            return
        data = parse(pid, text)
        seen.add(text)
        cases.append({'input': text, 'output': answer(pid, data) + '\n',
                      'reason': reason, 'category': category})

    for addresses, k, reason in [
        ([0], 1, 'minimum n and k; /0 is forbidden, choose /1'),
        ([(1 << 32) - 1], 1, 'all-one IPv4 is legal; no host-address restrictions'),
        ([0, 1 << 31], 1, 'no legal /0 mask despite k=1'),
        ([0, 1], 2, 'distinct addresses differ only at last bit; /32 forbidden'),
        ([(1 << 32) - 1, (1 << 32) - 2], 2, 'upper IPv4 limit, /32 forbidden'),
        ([0, 1, 2, 3], 3, 'prefix network count skips k=3'),
        ([0, 1, 2, 3], 4, 'four addresses occupy only two /31 networks'),
        ([0, 1, 2, 3], 2, 'least possible mask on a long constant-count plateau'),
        ([0, 1 << 30, 1 << 31, 3 << 30], 3, 'count jumps from two to four'),
    ]:
        add(addresses, k, reason, 'boundary')
    for bit in range(32):
        for k in (1, 2):
            add([0, 1 << bit], k,
                f'single differing bit {bit}; bit order, minimal mask, /1 and /31 endpoints',
                'boundary')
    for prefix in (1, 7, 8, 9, 15, 16, 17, 23, 24, 25, 30, 31):
        addresses = [0, 1 << (32 - prefix), (1 << 32) - 1]
        rng.shuffle(addresses)
        add(addresses, 3, 'split at an octet boundary or neighboring bit; unsorted input')
    for k in (1, 2, 3, 4, 5):
        add([1, 65794, 513, 65792, 515], k,
            'official sample topology at every k; recompute networks for each mask')
    for _ in range(64):
        n = rng.randint(3, 60)
        if rng.randrange(2):
            width = rng.randint(8, 31)
            base = rng.randrange(1 << (32 - width)) << width
            addresses = [base + value for value in rng.sample(range(1 << width), n)]
        else:
            addresses = rng.sample(range(1 << 32), n)
        rng.shuffle(addresses)
        add(addresses, rng.randint(1, n),
            'fixed-seed small full-range/shared-prefix inputs with feasible and skipped counts')
    add(list(range(100000)), 50000,
        'maximum n, consecutive distinct IPs; /31 reaches exactly 50000', 'maxSize')
    add(list(range(99999, -1, -1)), 100000,
        'maximum n=k; reverse order and paired /31 hosts make target impossible', 'maxSize')
    add([value << 15 for value in range(100000)], 100000,
        'maximum n=k spread over distinct prefixes; earliest feasible mask is /17', 'maxSize')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    failures = []
    for name, pair in [*tests, *samples]:
        try:
            expected = answer(pid, parse(pid, pair['input']))
            if pair['output'].split() != [expected]:
                failures.append({'test': name, 'reason': 'exact oracle disagreement',
                                 'expected': expected, 'actual': pair['output']})
        except ValueError as exc:
            failures.append({'test': name, 'reason': str(exc)})
    return failures
