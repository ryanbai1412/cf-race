from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_237C as recipe

OFFICIAL = {
    '2 4 2\r\n': '3', '6 13 1\r\n': '4', '1 4 3\r\n': '-1', '1 1000000 10000\r\n': '137970',
    '690059 708971 10000\r\n': '-1', '1 1000000 78498\r\n': '999999', '1 1000000 78499\r\n': '-1',
    '1 1000000 1\r\n': '114', '999953 999953 1\r\n': '1', '999931 999953 2\r\n': '23', '1 1 1\r\n': '-1',
    '20 1000000 40000\r\n': '539580', '1 5 3\r\n': '5', '3 5 1\r\n': '2',
}


class ParseTests(unittest.TestCase):
    def test_accepts_single_line_including_crlf(self):
        self.assertEqual(recipe.parse('237C', '2 4 2\n'), (2, 4, 2))
        self.assertEqual(recipe.parse('237C', '1 1000000 1000000\r\n'), (1, 10**6, 10**6))

    def test_rejects_layout_arity_and_range(self):
        for text in ('2 4\n2\n', '2\n4\n2\n', '2 4\n', '2 4 2 1\n', '', '0 4 2\n', '5 4 2\n', '1 1000001 1\n',
                     '1 2 1000001\n', '1 2 0\n', '1 2 -1\n', '1 2 1.0\n', '1 2 +1\n', '1 2 1_0\n', '1 02 1\n'):
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse('237C', text)


class OracleTests(unittest.TestCase):
    def test_official_pairs(self):
        for text, output in OFFICIAL.items():
            self.assertEqual(str(recipe.answer('237C', recipe.parse('237C', text))), output, text)

    def test_review_flags_disagreement_and_malformed_input(self):
        good = ('ok', {'input': '2 4 2\r\n', 'output': '3\r\n'})
        self.assertEqual(recipe.review('237C', [good], []), [])
        failures = recipe.review('237C', [('wrong', {'input': '2 4 2\n', 'output': '4\n'}),
                                          ('range', {'input': '0 4 2\n', 'output': '3\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['wrong', 'range'])

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'237C'})
        self.assertGreaterEqual(counts['237C'], 10000)


class ExtrasTests(unittest.TestCase):
    def test_generated_inputs_are_valid_and_independently_checked(self):
        cases = recipe.extras('237C')
        self.assertEqual(cases, recipe.extras('237C'))
        self.assertGreaterEqual(len(cases), 100)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        self.assertEqual({c['category'] for c in cases}, {'boundary', 'adversarial', 'maxSize'})
        lengths = set()
        for case in cases:
            self.assertEqual(case['input'].count('\n'), 1)
            self.assertTrue(case['input'].endswith('\n') and case['output'].endswith('\n'))
            data = recipe.parse('237C', case['input'])
            value = int(case['output'])
            lengths.add(data[1] - data[0] + 1)
            if data[1] - data[0] <= 300:
                self.assertEqual(recipe.brute('237C', data), value, case)
            else:
                self.assertTrue(recipe.certify(data, value), case)
        self.assertIn(1, lengths)
        self.assertIn(10**6, lengths)
        self.assertIn('1 1 1\n', {c['input'] for c in cases})


if __name__ == '__main__':
    unittest.main()
