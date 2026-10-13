"""Functional recipe tests; no public submission is imported or executed."""
from bisect import bisect_left, bisect_right
import hashlib
import json
from pathlib import Path
import unittest

import recipe_607A as recipe


OFFICIAL = [
    {'input': '4\r\n1 9\r\n3 1\r\n6 1\r\n7 4\r\n', 'output': '1\r\n'},
    {'input': '7\r\n1 1\r\n2 1\r\n3 1\r\n4 1\r\n5 1\r\n6 1\r\n7 1\r\n', 'output': '3\r\n'},
    {'input': '1\r\n0 1\r\n', 'output': '0\r\n'},
    {'input': '1\r\n0 1000000\r\n', 'output': '0\r\n'},
    {'input': '1\r\n1000000 1000000\r\n', 'output': '0\r\n'},
    {'input': '7\r\n1 1\r\n2 1\r\n3 1\r\n4 1\r\n5 1\r\n6 6\r\n7 7\r\n', 'output': '4\r\n'},
    {'input': '5\r\n1 1\r\n3 1\r\n5 1\r\n7 10\r\n8 10\r\n', 'output': '2\r\n'},
    {'input': '11\r\n110 90\r\n100 70\r\n90 10\r\n80 10\r\n70 1\r\n60 1\r\n50 10\r\n40 1\r\n30 1\r\n10 1\r\n20 1\r\n', 'output': '4\r\n'},
]
SAMPLES = [
    {'input': '4\n1 9\n3 1\n6 1\n7 4', 'output': '1'},
    {'input': '7\n1 1\n2 1\n3 1\n4 1\n5 1\n6 1\n7 1', 'output': '3'},
]


def variant(data, *, ordered=True, inclusive=True, suffix=True):
    beacons = sorted(data) if ordered else list(data)
    positions = [a for a, _ in beacons]
    survivors = [0]
    for i, (a, b) in enumerate(beacons):
        search = bisect_left if inclusive else bisect_right
        j = search(positions, a - b, 0, i)
        survivors.append(survivors[j] + 1)
    return len(data) - (max(survivors) if suffix else survivors[-1])


