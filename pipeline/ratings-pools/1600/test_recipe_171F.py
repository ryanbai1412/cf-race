from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_171F as recipe

OFFICIAL = [
    (1, 13), (2, 17), (3, 31), (4, 37), (5, 71), (6, 73), (7, 79), (8, 97), (9, 107), (10, 113),
    (8216, 768377), (119, 3359), (10618, 975193), (6692, 399731), (10962, 990511), (6848, 706463),
    (4859, 323149), (8653, 787433), (6826, 705533), (10526, 971513), (9819, 939487), (10844, 984341),
    (7779, 748169), (1340, 91009), (4020, 190871), (2279, 122867), (5581, 353057), (11107, 997001),
    (7397, 731053), (5273, 340573), (10476, 969481), (7161, 720611), (4168, 196193), (1438, 93887),
    (6327, 384913), (10107, 953077), (6399, 388313), (11182, 999853), (11183, 999931), (11184, 999983),
]


def independent_is_prime(n):
    return n > 1 and all(n % f for f in range(2, int(n ** 0.5) + 1))


class EmirpLayoutTests(unittest.TestCase):
    def test_accepts_single_line_with_lf_crlf_or_no_newline(self):
        self.assertEqual(recipe.parse('171F', '1'), 1)
        self.assertEqual(recipe.parse('171F', '11184\n'), 11184)
        self.assertEqual(recipe.parse('171F', '11184\r\n'), 11184)

    def test_rejects_bad_layout_arity_and_range(self):
        for text in ('', '\n', '0\n', '11185\n', '-1\n', '1 2\n', '1\n2\n', '1\n\n', '05\n', '+5\n', 'x\n', '1.0\n'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('171F', text)


class EmirpOracleTests(unittest.TestCase):
    def test_official_pairs_and_sample(self):
        tests = [(f'{i:04d}', {'input': f'{d}\r\n', 'output': f'{e}\r\n'}) for i, (d, e) in enumerate(OFFICIAL, 1)]
        self.assertEqual(recipe.review('171F', tests, [('sample', {'input': '1', 'output': '13'})]), [])

    def test_review_reports_disagreement_and_invalid_input(self):
        failures = recipe.review('171F', [('a', {'input': '9\n', 'output': '101\n'}), ('b', {'input': '0\n', 'output': '2\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b'])
        self.assertEqual(failures[0]['expected'], ['107'])

    def test_answers_are_distinct_reversal_primes(self):
        for d in list(range(1, 60)) + list(range(11120, 11185)):
            e = recipe.answer('171F', d)
            r = int(str(e)[::-1])
            self.assertTrue(independent_is_prime(e) and independent_is_prime(r) and r != e, (d, e))

    def test_brute_checks_cover_whole_domain(self):
        self.assertEqual(recipe.brute_checks(), {'171F': recipe.MAX_D + 2})


class EmirpExtrasTests(unittest.TestCase):
    def test_extras_layout_answers_and_coverage(self):
        cases = recipe.extras('171F')
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        reference = recipe.brute_emirps()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertRegex(case['input'], r'^[1-9][0-9]*\n$')
            d = recipe.parse('171F', case['input'])
            self.assertEqual(case['output'], f'{reference[d - 1]}\n')
        inputs = {recipe.parse('171F', c['input']) for c in cases}
        self.assertTrue({1, recipe.MAX_D} <= inputs)
        self.assertEqual(recipe.extras('171F'), cases)

    def test_palindrome_and_leading_digit_labels_are_true(self):
        for case in recipe.extras('171F'):
            d = recipe.parse('171F', case['input'])
            e = recipe.answer('171F', d)
            if 'palindromic prime' in case['reason']:
                p = int(case['reason'].split('palindromic prime ')[1].split(':')[0])
                self.assertEqual(str(p), str(p)[::-1])
                self.assertTrue(independent_is_prime(p))
                self.assertGreater(e, p)
                self.assertTrue(d == 1 or recipe.answer('171F', d - 1) < p)


if __name__ == '__main__':
    unittest.main()
