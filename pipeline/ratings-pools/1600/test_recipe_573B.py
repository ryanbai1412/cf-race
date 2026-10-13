import json
from pathlib import Path
import unittest

import recipe_573B as recipe


SAMPLES = [('6\n2 1 4 6 2 2', '3'), ('7\n3 3 3 1 3 3 3', '2')]
INT_MAX = 2**31 - 1


def _ported_12761046(h):
    n = len(h); tl = [0] * n; tr = [0] * n; tl[0] = 1
    for i in range(1, n):
        tl[i] = min(tl[i - 1] + 1, h[i])
    tr[n - 1] = 1
    for i in range(n - 2, -1, -1):
        tr[i] = min(tr[i + 1] + 1, h[i])
    return max([-1] + [min(tl[i], tr[i]) for i in range(1, n)])


def _ported_12761891(h):
    n = len(h); a = [0] + h + [0]; L = [0] * (n + 2); R = [0] * (n + 2)
    length = 1; L[1] = 1
    for i in range(2, n + 1):
        length = length + 1 if a[i] > length else a[i]; L[i] = length
    length = 1; R[n - 1] = 1
    for i in range(n - 1, 0, -1):
        length = length + 1 if a[i] > length else a[i]; R[i] = length
    return max(min(L[i], R[i]) for i in range(1, n + 1))


def _ported_12761564(h):
    n = len(h); b = [0] * n
    wc = 1 if h[0] > 0 else h[0]
    for i in range(1, n):
        b[i] = min(wc + i, h[i]); wc = min(wc, h[i] - i)
    wc = min(h[n - 1] + n - 1, n)
    for i in range(n - 2, -1, -1):
        b[i] = min(wc - i, b[i]); wc = min(wc, h[i] + i)
    return max([0] + b[1:n - 1])


def _ported_12759818(h):
    n = len(h)
    if n <= 2:
        return 0
    l = [0] * n; r = [0] * n
    l[1] = min(1, h[1] - 1)
    for i in range(2, n - 1):
        l[i] = min(h[i] - 1, l[i - 1] + 1)
    r[n - 2] = min(1, h[n - 2] - 1)
    for i in range(n - 3, 0, -1):
        r[i] = min(h[i] - 1, r[i + 1] + 1)
    return max(min(l[i], r[i]) for i in range(n)) + 1


def _ported_12760110(h):
    def make(a):
        if not a:
            return 0
        if all(x == a[0] for x in a):
            return (len(a) + 1) // 2
        best = 0; tem = []
        for i in range(1, len(a) - 1):
            k = min(a[i - 1], a[i], a[i + 1])
            if k == a[i]:
                k -= 1
            if k > 0:
                tem.append(k)
            else:
                best = max(best, make(tem)); tem = []
        return max(best, make(tem)) + 1
    return make(list(h))


def _ported_12762143(h):
    n = len(h); ops = [0] * (n + 1)

    def min_neib(i):
        if i == 0 or ops[i - 1] == 0:
            return INT_MAX if ops[i + 1] == 0 else ops[i + 1] + 1
        if i == n - 1 or ops[i + 1] == 0:
            return INT_MAX if ops[i - 1] == 0 else ops[i - 1] + 1
        return min(ops[i - 1], ops[i + 1]) + 1
    best = 0
    for value, i in sorted((v, i) for i, v in enumerate(h)):
        ops[i] = min(min(i + 1, n - i), value, min_neib(i)); best = max(best, ops[i])
    return best


def _ported_12762029(h):
    def solve(v):
        n = len(v); ans = [0] * n; best = None
        for i in range(n - 1, 0, -1):
            if i == n - 1:
                ans[i] = 1
            else:
                ans[i] = min(n - i, v[i])
                if best[0] <= v[i] + i:
                    ans[i] = min(ans[i], ans[best[1]] + best[1] - i)
            key = (v[i] + i, i)
            best = key if best is None or key < best else best
        return ans
    if len(h) == 1:
        return 0
    forward = solve(h); backward = solve(h[::-1])
    return max(min(forward[i], backward[len(h) - i - 1]) for i in range(len(h)))


