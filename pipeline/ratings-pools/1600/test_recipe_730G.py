"""Functional recipe tests; imported public submissions are never executed."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys
import tarfile
import unittest

import recipe_730G as recipe


BASE = Path(__file__).resolve().parent


def forbidden_start_reference(requests):
    reservations = []
    tokens = []
    for preferred, duration in requests:
        forbidden = sorted((max(1, left - duration + 1), right)
                           for left, right in reservations)
        if any(left <= preferred <= right for left, right in forbidden):
            start = 1
            for left, right in forbidden:
                if start < left:
                    break
                start = max(start, right + 1)
        else:
            start = preferred
        finish = start + duration - 1
        tokens.extend((start, finish))
        reservations.append((start, finish))
    return tokens


class Recipe730GTests(unittest.TestCase):
    def test_identity_and_unsupported_ids(self):
        self.assertEqual(recipe.IDS, ('730G',))
        self.assertEqual(set(recipe.SEMANTICS), {'730G'})
        for function, args in ((recipe.parse, ('1\n1 1\n',)),
                               (recipe.answer, (((1, 1),),)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.subTest(function=function.__name__):
                with self.assertRaises(ValueError):
                    function('730F', *args)

    def test_parse_valid_boundaries_and_line_endings(self):
        for newline in ('\n', '\r\n'):
            for trailing in ('', newline):
                text = newline.join(('2', '1 1', '1000000000 5000000')) + trailing
                self.assertEqual(recipe.parse('730G', text),
                                 ((1, 1), (10**9, 5 * 10**6)))
        self.assertEqual(recipe.parse('730G', '1\n  +01\t+1  \n'), ((1, 1),))

    def test_parse_rejects_arity_range_and_flattened_layout(self):
        invalid = (
            '', '0\n', '201\n', '-1\n', '1 1\n1 1\n', '1\n',
            '1\n0 1\n', '1\n1 0\n', '1\n-1 1\n', '1\n1 -1\n',
            '1\n1000000001 1\n', '1\n1 5000001\n', '1\n1\n1\n',
            '1\n1 1 1\n', '2\n1 1 2 2\n', '2 1 1 2 2\n',
            '2\n1 1\n', '1\n1 1\n2 2\n', '\n1\n1 1\n',
            '2\n1 1\n\n2 2\n', '1\n1 1\n\n', '1.0\n1 1\n',
            '1\n1e9 1\n', '1\n1.0 1\n', '1\n١ 1\n', '1\n1_0 1\n',
        )
        for text in invalid:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    recipe.parse('730G', text)

    def test_literal_schedules(self):
        cases = (
            (((10, 1),), [10, 10]),
            (((9, 2), (7, 3), (2, 4)), [9, 10, 1, 3, 4, 7]),
            (((5, 2), (1, 2), (5, 2)), [5, 6, 1, 2, 3, 4]),
            (((5, 2), (1, 2), (5, 3)), [5, 6, 1, 2, 7, 9]),
            (((10, 2), (12, 1)), [10, 11, 12, 12]),
            (((10, 2), (11, 1)), [10, 11, 1, 1]),
            (((5, 2), (4, 4)), [5, 6, 1, 4]),
            (((5, 6), (7, 1)), [5, 10, 1, 1]),
            (((1, 1), (3, 1), (5, 1), (1, 2)), [1, 1, 3, 3, 5, 5, 6, 7]),
            (((1, 3), (2, 2)), [1, 3, 4, 5]),
        )
        for requests, expected in cases:
            with self.subTest(requests=requests):
                self.assertEqual(recipe.answer('730G', requests), expected)
                self.assertEqual(forbidden_start_reference(requests), expected)

    def test_real_exhaustive_and_random_day_brute(self):
        self.assertEqual(recipe.brute_checks(), {'730G': 23120})

    def test_independent_references_agree_on_small_space(self):
        choices = tuple(itertools.product(range(1, 4), range(1, 3)))
        for requests in itertools.product(choices, repeat=3):
            with self.subTest(requests=requests):
                self.assertEqual(forbidden_start_reference(requests),
                                 recipe._day_brute(requests))

    def test_generated_pairs_are_unique_deterministic_and_layout_valid(self):
        tests = recipe.extras('730G')
        self.assertEqual(tests, recipe.extras('730G'))
        self.assertEqual(len(tests), 160)
        self.assertEqual(len({pair['input'] for pair in tests}), 160)
        self.assertEqual({pair['category'] for pair in tests},
                         {'boundary', 'adversarial', 'maxSize'})
        for i, pair in enumerate(tests):
            with self.subTest(generated=i):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                self.assertTrue(pair['reason'])
                self.assertNotIn('\r', pair['input'] + pair['output'])
                self.assertTrue(pair['input'].endswith('\n'))
                self.assertTrue(pair['output'].endswith('\n'))
                data = recipe.parse('730G', pair['input'])
                self.assertEqual(len(pair['input'].splitlines()), len(data) + 1)
                self.assertEqual(len(pair['output'].splitlines()), len(data))
                for line in pair['output'].splitlines():
                    self.assertEqual(len(line.split()), 2)
                expected = forbidden_start_reference(data)
                self.assertEqual(list(map(int, pair['output'].split())), expected)
                self.assertEqual(recipe.answer('730G', data), expected)
                if all(s <= 80 and d <= 30 for s, d in data):
                    self.assertEqual(recipe._day_brute(data), expected)
        self.assertEqual(recipe.review('730G', list(enumerate(tests)), []), [])

    def test_maximum_dimension_and_extreme_answers(self):
        duration = 5 * 10**6
        requests = ((1, duration),) * 200
        expected = [v for i in range(200)
                    for v in (i * duration + 1, (i + 1) * duration)]
        self.assertEqual(recipe.answer('730G', requests), expected)
        requests = ((10**9, duration),) * 200
        expected = [10**9, 10**9 + duration - 1] + [
            v for i in range(199) for v in (i * duration + 1, (i + 1) * duration)]
        self.assertEqual(recipe.answer('730G', requests), expected)
        generated = [recipe.parse('730G', p['input']) for p in recipe.extras('730G')]
        self.assertIn(((1, 1),), generated)
        self.assertIn(requests, generated)
        self.assertTrue(any(len(data) == 200 for data in generated))

    def test_selected_defect_motivations_with_self_authored_mutants(self):
        interior = ((1, 2), (10, 2), (10, 3))
        correct = recipe._day_brute(interior)
        prefix_or_tail = [1, 2, 10, 11, 12, 14]
        self.assertEqual(correct, [1, 2, 10, 11, 3, 5])
        self.assertNotEqual(correct, prefix_or_tail)

        gap_sum = ((2, 1), (10, 1), (2, 8))
        left_end, right_start, duration = 2, 10, 8
        self.assertGreaterEqual(left_end + right_start - 1, duration)
        self.assertLess(right_start - left_end - 1, duration)
        self.assertEqual(recipe._day_brute(gap_sum), [2, 2, 10, 10, 11, 18])
        self.assertNotEqual(recipe._day_brute(gap_sum), [2, 2, 10, 10, 3, 10])

        stale_end = ((1, 3), (2, 2))
        self.assertNotEqual(recipe._day_brute(stale_end), [1, 3, 4, 3])
        self.assertNotEqual(recipe._day_brute(((10, 1),)), [1, 1])
        inputs = {p['input'] for p in recipe.extras('730G')}
        for data in (interior, gap_sum, stale_end, ((10, 1),)):
            self.assertIn(recipe._input(data), inputs)

    def test_review_reports_every_error_without_changing_pairs(self):
        good = {'input': '1\n1 1\n', 'output': '1 1\n'}
        cases = [
            ('flattened-input', {'input': '2\n1 1 2 2\n', 'output': '1 1\n2 3\n'}),
            ('wrong-answer', dict(good, output='2 2\n')),
            ('missing-output-line', dict(good, output='')),
            ('flattened-output', {'input': '2\n1 1\n2 2\n', 'output': '1 1 2 3\n'}),
            ('extra-output-token', dict(good, output='1 1 1\n')),
            ('float-output', dict(good, output='1.0 1\n')),
        ]
        original = json.dumps(cases, sort_keys=True)
        failures = recipe.review('730G', cases, [('good', good)])
        self.assertEqual([failure['test'] for failure in failures],
                         [name for name, _ in cases])
        self.assertEqual(json.dumps(cases, sort_keys=True), original)
        self.assertEqual(recipe.review('730G', [('crlf', {
            'input': '1\r\n1 1\r\n', 'output': '1 1\r\n'})], []), [])

    def test_public_statement_attestation_and_proposed_replacements(self):
        report = json.loads((BASE / 'recipe-reports/730G.json').read_text())
        source = report['statementAttestation']
        body = (BASE / source['path']).read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), source['bodySha256'])
        text = body.decode('utf-8')
        section = text.split('<div class="input-specification">', 1)[1]
        section = section.split('<div class="output-specification">', 1)[0]
        self.assertIn('10<sup class="upper-index">9</sup>', section)
        self.assertIn('5·10<sup class="upper-index">6</sup>', section)
        self.assertIn('one request per line', section)
        self.assertIn('chooses the smallest positive', text)
        self.assertIn('will be less than', text)
        self.assertEqual(report['statementNormalizationProposal']['replacements'], [
            {'field': 'input_format', 'from': '≤ 109,',
             'to': '≤ 10<sup>9</sup>,', 'occurrences': 1},
            {'field': 'input_format', 'from': '≤ 5·106)',
             'to': '≤ 5·10<sup>6</sup>)', 'occurrences': 1},
        ])

    @unittest.skipUnless(os.environ.get('RECIPE_730G_INPUT_ARCHIVE'),
                         'set RECIPE_730G_INPUT_ARCHIVE to the pinned author input archive')
    def test_pinned_source_bytes_and_all_available_official_pairs(self):
        sys.path.insert(0, str(BASE.parents[1]))
        from pool_contract import digest
        archive = Path(os.environ['RECIPE_730G_INPUT_ARCHIVE'])
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),
                         'b5d674a6b75b1a5faeaccb187f45c787b70c71508f2e00a3fff922298761d98f')
        with tarfile.open(archive) as tar:
            manifest = json.load(tar.extractfile('inputs/MANIFEST.json'))
            raw = tar.extractfile('inputs/730G.json').read()
        self.assertEqual(len(raw), manifest['files']['inputs/730G.json']['bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
                         manifest['files']['inputs/730G.json']['sha256'])
        source = json.loads(raw)
        row = source['sourceRow']
        self.assertEqual(digest(row), source['sourceRowHash'])
        self.assertEqual(source['pins'], {
            'open-r1/codeforces': 'fbe3f6e903ee854eec2e69e9d96d0306cde59baf',
            'open-r1/codeforces-submissions': '07e7bf31f284b0e90e02dfc7ab675d5821e1c068',
        })
        originals = digest(source)
        tests = [(f'official/{i:04d}', p) for i, p in enumerate(row['official_tests'], 1)]
        samples = [(f'sample/{i:04d}', p) for i, p in enumerate(row['examples'], 1)]
        self.assertEqual(len(tests), 12)
        self.assertEqual(len(samples), 2)
        self.assertEqual(recipe.review('730G', tests, samples), [])
        for name, pair in [*tests, *samples]:
            with self.subTest(sourcePair=name):
                data = recipe.parse('730G', pair['input'])
                self.assertEqual(list(map(int, pair['output'].split())),
                                 forbidden_start_reference(data))
        for replacement in json.loads((BASE / 'recipe-reports/730G.json').read_text())[
                'statementNormalizationProposal']['replacements']:
            self.assertEqual(row[replacement['field']].count(replacement['from']),
                             replacement['occurrences'])
        self.assertEqual(digest(source), originals)


if __name__ == '__main__':
    unittest.main()
