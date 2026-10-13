"""Functional author checks; never executes downloaded public submissions."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import unittest

import recipe_411B as recipe


BASE = Path(__file__).resolve().parent
ARCHIVE_SHA256 = 'b5d674a6b75b1a5faeaccb187f45c787b70c71508f2e00a3fff922298761d98f'
INPUT_SHA256 = 'e334af46831f1f44aa1e3dec4a9d631d3dde248a18059662eea0c8751b2d0cc1'
ROW_HASH = '62dcfe7599eb5a057e4776677cf2776a04e76f48397f014864d94a5c21017e31'


def _mutant(data, *, idle=False, reset=False, dead_writers=False,
            skip_last=False, overwrite=False):
    n, m, k, rows = data
    times = [0] * n
    blocked = set()
    for cycle in range(m):
        if reset:
            blocked.clear()
        counts = {}
        for core, row in enumerate(rows):
            cell = row[cycle]
            if (dead_writers or times[core] == 0) and (idle or cell != 0):
                counts[cell] = counts.get(cell, 0) + 1
        blocked.update(cell for cell, count in counts.items()
                       if count > 1 and (not skip_last or cell < k))
        for core, row in enumerate(rows):
            if (overwrite or times[core] == 0) and row[cycle] in blocked:
                times[core] = cycle + 1
    return times


class Recipe411BTests(unittest.TestCase):
    def test_interface_and_wrong_ids(self):
        self.assertEqual(recipe.IDS, ('411B',))
        self.assertEqual(set(recipe.SEMANTICS), {'411B'})
        for operation, arguments in ((recipe.parse, ('1 1 1\n0\n',)),
                                     (recipe.answer, ((1, 1, 1, ((0,),)),)),
                                     (recipe.extras, ()),
                                     (recipe.review, ([], []))):
            with self.subTest(operation=operation.__name__):
                with self.assertRaises(ValueError):
                    operation('411A', *arguments)

    def test_parser_preserves_rows_and_accepts_crlf(self):
        self.assertEqual(recipe.parse('411B', '2 3 2\r\n0 1 2\r\n2 0 1\r\n'),
                         (2, 3, 2, ((0, 1, 2), (2, 0, 1))))
        self.assertEqual(recipe.parse('411B', '1\t2 1 \n 0 1 '),
                         (1, 2, 1, ((0, 1),)))

    def test_parser_rejects_bad_layout_arity_and_range(self):
        bad = ['', '\n1 1 1\n0\n', '1 1\n0\n', '1 1 1 0\n',
               '2 2 1\n0 1 1 0\n', '2 2 1\n0 1\n1\n0\n',
               '2 1 1\n0\n', '1 1 1\n0\n0\n', '1 1 1\n\n0\n',
               '1 1 1\n0\n\n', '0 1 1\n', '1 0 1\n0\n',
               '1 1 0\n0\n', '101 1 1\n0\n', '1 101 1\n0\n',
               '1 1 101\n0\n', '1 1 1\n2\n', '1 1 1\n-1\n',
               '+1 1 1\n0\n', '1 1 1\n+0\n', '1 1 1\n0.0\n',
               '1 1 1\n1_0\n', '1 1 1\nidle\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('411B', text)

    def test_hand_computed_samples_and_cascades(self):
        examples = [
            ('4 3 5\n1 0 0\n1 0 2\n2 3 1\n3 2 0', [1, 1, 3, 0]),
            ('3 2 2\n1 2\n1 2\n2 2', [1, 1, 0]),
            ('1 1 1\n0', [0]),
            ('3 3 2\n1 0 0\n1 0 0\n0 0 1', [1, 1, 3]),
            ('4 3 3\n1 1 1\n1 2 2\n0 1 2\n0 0 2', [1, 1, 2, 0]),
            ('3 2 2\n1 0\n0 1\n0 0', [0, 0, 0]),
        ]
        for text, expected in examples:
            with self.subTest(text=text):
                data = recipe.parse('411B', text)
                self.assertEqual(recipe.answer('411B', data), expected)
                self.assertEqual(recipe._pairwise(data), expected)

    def test_reasoned_mutation_witnesses(self):
        generated_inputs = {case['input'] for case in recipe.extras('411B')}
        witnesses = [
            ('2 1 1\n0\n0\n', [0, 0], {'idle': True}),
            ('3 2 1\n1 0\n1 0\n0 1\n', [1, 1, 2], {'reset': True}),
            ('3 2 2\n1 2\n1 2\n2 2\n', [1, 1, 0], {'dead_writers': True}),
            ('2 1 3\n3\n3\n', [1, 1], {'skip_last': True}),
            ('2 2 1\n1 1\n1 0\n', [1, 1], {'overwrite': True}),
        ]
        for text, expected, mutation in witnesses:
            with self.subTest(mutation=mutation):
                data = recipe.parse('411B', text)
                self.assertIn(text, generated_inputs)
                self.assertEqual(recipe.answer('411B', data), expected)
                self.assertNotEqual(_mutant(data, **mutation), expected)

    def test_generated_cases_are_unique_valid_and_reference_checked(self):
        cases = recipe.extras('411B')
        self.assertEqual(len(cases), 160)
        self.assertEqual(len({case['input'] for case in cases}), 160)
        for case in cases:
            with self.subTest(reason=case['reason'], input=case['input'][:100]):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertTrue(case['reason'])
                self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
                data = recipe.parse('411B', case['input'])
                expected = recipe._pairwise(data)
                self.assertEqual(recipe.answer('411B', data), expected)
                self.assertEqual(case['output'], ''.join(f'{value}\n' for value in expected))
                self.assertEqual(recipe.review('411B', [('extra', case)], []), [])

    def test_maximum_dimensions_have_known_answers(self):
        cases = [case for case in recipe.extras('411B') if case['category'] == 'maxSize']
        self.assertEqual(len(cases), 5)
        for case, expected in zip(cases, ([0] * 100, [0] * 100, [1] * 100,
                                          [100] * 100, [1, 1] + list(range(3, 101)))):
            self.assertEqual(recipe.parse('411B', case['input'])[:3], (100, 100, 100))
            self.assertEqual(case['output'].split(), list(map(str, expected)))

    def test_brute_checks_exhaustive_random_and_generated(self):
        self.assertEqual(recipe.brute_checks(), {'411B': 7108})

    def test_review_rejects_wrong_values_and_output_layout(self):
        text = '2 1 1\n1\n1\n'
        bad = ['1 1\n', '1\n', '1\n1\n1\n', '1\n0\n', '1\n-1\n',
               '1\n+1\n', '1\n1.0\n', '1\n1\n\n']
        for output in bad:
            self.assertEqual(len(recipe.review('411B', [('bad', {'input': text,
                                                                      'output': output})], [])), 1)
        self.assertEqual(recipe.review('411B', [], [('valid', {'input': text,
                                                              'output': '1\r\n1\r\n'})]), [])
        self.assertEqual(len(recipe.review('411B', [('bad', {'input': '2 1 1 1 1',
                                                            'output': '1\n1\n'})], [])), 1)

    def test_determinism_under_different_hash_seeds(self):
        script = ('import hashlib,json,recipe_411B as r;'
                  'print(hashlib.sha256(json.dumps(r.extras("411B"),sort_keys=True)'
                  '.encode()).hexdigest())')
        hashes = [subprocess.check_output([sys.executable, '-c', script], cwd=BASE,
                                         env={**os.environ, 'PYTHONHASHSEED': seed})
                  for seed in ('1', '97')]
        self.assertEqual(hashes[0], hashes[1])

    def test_report_binds_original_statement_copy(self):
        report = json.loads((BASE / 'recipe-reports/411B.json').read_text())
        source = report['publicStatement']
        captured = (BASE / source['preservedPath']).read_bytes()
        self.assertEqual(hashlib.sha256(captured).hexdigest(), source['preservedSha256'])
        self.assertTrue(captured.startswith(b'<div class="problem-statement">'))
        self.assertIn(b'Multi-core Processor', captured)
        self.assertEqual(report['inputVerification']['fileSha256'], INPUT_SHA256)
        self.assertEqual(report['inputVerification']['sourceRowHash'], ROW_HASH)
        self.assertEqual(report['statementNormalization']['replacements'], [])
        self.assertFalse(report['qualification']['performed'])

    @unittest.skipUnless(os.environ.get('RECIPE_411B_INPUT_ARCHIVE'),
                         'set RECIPE_411B_INPUT_ARCHIVE for pinned upstream review')
    def test_pinned_upstream_bytes_constraints_and_oracle(self):
        path = Path(os.environ['RECIPE_411B_INPUT_ARCHIVE'])
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), ARCHIVE_SHA256)
        sys.path.insert(0, str(BASE.parents[1]))
        try:
            from pool_contract import digest
        finally:
            sys.path.pop(0)
        with tarfile.open(path) as archive:
            manifest = json.load(archive.extractfile('inputs/MANIFEST.json'))
            raw = archive.extractfile('inputs/411B.json').read()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), INPUT_SHA256)
        self.assertEqual(manifest['files']['inputs/411B.json'],
                         {'bytes': len(raw), 'sha256': INPUT_SHA256})
        data = json.loads(raw)
        row = data['sourceRow']
        self.assertEqual(digest(row), ROW_HASH)
        self.assertEqual(data['sourceRowHash'], ROW_HASH)
        self.assertEqual(data['pins'], {
            'open-r1/codeforces': 'fbe3f6e903ee854eec2e69e9d96d0306cde59baf',
            'open-r1/codeforces-submissions': '07e7bf31f284b0e90e02dfc7ab675d5821e1c068'})
        tests = [(f'official-{i + 1}', pair) for i, pair in enumerate(row['official_tests'])]
        samples = [(f'sample-{i + 1}', pair) for i, pair in enumerate(row['examples'])]
        self.assertEqual((len(tests), len(samples)), (16, 3))
        self.assertEqual(recipe.review('411B', tests, samples), [])
        for name, pair in tests + samples:
            with self.subTest(name=name):
                parsed = recipe.parse('411B', pair['input'])
                self.assertEqual(list(map(int, pair['output'].split())), recipe._pairwise(parsed))


if __name__ == '__main__':
    unittest.main()
