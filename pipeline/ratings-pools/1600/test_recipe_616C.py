"""Functional source tests for the author-only 616C recipe."""
import json
import os
from pathlib import Path
import unittest

import recipe_616C as recipe


def raster_union_reference(rows):
    n, m = len(rows), len(rows[0])
    parents = list(range(n * m))
    weights = [1] * (n * m)

    def root(u):
        while parents[u] != u:
            parents[u] = parents[parents[u]]
            u = parents[u]
        return u

    def unite(u, v):
        a, b = root(u), root(v)
        if a != b:
            if weights[a] < weights[b]:
                a, b = b, a
            parents[b] = a
            weights[a] += weights[b]

    for r in range(n):
        for c in range(m):
            if rows[r][c] == '.':
                u = r * m + c
                if r and rows[r - 1][c] == '.':
                    unite(u, u - m)
                if c and rows[r][c - 1] == '.':
                    unite(u, u - 1)
    result = []
    for r in range(n):
        output = []
        for c in range(m):
            if rows[r][c] == '.':
                output.append('.')
                continue
            roots = set()
            for x, y in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= x < n and 0 <= y < m and rows[x][y] == '.':
                    roots.add(root(x * m + y))
            output.append(str((1 + sum(weights[u] for u in roots)) % 10))
        result.append(''.join(output))
    return result


