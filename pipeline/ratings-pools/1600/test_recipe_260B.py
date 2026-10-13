"""Functional recipe checks; optional pinned archive fixture stays external."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tarfile
import unittest

import recipe_260B as recipe


PID = '260B'


class Recipe260BTests(unittest.TestCase):
    def test_minima_and_line_endings(self):
        for token in ('01-01-2013', '28-02-2014', '31-12-2015'):
            for ending in ('', '\n', '\r\n'):
                with self.subTest(token=token, ending=ending):
                    self.assertEqual(recipe.parse(PID, token + ending), token)
                    self.assertEqual(recipe.answer(PID, token), [token])

    def test_layout_alphabet_length_and_guarantees(self):
        invalid = ('', '\n', '01-01-2013\n\n', '01-01-2013\n31-12-2015\n',
                   '01-01-2013 31-12-2015', ' 01-01-2013', '01-01-2013 ',
                   '01-01-2013\r', '01-01-2013\v', '０１-01-2013',
                   '01-01-2013\x00', '0' * 100001, '1-1-2013',
                   '29-02-2013', '01-01-2012', '01-01-2016', '31-04-2015',
                   '00-01-2013', '01-00-2013', '01-13-2013', '----------',
                   '01-01-2013---31-12-2015')
        for text in invalid:
            with self.subTest(text=text[:40]):
                with self.assertRaises(ValueError):
                    recipe.parse(PID, text)

    def test_calendar_boundaries_and_frequency(self):
        word = '---'.join(['29-02-2013', '31-04-2014', '00-01-2015',
                         '01-00-2013', '01-13-2014', '01-01-2012'] * 3
                        + ['28-02-2015'])
        self.assertEqual(recipe.answer(PID, recipe.parse(PID, word)), ['28-02-2015'])
        for word in ('01-01-2013---31-12-2015---31-12-2015',
                     '31-12-2015---31-12-2015---01-01-2013'):
            self.assertEqual(recipe.answer(PID, recipe.parse(PID, word)), ['31-12-2015'])

    def test_overlapping_occurrences(self):
        word = '777-444---21-12-2013-12-2013-12-2013---444-777'
        self.assertEqual(recipe.answer(PID, recipe.parse(PID, word)), ['13-12-2013'])
        word = '13-12-2013-12-2013---01-01-2015'
        self.assertEqual(recipe.answer(PID, recipe.parse(PID, word)), ['13-12-2013'])
        self.assertEqual(recipe.brute(PID, word), ['13-12-2013'])

    def test_generated_suite(self):
        cases = recipe.extras(PID)
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras(PID))
        self.assertEqual(len({p['input'] for p in cases}), len(cases))
        self.assertEqual({p['category'] for p in cases}, {'boundary', 'adversarial', 'maxSize'})
        maxima = []
        for i, pair in enumerate(cases):
            with self.subTest(case=i):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                data = recipe.parse(PID, pair['input'])
                self.assertEqual(pair['output'].split(), recipe.answer(PID, data))
                self.assertEqual(pair['output'].split(), recipe.brute(PID, data))
                self.assertTrue(pair['reason'])
                self.assertEqual(len(pair['input'].splitlines()), 1)
                if pair['category'] == 'maxSize':
                    maxima.append(len(data))
        self.assertEqual(maxima, [100000, 100000, 100000])
        self.assertEqual(min(len(p['input'].rstrip('\n')) for p in cases), 10)

    def test_real_exhaustive_and_random_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {PID})
        self.assertGreaterEqual(counts[PID], 8105)

    def test_review_reports_invalid_pairs_without_repair(self):
        samples = [('sample', {'input': '01-01-2013', 'output': '01-01-2013'})]
        self.assertEqual(recipe.review(PID, [], samples), [])
        tests = [('wrong', {'input': '31-12-2015\r\n', 'output': '01-01-2013\r\n'}),
                 ('bad-layout', {'input': '01-01-2013\n\n', 'output': '01-01-2013'}),
                 ('tie', {'input': '01-01-2013---31-12-2015', 'output': '01-01-2013'})]
        before = json.dumps(tests)
        errors = recipe.review(PID, tests, samples)
        self.assertEqual([error['test'] for error in errors], ['wrong', 'bad-layout', 'tie'])
        self.assertEqual(json.dumps(tests), before)

    def test_unknown_pid(self):
        for function, args in ((recipe.parse, ('01-01-2013',)),
                               (recipe.answer, ('01-01-2013',)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                function('other', *args)

    @unittest.skipUnless(os.environ.get('CF260B_SOURCE_ARCHIVE'), 'external pinned source fixture not set')
    def test_pinned_official_tests_and_sample(self):
        archive = Path(os.environ['CF260B_SOURCE_ARCHIVE'])
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),
                         'b5d674a6b75b1a5faeaccb187f45c787b70c71508f2e00a3fff922298761d98f')
        with tarfile.open(archive) as handle:
            manifest = json.load(handle.extractfile('inputs/MANIFEST.json'))
            raw = handle.extractfile('inputs/260B.json').read()
        self.assertEqual(manifest['files']['inputs/260B.json'],
                         {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        source = json.loads(raw)
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
        from pool_contract import digest
        self.assertEqual(digest(source['sourceRow']), source['sourceRowHash'])
        self.assertEqual(source['pins'], {
            'open-r1/codeforces': 'fbe3f6e903ee854eec2e69e9d96d0306cde59baf',
            'open-r1/codeforces-submissions': '07e7bf31f284b0e90e02dfc7ab675d5821e1c068',
        })
        row = source['sourceRow']
        self.assertEqual(len(row['official_tests']), 27)
        self.assertEqual(len(row['examples']), 1)
        before = digest(source)
        tests = [(f'official-{i}', pair) for i, pair in enumerate(row['official_tests'], 1)]
        samples = [(f'sample-{i}', pair) for i, pair in enumerate(row['examples'], 1)]
        self.assertEqual(recipe.review(PID, tests, samples), [])
        for _, pair in tests + samples:
            data = recipe.parse(PID, pair['input'])
            self.assertEqual(recipe.brute(PID, data), pair['output'].split())
        self.assertEqual(digest(source), before)


if __name__ == '__main__':
    unittest.main()
