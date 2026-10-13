"""Functional recipe tests; no external submission execution or qualification."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

import recipe_297B as recipe


class FishWeightRecipeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('297B')

    def test_real_independent_brute(self):
        self.assertEqual(recipe.brute_checks(), {'297B': 2486})

    def test_generated_inputs_layout_and_answers(self):
        self.assertEqual(len(self.cases), 160)
        self.assertEqual(len({p['input'] for p in self.cases}), 160)
        for pair in self.cases:
            with self.subTest(reason=pair['reason']):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                self.assertIn(pair['category'], ('boundary', 'adversarial', 'maxSize'))
                data = recipe.parse('297B', pair['input'])
                self.assertEqual(pair['output'].split(), recipe.answer('297B', data))
                self.assertEqual(pair['output'].split(), recipe._suffix_reference(data))
                lines = pair['input'].splitlines()
                self.assertEqual(len(lines), 3)
                n, m, _ = map(int, lines[0].split())
                self.assertEqual(list(map(lambda s: len(s.split()), lines)), [3, n, m])

    def test_minimum_and_real_maximum_dimensions(self):
        self.assertEqual(recipe.parse('297B', self.cases[0]['input']), (1, (1,), (1,)))
        maxima = [recipe.parse('297B', p['input']) for p in self.cases if p['category'] == 'maxSize']
        self.assertEqual(len(maxima), 5)
        self.assertTrue(any(k == 10**9 and len(a) == len(b) == 100000 for k, a, b in maxima))
        self.assertTrue(any(len(a) == 1 and len(b) == 100000 for _, a, b in maxima))

    def test_source_samples_and_strict_equality(self):
        for text, expected in (
            ('3 3 3\n2 2 2\n1 1 3\n', ['YES']),
            ('4 7 9\n5 2 7 3\n3 5 2 7 3 8 7\n', ['NO']),
            ('2 2 3\n3 1\n3 2\n', ['NO']),
            ('2 2 6\n5 2\n6 1\n', ['YES']),
            ('1 1 1\n1\n1\n', ['NO']),
        ):
            self.assertEqual(recipe.answer('297B', recipe.parse('297B', text)), expected)

    def test_invalid_layout_ranges_and_tokens(self):
        for text in (
            '', '1 1 1 1 1\n', '1 1 1\n1 1\n', '1 1 1\n1\n\n1\n',
            '1 1\n1\n1\n', '1 1 1 9\n1\n1\n', '2 1 3\n1\n2\n',
            '1 1 3\n1 2\n2\n', '1 1 3\n1\n2 3\n', '1 1 3\n1\n2\n9\n',
            '0 1 1\n1\n1\n', '100001 1 1\n1\n1\n', '1 100001 1\n1\n1\n',
            '1 1 0\n1\n1\n', '1 1 1000000001\n1\n1\n',
            '1 1 3\n0\n1\n', '1 1 3\n1\n4\n', '1 1 3\n-1\n1\n',
            '1 1 3\n+1\n1\n', '1 1 3\n1_0\n1\n', '1 1 3\n1.0\n1\n',
            '1 1 3\n１\n1\n', '1 1 3\n01\n1\n',
        ):
            with self.subTest(input=text), self.assertRaises(ValueError):
                recipe.parse('297B', text)

    def test_crlf_and_horizontal_whitespace(self):
        self.assertEqual(recipe.parse('297B', '1\t1 2\r\n 2 \r\n1\r\n'), (2, (2,), (1,)))

    def test_review_reports_without_modifying_pairs(self):
        tests = [('good', {'input': '1 1 2\n2\n1\n', 'output': 'YES\r\n'}),
                 ('malformed', {'input': '1 1 2 2 1\n', 'output': 'YES\n'}),
                 ('contradiction', {'input': '1 1 2\n2\n1\n', 'output': 'NO\n'}),
                 ('extra-output', {'input': '1 1 2\n2\n1\n', 'output': 'YES YES\n'})]
        before = json.dumps(tests)
        failures = recipe.review('297B', tests, [])
        self.assertEqual([f['test'] for f in failures], ['malformed', 'contradiction', 'extra-output'])
        self.assertEqual(json.dumps(tests), before)
        self.assertEqual(recipe.review('297B', [], [('sample', tests[0][1])]), [])

    def test_determinism_across_hash_seeds(self):
        code = ('import hashlib,json,recipe_297B; '
                'print(hashlib.sha256(json.dumps(recipe_297B.extras("297B"),'
                'sort_keys=True,separators=(",",":")).encode()).hexdigest())')
        hashes = [subprocess.check_output([sys.executable, '-c', code],
                  cwd=Path(__file__).parent, env={**os.environ, 'PYTHONHASHSEED': seed},
                  text=True).strip() for seed in ('1', '999')]
        self.assertEqual(hashes[0], hashes[1])

    def test_unknown_problem_is_rejected(self):
        for function, args in ((recipe.parse, ('297A', '1 1 1\n1\n1\n')),
                               (recipe.answer, ('297A', (1, (1,), (1,)))),
                               (recipe.extras, ('297A',)), (recipe.review, ('297A', [], []))):
            with self.assertRaises(ValueError):
                function(*args)

    @unittest.skipUnless(os.environ.get('RECIPE_297B_INPUT'), 'set RECIPE_297B_INPUT to pinned input')
    def test_supplied_source_pairs_and_hash_bindings(self):
        path = Path(os.environ['RECIPE_297B_INPUT'])
        data = json.loads(path.read_bytes())
        manifest = json.loads(path.with_name('MANIFEST.json').read_bytes())
        report = json.loads(Path(__file__).with_name('recipe-reports').joinpath('297B.json').read_bytes())
        recorded = manifest['files']['inputs/297B.json']
        self.assertEqual(path.stat().st_size, recorded['bytes'])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), recorded['sha256'])
        spec = importlib.util.spec_from_file_location('pool_contract_297B', Path(__file__).parents[2] / 'pool_contract.py')
        module = importlib.util.module_from_spec(spec)
        sys.path.insert(0, str(Path(__file__).parents[2]))
        try:
            spec.loader.exec_module(module)
        finally:
            sys.path.pop(0)
        self.assertEqual(module.digest(data['sourceRow']), data['sourceRowHash'])
        self.assertEqual(data['sourceRowHash'], report['inputProvenance']['sourceRowHash'])
        self.assertEqual(data['pins'], report['inputProvenance']['pins'])
        row = data['sourceRow']
        tests = [(f'official/{i}', pair) for i, pair in enumerate(row['official_tests'], 1)]
        samples = [(f'sample/{i}', pair) for i, pair in enumerate(row['examples'], 1)]
        before = module.digest(row)
        self.assertEqual(recipe.review('297B', tests, samples), [])
        self.assertEqual(module.digest(row), before)
        self.assertEqual(len(tests), 13)
        self.assertEqual(len(samples), 2)
        for record, (name, pair) in zip(report['upstreamPairs']['bindings'], tests + samples):
            self.assertEqual(record['name'], name)
            for key in ('input', 'output'):
                self.assertEqual(hashlib.sha256(pair[key].encode()).hexdigest(), record[key + 'Sha256'])


if __name__ == '__main__':
    unittest.main()
