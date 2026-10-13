"""Functional recipe tests; no public submission execution or qualification."""
import random
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_243A as recipe


def _cumulative_union_count(values):
    total = set()
    for value in values:
        total |= {value | old for old in total} | {value}
    return len(total)


class BrandNewFunctionRecipeTests(unittest.TestCase):
    def test_id_contract(self):
        self.assertEqual(recipe.IDS, ('243A',))
        self.assertIn('1000000', recipe.SEMANTICS['243A'])
        for function, args in ((recipe.parse, ('243B', '1\n0\n')),
                               (recipe.answer, ('243B', (0,))),
                               (recipe.extras, ('243B',)),
                               (recipe.review, ('243B', [], []))):
            with self.assertRaises(ValueError):
                function(*args)

    def test_exact_layout_and_ranges(self):
        for text in ('3\n1 2 0', '3\n1 2 0\n', '3\r\n1 2 0\r\n', '3\r\n1 2 0'):
            self.assertEqual(recipe.parse('243A', text), (1, 2, 0))
        self.assertEqual(recipe.parse('243A', '1\n1000000\n'), (1000000,))
        malformed = ('', '\n', '3', '3\n', '3 1 2 0\n', '3\n1 2\n0\n', '3\n1 2 0\n\n',
                     '3\n1  2 0\n', '3\n 1 2 0\n', '3\n1 2 0 \n', '3 \n1 2 0\n', '3\n1\t2 0\n',
                     '3\n1 2\n', '3\n1 2 0 0\n', '0\n\n', '0\n0\n', '1\n-1\n', '1\n1000001\n',
                     '1\n01\n', '01\n1\n', '1\n+1\n', '1\n1.0\n', '1\r\r\n1\n', '1\n1\r',
                     '100001\n' + ' '.join(['0'] * 100001) + '\n', '1\n\u0661\n')
        for text in malformed:
            with self.subTest(text=repr(text[:30])):
                with self.assertRaises(ValueError):
                    recipe.parse('243A', text)
        self.assertEqual(len(recipe.parse('243A', '100000\n' + ' '.join(['1000000'] * 100000) + '\n')), 100000)

    def test_samples_and_hand_derived_answers(self):
        for text, expected in (('3\n1 2 0', 4), ('10\n1 2 3 4 5 6 1 2 9 10', 11),
                               ('3\n1 2 4\n', 6), ('3\n1 0 4\n', 4), ('2\n0 0\n', 1),
                               ('4\n1 2 1 2\n', 3), ('1\n0\n', 1), ('2\n1 2\n', 3),
                               ('20\n' + ' '.join(str(1 << b) for b in range(20)) + '\n', 210)):
            with self.subTest(text=text[:30]):
                self.assertEqual(recipe.answer('243A', recipe.parse('243A', text)), expected)

    def test_reviews_upstream_style_pairs(self):
        pairs = [('crlf', {'input': '3\r\n1 2 0\r\n', 'output': '4'}),
                 ('bad-output', {'input': '3\n1 2 0\n', 'output': '5\n'}),
                 ('bad-range', {'input': '1\n1000001\n', 'output': '1\n'})]
        failures = recipe.review('243A', pairs, [('sample', {'input': '3\n1 2 0', 'output': '4'})])
        self.assertEqual([f['test'] for f in failures], ['bad-output', 'bad-range'])

    def test_independent_references_agree(self):
        rng = random.Random(24316)
        for _ in range(300):
            values = tuple(rng.randint(0, recipe.MAX_A) for _ in range(rng.randint(1, 25)))
            self.assertEqual(recipe._brute_answer(values), recipe.answer('243A', values))
            self.assertEqual(recipe._last_bit_answer(values), recipe.answer('243A', values))

    def test_generated_suite_is_deterministic_legal_and_independently_correct(self):
        cases = recipe.extras('243A')
        self.assertEqual(cases, recipe.extras('243A'))
        self.assertEqual(len(cases), 170)
        self.assertEqual(len({case['input'] for case in cases}), len(cases))
        self.assertEqual({case['category'] for case in cases}, {'boundary', 'adversarial', 'maxSize'})
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertTrue(case['reason'])
                values = recipe.parse('243A', case['input'])
                self.assertEqual(case['input'], f'{len(values)}\n' + ' '.join(map(str, values)) + '\n')
                reference = recipe._brute_answer if len(values) <= 300 else recipe._last_bit_answer
                self.assertEqual(case['output'], f'{reference(values)}\n')
        self.assertEqual(recipe.review('243A', list(enumerate(cases)), []), [])

    def test_real_maximum_and_minimum_dimensions(self):
        cases = recipe.extras('243A')
        sizes = [len(recipe.parse('243A', case['input'])) for case in cases]
        self.assertIn(1, sizes)
        maximum = [case for case, size in zip(cases, sizes) if size == recipe.MAX_N]
        self.assertGreaterEqual(len(maximum), 6)
        self.assertTrue(all(case['category'] == 'maxSize' for case in maximum))
        values = {v for case in cases for v in recipe.parse('243A', case['input'])}
        self.assertTrue({0, recipe.MAX_A} <= values)

    def test_suite_kills_cumulative_union_mistake(self):
        killed = [case for case in recipe.extras('243A')
                  if len(case['input']) < 5000
                  and _cumulative_union_count(recipe.parse('243A', case['input'])) != int(case['output'])]
        self.assertGreaterEqual(len(killed), 20)

    def test_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'243A': 13226})


if __name__ == '__main__':
    unittest.main()
