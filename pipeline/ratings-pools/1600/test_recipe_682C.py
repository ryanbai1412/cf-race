from pathlib import Path
import hashlib
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_682C as recipe

PID = '682C'
SAMPLE = ("9\n88 22 83 14 95 91 98 53 11\n3 24\n7 -8\n1 67\n1 64\n9 65\n5 12\n6 -80\n3 8", "5")
OFFICIAL_DIGEST = '2491d2678414079298c5d6267937a015251faf5682374cab0ce9fffd63abc38b'
# 161260901 (CF passedTestCount 16) first fails row 15, whose only c=-1 edge hides removed vertex 20. If this hand
# transcription is faithful, the pinned row is a non-prefix subset of the 106 CF tests and row 15 is CF test 17 or later.
FIRST_FAILING_ROW = {'18888172': 4, '20763132': 3, '20764615': 4, '37707078': 4, '126037219': 2, '161217644': 4, '161260901': 15}
PASSED = {"18888172": 3, "20763132": 2, "20764615": 3, "37707078": 3, "126037219": 1, "161217644": 3, "161260901": 16}
OFFICIAL = [
    ("9\r\n88 22 83 14 95 91 98 53 11\r\n3 24\r\n7 -8\r\n1 67\r\n1 64\r\n9 65\r\n5 12\r\n6 -80\r\n3 8\r\n", "5\r\n"),
    ("6\r\n53 82 15 77 71 23\r\n5 -77\r\n6 -73\r\n2 0\r\n1 26\r\n4 -92\r\n", "0\r\n"),
    ("10\r\n99 60 68 46 51 11 96 41 48 99\r\n4 50\r\n6 -97\r\n3 -92\r\n7 1\r\n9 99\r\n2 79\r\n1 -15\r\n8 -68\r\n5 -84\r\n", "7\r\n"),
    ("8\r\n53 41 22 22 34 95 56 24\r\n3 -20\r\n7 -56\r\n5 -3\r\n3 22\r\n1 37\r\n6 -34\r\n2 32\r\n", "1\r\n"),
    ("8\r\n2 19 83 95 9 87 15 6\r\n6 16\r\n7 98\r\n5 32\r\n7 90\r\n8 37\r\n2 -34\r\n1 -83\r\n", "5\r\n"),
    ("6\r\n60 89 33 64 92 75\r\n4 50\r\n1 32\r\n5 21\r\n3 77\r\n1 86\r\n", "4\r\n"),
    ("4\r\n14 66 86 37\r\n3 -9\r\n1 93\r\n2 -57\r\n", "3\r\n"),
    ("9\r\n59 48 48 14 51 51 86 53 58\r\n1 -47\r\n5 10\r\n8 -6\r\n9 46\r\n2 -69\r\n8 -79\r\n9 92\r\n6 12\r\n", "5\r\n"),
    ("3\r\n17 26 6\r\n1 -41\r\n2 -66\r\n", "0\r\n"),
    ("7\r\n63 3 67 55 14 19 96\r\n4 35\r\n1 -23\r\n3 -66\r\n2 80\r\n3 80\r\n2 -42\r\n", "4\r\n"),
    ("5\r\n91 61 4 61 35\r\n5 75\r\n2 13\r\n2 -15\r\n1 90\r\n", "4\r\n"),
    ("19\r\n40 99 20 54 5 31 67 73 10 46 70 68 80 74 7 58 75 25 13\r\n13 -28\r\n12 -33\r\n9 -62\r\n12 34\r\n15 70\r\n5 -22\r\n7 83\r\n2 -24\r\n6 -64\r\n17 62\r\n14 -28\r\n1 -83\r\n4 34\r\n8 -24\r\n11 19\r\n6 31\r\n7 -8\r\n16 90\r\n", "11\r\n"),
    ("39\r\n98 80 74 31 81 15 23 52 54 86 56 9 95 91 29 20 97 78 62 65 17 95 12 39 77 17 60 78 76 51 36 56 74 66 43 23 17 9 13\r\n15 21\r\n34 -35\r\n28 80\r\n13 -15\r\n29 -34\r\n38 -8\r\n18 10\r\n18 19\r\n27 54\r\n7 42\r\n16 49\r\n12 90\r\n39 33\r\n20 53\r\n2 91\r\n33 59\r\n29 -93\r\n36 29\r\n26 50\r\n5 -12\r\n33 -6\r\n17 -60\r\n27 7\r\n17 85\r\n31 63\r\n26 80\r\n1 -99\r\n4 -40\r\n10 -39\r\n11 36\r\n21 22\r\n16 -15\r\n14 -25\r\n25 30\r\n33 97\r\n38 26\r\n8 -78\r\n10 -7\r\n", "37\r\n"),
    ("19\r\n51 5 39 54 26 71 97 99 73 16 31 9 52 38 89 87 55 12 3\r\n18 -94\r\n19 -48\r\n2 -61\r\n10 72\r\n1 -82\r\n13 4\r\n19 -40\r\n16 -96\r\n6 -16\r\n19 -40\r\n13 44\r\n11 38\r\n15 -7\r\n6 8\r\n18 -32\r\n8 -75\r\n3 58\r\n10 -15\r\n", "7\r\n"),
    ("39\r\n100 83 92 26 10 63 56 85 12 64 25 50 75 51 11 41 78 53 52 96 63 12 48 88 57 57 25 52 69 45 4 97 5 87 58 15 72 59 100\r\n35 -60\r\n33 -39\r\n1 65\r\n11 -65\r\n34 -63\r\n38 84\r\n4 76\r\n22 -9\r\n6 -91\r\n23 -65\r\n18 7\r\n2 -17\r\n29 -15\r\n19 26\r\n29 23\r\n14 -12\r\n30 -72\r\n9 14\r\n12 -1\r\n27 -21\r\n32 -67\r\n7 -3\r\n26 -18\r\n12 -45\r\n33 75\r\n14 -86\r\n34 -46\r\n24 -44\r\n27 -29\r\n22 -39\r\n17 -73\r\n36 -72\r\n18 -76\r\n27 -65\r\n8 65\r\n24 -15\r\n35 79\r\n27 61\r\n", "38\r\n"),
    ("2\r\n83 33\r\n1 67\r\n", "1\r\n"),
    ("6\r\n538779323 241071283 506741761 673531032 208769045 334127496\r\n1 -532301622\r\n5 -912729787\r\n6 -854756762\r\n4 -627791911\r\n2 -289935846\r\n", "0\r\n"),
    ("10\r\n909382626 193846090 573881879 291637627 123338066 411896152 123287948 171497812 135534629 568762298\r\n9 -257478179\r\n4 -502075958\r\n2 -243790121\r\n2 -927464462\r\n8 -89981403\r\n1 -792322781\r\n10 -326468006\r\n7 -261940740\r\n4 -565652087\r\n", "0\r\n"),
]