class Recipe607ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('607A')

    def test_interface(self):
        self.assertEqual(recipe.IDS, ('607A',))
        self.assertEqual(set(recipe.SEMANTICS), {'607A'})
        self.assertIn('<=b', recipe.SEMANTICS['607A'])

    def test_known_answers(self):
        for data, expected in [
            ([(0, 1)], 0),
            ([(0, 1), (1, 1)], 1),
            ([(0, 1), (2, 1)], 0),
            ([(0, 1), (1000000, 1000000)], 1),
            ([(0, 1), (1000000, 999999)], 0),
            ([(0, 1), (2, 2), (4, 2)], 1),
            ([(0, 1), (2, 1), (4, 1), (6, 100), (8, 100)], 2),
            ([(8, 100), (0, 1), (6, 100), (4, 1), (2, 1)], 2),
        ]:
            with self.subTest(data=data):
                self.assertEqual(recipe.answer('607A', data), expected)
                self.assertEqual(recipe.brute(data), expected)

    def test_valid_line_layout_and_bounds(self):
        self.assertEqual(recipe.parse('607A', '2\r\n1000000 1000000\r\n0 1\r\n'),
                         ((1000000, 1000000), (0, 1)))
        self.assertEqual(recipe.parse('607A', ' 1 \n 0\t1 '), ((0, 1),))

    def test_reject_invalid_arity_layout_and_range(self):
        invalid = [
            '', '0\n', '100001\n', '1 0 1\n', '1\n0\n1\n',
            '1\n0 1 2\n', '2\n0 1 2 1\n', '2\n0 1\n',
            '1\n0 1\n2 1\n', '2\n0 1\n0 2\n',
            '1\n-1 1\n', '1\n1000001 1\n', '1\n0 0\n',
            '1\n0 1000001\n', '1\n0 -1\n', '1\n0 1.0\n',
            '+1\n0 1\n', '1\n+0 1\n', '1\n0 1_000\n',
            '1\n\n0 1\n', '\n1\n0 1\n', '1\n0 1\n\n',
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('607A', text)

    def test_reject_unknown_pid(self):
        for func, args in [(recipe.parse, ('1\n0 1\n',)),
                           (recipe.answer, ([(0, 1)],)),
                           (recipe.extras, ()), (recipe.review, ([], []))]:
            with self.assertRaises(ValueError):
                func('607B', *args)

    def test_real_exhaustive_and_random_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'607A': 16024})

    def test_generated_suite_metadata(self):
        self.assertEqual(len(self.cases), 160)
        self.assertEqual(len({case['input'] for case in self.cases}), 160)
        self.assertEqual({case['category'] for case in self.cases},
                         {'boundary', 'adversarial', 'maxSize'})
        for case in self.cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertTrue(case['reason'])

    def test_all_generated_layouts_and_answers(self):
        for i, case in enumerate(self.cases):
            with self.subTest(case=i):
                data = recipe.parse('607A', case['input'])
                self.assertEqual(len(case['input'].splitlines()), len(data) + 1)
                self.assertEqual(case['output'], str(recipe.answer('607A', data)) + '\n')
        self.assertEqual(recipe.review('607A', list(enumerate(self.cases)), []), [])

    def test_generated_nonmaximum_against_literal_simulation(self):
        checked = 0
        for i, case in enumerate(self.cases):
            if case['category'] == 'maxSize':
                continue
            with self.subTest(case=i):
                data = recipe.parse('607A', case['input'])
                self.assertEqual(case['output'].split(), [str(recipe.brute(data))])
                checked += 1
        self.assertEqual(checked, 156)

    def test_real_maximum_dimension_closed_forms(self):
        maxima = [case for case in self.cases if case['category'] == 'maxSize']
        self.assertEqual(len(maxima), 4)
        for case, expected in zip(maxima, (50000, 0, 99999, 49999)):
            data = recipe.parse('607A', case['input'])
            self.assertEqual(len(data), 100000)
            self.assertEqual(case['output'].split(), [str(expected)])
        self.assertEqual(max(a for a, _ in recipe.parse('607A', maxima[1]['input'])), 1000000)

    def test_generation_deterministic(self):
        other = recipe.extras('607A')
        self.assertEqual(self.cases, other)

    def test_all_supplied_pairs_preserved_and_reviewed(self):
        report = json.loads(Path(__file__).with_name('recipe-reports').joinpath('607A.json').read_text())
        for label, pairs in [('official_tests', OFFICIAL), ('examples', SAMPLES)]:
            self.assertEqual(len(pairs), len(report['upstreamPairs'][label]))
            for pair, binding in zip(pairs, report['upstreamPairs'][label]):
                for field in ('input', 'output'):
                    self.assertEqual(hashlib.sha256(pair[field].encode()).hexdigest(),
                                     binding[field + 'Sha256'])
                expected = recipe.brute(recipe.parse('607A', pair['input']))
                self.assertEqual(pair['output'].split(), [str(expected)])
        tests = [(f'official_tests/{i}', pair) for i, pair in enumerate(OFFICIAL)]
        samples = [(f'examples/{i}', pair) for i, pair in enumerate(SAMPLES)]
        self.assertEqual(recipe.review('607A', tests, samples), [])

    def test_review_reports_errors_without_mutating_input(self):
        pair = {'input': '2\n0 1\n1 1\n', 'output': '0\n'}
        original = dict(pair)
        errors = recipe.review('607A', [('wrong', pair)], [])
        self.assertEqual(errors[0]['expected'], '1')
        self.assertEqual(errors[0]['test'], 'wrong')
        self.assertEqual(pair, original)
        malformed = {'input': '2\n0 1 1 1\n', 'output': '1\n'}
        self.assertEqual(len(recipe.review('607A', [('bad-layout', malformed)], [])), 1)
        multiple = {'input': '1\n0 1\n', 'output': '0 0\n'}
        self.assertEqual(len(recipe.review('607A', [], [('extra-output', multiple)])), 1)

    def test_algorithmic_defect_motifs_have_legal_witnesses(self):
        equality = ((0, 1), (1, 1))
        self.assertEqual(variant(equality, inclusive=False), 0)
        self.assertEqual(recipe.brute(equality), 1)
        zero = ((0, 1), (2, 1))
        missing_zero = tuple((a, b) for a, b in zero if a != 0)
        omitted_zero_answer = len(zero) - (len(missing_zero) - recipe.answer('607A', missing_zero))
        self.assertEqual(omitted_zero_answer, 1)
        self.assertEqual(recipe.brute(zero), 0)
        unsorted = ((90, 1), (0, 1), (30, 1), (60, 1))
        self.assertNotEqual(variant(unsorted, ordered=False), recipe.brute(unsorted))
        suffix = ((0, 1), (2, 1), (4, 1), (6, 100), (8, 100))
        self.assertEqual(variant(suffix, suffix=False), 4)
        self.assertEqual(min(recipe._literal_destroyed(suffix, len(suffix) - k)
                             for k in (0, 1)), 4)
        self.assertEqual(recipe.brute(suffix), 2)
        for data in (equality, zero, unsorted, suffix):
            self.assertIn(recipe._input(data), {case['input'] for case in self.cases})


if __name__ == '__main__':
    unittest.main()
