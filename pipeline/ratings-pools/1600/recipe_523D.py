"""Source-attested FIFO video scheduling recipe; not a qualification or audit."""
from collections import deque
from heapq import heapreplace
import itertools
import random
import re


IDS = ('523D',)
SEMANTICS = {
    '523D': 'Public English 523/D: 1<=n,k<=500000; n chronological rows '
            'of distinct arrivals 1<=s<=10^9 and durations 1<=m<=10^9. '
            'Identical servers start available at time 0; FIFO jobs start '
            'immediately on an idle server (including exact completion ties). '
            'Output n unique integer completion times in upload order, not '
            'completion order. A min-heap schedules in O(n log(min(n,k))); '
            'an independent arrival/release event simulation checks small cases.'
}
MAX_COUNT = 500000
MAX_TIME = 10**9
SEED = 1600523


def _require_pid(pid):
    if pid not in IDS:
        raise ValueError('unsupported problem: ' + str(pid))


def _row(line):
    tokens = line.split()
    if len(tokens) != 2 or any(re.fullmatch(r'[0-9]+', token) is None for token in tokens):
        raise ValueError('each line must contain exactly two decimal integers')
    return tuple(map(int, tokens))


def parse(pid, text):
    _require_pid(pid)
    lines = text.splitlines()
    if not lines:
        raise ValueError('empty input')
    n, k = _row(lines[0])
    if not (1 <= n <= MAX_COUNT and 1 <= k <= MAX_COUNT):
        raise ValueError('video/server count outside 1..500000')
    if len(lines) != n + 1:
        raise ValueError('expected a header followed by exactly n video rows')
    videos = []
    previous = 0
    for line in lines[1:]:
        arrival, duration = _row(line)
        if not (previous < arrival <= MAX_TIME and 1 <= duration <= MAX_TIME):
            raise ValueError('arrival/duration range or strictly increasing upload order')
        previous = arrival
        videos.append((arrival, duration))
    return k, videos


def answer(pid, data):
    _require_pid(pid)
    k, videos = data
    available = [0] * min(k, len(videos))
    result = []
    for arrival, duration in videos:
        finish = max(arrival, available[0]) + duration
        heapreplace(available, finish)
        result.append(finish)
    return result


def _event_reference(data):
    k, videos = data
    busy = [None] * min(k, len(videos))
    waiting = deque()
    next_upload = 0
    result = [None] * len(videos)
    while next_upload < len(videos) or waiting or any(t is not None for t in busy):
        events = [t for t in busy if t is not None]
        if next_upload < len(videos):
            events.append(videos[next_upload][0])
        time = min(events)
        for server, finish in enumerate(busy):
            if finish is not None and finish <= time:
                busy[server] = None
        while next_upload < len(videos) and videos[next_upload][0] <= time:
            waiting.append(next_upload)
            next_upload += 1
        for server, finish in enumerate(busy):
            if finish is None and waiting:
                job = waiting.popleft()
                busy[server] = time + videos[job][1]
                result[job] = busy[server]
    return result


def brute_checks():
    count = 0
    for n in range(1, 6):
        for arrivals in itertools.combinations(range(1, 6), n):
            for durations in itertools.product(range(1, 4), repeat=n):
                videos = list(zip(arrivals, durations))
                for k in range(1, n + 3):
                    data = k, videos
                    assert answer('523D', data) == _event_reference(data), data
                    count += 1
    rng = random.Random(SEED + 1)
    for _ in range(500):
        n = rng.randint(1, 40)
        data = rng.randint(1, n + 5), list(zip(
            sorted(rng.sample(range(1, 300), n)),
            [rng.randint(1, 100) for _ in range(n)]))
        assert answer('523D', data) == _event_reference(data), data
        count += 1
    return {'523D': count}