def rooted(data):
    n, a, edges = data
    children = [[] for _ in range(n + 1)]
    for i, (p, c) in enumerate(edges):
        children[p].append((i + 2, c))
    order = [1]
    for u in order:
        order.extend(v for v, _ in children[u])
    return n, a, children, order


def subtree_size(children, v):
    stack, size = [v], 0
    while stack:
        u = stack.pop()
        size += 1
        stack.extend(w for w, _ in children[u])
    return size


def root_distance(data):
    n, a, children, _ = rooted(data)
    removed, stack = 0, [(1, 0)]
    while stack:
        u, d = stack.pop()
        if d > a[u - 1]:
            removed += subtree_size(children, u)
            continue
        stack.extend((v, d + c) for v, c in children[u])
    return removed


def positive_accumulation(data):
    n, a, children, _ = rooted(data)
    removed, stack = 0, [(1, 0)]
    while stack:
        u, value = stack.pop()
        for v, c in children[u]:
            if value + c > a[v - 1]:
                removed += subtree_size(children, v)
            else:
                stack.append((v, max(value, value + c)))
    return removed


def count_sad_only(data):
    n, a, children, _ = rooted(data)
    count, stack = 0, [(1, 0)]
    while stack:
        u, d = stack.pop()
        stack.extend((v, d + c) for v, c in children[u])
        count += d > a[u - 1]
    return count


