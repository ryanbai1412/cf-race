import bisect
import itertools
import unittest

import recipe_446A as recipe


def window_reference(values):
    """Binary search a length; enumerate all windows and their violated edges."""
    n = len(values)
    broken = [i for i in range(n - 1) if values[i] >= values[i + 1]]

    def feasible(length):
        for start in range(n - length + 1):
            end = start + length - 1
            lo = bisect.bisect_left(broken, start)
            hi = bisect.bisect_left(broken, end)
            if lo == hi:
                return True
            if hi - lo != 1:
                continue
            edge = broken[lo]
            if edge == start or values[edge - 1] + 1 < values[edge + 1]:
                return True
            if edge + 1 == end or values[edge] + 1 < values[edge + 2]:
                return True
        return False

    low, high = 1, n
    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1
    return low


class Recipe446ATests(unittest.TestCase):
    def test_interfaces_and_minima(self):
        self.assertEqual(recipe.IDS, ('446A',))
        self.assertIn('ANY integer', recipe.SEMANTICS['446A'])
        for values, expected in (((1,), 1), ((1000000000,), 1),
                                 ((1, 1), 2), ((2, 1), 2),
                                 ((1, 1, 2, 3), 4),
                                 ((999999997, 999999998, 1000000000, 1000000000), 4)):
            with self.subTest(values=values):
                self.assertEqual(recipe.answer('446A', values), expected)
                self.assertEqual(recipe.brute(values), expected)

    def test_strict_parser(self):
        self.assertEqual(recipe.parse('446A', '3\r\n1 2 3\r\n'), (1, 2, 3))
        self.assertEqual(recipe.parse('446A', '1\n1000000000'), (1000000000,))
        for text in ('', '0\n1\n', '100001\n1\n', '3 1 2 3\n',
                     '3\n1 2\n3\n', '2\n1\n2\n', '1 2\n1 2\n',
                     '1\n0\n', '1\n1000000001\n', '1\n-1\n',
                     '1\n+1\n', '1\n1_000\n', '+1\n1\n',
                     '1\n1 2\n', '\n1\n1\n', '2\n1\n', '1\n1.0\n'):
            with self.subTest(text=text):
                self.assertRaises(ValueError, recipe.parse, '446A', text)
        for function, argument in ((recipe.parse, '1\n1\n'),
                                   (recipe.answer, (1,)), (recipe.extras, None)):
            if function is recipe.extras:
                self.assertRaises(ValueError, function, 'other')
            else:
                self.assertRaises(ValueError, function, 'other', argument)

    def test_generated_layout_and_independent_answers(self):
        cases = recipe.extras('446A')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('446A'))
        self.assertEqual(len({case['input'] for case in cases}), 160)
        maximums = 0
        for i, case in enumerate(cases):
            with self.subTest(case=i, reason=case['reason']):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
                self.assertTrue(case['reason'])
                self.assertEqual(len(case['input'].splitlines()), 2)
                values = recipe.parse('446A', case['input'])
                self.assertEqual(case['output'].split(), [str(window_reference(values))])
                self.assertEqual(recipe.answer('446A', values), int(case['output']))
                if len(values) <= 17:
                    self.assertEqual(recipe.brute(values), int(case['output']))
                if case['category'] == 'maxSize':
                    self.assertEqual(len(values), 100000)
                    maximums += 1
        self.assertEqual(maximums, 5)
        self.assertEqual(recipe.review('446A', list(enumerate(cases)), []), [])

    def test_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'446A': 5860})

    def test_window_reference_against_replacement_enumeration(self):
        for n in range(1, 6):
            for values in itertools.product(range(1, 4), repeat=n):
                self.assertEqual(window_reference(values), recipe.brute(values), values)

    def test_real_bridge_gap_mutation(self):
        values = (1, 2, 2, 3)
        # Ignoring a single non-increasing edge is the defect in 10175997.
        ignoring_one_break = max(
            end - start + 1
            for start in range(len(values)) for end in range(start, len(values))
            if sum(values[i] >= values[i + 1] for i in range(start, end)) <= 1)
        self.assertEqual(ignoring_one_break, 4)
        self.assertEqual(recipe.brute(values), 3)
        self.assertEqual(recipe.answer('446A', values), 3)
        self.assertTrue(any(recipe.parse('446A', case['input']) == values
                            for case in recipe.extras('446A')))

    def test_review_records_errors_without_rewriting(self):
        sample = {'input': '6\n7 2 3 1 5 6', 'output': '5'}
        self.assertEqual(recipe.review('446A', [], [('sample', sample)]), [])
        bad = [('bad-input', {'input': '3\n1 2\n', 'output': '3\n'}),
               ('bad-answer', {'input': '4\n1 2 2 3\n', 'output': '4\n'}),
               ('two-tokens', {'input': '1\n1\n', 'output': '1 1\n'}),
               ('two-lines', {'input': '1\n1\n', 'output': '1\n1\n'})]
        originals = [(name, dict(pair)) for name, pair in bad]
        self.assertEqual([error['test'] for error in recipe.review('446A', bad, [])],
                         [name for name, _ in bad])
        self.assertEqual(bad, originals)


if __name__ == '__main__':
    unittest.main()
