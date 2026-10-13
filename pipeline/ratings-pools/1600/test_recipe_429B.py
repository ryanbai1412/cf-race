import json
from pathlib import Path
import unittest

import recipe_429B as recipe


OFFICIAL = [
    ('3 3\r\n100 100 100\r\n100 1 100\r\n100 100 100\r\n', '800'),
    ('4 5\r\n87882 40786 3691 85313 46694\r\n28884 16067 3242 97367 78518\r\n4250 35501 9780 14435 19004\r\n'
     '64673 65438 56977 64495 27280\r\n', '747898'),
    ('3 3\r\n3 1 2\r\n3 2 0\r\n2 3 2\r\n', '16'),
    ('3 3\r\n1 10 1\r\n1 10 1\r\n1 10 1\r\n', '26'),
    ('3 3\r\n0 0 0\r\n0 10000 0\r\n0 0 0\r\n', '0'),
    ('3 3\r\n1 1 1\r\n0 10000 0\r\n1 1 1\r\n', '6'),
    ('3 3\r\n9 0 9\r\n0 9 9\r\n9 9 9\r\n', '54'),
    ('3 3\r\n0 0 0\r\n0 100 0\r\n0 0 0\r\n', '0'),
    ('3 3\r\n100000 100000 100000\r\n1 100000 100000\r\n1 1 100000\r\n', '500003'),
    ('3 3\r\n100 0 100\r\n1 100 100\r\n0 100 100\r\n', '501'),
]
SAMPLE = ('3 3\n100 100 100\n100 1 100\n100 100 100', '800')


def corner_tables(n, m, a):
    def get(t, i, j):
        return t[i][j] if 0 <= i < n and 0 <= j < m else 0
    tl = [[0] * m for _ in range(n)]
    br = [[0] * m for _ in range(n)]
    bl = [[0] * m for _ in range(n)]
    tr = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            tl[i][j] = a[i][j] + max(get(tl, i - 1, j), get(tl, i, j - 1))
    for i in reversed(range(n)):
        for j in reversed(range(m)):
            br[i][j] = a[i][j] + max(get(br, i + 1, j), get(br, i, j + 1))
    for i in reversed(range(n)):
        for j in range(m):
            bl[i][j] = a[i][j] + max(get(bl, i + 1, j), get(bl, i, j - 1))
    for i in range(n):
        for j in reversed(range(m)):
            tr[i][j] = a[i][j] + max(get(tr, i - 1, j), get(tr, i, j + 1))
    return lambda t, i, j: get({'tl': tl, 'br': br, 'bl': bl, 'tr': tr}[t], i, j)


def wrong_ideas(n, m, a):
    g = corner_tables(n, m, a)
    interior = [(i, j) for i in range(1, n - 1) for j in range(1, m - 1)]
    cells = [(i, j) for i in range(n) for j in range(m)]

    def v(i, j):
        return g('tl', i - 1, j) + g('br', i + 1, j) + g('bl', i, j - 1) + g('tr', i, j + 1)

    def h(i, j):
        return g('tl', i, j - 1) + g('br', i, j + 1) + g('bl', i + 1, j) + g('tr', i - 1, j)

    return {
        'meet allowed on border (loop bounds of 88877564)': max(max(v(i, j), h(i, j)) for i, j in cells),
        'vertical crossing only': max(v(i, j) for i, j in interior),
        'horizontal crossing only': max(h(i, j) for i, j in interior),
        'sum of four tables minus 4a (6723316)': max(g('tl', i, j) + g('br', i, j) + g('bl', i, j) + g('tr', i, j) - 4 * a[i][j]
                                                     for i, j in cells),
        'dropped dp1[i][j-1] from second orientation (125012463)': max(
            max(v(i, j), g('tl', i, j - 1), g('br', i, j + 1) + g('bl', i + 1, j) + g('tr', i - 1, j)) for i, j in interior),
        'second orientation uses start cell a[n][1] (45491862)': max(
            max(v(i, j), g('tl', i, j - 1) + a[n - 1][0] + g('br', i, j + 1) + g('tr', i - 1, j)) for i, j in interior),
        'total minus minimum interior cell': sum(map(sum, a)) - min(a[i][j] for i, j in interior),
    }


