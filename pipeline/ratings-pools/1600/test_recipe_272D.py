"""Functional recipe tests; no public submission execution or qualification."""
from collections import Counter
import json
import math
from pathlib import Path
import random
import unittest

import recipe_272D as recipe


OFFICIAL = [
    {'input': '1\r\n1\r\n2\r\n7\r\n', 'output': '1\r\n'},
    {'input': '2\r\n1 2\r\n2 3\r\n11\r\n', 'output': '2\r\n'},
    {'input': '2\r\n1 2\r\n1 2\r\n4\r\n', 'output': '1\r\n'},
    {'input': '4\r\n1 2 3 4\r\n4 3 2 1\r\n1009\r\n', 'output': '16\r\n'},
    {'input': '5\r\n1 2 3 3 5\r\n1 2 3 5 3\r\n12\r\n', 'output': '0\r\n'},
    {'input': '1\r\n1000000000\r\n1000000000\r\n2\r\n', 'output': '1\r\n'},
    {'input': '2\r\n1 2\r\n2 2\r\n4\r\n', 'output': '3\r\n'},
]
SAMPLES = [
    {'input': '1\n1\n2\n7', 'output': '1'},
    {'input': '2\n1 2\n2 3\n11', 'output': '2'},
]


class Recipe272DTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('272D')

    def test_interface_and_unsupported_ids(self):
        self.assertEqual(recipe.IDS, ('272D',))
        self.assertEqual(set(recipe.SEMANTICS), {'272D'})
        for call in (lambda: recipe.parse('0A', '1\n1\n1\n2'),
                     lambda: recipe.answer('0A', ([1], [1], 2)),
                     lambda: recipe.extras('0A'),
                     lambda: recipe.review('0A', [], [])):
            with self.assertRaises(ValueError):
                call()

    def test_original_official_and_sample_bytes(self):
        self.assertEqual(recipe.review('272D', list(enumerate(OFFICIAL)),
                                       list(enumerate(SAMPLES))), [])
        for pair in OFFICIAL + SAMPLES:
            data = recipe.parse('272D', pair['input'])
            self.assertEqual(str(recipe._interleaving_answer(data)), pair['output'].strip())
        import hashlib
        for pairs, expected in ((OFFICIAL, '828cb6cd796df75de6b9a5716f461c8108299c13e921354abbeae13da282eae7'),
                                (SAMPLES, '9fa93a20ef1eaa05f80a85d7a05efc9e83578790d5cec8c5acfecb7a6f878832')):
            encoded = json.dumps(pairs, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), expected)

    def test_generated_layout_answers_and_determinism(self):
        self.assertTrue(120 <= len(self.cases) <= 180)
        self.assertEqual(len({case['input'] for case in self.cases}), len(self.cases))
        self.assertEqual(self.cases, recipe.extras('272D'))
        self.assertEqual(sum(case['category'] == 'maxSize' for case in self.cases), 4)
        for case in self.cases:
            with self.subTest(reason=case['reason'], input_prefix=case['input'][:50]):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
                self.assertTrue(case['reason'])
                lines = case['input'].splitlines()
                self.assertEqual(len(lines), 4)
                n = int(lines[0])
                self.assertEqual(len(lines[1].split()), n)
                self.assertEqual(len(lines[2].split()), n)
                data = recipe.parse('272D', case['input'])
                self.assertEqual(case['output'], str(recipe.answer('272D', data)) + '\n')
                self.assertEqual(case['output'], str(recipe._interleaving_answer(data)) + '\n')
                if case['category'] == 'maxSize':
                    self.assertEqual(n, 100000)

    def test_exhaustive_and_random_literal_sequence_enumeration(self):
        counts = recipe.brute_checks()
        self.assertEqual(counts, {'272D': 7576 + len(self.cases)})
        print('272D independent brute/interleaving assertions:', counts['272D'])

    def test_independent_exact_big_integer_factorial_reference(self):
        rng = random.Random(2721602)
        for _ in range(100):
            n = rng.randint(1, 25)
            a = [rng.randint(1, 5) for _ in range(n)]
            b = [rng.randint(1, 5) for _ in range(n)]
            modulus = rng.choice((2, 4, 6, 8, 9, 25, 97, 1000000007))
            product = math.prod(math.factorial(c) for c in Counter(a + b).values())
            divisor = 2 ** sum(x == y for x, y in zip(a, b))
            self.assertEqual(product % divisor, 0)
            self.assertEqual(recipe.answer('272D', (a, b, modulus)), product // divisor % modulus)

    def test_hand_counted_values_and_composite_cancellation(self):
        cases = [
            (([1], [1], 2), 1),
            (([1], [2], 2), 1),
            (([1, 1], [1, 1], 1009), 6),
            (([1, 1], [1, 1], 4), 2),
            (([1, 1, 1], [1, 1, 1], 8), 2),
            (([1, 1, 1], [2, 2, 2], 1009), 36),
            (([1, 2], [2, 2], 4), 3),
            (([1, 2, 3, 4], [4, 3, 2, 1], 1009), 16),
        ]
        for data, expected in cases:
            self.assertEqual(recipe.answer('272D', data), expected)
            self.assertEqual(recipe._enumerated_count(data[0], data[1]) % data[2], expected)

    def test_parse_ranges_arity_and_four_line_layout(self):
        invalid = [
            '', '1 1 1 2', '1\n1\n1', '1\n1\n1\n2\n2',
            '\n1\n1\n1\n2', '1\n1\n1\n2\n\n', '1\n\n1\n1\n2',
            '2\n1\n1 2\n2', '2\n1 2 3\n1 2\n2',
            '2\n1\n2\n1 2\n2', '1 2\n1\n1\n2', '1\n1\n1\n2 3',
            '0\n1\n1\n2', '100001\n1\n1\n2',
            '1\n0\n1\n2', '1\n1\n1000000001\n2',
            '1\n1\n1\n1', '1\n1\n1\n1000000008',
            '1\n-1\n1\n2', '1\n+1\n1\n2', '1\n1_0\n1\n2',
            '1\n1.0\n1\n2', '1\n١\n1\n2', '1\r1\r1\r2',
            '2\n1\v2\n1 2\n2', '2\n1\u20282\n1 2\n2',
        ]
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('272D', text)
        self.assertEqual(recipe.parse('272D', '1\n1\n1\n2'), ([1], [1], 2))
        self.assertEqual(recipe.parse('272D', '1\r\n1 \r\n1\r\n2\r\n'), ([1], [1], 2))

    def test_review_reports_bad_pairs_without_modification(self):
        pairs = [('bad-layout', {'input': '1 1 1 2', 'output': '1'}),
                 ('bad-answer', {'input': '1\n1\n1\n2', 'output': '0'}),
                 ('extra-output', {'input': '1\n1\n1\n2', 'output': '1 1'})]
        before = json.dumps(pairs)
        failures = recipe.review('272D', pairs, [])
        self.assertEqual([failure['test'] for failure in failures], [name for name, _ in pairs])
        self.assertEqual(json.dumps(pairs), before)

    def test_committed_constraint_attestation(self):
        body = (Path(__file__).parent / 'statement-sources'
                / '272D.recipe-author.original.html').read_bytes()
        import hashlib
        self.assertEqual(hashlib.sha256(body).hexdigest(),
                         '99bc653b4c2ed299f68cd913596c2f8373111562472a24ab3ec9917b25e0c86b')
        self.assertIn(b'10<sup class="upper-index">5</sup>', body)
        self.assertEqual(body.count(b'10<sup class="upper-index">9</sup>'), 3)


if __name__ == '__main__':
    unittest.main()
