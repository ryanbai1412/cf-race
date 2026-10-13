"""Functional recipe tests, with original pinned official/sample bytes."""
import copy
import hashlib
import unittest

import recipe_380A as recipe


OFFICIAL = [
    {'input': '6\r\n1 1\r\n1 2\r\n2 2 1\r\n1 3\r\n2 5 2\r\n1 4\r\n16\r\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16\r\n',
     'output': '1 2 1 2 3 1 2 1 2 3 1 2 1 2 3 4\r\n'},
    {'input': '2\r\n1 33085\r\n1 44638\r\n2\r\n1 2\r\n', 'output': '33085 44638\r\n'},
    {'input': '10\r\n1 57757\r\n1 45234\r\n1 80807\r\n1 38496\r\n1 27469\r\n1 42645\r\n1 72643\r\n1 33235\r\n1 10843\r\n1 80598\r\n10\r\n1 2 3 4 5 6 7 8 9 10\r\n',
     'output': '57757 45234 80807 38496 27469 42645 72643 33235 10843 80598\r\n'},
    {'input': '3\r\n1 97601\r\n1 32580\r\n1 70519\r\n3\r\n1 2 3\r\n', 'output': '97601 32580 70519\r\n'},
    {'input': '7\r\n1 53989\r\n1 47249\r\n1 71935\r\n2 1 3\r\n1 84520\r\n1 84185\r\n2 6 1\r\n14\r\n1 2 3 4 5 6 7 8 9 10 11 12 13 14\r\n',
     'output': '53989 47249 71935 53989 53989 53989 84520 84185 53989 47249 71935 53989 53989 53989\r\n'},
    {'input': '1\r\n1 1\r\n1\r\n1\r\n', 'output': '1\r\n'},
]
SAMPLES = [{'input': '6\n1 1\n1 2\n2 2 1\n1 3\n2 5 2\n1 4\n16\n1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16',
            'output': '1 2 1 2 3 1 2 1 2 3 1 2 1 2 3 4'}]