class Recipe616CTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('616C')

    def test_identity(self):
        self.assertEqual(recipe.IDS, ('616C',))
        self.assertEqual(set(recipe.SEMANTICS), {'616C'})
        for function, args in ((recipe.parse, ('1 1\n.\n',)),
                               (recipe.answer, (['.'],)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                function('616D', *args)

    def test_parse_lf_crlf_and_no_final_newline(self):
        for text in ('2 3\n.*.\n***', '2 3\n.*.\n***\n',
                     '2\t3\r\n.*.\r\n***\r\n'):
            self.assertEqual(recipe.parse('616C', text), ('.*.', '***'))

    def test_reject_bad_dimensions_arity_alphabet_and_layout(self):
        bad = ('', '0 1\n.\n', '1 0\n\n', '1001 1\n.\n', '1 1001\n.\n',
               '+1 1\n.\n', '-1 1\n.\n', '1_0 1\n.\n', '1.0 1\n.\n',
               '1e0 1\n.\n', '١ 1\n.\n', '1\n.\n', '1 1 1\n.\n',
               '2 2\n.. **\n', '2 2\n....\n', '2 2\n..\n',
               '1 1\n.\n*\n', '1 2\n. *\n', '1 2\n .\n',
               '1 1\na\n', '1 1\n0\n', '1 1\n.\r', '1 1\n.\n\n',
               '\n1 1\n.\n', '1 1\n\t.\n')
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('616C', text)

    def test_small_explicit_semantics(self):
        fixtures = ((['.'], ['.']), (['*'], ['1']),
                    (['...', '.*.', '...'], ['...', '.9.', '...']),
                    (['.**.'], ['.22.']), (['.*', '*.'], ['.3', '3.']),
                    (['*' + '.' * 9], ['0' + '.' * 9]),
                    (['*' + '.' * 19], ['0' + '.' * 19]),
                    (['*.*', '.*.', '*.*'], ['3.3', '.5.', '3.3']))
        for rows, expected in fixtures:
            self.assertEqual(recipe.answer('616C', rows), expected)
            self.assertEqual(recipe._literal_brute(rows), expected)
            self.assertEqual(raster_union_reference(rows), expected)

    def test_real_exhaustive_and_random_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'616C': 1562})

    def test_generated_inputs_outputs_and_independent_union_oracle(self):
        self.assertEqual(len(self.cases), 160)
        self.assertEqual(len({case['input'] for case in self.cases}), 160)
        self.assertEqual({case['category'] for case in self.cases},
                         {'boundary', 'adversarial', 'maxSize'})
        for i, case in enumerate(self.cases):
            with self.subTest(case=i):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertTrue(case['reason'])
                rows = recipe.parse('616C', case['input'])
                self.assertEqual(len(case['input'].splitlines()), len(rows) + 1)
                output = case['output'].splitlines()
                self.assertEqual(len(output), len(rows))
                self.assertTrue(all(len(row) == len(rows[0]) for row in output))
                self.assertEqual(output, recipe.answer('616C', rows))
                self.assertEqual(output, raster_union_reference(rows))
                if len(rows) * len(rows[0]) <= 144:
                    self.assertEqual(output, recipe._literal_brute(rows))
        self.assertEqual(recipe.review('616C', list(enumerate(self.cases)), []), [])
        # Keep the combined generated JSON below the qualification stdout file cap.
        self.assertLess(len(json.dumps(self.cases).encode()), 8 * 1024 * 1024)

    def test_maximum_dimensions_with_analytic_expectations(self):
        maximum = [case for case in self.cases
                   if case['input'].splitlines()[0] == '1000 1000']
        self.assertEqual(len(maximum), 3)
        for case in maximum:
            rows = recipe.parse('616C', case['input'])
            output = case['output'].splitlines()
            if not any('*' in row for row in rows):
                self.assertEqual(output, ['.' * 1000] * 1000)
            elif rows[0] == '.' * 1000:
                expected = ['.' * 1000] * 1000
                expected[500] = '.' * 500 + '0' + '.' * 499
                self.assertEqual(output, expected)
            else:
                expected = [''.join('.' if (r + c) % 2 == 0 else
                                    str(1 + (r > 0) + (r < 999) + (c > 0) + (c < 999))
                                    for c in range(1000)) for r in range(1000)]
                self.assertEqual(output, expected)

    def test_modulo_and_dedup_mutation_witnesses(self):
        row = '*' + '.' * 9
        self.assertEqual(recipe._literal_brute([row]), ['0' + '.' * 9])
        self.assertNotEqual(['10' + '.' * 9], recipe.answer('616C', [row]))
        ring = ['...', '.*.', '...']
        independently_reached_neighbor_sizes = [8, 8, 8, 8]
        duplicate_sum_digit = str((1 + sum(independently_reached_neighbor_sizes)) % 10)
        self.assertEqual(duplicate_sum_digit, '3')
        self.assertEqual(recipe._literal_brute(ring)[1][1], '9')
        self.assertNotEqual(duplicate_sum_digit, recipe.answer('616C', ring)[1][1])

    def test_review_reports_contradictions_without_rewriting_pairs(self):
        pairs = [('good', {'input': '1 1\r\n*\r\n', 'output': '1\r\n'}),
                 ('bad-count', {'input': '1 1\n*\n', 'output': '0\n'}),
                 ('bad-input', {'input': '2 2\n....\n', 'output': '..\n..\n'}),
                 ('bad-output', {'input': '1 2\n**\n', 'output': '1 1\n'})]
        original = json.dumps(pairs)
        errors = recipe.review('616C', pairs, [])
        self.assertEqual([error['test'] for error in errors],
                         ['bad-count', 'bad-input', 'bad-output'])
        self.assertEqual(json.dumps(pairs), original)

    def test_review_supplied_pinned_tests_and_samples(self):
        path = os.environ.get('RECIPE_616C_INPUT')
        if not path:
            self.skipTest('set RECIPE_616C_INPUT to the authenticated input file')
        raw = Path(path).read_bytes()
        row = json.loads(raw)['sourceRow']
        tests = [(f'official/{i + 1}', pair) for i, pair in enumerate(row['official_tests'])]
        samples = [(f'sample/{i + 1}', pair) for i, pair in enumerate(row['examples'])]
        self.assertEqual(recipe.review('616C', tests, samples), [])
        for _, pair in tests + samples:
            rows = recipe.parse('616C', pair['input'])
            self.assertEqual(pair['output'].split(), recipe._literal_brute(rows))
        self.assertEqual(Path(path).read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
