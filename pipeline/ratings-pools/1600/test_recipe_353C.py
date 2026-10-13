from pathlib import Path
import json
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_353C as recipe

OFFICIAL_SMALL = [
    ('2\r\n3 8\r\n10\r\n', '3\r\n'),
    ('5\r\n17 0 10 2 1\r\n11010\r\n', '27\r\n'),
    ('1\r\n0\r\n1\r\n', '0\r\n'),
    ('1\r\n1\r\n0\r\n', '0\r\n'),
    ('1\r\n1\r\n1\r\n', '1\r\n'),
    ('1\r\n0\r\n0\r\n', '0\r\n'),
    ('2\r\n10000 10000\r\n11\r\n', '20000\r\n'),
    ('2\r\n10000 9999\r\n10\r\n', '10000\r\n'),
    ('2\r\n9999 10000\r\n10\r\n', '9999\r\n'),
    ('2\r\n10000 10000\r\n00\r\n', '0\r\n'),
]


def drop_top_only(a, s):
    ones = [i for i, c in enumerate(s) if c == '1']
    kept = sum(a[i] for i in ones)
    return max(kept, sum(a[:ones[-1]])) if ones else 0


def segment_greedy(a, s):
    con = total = 0
    for value, c in zip(a, s):
        if c == '1':
            total += max(con, value)
            con = 0
        else:
            con += value
    return total


def skip_last_index(a, s):
    pref = [sum(a[:i + 1]) for i in range(len(a))]
    suff = [sum(a[j] * int(s[j]) for j in range(i, len(a))) for i in range(len(a))]
    best = suff[0]
    for i in range(1, len(s) - 1):
        if s[i] == '1':
            best = max(best, pref[i - 1] + suff[i + 1])
    return best


def x_below_m(a, s):
    m = int(s[::-1], 2)
    return max((sum(a[i] for i in range(len(a)) if x >> i & 1) for x in range(m)), default=0)


class LayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        self.assertEqual(recipe.parse('353C', '2\n3 8\n10'), (2, [3, 8], '10'))
        self.assertEqual(recipe.parse('353C', '2\r\n3 8\r\n10\r\n'), (2, [3, 8], '10'))

    def test_rejects_bad_layout_arity_and_range(self):
        bad = ['', '1\n0\n', '1\n0\n1\n\n', '1 0\n1\n', '0\n\n\n', '100001\n0\n1\n', '2\n3\n10\n', '2\n3 8 1\n10\n',
               '2\n3 8\n1\n', '2\n3 8\n101\n', '2\n3 8\n12\n', '2\n3 10001\n10\n', '2\n3 -8\n10\n', '2\n+3 8\n10\n',
               '2\n03 8\n10\n', '02\n3 8\n10\n', '2\n3 8\n1 0\n', '2\n3 8 \n10\n10\n', '2\n3\n8\n10\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('353C', text)


class OracleTests(unittest.TestCase):
    def test_official_and_samples(self):
        tests = [(f'{i:04d}', {'input': x, 'output': y}) for i, (x, y) in enumerate(OFFICIAL_SMALL, 1)]
        samples = [('s1', {'input': '2\n3 8\n10', 'output': '3'}), ('s2', {'input': '5\n17 0 10 2 1\n11010', 'output': '27'})]
        self.assertEqual(recipe.review('353C', tests, samples), [])

    def test_review_reports_disagreement_and_invalid(self):
        failures = recipe.review('353C', [('a', {'input': '2\n3 8\n11\n', 'output': '8\n'}), ('b', {'input': '2\n3 8\n1\n', 'output': '3\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b'])
        self.assertEqual(failures[0]['expected'], ['11'])

    def test_exhaustive_small_against_enumeration(self):
        rng = random.Random(7)
        checked = 0
        for n in range(1, 8):
            for mask in range(1 << n):
                s = ''.join('1' if mask >> i & 1 else '0' for i in range(n))
                a = [rng.randint(0, 30) for _ in range(n)]
                expected = max(sum(a[i] for i in range(n) if x >> i & 1) for x in range(mask + 1))
                self.assertEqual(recipe.answer('353C', (n, a, s)), expected)
                checked += 1
        self.assertEqual(checked, 254)

    def test_brute_checks(self):
        result = recipe.brute_checks()
        self.assertEqual(set(result), {'353C'})
        self.assertGreater(result['353C'], 3000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('353C')

    def test_count_layout_and_answers(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        sizes = set()
        for case in self.cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertRegex(case['input'], r'\A[1-9][0-9]*\n(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*\n[01]+\n\Z')
            n, a, s = recipe.parse('353C', case['input'])
            sizes.add(n)
            reference = recipe.brute_enumerate(a, s) if n <= 12 else recipe.brute_dp(a, s)
            self.assertEqual(case['output'], f'{reference}\n')
        self.assertIn(1, sizes)
        self.assertIn(recipe.MAX_N, sizes)
        self.assertEqual(recipe.extras('353C'), self.cases)

    def test_categories(self):
        categories = {c['category'] for c in self.cases}
        self.assertEqual(categories, {'boundary', 'adversarial', 'maxSize'})
        self.assertLess(sum(c['category'] == 'maxSize' for c in self.cases), 10)

    def test_mutants_of_selected_wrong_sources_are_killed_by_labeled_cases(self):
        by_reason = {c['reason']: recipe.parse('353C', c['input']) for c in self.cases}

        def kills(mutant, fragment):
            hits = [data for reason, data in by_reason.items() if fragment in reason]
            self.assertTrue(hits, fragment)
            return any(mutant(a, s) != recipe.answer('353C', (n, a, s)) for n, a, s in hits)

        self.assertTrue(kills(drop_top_only, 'catches m-or-drop-top-only'))
        self.assertTrue(kills(segment_greedy, 'per-segment greedy'))
        self.assertTrue(kills(skip_last_index, '82906026 loop bound'))
        middle = [data for reason, data in by_reason.items() if 'clears the middle set bit' in reason]
        n, a, s = middle[0]
        self.assertNotEqual(drop_top_only(a, s), recipe.answer('353C', (n, a, s)))

    def test_x_below_m_mutant_is_killed(self):
        small = [recipe.parse('353C', c['input']) + (c['output'],) for c in self.cases]
        self.assertTrue(any(n <= 10 and x_below_m(a, s) != int(out) for n, a, s, out in small))


if __name__ == '__main__':
    unittest.main()