def skip_minus_one(data):
    n, a, edges = data
    graph = [[] for _ in range(n)]
    for i, (p, c) in enumerate(edges):
        graph[i + 1].append((p - 1, c))
        graph[p - 1].append((i + 1, c))
    ready, dist, to_see, cutting = [False] * n, [0] * n, [0], []
    ready[0] = True
    while to_see:
        v = to_see.pop()
        for u, c in graph[v]:
            if not ready[u] and c != -1:
                ready[u] = True
                dist[u] = max(c, dist[v] + c)
                (cutting if dist[u] > a[u] else to_see).append(u)
    count = 0
    while cutting:
        v = cutting.pop()
        count += 1
        for u, c in graph[v]:
            if not ready[u] and c != -1:
                ready[u] = True
                cutting.append(u)
    return count


def index_bug(data):
    n, a, edges = data
    values = [0] + a
    graph = [[] for _ in range(n + 2)]
    for i, (p, c) in enumerate(edges):
        graph[i].append((p, c))
        graph[p].append((i, c))
    dist, visited, queue, count = [0] * (n + 2), [False] * (n + 2), [0], 0
    visited[0] = True
    for e in queue:
        if values[e] < dist[e]:
            continue
        count += 1
        for p, c in graph[e]:
            if not visited[p]:
                visited[p] = True
                dist[p] = max(dist[e] + c, 0)
                queue.append(p)
    return n - count


def ge_instead_of_gt(data):
    n, a, children, order = rooted(data)
    best, bad = [0] * (n + 1), [False] * (n + 1)
    for u in order:
        for v, c in children[u]:
            best[v] = max(best[u], 0) + c
            bad[v] = bad[u] or best[v] >= a[v - 1]
    return sum(bad)


def index_order_dp(data):
    n, a, edges = data
    best, bad = [0] * (n + 1), [False] * (n + 1)
    for i, (p, c) in enumerate(edges):
        best[i + 2] = max(best[p], 0) + c
        bad[i + 2] = bad[p] or best[i + 2] > a[i + 1]
    return sum(bad)


SOURCE_MUTANTS = {
    '20764615': root_distance,
    '161217644': root_distance,
    '37707078': root_distance,
    '18888172': positive_accumulation,
    '20763132': count_sad_only,
    '161260901': skip_minus_one,
    '126037219': index_bug,
}
MUTANTS = {
    'root-distance': root_distance,
    'positive-accumulation': positive_accumulation,
    'count-sad-only': count_sad_only,
    'skip-minus-one': skip_minus_one,
    'index-bug': index_bug,
    'ge-instead-of-gt': ge_instead_of_gt,
    'index-order-dp': index_order_dp,
}


