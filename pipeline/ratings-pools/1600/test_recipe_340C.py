"""Functional tests for the authored 340C recipe, not external-source execution."""
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_340C as recipe


def pair_reference(values):
    distance = sum(abs(x - y) for x, y in itertools.combinations(values, 2))
    expected = Fraction(sum(values) + 2 * distance, len(values))
    return expected.numerator, expected.denominator


def gap_reference(values):
    values = sorted(values)
    n = len(values)
    distance = sum((values[i] - values[i - 1]) * i * (n - i)
                   for i in range(1, n))
    expected = Fraction(sum(values) + 2 * distance, n)
    return expected.numerator, expected.denominator


class Recipe340CTests(unittest.TestCase):
    def test_sample_and_hand_enumerated_minima(self):
        self.assertEqual(recipe.answer('340C', recipe.parse('340C', '3\n2 3 5')), (22, 3))
        for values, expected in (((1, 2), (5, 2)), ((1, 3), (4, 1)),
                                 ((1, 2, 3, 4), (15, 2)),
                                 ((1, 10000000), (29999999, 2))):
            with self.subTest(values=values):
                self.assertEqual(recipe.answer('340C', values), expected)
                self.assertEqual(recipe._route_brute(values), expected)

    def test_strict_input_constraints_and_layout(self):
        invalid = ('', '1\n1\n', '100001\n1 2\n', '2 1 2\n',
                   '2\n1\n2\n', '2\n\n1 2\n', '2\n1 2\n3\n',
                   '2\n1\n', '2\n1 2 3\n', '2\n1 1\n',
                   '2\n0 1\n', '2\n-1 2\n', '2\n1 10000001\n',
                   '+2\n1 2\n', '2\n+1 2\n', '2\n1_000 2\n',
                   '2\n1.0 2\n', '2\n١ 2\n')
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('340C', text)
        self.assertEqual(recipe.parse('340C', '2\r\n 1\t2 \r\n'), (1, 2))
        self.assertEqual(recipe.parse('340C', '2\n1 10000000\n'), (1, 10000000))
        self.assertEqual(recipe.parse('340C', '02\n01 2\n'), (1, 2))

    def test_unknown_problem_fails_closed(self):
        for function, args in ((recipe.parse, ('x', '2\n1 2\n')),
                               (recipe.answer, ('x', (1, 2))),
                               (recipe.extras, ('x',)),
                               (recipe.review, ('x', [], []))):
            with self.assertRaises(ValueError):
                function(*args)

    def test_all_extras_have_valid_layout_and_independent_answers(self):
        cases = recipe.extras('340C')
        self.assertEqual(len(cases), 160)
        self.assertEqual(len({p['input'] for p in cases}), len(cases))
        self.assertEqual({p['category'] for p in cases}, {'boundary', 'adversarial', 'maxSize'})
        maximum = 0
        for i, pair in enumerate(cases):
            with self.subTest(i=i):
                values = recipe.parse('340C', pair['input'])
                self.assertEqual(list(map(len, (line.split() for line in pair['input'].splitlines()))),
                                 [1, len(values)])
                self.assertTrue(pair['reason'])
                expected = gap_reference(values) if len(values) > 200 else pair_reference(values)
                self.assertEqual(tuple(map(int, pair['output'].split())), expected)
                self.assertEqual(recipe.answer('340C', values), expected)
                self.assertEqual(math.gcd(*expected), 1)
                if len(values) == recipe.MAX_N:
                    maximum += 1
                    self.assertEqual(pair['category'], 'maxSize')
        self.assertEqual(maximum, 4)
        self.assertEqual(recipe.review('340C', list(enumerate(cases)), []), [])

    def test_generation_is_repeatable(self):
        def signature():
            return hashlib.sha256(json.dumps(recipe.extras('340C'), sort_keys=True).encode()).hexdigest()
        self.assertEqual(signature(), signature())

    def test_actual_exhaustive_and_random_route_checks(self):
        self.assertEqual(recipe.brute_checks(), {'340C': 1432})

    def test_review_preserves_and_reports_bad_pairs(self):
        sample = {'input': '3\r\n2 3 5\r\n', 'output': '22 3'}
        cases = [('unreduced', {**sample, 'output': '44 6'}),
                 ('slash', {**sample, 'output': '22/3'}),
                 ('extra', {**sample, 'output': '22 3 debug'}),
                 ('duplicate', {'input': '2\n1 1\n', 'output': '1 1'}),
                 ('layout', {'input': '3\n2\n3 5\n', 'output': '22 3'})]
        before = json.dumps(cases)
        failures = recipe.review('340C', cases, [('sample', sample)])
        self.assertEqual([error['test'] for error in failures], [name for name, _ in cases])
        self.assertEqual(json.dumps(cases), before)
        self.assertEqual(sample, {'input': '3\r\n2 3 5\r\n', 'output': '22 3'})

    def test_order_and_translation_invariants(self):
        values = (17, 1, 40, 3, 29)
        expected = Fraction(*recipe.answer('340C', values))
        for ordering in itertools.permutations(values):
            self.assertEqual(Fraction(*recipe.answer('340C', ordering)), expected)
        self.assertEqual(Fraction(*recipe.answer('340C', tuple(x + 123 for x in values))), expected + 123)

    def test_motivating_faulty_algorithms_have_legal_witnesses(self):
        values = (5, 2, 3)
        unsorted = Fraction(sum(values) + 2 * sum((2 * i - len(values) + 1) * x
                                                for i, x in enumerate(values)), len(values))
        self.assertNotEqual(unsorted, Fraction(*recipe._route_brute(values)))
        values = tuple(range(1, 13))
        self.assertNotEqual(pair_reference(values[:1]), pair_reference(values))
        values = (1, 2, 4, 8)
        numerator = sum(values) + 2 * sum(abs(x - y) for x, y in itertools.combinations(values, 2))
        self.assertNotEqual(Fraction(numerator, math.factorial(len(values))),
                            Fraction(*recipe._route_brute(values)))
        values = tuple(range(1, 100001))
        numerator = sum(values) + 2 * sum(i * (len(values) - i) for i in range(1, len(values)))
        self.assertGreater(numerator, 2**31 - 1)
        self.assertEqual(recipe.answer('340C', values), gap_reference(values))


if __name__ == '__main__':
    unittest.main()
