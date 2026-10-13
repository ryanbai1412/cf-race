import json
import math
from pathlib import Path
import unittest

import recipe_333A as recipe


OFFICIAL = [
    (1, 1), (4, 2), (3, 1), (8, 3), (10, 4), (100000000000000000, 33333333333333334),
    (99999999999999999, 3703703703703704), (50031545098999707, 1), (16677181699666569, 1),
    (72900000000000, 33333333334), (99999999999999997, 33333333333333333), (58061299250691018, 32),
    (49664023559436051, 128191526), (66708726798666276, 2), (29442431889534807, 48),
    (70414767176369958, 13), (93886356235159944, 51), (97626528902553453, 551104613133),
    (52013157885656046, 880847395988), (37586570003500923, 548), (34391854792828422, 582429080812),
    (205891132094649, 1), (243, 1), (5559060566555523, 1), (81, 1), (108, 2), (2, 1), (1129718145924, 2),
]

WRONG_IDEAS = {
    'ceil(n/3)': lambda n: -(-n // 3),
    'ternary digit sum': lambda n: sum(int(d) for d in _ternary(n)),
    'float int(n/p)+1': lambda n: int(n / _stripped(n)) + 1,
    'float ceil(n/p) with n==1 special': lambda n: 1 if n == 1 else math.ceil(n / _stripped(n)),
    'n//(p+1)+1': lambda n: n // (_stripped(n) + 1) + 1,
    'n%3+1 above 3': lambda n: n % 3 + 1 if n > 3 else 1,
    'answer 1 for powers else 2': lambda n: 1 if _stripped(n) > n else 2,
}


def _ternary(n):
    digits = ''
    while n:
        n, d = divmod(n, 3)
        digits = str(d) + digits
    return digits


def _stripped(n):
    p = 1
    while n % p == 0:
        p *= 3
    return p


class Recipe333ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('333A')

    def test_parse_layout_and_range(self):
        self.assertEqual(recipe.parse('333A', '1\n'), 1)
        self.assertEqual(recipe.parse('333A', '100000000000000000\r\n'), 10**17)
        self.assertEqual(recipe.parse('333A', '7'), 7)
        for bad in ('0\n', '100000000000000001\n', '+5\n', '1_000\n', ' 5\n', '5 \n', '5\n\n',
                    '05\n', '1 2\n', '1\n2\n', '', '-3\n', '5.0\n'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                recipe.parse('333A', bad)

    def test_statement_samples_and_note(self):
        self.assertEqual(recipe.answer('333A', 1), 1)
        self.assertEqual(recipe.answer('333A', 4), 2)

    def test_official_pairs_agree(self):
        tests = [(f'{i:04d}', {'input': f'{n}\r\n', 'output': f'{a}\r\n'}) for i, (n, a) in enumerate(OFFICIAL, 1)]
        samples = [('sample-0001', {'input': '1', 'output': '1'}), ('sample-0002', {'input': '4', 'output': '2'})]
        self.assertEqual(recipe.review('333A', tests, samples), [])

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review('333A', [('x', {'input': '4\n', 'output': '3\n'}),
                                          ('y', {'input': '0\n', 'output': '1\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['x', 'y'])
        self.assertEqual(failures[0]['expected'], ['2'])

    def test_exhaustive_coin_brute_matches_small(self):
        for n in range(1, 41):
            self.assertEqual(recipe.answer('333A', n), recipe.coin_brute(n), n)

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'333A'})
        self.assertGreaterEqual(counts['333A'], 12000)

    def test_extras_are_valid_distinct_and_categorized(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        for case in self.cases:
            n = recipe.parse('333A', case['input'])
            self.assertEqual(case['input'], f'{n}\n')
            self.assertEqual(case['output'], f'{recipe.ternary_answer(n)}\n')
            self.assertEqual(recipe.rational_answer(n), recipe.answer('333A', n))
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertTrue(case['reason'])
        values = {recipe.parse('333A', c['input']) for c in self.cases}
        self.assertIn(1, values)
        self.assertIn(10**17, values)
        self.assertIn(3**35, values)
        self.assertEqual(recipe.extras('333A'), self.cases)

    def test_extras_kill_each_common_wrong_idea(self):
        values = [recipe.parse('333A', c['input']) for c in self.cases]
        for name, wrong in WRONG_IDEAS.items():
            with self.subTest(idea=name):
                self.assertTrue(any(wrong(n) != recipe.answer('333A', n) for n in values))
        float_kills = [n for n in values if WRONG_IDEAS['float int(n/p)+1'](n) != recipe.answer('333A', n)]
        self.assertGreaterEqual(len(float_kills), 5)

    def test_report_binds_recipe_identity(self):
        report = json.loads((Path(__file__).parent / 'recipe-reports' / '333A.json').read_text())
        self.assertEqual(report['id'], '333A')
        self.assertEqual(report['extraPairs'], len(self.cases))
        self.assertEqual(report['officialReview']['failures'], [])
        self.assertFalse(report['validated'])


if __name__ == '__main__':
    unittest.main()
