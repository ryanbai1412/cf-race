from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_741B as recipe

PID = '741B'
OFFICIAL = [
    ('3 1 5\r\n3 2 5\r\n2 4 2\r\n1 2\r\n',
     '6\r\n'),
    ('4 2 11\r\n2 4 6 6\r\n6 4 2 1\r\n1 2\r\n2 3\r\n',
     '7\r\n'),
    ('10 5 100\r\n70 67 8 64 28 82 18 61 82 7\r\n596434 595982 237932 275698 361351 850374 936914 877996 789231 331012\r\n1 7\r\n2 4\r\n3 6\r\n5 7\r\n1 5\r\n',
     '2383854\r\n'),
    ('10 5 100\r\n64 90 3 94 96 97 52 54 82 31\r\n796554 444893 214351 43810 684158 555762 686198 339093 383018 699152\r\n6 8\r\n8 3\r\n3 9\r\n2 3\r\n10 3\r\n',
     '1495706\r\n'),
    ('10 5 100\r\n6 18 35 6 87 58 4 53 37 71\r\n465782 57034 547741 748298 315223 370368 679320 349012 9740 622511\r\n1 2\r\n10 9\r\n6 7\r\n3 6\r\n7 1\r\n',
     '2050129\r\n'),
    ('10 5 100\r\n78 89 3 2 95 96 87 11 13 60\r\n694709 921 799687 428614 221900 536251 117674 36488 219932 771513\r\n4 5\r\n3 4\r\n6 2\r\n2 3\r\n8 3\r\n',
     '1791132\r\n'),
    ('10 5 100\r\n48 73 30 46 95 19 98 73 94 24\r\n501216 675859 843572 565104 879875 828759 80776 766980 213551 492652\r\n1 2\r\n6 5\r\n7 6\r\n10 3\r\n8 1\r\n',
     '2237435\r\n'),
    ('10 5 100\r\n68 55 15 94 53 100 52 68 24 3\r\n286803 660813 226501 624597 215418 290774 416040 961916 910482 50278\r\n1 5\r\n7 2\r\n2 8\r\n5 3\r\n10 3\r\n',
     '1922676\r\n'),
    ('10 5 100\r\n19 8 95 18 9 79 42 94 20 49\r\n735491 935681 717266 935275 521356 866021 356037 394445 589369 585077\r\n9 4\r\n5 6\r\n5 1\r\n1 4\r\n7 1\r\n',
     '2456033\r\n'),
]
SAMPLES = [
    ('3 1 5\n3 2 5\n2 4 2\n1 2', '6'),
    ('4 2 11\n2 4 6 6\n6 4 2 1\n1 2\n2 3', '7'),
]
RECORDED_PASSED = {'22883084': 2, '24463764': 3, '31203300': 1, '99278712': 2, '99288023': 3, '217131005': 1, '217134094': 0}


def _groups_dsu(n, edges):
    return recipe.groups_dsu(n, edges)


def index_as_weight(data):
    lim, w, b, edges = data
    n = len(w)
    w, b = [0] + w, [0] + b
    fa = list(range(n + 1))

    def find(x):
        while fa[x] != x:
            x = fa[x]
        return x

    for x, y in edges:
        fa[find(x)] = find(y)
    c, d, v = [0] * (n + 1), [0] * (n + 1), [[] for _ in range(n + 1)]
    for i in range(1, n + 1):
        c[i] += w[i]
        d[i] += b[i]
        v[find(i)].append(i)
    f = [0] * (lim + 100)
    for i in range(1, n + 1):
        if fa[i] == i:
            for j in range(lim, -1, -1):
                for t in v[i]:
                    if j >= t:
                        f[j] = max(f[j], f[j - t] + b[t])
                if j >= c[i]:
                    f[j] = max(f[j], f[j - c[i]] + d[i])
    return f[lim]


