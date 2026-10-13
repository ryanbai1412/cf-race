import hashlib
import json
import os
from pathlib import Path
import unittest

import recipe_291C as recipe


class Recipe291CTests(unittest.TestCase):
    def test_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'291C': 8656})

    def test_legal_mask_endpoints_and_ties(self):
        cases = [
            ('1 1\n0.0.0.0\n', '128.0.0.0'),
            ('2 1\n0.0.0.0\n128.0.0.0\n', '-1'),
            ('2 2\n0.0.0.0\n128.0.0.0\n', '128.0.0.0'),
            ('2 2\n0.0.0.0\n0.0.0.2\n', '255.255.255.254'),
            ('2 2\n0.0.0.0\n0.0.0.1\n', '-1'),
            ('4 3\n0.0.0.0\n64.0.0.0\n128.0.0.0\n192.0.0.0\n', '-1'),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(recipe.answer('291C', recipe.parse('291C', text)), expected)

    def test_line_layout_and_canonical_octets(self):
        invalid = [
            '', '1\n1\n0.0.0.0\n', '1 1 0.0.0.0\n',
            '2 1\n0.0.0.0 0.0.0.1\n', '2 1\n0.0.0.0\n',
            '1 1\n0.0.0.0\n0.0.0.1\n', '\n1 1\n0.0.0.0\n',
            '1 1\n\n0.0.0.0\n', '1 1\n0.0.0.0\n\n',
            '0 0\n', '100001 1\n', '1 0\n0.0.0.0\n', '1 2\n0.0.0.0\n',
            '+1 1\n0.0.0.0\n', '01 1\n0.0.0.0\n', '1_0 1\n0.0.0.0\n',
            '1 1\n0.0.0.01\n', '1 1\n0.0.0.+1\n', '1 1\n0.0.0.-1\n',
            '1 1\n0.0.0.256\n', '1 1\n0.0.0.1_0\n', '1 1\n0.0.0.١\n',
            '1 1\n0.0.0\n', '1 1\n0.0.0.0.0\n', '1 1\n0..0.0\n',
            '2 1\n0.0.0.1\n0.0.0.1\n',
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('291C', text)
        self.assertEqual(recipe.parse('291C', '2 1\r\n0.0.0.0\r\n255.255.255.255\r\n'),
                         (1, [0, (1 << 32) - 1]))

    def test_extras_layout_answers_and_independent_reference(self):
        cases = recipe.extras('291C')
        self.assertTrue(120 <= len(cases) <= 180)
        self.assertEqual(len(cases), len({pair['input'] for pair in cases}))
        self.assertEqual(recipe.review('291C', list(enumerate(cases)), []), [])
        for pair in cases:
            with self.subTest(reason=pair['reason']):
                data = recipe.parse('291C', pair['input'])
                self.assertEqual(pair['output'], recipe._brute(data) + '\n')
                self.assertIn(pair['category'], ('boundary', 'adversarial', 'maxSize'))
                self.assertTrue(pair['reason'])
                self.assertEqual(len(pair['input'].splitlines()), len(data[1]) + 1)

    def test_maximum_dimension_cases(self):
        cases = [pair for pair in recipe.extras('291C') if pair['category'] == 'maxSize']
        self.assertEqual(len(cases), 3)
        self.assertEqual([pair['output'] for pair in cases],
                         ['255.255.255.254\n', '-1\n', '255.255.128.0\n'])
        for pair in cases:
            self.assertEqual(len(recipe.parse('291C', pair['input'])[1]), 100000)

    def test_fixed_seed_determinism(self):
        self.assertEqual(recipe.extras('291C'), recipe.extras('291C'))

    def test_review_reports_bad_input_and_bad_output(self):
        pairs = [('bad-layout', {'input': '1 1 0.0.0.0\n', 'output': '-1'}),
                 ('wrong-mask', {'input': '1 1\n0.0.0.0\n', 'output': '0.0.0.0'})]
        failures = recipe.review('291C', pairs, [])
        self.assertEqual([pair['test'] for pair in failures], ['bad-layout', 'wrong-mask'])
        self.assertEqual(failures[1]['expected'], '128.0.0.0')

    def test_unsupported_problem(self):
        for function, args in [(recipe.parse, ('1 1\n0.0.0.0\n',)),
                               (recipe.answer, ((1, [0]),)), (recipe.extras, ()),
                               (recipe.review, ([], []))]:
            with self.assertRaises(ValueError):
                function('291D', *args)

    @unittest.skipUnless(os.environ.get('RECIPE_291C_INPUT'), 'optional pinned author attachment')
    def test_pinned_official_pairs_unchanged(self):
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
        from pool_contract import digest
        path = Path(os.environ['RECIPE_291C_INPUT'])
        payload = path.read_bytes()
        self.assertEqual(hashlib.sha256(payload).hexdigest(),
                         'b5a927f3c37a05b7b147f06e6c1bdd9c954d1cde26c51cf13b506fdda31da5dc')
        data = json.loads(payload)
        self.assertEqual(digest(data['sourceRow']), data['sourceRowHash'])
        row = data['sourceRow']
        tests, samples = list(enumerate(row['official_tests'])), list(enumerate(row['examples']))
        self.assertEqual((len(tests), len(samples)), (15, 3))
        self.assertEqual(recipe.review('291C', tests, samples), [])
        for _, pair in [*tests, *samples]:
            self.assertEqual(recipe._brute(recipe.parse('291C', pair['input'])), pair['output'].strip())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), hashlib.sha256(payload).hexdigest())


if __name__ == '__main__':
    unittest.main()
