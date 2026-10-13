import hashlib
import json
from pathlib import Path
import unittest

import recipe_70B as recipe


BASE = Path(__file__).resolve().parent


def dynamic_minimum(n, text):
    ends = [0] + [i + 1 for i, c in enumerate(text) if c in '.?!']
    costs = [0] + [len(ends)] * (len(ends) - 1)
    for right in range(1, len(ends)):
        for left in range(right - 1, -1, -1):
            start = ends[left] + bool(left)
            if len(text[start:ends[right]]) > n:
                break
            costs[right] = min(costs[right], costs[left] + 1)
    return 'Impossible' if costs[-1] >= len(ends) else costs[-1]


class TextMessagingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = json.loads((BASE / 'recipe-reports' / '70B.json').read_text())
        cls.cases = recipe.extras('70B')

    def test_actual_exhaustive_and_random_cut_enumeration(self):
        self.assertEqual(recipe.brute_checks(), {'70B': 18864})

    def test_all_generated_pairs_against_independent_dynamic_program(self):
        self.assertEqual(len(self.cases), 150)
        self.assertEqual(len({c['input'] for c in self.cases}), 150)
        for i, case in enumerate(self.cases):
            with self.subTest(case=i):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertIn(case['category'], {'boundary', 'adversarial', 'maxSize'})
                self.assertTrue(case['reason'])
                self.assertEqual(len(case['input'].splitlines()), 2)
                n, text = recipe.parse('70B', case['input'])
                expected = dynamic_minimum(n, text)
                self.assertEqual(recipe.answer('70B', (n, text)), expected)
                self.assertEqual(case['output'], str(expected) + '\n')
        self.assertEqual(recipe.review('70B', list(enumerate(self.cases)), []), [])

    def test_supplied_official_tests_and_samples_unchanged_and_reviewed(self):
        fixtures = self.report['upstreamPairs']
        self.assertEqual(len(fixtures), 18)
        for fixture in fixtures:
            with self.subTest(pair=fixture['name']):
                pair = fixture['pair']
                for side in ('input', 'output'):
                    self.assertEqual(hashlib.sha256(pair[side].encode()).hexdigest(),
                                     fixture[side + 'Sha256'])
                n, text = recipe.parse('70B', pair['input'])
                expected = dynamic_minimum(n, text)
                self.assertEqual(pair['output'].split(), [str(expected)])
                self.assertEqual(recipe.answer('70B', (n, text)), expected)
        tests = [(f['name'], f['pair']) for f in fixtures if f['name'].startswith('tests/')]
        samples = [(f['name'], f['pair']) for f in fixtures if f['name'].startswith('samples/')]
        self.assertEqual(recipe.review('70B', tests, samples), [])

    def test_real_maximum_dimensions_and_minima(self):
        maximum = [c for c in self.cases if len(recipe.parse('70B', c['input'])[1]) == 10000]
        self.assertEqual(len(maximum), 5)
        self.assertTrue(all(c['category'] == 'maxSize' for c in maximum))
        self.assertIn(('2\na.\n', '1\n'), [(c['input'], c['output']) for c in self.cases])
        self.assertIn(('2\na. b.\n', '2\n'), [(c['input'], c['output']) for c in self.cases])
        long_feasible = ' '.join(['a.'] * 3333)
        self.assertEqual(recipe.answer('70B', recipe.parse('70B', '2\n' + long_feasible + '\n')), 3333)

    def test_exact_layout_grammar_and_ranges(self):
        invalid = (
            '', '2', '2\n', '1\na.\n', '256\na.\n', '2 3\na.\n', '2 a.\n',
            '2\na.\nb.\n', '2\na.\n\n', '2\n a.\n', '2\na. \n',
            '2\na\n', '2\n.\n', '2\na..\n', '2\na.?\n', '2\na.b.\n',
            '2\na.  b.\n', '2\na  b.\n', '2\na .\n', '2\na\tb.\n',
            '2\na1.\n', '2\né.\n', '2\n_a.\n', '2\na. b\n',
            '2\n' + 'a' * 10000 + '.\n',
        )
        for value in invalid:
            with self.subTest(value=value[:50]), self.assertRaises(ValueError):
                recipe.parse('70B', value)
        self.assertEqual(recipe.parse('70B', '255\r\nHello! A b? c.\r\n'),
                         (255, 'Hello! A b? c.'))
        self.assertEqual(recipe.parse('70B', '2\na.'), (2, 'a.'))
        self.assertEqual(recipe.parse('70B', ' 2\t\na.\n'), (2, 'a.'))
        self.assertEqual(recipe.parse('70B', '2\n' + 'a' * 9999 + '.\n')[0], 2)

    def test_review_reports_invalid_inputs_and_wrong_outputs(self):
        failures = recipe.review('70B', [('invalid', {'input': '2\na.b.\n', 'output': '2'})],
                                 [('wrong', {'input': '5\na. b.\n', 'output': '2'})])
        self.assertEqual([f['test'] for f in failures], ['invalid', 'wrong'])
        self.assertEqual(recipe.review('70B', [], [('crlf', {'input': '2\r\na.\r\n',
                                                           'output': '1\r\n'})]), [])

    def test_source_bound_grammar_and_exponent_restoration(self):
        source = self.report['publicStatement']
        raw = (BASE / source['capturedPath']).read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), source['bodySha256'])
        self.assertIn(b'10<sup class="upper-index">4</sup>', raw)
        grammar = self.report['normalizationNeeded'][0]['replacementHtml']
        self.assertIn(grammar.encode(), raw)
        self.assertEqual(self.report['role'], 'recipe-author-not-auditor')

    def test_distinct_bug_motifs_by_hand_reimplemented_mutants(self):
        for n, text, bad in ((4, 'a. b.', 1), (8, 'a. b. c.', 3), (2, 'aa.', 2)):
            with self.subTest(n=n, text=text):
                actual = recipe.answer('70B', recipe.parse('70B', f'{n}\n{text}\n'))
                self.assertNotEqual(actual, bad)
        strict_fit = 2 if 2 + 1 + 2 >= 5 else 1
        self.assertNotEqual(recipe.answer('70B', (5, 'a. b.')), strict_fit)
        divided_total = (len('aa. bb. cc. dd.') + 5) // 6
        self.assertNotEqual(recipe.answer('70B', (6, 'aa. bb. cc. dd.')), divided_total)

    def test_unknown_ids_and_bounded_brute(self):
        for function, args in ((recipe.parse, ('2\na.\n',)),
                               (recipe.answer, ((2, 'a.'),)),
                               (recipe.brute, ((2, 'a.'),)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.subTest(function=function.__name__), self.assertRaises(ValueError):
                function('70A', *args)
        with self.assertRaises(ValueError):
            recipe.brute('70B', (2, ' '.join(['a.'] * 11)))


if __name__ == '__main__':
    unittest.main()