def directed_adjacency(data):
    cap, w, b, edges = data
    n = len(w)
    adj = {}
    for x, y in edges:
        adj.setdefault(x, []).append(y)
        adj.setdefault(y, []).append(y)
    visited, components = set(), []
    for i in range(1, n + 1):
        if i not in visited:
            visited.add(i)
            comp, queue = [i], [i]
            while queue:
                cur = queue.pop(0)
                for j in adj.get(cur, []):
                    if j not in visited:
                        visited.add(j)
                        queue.append(j)
                        comp.append(j)
            components.append([u - 1 for u in comp])
    return _grouped(cap, w, b, components)


def _grouped(cap, w, b, groups):
    dp = [0] * (cap + 1)
    for g in groups:
        options = [(w[i], b[i]) for i in g] + [(sum(w[i] for i in g), sum(b[i] for i in g))]
        new = dp[:]
        for j in range(cap + 1):
            for wt, val in options:
                if wt <= j:
                    new[j] = max(new[j], dp[j - wt] + val)
        dp = new
    return dp[cap]


def independent_members(data):
    cap, w, b, edges = data
    groups = _groups_dsu(len(w), edges)
    d = [1] + [0] * cap

    def item(W, B):
        for D in range(cap - W, -1, -1):
            if d[D]:
                d[D + W] = max(d[D + W], d[D] + B)

    for g in groups:
        if len(g) < 2:
            continue
        item(sum(w[i] for i in g), sum(b[i] for i in g))
        for i in g:
            item(w[i], b[i])
    for g in groups:
        if len(g) == 1:
            item(w[g[0]], b[g[0]])
    return max(d) - 1


def ratio_representative(data):
    cap, weights, beauties, edges = data
    n = len(weights)
    adj = [[False] * n for _ in range(n)]
    for x, y in edges:
        adj[x - 1][y - 1] = adj[y - 1][x - 1] = True
    remaining = set(range(n))

    def dfs(u):
        tw = mw = weights[u]
        tb = mb = beauties[u]
        for v in range(n):
            if v in remaining and adj[u][v]:
                remaining.remove(v)
                pair = dfs(v)
                tw += pair[0]
                tb += pair[1]
                if pair[3] / pair[2] > mb / mw:
                    mw, mb = pair[2], pair[3]
        return tw, tb, mw, mb

    ws, bs, mws, mbs = [], [], [], []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        pair = dfs(start)
        ws.append(pair[0])
        bs.append(pair[1])
        mws.append(pair[2])
        mbs.append(pair[3])
    dp = [[0] * (cap + 1) for _ in range(len(ws))]
    for j in range(cap + 1):
        if ws[0] <= j:
            dp[0][j] = bs[0]
        if mws[0] <= j and mbs[0] > dp[0][j]:
            dp[0][j] = mbs[0]
    for i in range(1, len(ws)):
        for j in range(1, cap + 1):
            if ws[i] <= j:
                dp[i][j] = max(bs[i], bs[i] + dp[i - 1][j - ws[i]], dp[i - 1][j])
            if mws[i] <= j:
                dp[i][j] = max(mbs[i], mbs[i] + dp[i - 1][j - mws[i]], dp[i - 1][j], dp[i][j])
    return dp[len(ws) - 1][cap]


def consecutive_slices(data):
    cap, ws, bs, edges = data
    n = len(ws)
    graph = {}
    for x, y in edges:
        graph.setdefault(x - 1, []).append(y - 1)
        graph.setdefault(y - 1, []).append(x - 1)
    groups, visited = [], set()

    def dfs(v, group):
        visited.add(v)
        group.add(v)
        for u in graph[v]:
            if u not in visited:
                dfs(u, group)

    for vertex in list(graph):
        if vertex not in visited:
            groups.append(set())
            dfs(vertex, groups[-1])
    groups += [{i} for i in range(n) if i not in visited]
    master, index, new_master = [0] * (cap + 1), 0, None
    for group in groups:
        matrix = [master] + [[0] * (cap + 1) for _ in group]
        pg = vg = 0
        for i in range(1, len(group) + 1):
            pi, vi = ws[index + i - 1], bs[index + i - 1]
            pg += pi
            vg += vi
            for p in range(1, cap + 1):
                com = commaster = 0
                if pi <= p:
                    com, commaster = vi, matrix[0][max(p - pi, 0)] + vi
                matrix[i][p] = max(com, matrix[i - 1][p], commaster)
        new_master = [0] * (cap + 1)
        for p in range(1, cap + 1):
            com = commaster = 0
            if pg <= p:
                com, commaster = vg, matrix[0][max(p - pg, 0)] + vg
            new_master[p] = max(com, matrix[-1][p], commaster)
        master = new_master
        index += len(group)
    return new_master[-1]