class Recipe380ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generated = recipe.extras('380A')

    def test_original_suite_review_preserves_bytes(self):
        before = copy.deepcopy((OFFICIAL, SAMPLES))
        self.assertEqual(recipe.review('380A', list(enumerate(OFFICIAL)), list(enumerate(SAMPLES))), [])
        self.assertEqual((OFFICIAL, SAMPLES), before)
        for pair in OFFICIAL + SAMPLES:
            operations, queries = recipe.parse('380A', pair['input'])
            literal = recipe._literal(operations)
            self.assertEqual(pair['output'].split(), [str(literal[q - 1]) for q in queries])

    def test_generated_layout_outputs_and_independent_references(self):
        self.assertEqual(len(self.generated), 160)
        self.assertEqual(len({pair['input'] for pair in self.generated}), 160)
        self.assertEqual({pair['category'] for pair in self.generated}, {'boundary', 'adversarial', 'maxSize'})
        for index, pair in enumerate(self.generated):
            with self.subTest(index=index, reason=pair['reason']):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                data = recipe.parse('380A', pair['input'])
                operations, queries = data
                expected = list(map(int, pair['output'].split()))
                self.assertEqual(expected, recipe.answer('380A', data))
                lines = pair['input'].splitlines()
                self.assertEqual(len(lines), len(operations) + 3)
                self.assertEqual(len(lines[-1].split()), len(queries))
                if recipe._length(operations) <= 1000000:
                    literal = recipe._literal(operations)
                    self.assertEqual(expected, [literal[q - 1] for q in queries])
                else:
                    indices = sorted({0, len(queries) // 4, len(queries) // 2, 3 * len(queries) // 4, len(queries) - 1})
                    self.assertEqual([expected[i] for i in indices],
                                     recipe._backwards(operations, [queries[i] for i in indices]))

    def test_maximum_dimension_and_64_bit_query_values(self):
        maxima = [recipe.parse('380A', pair['input']) for pair in self.generated if pair['category'] == 'maxSize']
        self.assertEqual(len(maxima), 4)
        self.assertTrue(all(len(ops) == 100000 for ops, _ in maxima))
        self.assertEqual(max(len(queries) for _, queries in maxima), 100000)
        operations, queries = maxima[1]
        self.assertGreater(queries[-1], 2**32)
        self.assertEqual(max(op[1] for op in operations if op[0] == 2), 100000)
        self.assertEqual(max(op[2] for op in operations if op[0] == 2), 10000)
        expected = []
        for q in queries:
            offset = q - 1 if q <= 170017 else (q - 170018) % 100000
            expected.append((offset % 17 + 1) * 97)
        self.assertEqual(recipe.answer('380A', (operations, queries)), expected)

    def test_exhaustive_and_fixed_seed_literal_brute(self):
        checks = recipe.brute_checks()
        self.assertEqual(set(checks), {'380A'})
        self.assertGreater(checks['380A'], 10000)

    def test_parser_rejects_invalid_arity_ranges_and_layout(self):
        invalid = [
            '', '0\n', '100001\n', '1 1\n1 7\n1\n1\n',
            '1\n1 7\n1\n1\n\n', '\n1\n1 7\n1\n1\n',
            '1\n1\n7\n1\n1\n', '1\n1 7 8\n1\n1\n',
            '1\n0 7\n1\n1\n', '1\n3 7\n1\n1\n',
            '1\n1 0\n1\n1\n', '1\n1 100001\n1\n1\n',
            '1\n2 1 1\n1\n1\n', '2\n1 7\n2 2 1\n1\n1\n',
            '2\n1 7\n2 1 0\n1\n1\n', '2\n1 7\n2 1 10001\n1\n1\n',
            '2\n1 7\n2 100001 1\n1\n1\n', '2\n1 7\n2 1\n1\n1\n',
            '2\n1 7\n2 1 1 1\n1\n1\n', '1\n1 7\n0\n1\n',
            '1\n1 7\n100001\n1\n', '1\n1 7\n1 2\n1\n',
            '1\n1 7\n2\n1\n', '1\n1 7\n1\n2\n',
            '1\n1 7\n1\n0\n', '2\n1 7\n1 8\n2\n2 1\n',
            '2\n1 7\n1 8\n2\n1 1\n', '2\n1 7\n1 8\n2\n1\n2\n',
        ]
        for token in ('+7', '-7', '7.0', '1e1', '1_000', '７'):
            invalid.append(f'1\n1 {token}\n1\n1\n')
        for text in invalid:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    recipe.parse('380A', text)

    def test_unsupported_problem(self):
        for func, args in ((recipe.parse, ('1\n1 7\n1\n1\n',)),
                           (recipe.answer, (([(1, 7)], [1]),)),
                           (recipe.extras, ()), (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                func('380B', *args)

    def test_real_semantic_mutant_witnesses(self):
        ops = [(1, 7), (1, 13), (1, 17), (2, 2, 2)]
        literal = recipe._literal(ops)
        self.assertEqual(literal[3:], [7, 13, 7, 13])
        self.assertNotEqual([literal[(q - 1) % 2] for q in range(4, 8)], literal[3:])
        suffix = [7, 13, 17] + [13, 17] * 2
        self.assertNotEqual(suffix, literal)
        self.assertEqual(recipe.answer('380A', ([(1, 9), (1, 8), (2, 1, 1)], [3])), [9])
        self.assertNotEqual([1], [9])

    def test_generation_is_deterministic(self):
        def fingerprint(cases):
            return [(hashlib.sha256(pair['input'].encode()).hexdigest(),
                     hashlib.sha256(pair['output'].encode()).hexdigest(),
                     pair['reason'], pair['category']) for pair in cases]
        self.assertEqual(fingerprint(self.generated), fingerprint(recipe.extras('380A')))


if __name__ == '__main__':
    unittest.main()