def _ported_12761207(h):
    v = list(h); n = len(v)
    if all(x == v[0] for x in v):
        return min(v[0], n // 2)
    ini, fim, flag, count = 0, n, 0, 0
    while not (ini > fim or flag):
        flag = 1; aux = v[ini]
        for i in range(ini + 1, fim - 1):
            if v[i] != 0:
                low = min(aux, v[i + 1])
                if v[i] <= low:
                    low = v[i] - 1
                aux = v[i]; v[i] = low
                if v[i] != 0:
                    flag = 0
        ini += 1; fim -= 1; count += 1
    return count


WRONG_IDEAS = {
    '12761046 skips column 0 in the final max (n=1 prints -1)': _ported_12761046,
    '12761891 right scan starts one column early': _ported_12761891,
    '12761564 excludes edge columns and offsets left/right limits': _ported_12761564,
    '12759818 off-by-one interior DP, prints 0 for n<=2': _ported_12759818,
    '12760110 recursive flat-segment (len+1)//2 shortcut': _ported_12760110,
    '12762143 sorted-height greedy with neighbour ops': _ported_12762143,
    '12762029 single-minimum set shortcut': _ported_12762029,
    '12761207 per-round simulation with flat shortcut min(h,n/2)': _ported_12761207,
}


class Recipe573BTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('573B')
        cls.rows = [recipe.parse('573B', c['input']) for c in cls.cases]

    def test_parse_layout_and_range(self):
        self.assertEqual(recipe.parse('573B', '6\n2 1 4 6 2 2'), [2, 1, 4, 6, 2, 2])
        self.assertEqual(recipe.parse('573B', '1\r\n1000000000\r\n'), [10**9])
        self.assertEqual(recipe.parse('573B', '2\n1 1\n'), [1, 1])
        for bad in ('', '0\n\n', '1\n0\n', '1\n1000000001\n', '2\n1\n', '2\n1 1 1\n', '1 1\n', '2\n1\n1\n',
                    '1\n1\n\n', ' 1\n1\n', '1\n 1\n', '1\n1 \n', '2\n1  1\n', '1\n01\n', '1\n+1\n', '1\n-1\n',
                    '01\n1\n', '100001\n' + ' '.join(['1'] * 100001) + '\n', '1\n1.0\n', '2\n1\t1\n'):
            with self.subTest(bad=bad[:30]), self.assertRaises(ValueError):
                recipe.parse('573B', bad)

    def test_statement_samples(self):
        for text, out in SAMPLES:
            self.assertEqual(str(recipe.answer('573B', recipe.parse('573B', text))), out)
            self.assertEqual(str(recipe.simulate(recipe.parse('573B', text))), out)

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review('573B', [('x', {'input': '3\n3 3 3\n', 'output': '1\n'}),
                                          ('y', {'input': '2\n1\n', 'output': '1\n'})],
                                 [('s', {'input': '1\r\n5\r\n', 'output': '1\r\n'})])
        self.assertEqual([f['test'] for f in failures], ['x', 'y'])
        self.assertEqual(failures[0]['expected'], ['2'])

    def test_simulation_and_distance_reference_agree_small(self):
        for heights in ([1], [2, 1, 4, 6, 2, 2], [3, 3, 3, 1, 3, 3, 3], [5, 1, 5], [4, 4, 4, 4, 4, 4, 4]):
            self.assertEqual(recipe.simulate(heights), recipe.distance_answer(heights))
            self.assertEqual(recipe.answer('573B', heights), recipe.simulate(heights))

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'573B'})
        self.assertGreaterEqual(counts['573B'], 10000)

    def test_extras_are_valid_distinct_and_categorized(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        for case, heights in zip(self.cases, self.rows):
            self.assertEqual(case['input'], f'{len(heights)}\n' + ' '.join(map(str, heights)) + '\n')
            self.assertEqual(case['output'], f'{recipe.answer("573B", heights)}\n')
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertTrue(case['reason'])
            if len(heights) <= 14 and max(heights) <= 12:
                self.assertEqual(case['output'], f'{recipe.simulate(heights)}\n')
            elif len(heights) <= 300:
                self.assertEqual(case['output'], f'{recipe.distance_answer(heights)}\n')
        lengths = [len(r) for r in self.rows]
        self.assertIn(1, lengths)
        self.assertIn(recipe.MAX_N, lengths)
        self.assertIn([recipe.MAX_H] * recipe.MAX_N, self.rows)
        self.assertGreaterEqual(sum(c['category'] == 'maxSize' for c in self.cases), 5)
        self.assertEqual(recipe.extras('573B'), self.cases)

    def test_max_cases_known_answers(self):
        known = {
            'maximum n and heights: width-limited answer 50000': 50000,
            'maximum n with unit heights': 1,
            'maximum n alternating unit/maximal towers': 2,
            'maximum n exact pyramid peak 50000': 50000,
            'maximum n split by a central unit pair': 25000,
        }
        for case in self.cases:
            if case['reason'] in known:
                self.assertEqual(case['output'], f"{known[case['reason']]}\n", case['reason'])

    def test_extras_kill_each_ported_wrong_idea(self):
        small = [r for r in self.rows if len(r) <= 300]
        for name, wrong in WRONG_IDEAS.items():
            with self.subTest(idea=name):
                self.assertTrue(any(wrong(r) != recipe.answer('573B', r) for r in small))

    def test_report_binds_recipe_identity(self):
        report = json.loads((Path(__file__).parent / 'recipe-reports' / '573B.json').read_text())
        self.assertEqual(report['id'], '573B')
        self.assertEqual(report['extraPairs'], len(self.cases))
        self.assertEqual(report['officialReview']['failures'], [])
        self.assertFalse(report['validated'])


if __name__ == '__main__':
    unittest.main()
