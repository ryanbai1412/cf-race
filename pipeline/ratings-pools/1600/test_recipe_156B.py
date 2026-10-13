"""Portable recipe tests, plus optional byte-pinned input attachment review."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import unittest


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import digest
import recipe_156B as recipe


class SuspectsRecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('156B')

    def test_independent_exhaustive_and_random_brute(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'156B'})
        self.assertGreater(counts['156B'], 4000)

    def test_generated_suite(self):
        self.assertEqual(len(self.cases), 150)
        self.assertEqual(len({c['input'] for c in self.cases}), 150)
        self.assertEqual({c['category'] for c in self.cases},
                         {'boundary', 'adversarial', 'maxSize'})
        for case in self.cases:
            with self.subTest(reason=case['reason']):
                n, m, statements = data = recipe.parse('156B', case['input'])
                self.assertEqual(len(case['input'].splitlines()), n + 1)
                self.assertEqual(case['output'], recipe.answer('156B', data))
                self.assertTrue(case['reason'])
                self.assertEqual(len(case['output'].splitlines()), n)
                self.assertLessEqual(set(case['output'].splitlines()),
                                     {'Truth', 'Lie', 'Not defined'})
                if n <= 50:
                    self.assertEqual(case['output'], recipe._brute(n, m, statements))

    def test_determinism(self):
        self.assertEqual(self.cases, recipe.extras('156B'))

    def test_maximum_dimensions(self):
        maximum = [c for c in self.cases if c['category'] == 'maxSize']
        self.assertEqual(len(maximum), 4)
        for case in maximum:
            self.assertEqual(recipe.parse('156B', case['input'])[0], 100000)
        self.assertEqual(maximum[0]['output'], 'Truth\n' * 100000)
        self.assertEqual(maximum[1]['output'], 'Not defined\n' * 100000)
        self.assertEqual(maximum[2]['output'], 'Not defined\n' * 100000)
        self.assertEqual(maximum[3]['output'], 'Not defined\n' * 50000
                         + 'Lie\n' * 25000 + 'Truth\n' * 25000)

    def test_samples_and_algorithmic_edge_cases(self):
        pairs = [
            ('1 1\n+1', 'Truth\n'),
            ('3 2\n-1\n-2\n-3', 'Not defined\n' * 3),
            ('4 1\n+2\n-3\n+4\n-1', 'Lie\nNot defined\nLie\nNot defined\n'),
            ('3 3\n+1\n-2\n-3', 'Truth\n' * 3),
            ('3 3\n+1\n+1\n-2', 'Truth\n' * 3),
            ('1 0\n-1', 'Lie\n'),
            ('2 1\n+2\n-2', 'Not defined\n' * 2),
        ]
        for text, expected in pairs:
            self.assertEqual(recipe.answer('156B', recipe.parse('156B', text)), expected)

    def test_invalid_layout_arity_and_ranges(self):
        invalid = [
            '', '1\n+1\n', '1 1 0\n+1\n', '1 1 +1\n',
            '2 1\n+1 +2\n', '2\n1\n+1\n+2\n', '1 1\n\n+1\n',
            '1 1\n+1\n\n', '1 1\n+1\n-1\n', '0 0\n',
            '100001 0\n', '1 -1\n+1\n', '1 2\n+1\n',
            '1 1\n1\n', '1 1\n+0\n', '1 1\n-0\n',
            '1 1\n+2\n', '1 0\n-2\n', '1 1\n+ 1\n',
            '1 1\n++1\n', '1 1\n+1.0\n', '1 1\n+١\n',
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('156B', text)

    def test_feasibility_guarantee_independently(self):
        for n in range(1, 4):
            domain = tuple(range(-n, 0)) + tuple(range(1, n + 1))
            for statements in itertools.product(domain, repeat=n):
                for m in range(n + 1):
                    text = f'{n} {m}\n' + ''.join(f'{v:+d}\n' for v in statements)
                    expected = recipe._brute(n, m, statements)
                    if expected is None:
                        with self.assertRaises(ValueError):
                            recipe.parse('156B', text)
                    else:
                        data = recipe.parse('156B', text)
                        self.assertEqual(recipe.answer('156B', data), expected)

    def test_crlf_and_surrounding_horizontal_whitespace(self):
        text = ' 3  3 \r\n +1 \r\n -2\t\r\n -3 \r\n'
        pair = {'input': text, 'output': 'Truth\r\nTruth\r\nTruth\r\n'}
        self.assertEqual(recipe.review('156B', [('crlf', pair)], []), [])

    def test_review_preserves_and_reports_bad_pairs(self):
        pairs = [('ok', {'input': '1 1\n+1', 'output': 'Truth'}),
                 ('wrong', {'input': '1 1\n+1', 'output': 'Lie'}),
                 ('bad-input', {'input': '1 1\n-1', 'output': 'Truth'}),
                 ('flattened-output', {'input': '2 1\n+1\n+2',
                                       'output': 'Not defined Not defined\n'})]
        original = digest(pairs)
        errors = recipe.review('156B', pairs, [])
        self.assertEqual([e['test'] for e in errors],
                         ['wrong', 'bad-input', 'flattened-output'])
        self.assertEqual(digest(pairs), original)
        self.assertEqual(recipe.review('156B', list(enumerate(self.cases)), []), [])

    def test_problem_dispatch(self):
        self.assertEqual(recipe.IDS, ('156B',))
        self.assertEqual(set(recipe.SEMANTICS), {'156B'})
        for function, args in [(recipe.parse, ('156C', '1 1\n+1')),
                               (recipe.answer, ('156C', (1, 1, (1,)))),
                               (recipe.extras, ('156C',)),
                               (recipe.review, ('156C', [], []))]:
            with self.assertRaises(ValueError):
                function(*args)

    def test_statement_attestation(self):
        report = json.loads((BASE / 'recipe-reports/156B.json').read_text())
        attestation = report['statementAttestation']
        content = (BASE / attestation['path']).read_bytes()
        self.assertEqual(hashlib.sha256(content).hexdigest(), attestation['sha256'])
        self.assertIn(b'10<sup class="upper-index">5</sup>', content)
        self.assertIn(b'It is guaranteed that at least one suspect exists', content)

    @unittest.skipUnless(os.environ.get('RECIPE_156B_INPUT'),
                         'set RECIPE_156B_INPUT to the pinned inputs/156B.json')
    def test_unchanged_authenticated_attachment(self):
        path = Path(os.environ['RECIPE_156B_INPUT'])
        raw = path.read_bytes()
        manifest = json.loads((path.parent / 'MANIFEST.json').read_text())
        metadata = manifest['files']['inputs/156B.json']
        self.assertEqual(len(raw), metadata['bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), metadata['sha256'])
        original = json.loads(raw)
        self.assertEqual(digest(original['sourceRow']), original['sourceRowHash'])
        self.assertEqual(original['pins'], manifest['pins'])
        row = original['sourceRow']
        tests = [(f'official-{i:03d}', pair)
                 for i, pair in enumerate(row['official_tests'], 1)]
        samples = [(f'sample-{i:03d}', pair)
                   for i, pair in enumerate(row['examples'], 1)]
        self.assertEqual(len(tests), 44)
        self.assertEqual(len(samples), 3)
        self.assertEqual(recipe.review('156B', tests, samples), [])
        for name, pair in tests + samples:
            data = recipe.parse('156B', pair['input'])
            self.assertEqual(recipe.answer('156B', data), recipe._brute(*data), name)
        self.assertEqual(path.read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
