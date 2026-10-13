import unittest

import recipe_150B as recipe


class Recipe150BTests(unittest.TestCase):
    def test_parse_exact_single_line(self):
        self.assertEqual(recipe.parse('150B', '1 1 1\n'), (1, 1, 1))
        self.assertEqual(recipe.parse('150B', '2000 2000 2000\r\n'), (2000, 2000, 2000))
        self.assertEqual(recipe.parse('150B', '5 2 4'), (5, 2, 4))
        for text in ('5 2\n', '5 2 4 1\n', '5\n2 4\n', '5 2\n4\n', '0 2 4\n', '5 2001 4\n', '5 2 0\n', '2001 1 1\n', '-1 2 3\n', '5 2 4.0\n', '+5 2 4\n', ''):
            with self.assertRaises(ValueError):
                recipe.parse('150B', text)

    def test_samples_and_official_pairs(self):
        pairs = [('1 1 1', 1), ('5 2 4', 2), ('7 4 20', 16384), ('784 1 1999', 1), ('1000 2 1001', 688423210),
                 ('2000 2000 2000', 321179016), ('2000 1999 1999', 3996001), ('2000 2000 1', 596636543), ('4 256 1', 294967268),
                 ('11 2 5', 4), ('20 3 3', 9), ('1 2000 2000', 2000)]
        self.assertEqual(recipe.review('150B', [(text, {'input': text + '\r\n', 'output': f'{out}\r\n'}) for text, out in pairs], []), [])
        for text, out in pairs:
            self.assertEqual(recipe.union_count(recipe.parse('150B', text)), out)

    def test_review_reports_wrong_and_malformed_pairs(self):
        failures = recipe.review('150B', [('wrong', {'input': '5 2 4\n', 'output': '4\n'}), ('range', {'input': '0 1 1\n', 'output': '1\n'})],
                                 [('layout', {'input': '1\n1 1\n', 'output': '1\n'})])
        self.assertEqual([f['test'] for f in failures], ['wrong', 'range', 'layout'])
        self.assertEqual(failures[0]['expected'], ['2'])

    def test_extras_layout_and_independent_answers(self):
        cases = recipe.extras('150B')
        self.assertGreaterEqual(len(cases), 100)
        self.assertEqual(len({case['input'] for case in cases}), len(cases))
        self.assertEqual(cases, recipe.extras('150B'))
        inputs = set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertRegex(case['input'], r'\A[0-9]+ [0-9]+ [0-9]+\n\Z')
            self.assertRegex(case['output'], r'\A[0-9]+\n\Z')
            data = recipe.parse('150B', case['input'])
            inputs.add(data)
            self.assertEqual(int(case['output']), recipe.union_count(data))
            if data[1] ** data[0] <= 20000:
                self.assertEqual(int(case['output']), recipe.exhaustive(data))
        self.assertIn((1, 1, 1), inputs)
        self.assertIn((2000, 2000, 2000), inputs)
        self.assertTrue(any(k > n for n, _, k in inputs))

    def test_wrong_algorithms_are_killed(self):
        inputs = [recipe.parse('150B', case['input']) for case in recipe.extras('150B')]
        wrong = {
            'parity only': lambda n, m, k: m if k % 2 == 0 else m * m,
            'k>n ignored': lambda n, m, k: pow(m, n, recipe.MOD) if k == 1 else pow(m, (n + 1) // 2, recipe.MOD) if k == n else m if k % 2 == 0 else m * m,
            'even k=n as m': lambda n, m, k: pow(m, n, recipe.MOD) if k == 1 or k > n else m if k == n and n % 2 == 0 else pow(m, (n + 1) // 2, recipe.MOD) if k == n else m * m if k % 2 else m,
            'k=1 below n as odd': lambda n, m, k: pow(m, n if k > n else (k + 1) // 2 if k == n else 2 if k % 2 else 1, recipe.MOD),
            'odd as m(m-1)': lambda n, m, k: pow(m, n, recipe.MOD) if k == 1 or k > n else pow(m, (n + 1) // 2, recipe.MOD) if k == n else m * (m - 1) if k % 2 else m,
            'components times m': lambda n, m, k: recipe.components(n, k) * m % recipe.MOD,
            'missing modulo': lambda n, m, k: m ** n if k == 1 or k > n else m ** ((n + 1) // 2) if k == n else m * m if k % 2 else m,
        }
        for name, solve in wrong.items():
            self.assertTrue(any(solve(*data) != recipe.answer('150B', data) for data in inputs), name)

    def test_brute_checks(self):
        self.assertGreaterEqual(recipe.brute_checks()['150B'], 2000)


if __name__ == '__main__':
    unittest.main()