class Recipe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)
        cls.parsed = [recipe.parse(PID, case['input']) for case in cls.cases]
        cls.official = [recipe.parse(PID, text) for text, _ in OFFICIAL]

    def test_embedded_official_matches_source_row(self):
        rows = [{'input': i, 'output': o} for i, o in OFFICIAL]
        blob = json.dumps(rows, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
        self.assertEqual(hashlib.sha256(blob).hexdigest(), OFFICIAL_DIGEST)

    def test_samples_and_official(self):
        self.assertEqual(recipe.answer(PID, recipe.parse(PID, SAMPLE[0])), 5)
        self.assertEqual(recipe.brute(recipe.parse(PID, SAMPLE[0])), 5)
        for data, (_, out) in zip(self.official, OFFICIAL):
            self.assertEqual(str(recipe.answer(PID, data)), out.strip())
        tests = [(f'{i + 1:04d}', {'input': t, 'output': o}) for i, (t, o) in enumerate(OFFICIAL)]
        self.assertEqual(recipe.review(PID, tests, [('sample', {'input': SAMPLE[0], 'output': SAMPLE[1]})]), [])

    def test_official_parents_point_toward_root(self):
        larger = 0
        for n, _, edges in self.official:
            larger += sum(p > i + 2 for i, (p, _) in enumerate(edges))
            _, _, children, order = rooted((n, [1] * n, edges))
            self.assertEqual(sorted(order), list(range(1, n + 1)))
        self.assertGreater(larger, 50)

    def test_source_mutants_first_failing_official_row(self):
        for sid, row in FIRST_FAILING_ROW.items():
            mutant = SOURCE_MUTANTS[sid]
            results = [str(mutant(d)) == out.strip() for d, (_, out) in zip(self.official, OFFICIAL)]
            self.assertEqual(results.index(False) + 1, row, sid)
            self.assertLessEqual(row, PASSED[sid] + 1, sid)

    def test_mutants_killed_by_extras(self):
        for name, mutant in MUTANTS.items():
            kills = sum(str(mutant(d)) != c['output'].strip() for d, c in zip(self.parsed, self.cases))
            self.assertGreaterEqual(kills, 10, name)
        for data, case in zip(self.parsed, self.cases):
            for name in MUTANTS:
                if f'[kills {name}]' in case['reason']:
                    self.assertNotEqual(str(MUTANTS[name](data)), case['output'].strip(), (name, case['reason']))

    def test_extras_shape(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        self.assertEqual({c['category'] for c in self.cases}, {'boundary', 'adversarial', 'maxSize'})
        sizes = [d[0] for d in self.parsed]
        self.assertIn(1, sizes)
        self.assertIn(recipe.MAX_N, sizes)
        for data, case in zip(self.parsed, self.cases):
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            n = data[0]
            lines = case['input'].split('\n')
            self.assertEqual(lines[-1], '')
            self.assertEqual([len(line.split()) for line in lines[:-1]], [1, n] + [2] * (n - 1))
            self.assertEqual(recipe.render(*data), case['input'])
            self.assertRegex(case['output'], r'^(0|[1-9][0-9]*)\n$')
            self.assertLessEqual(int(case['output']), n - 1)
        self.assertEqual(recipe.extras(PID), self.cases)
        self.assertTrue(any(max(abs(c) for _, c in d[2]) == recipe.MAX_A for d in self.parsed if d[2]))

    def test_large_extras_two_references(self):
        for data, case in zip(self.parsed, self.cases):
            if data[0] > 8:
                self.assertEqual(recipe.prefix_reference(data), int(case['output']))

    def test_parse_rejects(self):
        bad = ['', '0\n', '100001\n', '1\n0\n', '1\n1000000001\n', '1\n1 2\n', '2\n1 1\n1 1000000001\n',
               '2\n1 1\n2 0\n', '2\n1 1\n3 0\n', '2\n1 1\n1\n', '2\n1 1\n1 0 0\n', '2\n1 1 1 0\n', '2\n1\n1\n1 0\n',
               '3\n1 1 1\n3 0\n2 0\n', '2\n1 1\n1 -0\n', '2\n1 1\n1 +5\n', '1\n01\n', '+1\n1\n', '2\n1 1\n\n1 0\n',
               '2\n1 1\n1 -1000000001\n', '3\n1 1 1\n1 0\n']
        for text in bad:
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse(PID, text)
        self.assertEqual(recipe.parse(PID, '2\r\n1 1\r\n1 -1000000000\r\n'), (2, [1, 1], [(1, -1000000000)]))
        self.assertEqual(recipe.parse(PID, '1\n7'), (1, [7], []))
        with self.assertRaises(ValueError):
            recipe.parse('682B', '1\n1\n')

    def test_review_flags_bad_pairs(self):
        bad = [('x', {'input': '2\n1 1\n1 1\n', 'output': '1\n'}), ('y', {'input': '2\n1 1\n1 2\n', 'output': '1 0\n'}),
               ('z', {'input': '2\n1 1\n2 2\n', 'output': '1\n'}), ('w', {'input': '1\n1\n', 'output': '0\n'})]
        self.assertEqual([f['test'] for f in recipe.review(PID, bad, [])], ['x', 'y', 'z'])

    def test_brute_is_exhaustive_and_agrees(self):
        self.assertGreater(recipe.brute_checks()[PID], 15000)
        self.assertEqual(recipe.brute((3, [1, 1, 9], [(1, 5), (2, -5)])), 2)
        self.assertEqual(recipe.brute((1, [1], [])), 0)
        self.assertEqual(recipe.brute((4, [10, 10, 10, 4], [(1, 5), (2, -5), (3, 3)])), 0)


if __name__ == '__main__':
    unittest.main()
