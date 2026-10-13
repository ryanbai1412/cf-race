"""Functional tests for the author-owned 149B recipe, not qualification."""
import importlib.util
import itertools
import json
from pathlib import Path
import unittest


BASE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('author_recipe_149B', BASE / 'recipe_149B.py')
recipe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recipe)


class Recipe149BTests(unittest.TestCase):
    def test_parser_accepts_exact_layout_and_line_endings(self):
        for ending in ('', '\n', '\r\n'):
            self.assertEqual(recipe.parse('149B', '000B:00001' + ending), ('000B', '00001'))

    def test_parser_rejects_invalid_ranges_arity_and_layout(self):
        invalid = ['', ':', '1:', ':1', '000000:0', '0:000000', 'a:0', '0:z',
                   '1 :2', '1: 2', '1:2 3', '1:2:3', '1\n:2', '1:2\n3:4\n',
                   '\n1:2', '1:2\n\n', ' 1:2', '1:2 ', '1\t:2', '１:2', '1:2\x00']
        for text in invalid:
            with self.subTest(text=repr(text)), self.assertRaises(ValueError):
                recipe.parse('149B', text)

    def test_unknown_pid_is_not_silently_dispatched(self):
        calls = [lambda: recipe.parse('149A', '0:0'),
                 lambda: recipe.answer('149A', ('0', '0')),
                 lambda: recipe.extras('149A'), lambda: recipe.review('149A', [], [])]
        for call in calls:
            with self.assertRaises(ValueError):
                call()

    def test_hand_derived_answers(self):
        cases = {
            '0:0': (-1,), '0:1': (-1,), 'N:Z': (-1,), 'O:0': (0,), 'Z:0': (0,),
            '0:Z': (-1,), '0000N:0000Z': (-1,), '0000O:0000Z': (0,),
            '0:10': tuple(range(2, 60)), '10:0': tuple(range(2, 24)),
            '0:11': tuple(range(2, 59)), '11:0': tuple(range(2, 23)),
            '0:1T': (30,), '0:1U': (0,), '1B:0': (12,), '1C:0': (0,),
            '0:10000': (2,), '10000:0': (2,), '11111:11111': (0,),
            '10101:11111': (2,), '00002:00130': (4, 5, 6), '01B:4A': (12,),
            '0:1N': tuple(range(24, 37)), '22:00': tuple(range(3, 11)),
        }
        for text, expected in cases.items():
            with self.subTest(clock=text):
                self.assertEqual(recipe.answer('149B', recipe.parse('149B', text)), expected)

    def test_all_generated_pairs_are_valid_unique_and_inverse_checked(self):
        cases = recipe.extras('149B')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('149B'))
        self.assertEqual(len({pair['input'] for pair in cases}), len(cases))
        self.assertEqual({pair['category'] for pair in cases}, {'boundary', 'adversarial', 'maxSize'})
        max_cases = []
        for pair in cases:
            with self.subTest(clock=pair['input']):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                data = recipe.parse('149B', pair['input'])
                self.assertEqual(len(pair['input'].splitlines()), 1)
                self.assertTrue(pair['input'].endswith('\n'))
                self.assertTrue(pair['reason'])
                expected = list(map(str, recipe._inverse_reference(data)))
                self.assertEqual(pair['output'].split(), expected)
                self.assertEqual(list(map(str, recipe.answer('149B', data))), expected)
                if pair['category'] == 'maxSize':
                    self.assertEqual(tuple(map(len, data)), (5, 5))
                    max_cases.append(pair)
        self.assertGreaterEqual(len(max_cases), 1)
        self.assertEqual(recipe.review('149B', list(enumerate(cases)), []), [])

    def test_real_exhaustive_and_seeded_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'149B': 7221})

    def test_inverse_encoder_round_trip_without_public_programs(self):
        for base in range(2, 60):
            for value in range(60):
                word = recipe._encode_clock_value(value, base)
                if word is not None:
                    self.assertEqual(sum(recipe.ALPHABET.index(c) * base ** i
                                         for i, c in enumerate(reversed(word))), value)

    def test_bases_beyond_59_are_only_constant_spellings(self):
        for base, limit in itertools.product((60, 61, 100, 1000, 10**6), (24, 60)):
            self.assertEqual(recipe._clock_spellings(base, limit),
                             frozenset(recipe.ALPHABET[:min(limit, 36)]))

    def test_review_checks_samples_and_reports_bad_pairs_without_repair(self):
        samples = [('sample1', {'input': '11:20', 'output': ' '.join(map(str, range(3, 23)))}),
                   ('sample2', {'input': '2A:13', 'output': '0'}),
                   ('sample3', {'input': '000B:00001', 'output': '-1'})]
        self.assertEqual(recipe.review('149B', [], samples), [])
        bad = [('bad-layout', {'input': '1:\n2\n', 'output': '-1'}),
               ('bad-output', {'input': '0:10', 'output': '-1'}),
               ('bad-order', {'input': '1B:0', 'output': '12 12'})]
        original = json.dumps(bad)
        errors = recipe.review('149B', bad, samples)
        self.assertEqual([error['test'] for error in errors], ['bad-layout', 'bad-output', 'bad-order'])
        self.assertEqual(json.dumps(bad), original)


if __name__ == '__main__':
    unittest.main()
