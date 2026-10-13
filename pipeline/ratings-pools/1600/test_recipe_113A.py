"""Functional recipe tests; no public submission execution or qualification."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_113A as recipe


class GrammarRecipeTests(unittest.TestCase):
    def test_id_contract(self):
        self.assertEqual(recipe.IDS, ('113A',))
        self.assertIn('100000', recipe.SEMANTICS['113A'])
        for function, args in ((recipe.parse, ('113B', 'etr')),
                               (recipe.answer, ('113B', ('etr',))),
                               (recipe.extras, ('113B',)),
                               (recipe.review, ('113B', [], []))):
            with self.assertRaises(ValueError):
                function(*args)

    def test_exact_layout_and_ranges(self):
        for text in ('etr', 'etr\n', 'etr\r\n'):
            self.assertEqual(recipe.parse('113A', text), ('etr',))
        malformed = ('', '\n', ' etr', 'etr ', 'etr  initis', 'etr\tinitis',
                     'etr\ninitis', 'etr\n\n', 'etr\r', 'etr\rinitis',
                     'Etr', 'étr', 'etr1', 'etr\0', 'etr\v', 'etr\f',
                     'etr\u2028', 'etr\u00a0initis', 'a' * 100001)
        for text in malformed:
            with self.subTest(text=repr(text[:30])):
                with self.assertRaises(ValueError):
                    recipe.parse('113A', text)
        self.assertEqual(len(recipe.parse('113A', 'a' * 100000)[0]), 100000)

    def test_samples_and_single_word_exception(self):
        examples = (
            ('petr', 'YES'),
            ('etis atis animatis etis atis amatis', 'NO'),
            ('nataliala kataliala vetra feinites', 'YES'),
        )
        for text, expected in examples:
            self.assertEqual(recipe.answer('113A', recipe.parse('113A', text)), expected)
        for ending in ('lios', 'liala', 'etr', 'etra', 'initis', 'inites'):
            self.assertEqual(recipe.answer('113A', (ending,)), 'YES')
            self.assertEqual(recipe.answer('113A', (ending, ending)), 'NO')

    def test_hand_derived_adversarial_cases(self):
        for text, expected in (
            ('lios etr initis', 'YES'), ('liala etra inites', 'YES'),
            ('lioslialapetrpetrainitisiniteslios petrainitisetr lialainitis', 'YES'),
            ('lios etr initis lios', 'NO'), ('etr etr', 'NO'),
            ('etr initis etr', 'NO'), ('a lios etr initis', 'NO'),
            ('liala etr initis', 'NO'), ('lios etra initis', 'NO'),
            ('liala etra initis', 'NO'), ('lioss', 'NO'),
            ('etrx', 'NO'), ('initis etr', 'NO'),
            ('etr lios initis', 'NO'), ('lios initis', 'NO'),
        ):
            with self.subTest(text=text):
                self.assertEqual(recipe.answer('113A', recipe.parse('113A', text)), expected)

    def test_generated_suite_is_deterministic_legal_and_independently_correct(self):
        cases = recipe.extras('113A')
        self.assertEqual(cases, recipe.extras('113A'))
        self.assertEqual(len(cases), 160)
        self.assertEqual(len({case['input'] for case in cases}), len(cases))
        self.assertEqual({case['category'] for case in cases}, {'boundary', 'adversarial', 'maxSize'})
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertTrue(case['reason'])
                words = recipe.parse('113A', case['input'])
                self.assertEqual(case['output'], recipe.answer('113A', words) + '\n')
                self.assertEqual(case['output'], recipe._brute_answer(words) + '\n')
                self.assertEqual(case['input'], ' '.join(words) + '\n')
        self.assertEqual(recipe.review('113A', list(enumerate(cases)), []), [])

    def test_real_maximum_and_minimum_dimensions(self):
        cases = recipe.extras('113A')
        maximum = [case for case in cases if case['category'] == 'maxSize']
        self.assertEqual(len(maximum), 12)
        for case in maximum:
            self.assertEqual(len(case['input']) - 1, 100000)
        self.assertEqual(max(len(recipe.parse('113A', case['input'])) for case in maximum), 50000)
        self.assertEqual(min(len(case['input']) - 1 for case in cases), 1)
        self.assertEqual([case['output'].strip() for case in maximum],
                         ['YES'] * 6 + ['NO', 'NO', 'YES', 'NO', 'YES', 'NO'])

    def test_review_preserves_failures_and_accepts_crlf(self):
        valid = {'input': 'lios etr initis\r\n', 'output': 'YES\r\n'}
        malformed = {'input': 'etr  initis\r\n', 'output': 'YES\r\n'}
        wrong = {'input': 'etr\r\n', 'output': 'NO\r\n'}
        extra_output = {'input': 'etr\n', 'output': 'YES YES\n'}
        before = json.dumps([valid, malformed, wrong, extra_output])
        failures = recipe.review('113A', [('valid', valid), ('bad-layout', malformed)],
                                 [('wrong-output', wrong), ('extra-output', extra_output)])
        self.assertEqual([failure['test'] for failure in failures],
                         ['bad-layout', 'wrong-output', 'extra-output'])
        self.assertEqual(json.dumps([valid, malformed, wrong, extra_output]), before)

    def test_exhaustive_and_random_independent_brute(self):
        self.assertEqual(recipe.brute_checks(), {'113A': 27647})

    def test_report_and_original_attestation_binding(self):
        base = Path(__file__).resolve().parent
        report = json.loads((base / 'recipe-reports/113A.json').read_text())
        source = report['statementAttestation']
        body = (base / source['bodyPath']).read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), source['bodySha256'])
        self.assertEqual(len(body), source['bodyBytes'])
        self.assertIn(b'10<sup class="upper-index">5</sup>', body)
        self.assertEqual(report['normalizationProposal']['field'], 'input_format')
        self.assertEqual(report['normalizationProposal']['old'], 'does not exceed 105.')
        self.assertEqual(report['normalizationProposal']['replacement'], 'does not exceed 10<sup>5</sup>.')
        self.assertFalse(report['qualificationPerformed'])


if __name__ == '__main__':
    unittest.main()
