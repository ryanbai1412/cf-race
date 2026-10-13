import itertools
import json
from parent_replay import BASE


def expected(pid, text):
    values = text.split()
    if pid == '514A':
        assert len(values) == 1 and values[0].isdigit() and 1 <= int(values[0]) <= 10**18
        out = ''
        for i, digit in enumerate(values[0]):
            choices = [digit, str(9 - int(digit))]
            if i == 0:
                choices = [d for d in choices if d != '0']
            out += min(choices)
        return out
    if pid == '55A':
        assert len(values) == 1
        n = int(values[0])
        assert 1 <= n <= 1000
        position = 0
        seen = {0}
        for jump in range(1, 2 * n + 1):
            position = (position + jump) % n
            seen.add(position)
        return 'YES' if len(seen) == n else 'NO'
    if pid == '560B':
        v = list(map(int, values))
        assert len(v) == 6 and all(1 <= x <= 1000 for x in v)
        W, H, a, b, c, d = v
        possible = any((w1 + w2 <= W and max(h1, h2) <= H) or
                       (max(w1, w2) <= W and h1 + h2 <= H)
                       for w1, h1 in [(a, b), (b, a)]
                       for w2, h2 in [(c, d), (d, c)])
        return 'YES' if possible else 'NO'
    if pid == '592A':
        assert len(values) == 8 and all(len(row) == 8 and set(row) <= set('.WB') for row in values)
        a = []; b = []
        for r in range(8):
            for c in range(8):
                if values[r][c] == 'W' and all(values[k][c] == '.' for k in range(r)):
                    a.append(r)
                if values[r][c] == 'B' and all(values[k][c] == '.' for k in range(r + 1, 8)):
                    b.append(7 - r)
        assert a or b
        return 'A' if min(a, default=99) <= min(b, default=99) else 'B'
    if pid == '732C':
        v = list(map(int, values))
        assert len(v) == 3 and all(0 <= x <= 10**18 for x in v) and sum(v) >= 1
        m = max(v); minimum = 10**20
        for length in range(max(1, 3 * m - 5), 3 * m + 4):
            for start in range(3):
                available = [length // 3] * 3
                for offset in range(length % 3):
                    available[(start + offset) % 3] += 1
                if all(available[i] >= v[i] for i in range(3)):
                    minimum = min(minimum, length - sum(v))
        return str(minimum)
    if pid == '743A':
        assert len(values) == 4
        n, a, b = map(int, values[:3]); s = values[3]
        assert 2 <= n <= 100000 and 1 <= a <= n and 1 <= b <= n and a != b
        assert len(s) == n and set(s) <= {'0', '1'}
        return str(int(s[a - 1] != s[b - 1]))
    if pid == '765C':
        v = list(map(int, values)); assert len(v) == 3
        k, a, b = v
        assert 1 <= k <= 10**9 and 0 <= a <= 10**9 and 0 <= b <= 10**9 and a + b > 0
        p, q = a // k, b // k
        if (p == 0 and b % k != 0) or (q == 0 and a % k != 0) or p + q == 0:
            return '-1'
        return str(p + q)
    if pid == '79A':
        assert len(values) == 2
        x, y = map(int, values); assert 0 <= x <= 10**6 and 0 <= y <= 10**6
        turn = 0
        while True:
            options = [(a, 22 - 10 * a) for a in range(3) if a <= x and 22 - 10 * a <= y]
            if not options:
                return 'Hanako' if turn == 0 else 'Ciel'
            a, b = max(options) if turn == 0 else min(options)
            x -= a; y -= b; turn ^= 1
    if pid == '812A':
        v = list(map(int, values)); assert len(v) == 16 and set(v) <= {0, 1}
        lights = [v[i:i + 4] for i in range(0, 16, 4)]
        hit = False
        for i in range(4):
            if not lights[i][3]:
                continue
            hit |= any(lights[i][:3])
            hit |= bool(lights[(i + 1) % 4][0] or lights[(i + 2) % 4][1] or lights[(i + 3) % 4][2])
        return 'YES' if hit else 'NO'
    if pid == '817A':
        v = list(map(int, values)); assert len(v) == 6
        x1, y1, x2, y2, a, b = v
        assert all(-10**5 <= x <= 10**5 for x in v[:4]) and 1 <= a <= 10**5 and 1 <= b <= 10**5
        dx, dy = x2 - x1, y2 - y1
        possible = dx % a == dy % b == 0 and (dx // a - dy // b) % 2 == 0
        return 'YES' if possible else 'NO'
    if pid == '854B':
        n, k = map(int, values); assert len(values) == 2 and 1 <= n <= 10**9 and 0 <= k <= n
        return f'{int(0 < k < n)} {min(2 * k, n - k)}'
    if pid == '870B':
        v = list(map(int, values)); n, k = v[:2]; a = v[2:]
        assert 1 <= k <= n <= 100000 and len(a) == n and all(-10**9 <= x <= 10**9 for x in a)
        if n <= 14:
            best = -10**10
            for cuts in itertools.combinations(range(1, n), k - 1):
                ends = (0,) + cuts + (n,)
                best = max(best, max(min(a[ends[i]:ends[i + 1]]) for i in range(k)))
        else:
            best = min(a) if k == 1 else max(a[0], a[-1]) if k == 2 else max(a)
        return str(best)
    if pid == '913B':
        v = list(map(int, values)); n = v[0]; parents = v[1:]
        assert 3 <= n <= 1000 and len(parents) == n - 1
        children = [[] for _ in range(n)]
        for vertex, parent in enumerate(parents, 1):
            assert 1 <= parent <= vertex
            children[parent - 1].append(vertex)
        assert len(children[0]) >= 2
        return 'Yes' if all(not c or sum(not children[child] for child in c) >= 3 for c in children) else 'No'
    if pid == '914B':
        v = list(map(int, values)); n = v[0]; a = v[1:]
        assert 1 <= n <= 10**5 and len(a) == n and all(1 <= x <= 10**5 for x in a)
        counts = {x: a.count(x) for x in set(a)}
        return 'Conan' if any(c % 2 for c in counts.values()) else 'Agasa'
    if pid == '928A':
        assert len(values) >= 3
        s, n = values[0], int(values[1]); logins = values[2:]
        assert 1 <= n <= 1000 and len(logins) == n
        def canonical(s):
            assert 1 <= len(s) <= 50 and all(c.isascii() and (c.isalnum() or c == '_') for c in s)
            return ''.join('0' if c in 'oO0' else '1' if c in 'iIlL1' else c.lower() for c in s)
        keys = [canonical(login) for login in logins]
        assert len(set(keys)) == len(keys)
        return 'No' if canonical(s) in keys else 'Yes'
    if pid == '931B':
        n, a, b = map(int, values)
        assert len(values) == 3 and 2 <= n <= 256 and n & (n - 1) == 0 and 1 <= a <= n and 1 <= b <= n and a != b
        round_number = 0; a -= 1; b -= 1
        while a != b:
            a //= 2; b //= 2; round_number += 1
        return 'Final!' if 2**round_number == n else str(round_number)
    if pid == '960A':
        assert len(values) == 1 and 1 <= len(values[0]) <= 5000 and set(values[0]) <= set('abc')
        s = values[0]; a, b, c = (s.count(ch) for ch in 'abc')
        return 'YES' if min(a, b, c) > 0 and s == 'a' * a + 'b' * b + 'c' * c and c in (a, b) else 'NO'
    if pid == '998B':
        v = list(map(int, values)); n, budget = v[:2]; a = v[2:]
        assert 2 <= n <= 100 and 1 <= budget <= 100 and len(a) == n and all(1 <= x <= 100 for x in a)
        assert sum(x % 2 for x in a) * 2 == n
        balance = 0; costs = []
        for i, x in enumerate(a[:-1]):
            balance += 1 if x % 2 else -1
            if balance == 0:
                costs.append(abs(x - a[i + 1]))
        best = [0] * (budget + 1)
        for cost in costs:
            for money in range(budget, cost - 1, -1):
                best[money] = max(best[money], best[money - cost] + 1)
        return str(best[budget])
    raise ValueError(pid)


def main():
    from parent_replay import audit_file, read
    replay = read(BASE / 'parent-replay.json')
    checked = []
    for pid, row in replay['packages'].items():
        if not row['childGate']['passed']:
            continue
        root = next((BASE / f"current-child-{row['child']}").iterdir())
        a = read(audit_file(root, row['child'], pid))
        for sid, analysis in a['incorrectAnalysis'].items():
            c = analysis['semanticReview']['counterexample']
            raw = next(c[k] for k in ['validLFInput', 'validLF', 'input'] if k in c)
            out = expected(pid, raw)
            assert out.lower().split() == str(c['correctAnswer']).lower().split(), (pid, sid, out, c['correctAnswer'])
            checked.append({'id': pid, 'submissionId': sid, 'test': c['test'], 'answer': out, 'constraintValid': True})
        print('PRIMARY_MATH', pid, 5, flush=True)
    counts = {state: sum(replay['packages'][r['id']]['technicalState'] == state for r in checked) for state in ['qualified', 'rejected', 'held']}
    (BASE / 'parent-math.json').write_text(json.dumps({'counterexamples': checked, 'count': len(checked), 'qualifiedCases': counts['qualified'], 'heldCases': counts['held'], 'rejectedCases': counts['rejected']}, indent=2) + '\n')


if __name__ == '__main__':
    main()