def group_blind(data):
    cap, w, b, _ = data
    dp = [0] * (cap + 1)
    for wt, val in zip(w, b):
        for j in range(cap, wt - 1, -1):
            dp[j] = max(dp[j], dp[j - wt] + val)
    return dp[cap]


def beauty_greedy(data):
    cap, w, b, edges = data
    friends = [[] for _ in w]
    for x, y in edges:
        friends[x - 1].append(y - 1)
        friends[y - 1].append(x - 1)
    total, invited = 0, set()
    for girl in sorted(range(len(w)), key=lambda i: b[i], reverse=True):
        if all(f not in invited for f in friends[girl]) and cap - w[girl] >= 0:
            total += b[girl]
            invited.add(girl)
            cap -= w[girl]
    return total


def unbounded_grouped(data):
    cap, w, b, edges = data
    dp = [0] * (cap + 1)
    for g in _groups_dsu(len(w), edges):
        options = [(w[i], b[i]) for i in g] + ([(sum(w[i] for i in g), sum(b[i] for i in g))] if len(g) > 1 else [])
        for j in range(cap + 1):
            for wt, val in options:
                if wt <= j:
                    dp[j] = max(dp[j], dp[j - wt] + val)
    return dp[cap]


def member_outer_in_place(data):
    cap, w, b, edges = data
    dp = [0] * (cap + 1)
    for g in _groups_dsu(len(w), edges):
        options = [(w[i], b[i]) for i in g] + ([(sum(w[i] for i in g), sum(b[i] for i in g))] if len(g) > 1 else [])
        for wt, val in options:
            for j in range(cap, wt - 1, -1):
                dp[j] = max(dp[j], dp[j - wt] + val)
    return dp[cap]


def whole_group_forgotten(data):
    cap, w, b, edges = data
    return _grouped_custom(cap, w, b, edges, whole=False, singles=True)


def singles_forgotten(data):
    cap, w, b, edges = data
    return _grouped_custom(cap, w, b, edges, whole=True, singles=False)


def _grouped_custom(cap, w, b, edges, whole, singles):
    dp = [0] * (cap + 1)
    for g in _groups_dsu(len(w), edges):
        options = [(w[i], b[i]) for i in g] if singles or len(g) == 1 else []
        if whole and len(g) > 1:
            options.append((sum(w[i] for i in g), sum(b[i] for i in g)))
        new = dp[:]
        for wt, val in options:
            for j in range(wt, cap + 1):
                new[j] = max(new[j], dp[j - wt] + val)
        dp = new
    return dp[cap]


RECORDED = {'22883084': index_as_weight, '24463764': directed_adjacency, '31203300': independent_members,
            '99278712': ratio_representative, '99288023': consecutive_slices, '217131005': group_blind,
            '217134094': beauty_greedy}
MUTANTS = {**{f.__name__: f for f in RECORDED.values()}, 'unbounded_grouped': unbounded_grouped,
           'member_outer_in_place': member_outer_in_place, 'whole_group_forgotten': whole_group_forgotten,
           'singles_forgotten': singles_forgotten}


class LayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        expected = (5, [3, 2, 5], [2, 4, 2], [(1, 2)])
        self.assertEqual(recipe.parse(PID, SAMPLES[0][0]), expected)
        self.assertEqual(recipe.parse(PID, OFFICIAL[0][0]), expected)
        self.assertEqual(recipe.parse(PID, '1 0 1\n1\n1'), (1, [1], [1], []))

    def test_rejects_bad_layout_arity_ranges_and_pairs(self):
        bad = ['', '1 0 1\n1\n', '0 0 1\n\n\n', '1001 0 1\n' + '1 ' * 1001 + '\n' + '1 ' * 1001 + '\n',
               '1 0 0\n1\n1\n', '1 0 1001\n1\n1\n', '1 1 1\n1\n1\n1 1\n', '2 2 5\n1 1\n1 1\n1 2\n2 1\n1 2\n',
               '2 1 5\n1 1\n1 1\n1 2\n1 2\n', '2 2 5\n1 1\n1 1\n1 2\n1 2\n', '2 1 5\n1 1\n1 1\n1 3\n', '2 1 5\n1 1\n1 1\n0 1\n',
               '1 0 1\n1001\n1\n', '1 0 1\n0\n1\n', '1 0 1\n1\n1000001\n', '1 0 1\n1\n0\n', '1 0 1\n+1\n1\n',
               '1 0 1\n01\n1\n', '1 0 1\n1 1\n1\n', '2 0 1\n1\n1 1\n1\n', '2 0 1\n1 1 1 1\n', '2 1 5\n1 1\n1 1\n1 2 1\n',
               '2 1 5\n1 1\n1 1\n1\n2\n', '1 0 1\n1\n1\n\n', '\n1 0 1\n1\n1\n', '1 0\n1\n1\n', '1 0 1 1\n1\n1\n', '1 -1 1\n1\n1\n',
               '3 0 5\n1 1 1\n1 1 1\n1 2\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse(PID, text)

    def test_reverse_pair_is_a_distinct_ordered_pair(self):
        self.assertEqual(recipe.parse(PID, '2 1 5\n1 1\n1 1\n2 1\n')[3], [(2, 1)])
        self.assertEqual(recipe.answer(PID, recipe.parse(PID, '2 1 1\n1 1\n3 4\n2 1\n')), 4)


class OracleTests(unittest.TestCase):
    def test_samples_and_official_rows(self):
        tests = [(f'{i:04d}', {'input': a, 'output': b}) for i, (a, b) in enumerate(OFFICIAL, 1)]
        samples = [(f's{i}', {'input': a, 'output': b}) for i, (a, b) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review(PID, tests, samples), [])
        for text, out in [*SAMPLES, *OFFICIAL]:
            data = recipe.parse(PID, text)
            self.assertEqual(recipe.sparse_exact(data), int(out))
            self.assertEqual(recipe.brute_subsets(data), int(out))
            self.assertEqual(recipe.brute_choices(data), int(out))

    def test_review_reports_disagreement_layout_and_invalid_input(self):
        failures = recipe.review(PID, [('a', {'input': '1 0 1\n1\n5\n', 'output': '4\n'}),
                                       ('b', {'input': '1 0 1\n1\n5\n', 'output': '5 0\n'}),
                                       ('c', {'input': '1 0 1\n1\n5\n', 'output': '5\n0\n'}),
                                       ('d', {'input': '1 1 1\n1\n5\n1 1\n', 'output': '5\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b', 'c', 'd'])
        self.assertEqual(failures[0]['expected'], '5')
        self.assertIn('layout', failures[1]['reason'])

    def test_recorded_wrong_answer_models_pass_then_fail_like_the_sources(self):
        rows = [recipe.parse(PID, text) for text, _ in OFFICIAL]
        expected = [int(out) for _, out in OFFICIAL]
        for sid, wrong in RECORDED.items():
            passed = RECORDED_PASSED[sid]
            with self.subTest(sid=sid):
                self.assertEqual([wrong(d) for d in rows[:passed]], expected[:passed])
                self.assertNotEqual(wrong(rows[passed]), expected[passed])

    def test_brute_checks_are_real(self):
        result = recipe.brute_checks()
        self.assertEqual(set(result), {PID})
        self.assertGreater(result[PID], 100000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)
        cls.parsed = [recipe.parse(PID, c['input']) for c in cls.cases]

    def test_layout_answers_and_counts(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        self.assertFalse({c['input'] for c in self.cases} & {a.replace('\r\n', '\n') for a, _ in OFFICIAL})
        self.assertLess(len(json.dumps(self.cases)), 6 * 2 ** 20)
        for case, data in zip(self.cases, self.parsed):
            cap, weights, beauties, edges = data
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            lines = case['input'].split('\n')
            self.assertEqual(len(lines), 4 + len(edges))
            self.assertEqual(lines[-1], '')
            self.assertEqual(lines[0], f'{len(weights)} {len(edges)} {cap}')
            self.assertEqual([len(lines[1].split(' ')), len(lines[2].split(' '))], [len(weights)] * 2)
            self.assertTrue(all(len(line.split(' ')) == 2 for line in lines[3:-1]))
            self.assertEqual(len({tuple(sorted(e)) for e in edges}), len(edges))
            self.assertEqual(case['output'], f'{recipe.answer(PID, data)}\n')
            self.assertEqual(case['output'], f'{recipe.sparse_exact(data)}\n')
            if len(weights) <= 10:
                self.assertEqual(case['output'], f'{recipe.brute_subsets(data)}\n')
                self.assertEqual(case['output'], f'{recipe.brute_choices(data)}\n')
        self.assertEqual(json.dumps(recipe.extras(PID)), json.dumps(self.cases))

    def test_extremes_present(self):
        dims = [(len(w), len(e), cap) for cap, w, _, e in self.parsed]
        self.assertIn((1, 0, 1), dims)
        self.assertIn((recipe.MAX_N, recipe.MAX_M, recipe.MAX_W), dims)
        outputs = [int(c['output']) for c in self.cases]
        self.assertIn(0, outputs)
        self.assertEqual(max(outputs), recipe.MAX_N * recipe.MAX_B)
        self.assertTrue(any(len(e) == len(w) * (len(w) - 1) // 2 and len(w) == 447 for _, w, _, e in self.parsed))

    def test_labelled_cases_kill_their_mutants(self):
        labels = {'w=10 variant of sample 2': (independent_members, group_blind),
                  'two members (10) are illegal': (group_blind, independent_members),
                  'group-blind knapsack and one-directional adjacency': (group_blind, directed_adjacency),
                  'never reaches 4': (directed_adjacency,), 'listed high-to-low': (directed_adjacency,),
                  'takes Hos 2 (4) and then nothing fits': (beauty_greedy,), 'stuck at 10': (beauty_greedy,),
                  'friend-skipping greedy and whole-group-forgotten': (beauty_greedy, whole_group_forgotten),
                  'costed by its index 1': (index_as_weight,), 'index-as-weight costing': (index_as_weight,),
                  'instead of carrying dp[i-1][j]': (ratio_representative,), 'dropped carry': (ratio_representative,),
                  'best-ratio representative': (ratio_representative,), 'forgetting single members': (singles_forgotten,),
                  'stack on the whole-group item': (independent_members, member_outer_in_place),
                  'member-outer in-place': (member_outer_in_place,), 'consecutive-index slicing': (consecutive_slices,),
                  'reuses the weight-1 Hos': (unbounded_grouped,), 'whole-group-forgotten solutions print 5': (whole_group_forgotten,)}
        for fragment, wrongs in labels.items():
            matching = [d for c, d in zip(self.cases, self.parsed) if fragment in c['reason']]
            with self.subTest(fragment=fragment):
                self.assertEqual(len(matching), 1)
                for wrong in wrongs:
                    self.assertNotEqual(wrong(matching[0]), recipe.answer(PID, matching[0]), wrong.__name__)

    def test_every_mutant_is_killed(self):
        small = [d for d in self.parsed if len(d[1]) <= 100]
        for name, wrong in MUTANTS.items():
            with self.subTest(wrong=name):
                self.assertTrue(any(wrong(d) != recipe.answer(PID, d) for d in small))


if __name__ == '__main__':
    unittest.main()