class Recipe429BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('429B')
        cls.parsed = [recipe.parse('429B', c['input']) for c in cls.cases]

    def test_parse_layout_and_range(self):
        self.assertEqual(recipe.parse('429B', '3 3\n0 0 0\n0 0 0\n0 0 0\n'), (3, 3, [[0] * 3] * 3))
        self.assertEqual(recipe.parse('429B', OFFICIAL[0][0])[2][1], [100, 1, 100])
        self.assertEqual(recipe.parse('429B', SAMPLE[0])[0:2], (3, 3))
        good = '3 4\n1 2 3 4\n5 6 7 8\n9 10 11 100000\n'
        self.assertEqual(recipe.parse('429B', good)[2][2][3], 100000)
        bad = [
            '2 3\n1 1 1\n1 1 1\n', '3 2\n1 1\n1 1\n1 1\n', '1001 3\n', '3 1001\n',
            '3 3\n1 1 1\n1 1 1\n', '3 3\n1 1 1\n1 1 1\n1 1 1\n1 1 1\n', '3 3\n1 1 1 1 1 1 1 1 1\n',
            '3 3\n1 1\n1 1 1 1\n1 1 1\n', '3 3\n1 1 1\n1 100001 1\n1 1 1\n', '3 3\n1 1 1\n1 -1 1\n1 1 1\n',
            '3 3\n1 1 1\n1 +1 1\n1 1 1\n', '3 3\n1 1 1\n1 01 1\n1 1 1\n', '3 3\n1 1 1 \n1 1 1\n1 1 1\n',
            '3 3\n1  1 1\n1 1 1\n1 1 1\n', '3 3\n1 1 1\n1 1 1\n1 1 1\n\n', ' 3 3\n1 1 1\n1 1 1\n1 1 1\n',
            '3 3 3\n1 1 1\n1 1 1\n1 1 1\n', '3 3\n1 1 1\n1 1_0 1\n1 1 1\n', '', '3 3\n1 1 1\t\n1 1 1\n1 1 1\n',
        ]
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('429B', text)

    def test_official_and_sample_pairs_agree_with_oracle_and_brute(self):
        tests = [(f'{i:04d}', {'input': t, 'output': o + '\r\n'}) for i, (t, o) in enumerate(OFFICIAL, 1)]
        samples = [('sample-0001', {'input': SAMPLE[0], 'output': SAMPLE[1]})]
        self.assertEqual(recipe.review('429B', tests, samples), [])
        for text, out in OFFICIAL + [SAMPLE]:
            self.assertEqual(recipe.brute('429B', recipe.parse('429B', text)), int(out))

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review('429B', [('x', {'input': OFFICIAL[0][0], 'output': '801\n'}),
                                          ('y', {'input': '3 3\n1 1 1\n1 1 1\n', 'output': '4\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['x', 'y'])
        self.assertEqual(failures[0]['expected'], ['800'])

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'429B'})
        self.assertGreaterEqual(counts['429B'], 20000)

    def test_extras_are_valid_distinct_and_categorized(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        dims = set()
        for case, data in zip(self.cases, self.parsed):
            n, m, a = data
            dims.add((n, m))
            self.assertEqual(case['input'], f'{n} {m}\n' + ''.join(' '.join(map(str, r)) + '\n' for r in a))
            self.assertEqual(case['output'], f'{recipe.flip_answer(data)}\n')
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertTrue(case['reason'])
            if n * m <= 42:
                self.assertEqual(case['output'], f'{recipe.brute("429B", data)}\n')
        self.assertIn((3, 3), dims)
        self.assertIn((1000, 1000), dims)
        self.assertIn((3, 1000), dims)
        self.assertIn((1000, 3), dims)
        everything_max = [c for c, d in zip(self.cases, self.parsed) if d[:2] == (1000, 1000) and min(map(min, d[2])) == 10**5]
        self.assertEqual([c['output'] for c in everything_max], ['399600000\n'])

    def test_witness_paths_for_mid_sized_extras(self):
        for data in self.parsed:
            if data[0] * data[1] <= 4000:
                value, iahub, iahubina = recipe.witness(data)
                self.assertTrue(recipe.check_witness(data, value, iahub, iahubina))

    def test_extras_deterministic(self):
        self.assertEqual(recipe.extras('429B'), self.cases)

    def test_extras_kill_each_wrong_idea(self):
        small = [(d, int(c['output'])) for c, d in zip(self.cases, self.parsed) if d[0] * d[1] <= 400]
        kills = {}
        for data, truth in small:
            for name, value in wrong_ideas(*data).items():
                if value != truth:
                    kills[name] = kills.get(name, 0) + 1
        for name in wrong_ideas(3, 3, [[1, 2, 3], [4, 5, 6], [7, 8, 9]]):
            with self.subTest(idea=name):
                self.assertGreaterEqual(kills.get(name, 0), 3)

    def test_report_binds_recipe_identity(self):
        report = json.loads((Path(__file__).parent / 'recipe-reports' / '429B.json').read_text())
        self.assertEqual(report['id'], '429B')
        self.assertEqual(report['extraPairs'], len(self.cases))
        self.assertEqual(report['officialReview']['failures'], [])
        self.assertEqual(report['independentChecks']['bruteChecks'], recipe.brute_checks())
        self.assertFalse(report['validated'])


if __name__ == '__main__':
    unittest.main()