def extras(pid):
    _require_pid(pid)
    cases = []
    seen = set()

    def add(k, videos, reason, category='adversarial'):
        text = f'{len(videos)} {k}\n' + ''.join(f'{s} {m}\n' for s, m in videos)
        if text in seen:
            return
        seen.add(text)
        output = '\n'.join(map(str, answer(pid, parse(pid, text)))) + '\n'
        cases.append({'input': text, 'output': output, 'reason': reason, 'category': category})

    add(1, [(1, 1)], 'minimum counts, arrival and duration', 'boundary')
    add(MAX_COUNT, [(MAX_TIME, MAX_TIME)], 'maximum server count with one late upload', 'maxSize')
    add(2, [(10, 3)], 'initial job starts at arrival, not k (selected WA 11440028)')
    add(1, [(1, 1), (100, 2)], 'idle gap needs max(arrival,release), selected WA 97105579')
    add(2, [(1, 100), (2, 1), (3, 1), (4, 1)],
        'reuse the same earliest server, not batched round robin (selected WA 18344591)')
    add(2, [(1, 10), (2, 1)], 'output upload order even when completion order reverses')
    add(1, [(1, 5), (2, 1), (3, 2)], 'backlog stays FIFO, not shortest-job-first')
    add(1, [(1, 1), (2, 1), (3, 1)], 'release exactly at arrival starts without a one-second delay', 'boundary')
    add(2, [(1, 4), (2, 3), (3, 2), (4, 1), (5, 3)], 'simultaneous releases preserve multiplicity')
    add(3, [(1, 99), (2, 98), (3, 97), (4, 1), (5, 1), (6, 1), (7, 1)],
        'three tied releases drain queued uploads in FIFO order')
    add(10, [(1, 100), (2, 1), (3, 1)], 'k>n is legal; unused servers stay idle', 'boundary')
    add(1, [(i, MAX_TIME) for i in range(1, 41)], 'serial backlog exceeds 32-bit completion time', 'boundary')
    add(2, [(MAX_TIME - 3 + i, MAX_TIME) for i in range(4)],
        'upper-bound arrivals and durations still need 64-bit sums', 'boundary')
    add(2, [(1, 100), (2, 2), (1000, 3), (1001, 1), (1002, 2)],
        'long idle period resets starts to upload times without losing server slots')

    for k in (1, 2, 3, 5):
        for length in (k, k + 1, 2 * k + 3):
            add(k, [(i + 1, 30) for i in range(length)], 'queue threshold and equal-duration waves')
            add(k, [(i + 1, 100 if i % 2 == 0 else 1) for i in range(length)],
                'alternating long/short jobs repeatedly reuse the earliest server')
            add(k, [(i * 101 + 1, i % 7 + 1) for i in range(length)],
                'sparse arrivals after all previous jobs finish')
            add(k, [(i + 1, length - i) for i in range(length)],
                'first wave has simultaneous completions; later wave may queue')

    rng = random.Random(SEED)
    while len(cases) < 159:
        n = rng.randint(1, 80)
        k = rng.randint(1, n + 5)
        mode = len(cases) % 4
        if mode == 0:
            arrivals = list(range(1, n + 1))
            durations = [rng.randint(1, 150) for _ in range(n)]
            reason = 'fixed-seed dense arrivals and sustained FIFO backlog'
        elif mode == 1:
            arrivals = sorted(rng.sample(range(1, MAX_TIME + 1), n))
            durations = [rng.randint(1, MAX_TIME) for _ in range(n)]
            reason = 'fixed-seed wide integer range and accumulated 64-bit completion times'
        elif mode == 2:
            arrivals = sorted(rng.sample(range(1, 2000), n))
            durations = [rng.choice((1, 2, 30, 1000)) for _ in range(n)]
            reason = 'fixed-seed sparse/clustered arrivals and mixed service durations'
        else:
            arrivals = list(range(MAX_TIME - n + 1, MAX_TIME + 1))
            durations = [rng.choice((1, MAX_TIME)) for _ in range(n)]
            reason = 'fixed-seed late dense arrivals and extreme duration imbalance'
        add(k, list(zip(arrivals, durations)), reason)

    add(MAX_COUNT, [(i, 1) for i in range(1, MAX_COUNT + 1)],
        'both counts at their legal maximum; every upload can start immediately', 'maxSize')
    return cases


def review(pid, tests, samples):
    _require_pid(pid)
    errors = []
    for name, pair in [*tests, *samples]:
        try:
            expected = list(map(str, answer(pid, parse(pid, pair['input']))))
            if pair['output'].split() != expected:
                raise ValueError('oracle output differs from supplied output tokens')
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            errors.append({'test': name, 'reason': str(exc)})
    return errors
