"""Functional recipe tests; upstream CRLF pairs are preserved verbatim."""
import hashlib
import json
from pathlib import Path
import unittest

import recipe_493C as recipe


OFFICIAL_PAIRS = json.loads(r'''[
  {
    "input": "3\r\n1 2 3\r\n2\r\n5 6\r\n",
    "output": "9:6\r\n"
  },
  {
    "input": "5\r\n6 7 8 9 10\r\n5\r\n1 2 3 4 5\r\n",
    "output": "15:10\r\n"
  },
  {
    "input": "5\r\n1 2 3 4 5\r\n5\r\n6 7 8 9 10\r\n",
    "output": "15:15\r\n"
  },
  {
    "input": "3\r\n1 2 3\r\n3\r\n6 4 5\r\n",
    "output": "9:9\r\n"
  },
  {
    "input": "10\r\n1 2 3 4 5 6 7 8 9 10\r\n1\r\n11\r\n",
    "output": "30:3\r\n"
  },
  {
    "input": "10\r\n1 2 3 4 5 6 7 8 9 11\r\n1\r\n10\r\n",
    "output": "30:3\r\n"
  },
  {
    "input": "3\r\n1 2 3\r\n3\r\n1 2 3\r\n",
    "output": "9:9\r\n"
  },
  {
    "input": "3\r\n1 2 3\r\n3\r\n3 4 5\r\n",
    "output": "9:9\r\n"
  },
  {
    "input": "4\r\n2 5 3 2\r\n4\r\n1 5 6 2\r\n",
    "output": "12:11\r\n"
  },
  {
    "input": "2\r\n3 3\r\n3\r\n1 3 3\r\n",
    "output": "6:8\r\n"
  },
  {
    "input": "3\r\n1 1 1\r\n4\r\n1 3 1 1\r\n",
    "output": "6:8\r\n"
  },
  {
    "input": "4\r\n4 2 1 1\r\n4\r\n3 2 2 2\r\n",
    "output": "9:8\r\n"
  },
  {
    "input": "3\r\n3 9 4\r\n2\r\n10 1\r\n",
    "output": "9:5\r\n"
  },
  {
    "input": "14\r\n4336 24047 24846 25681 28597 30057 32421 34446 48670 67750 68185 69661 85721 89013\r\n30\r\n8751 10576 14401 22336 22689 35505 38649 43073 43176 44359 44777 50210 50408 51361 53181 60095 65554 68201 68285 68801 72501 75881 80251 80509 83306 93167 95365 95545 97201 97731\r\n",
    "output": "28:60\r\n"
  },
  {
    "input": "1\r\n1\r\n2\r\n1 2\r\n",
    "output": "2:4\r\n"
  },
  {
    "input": "18\r\n450 3726 12063 27630 29689 30626 33937 35015 45951 46217 53004 59541 75551 75836 78996 81297 93876 96211\r\n47\r\n3393 5779 6596 7935 9549 10330 11145 13121 14801 15578 24104 24125 25871 31280 35036 38969 40077 41342 42708 46033 47491 48451 49152 51905 55002 55689 56565 57901 59481 60017 66075 67081 68397 71122 74961 78501 84098 87083 87893 89281 89739 90321 92046 95821 96717 96921 96951\r\n",
    "output": "36:94\r\n"
  },
  {
    "input": "3\r\n3 3 4\r\n6\r\n2 2 3 3 3 3\r\n",
    "output": "7:12\r\n"
  },
  {
    "input": "3\r\n2 2 2\r\n3\r\n1 1 1\r\n",
    "output": "9:6\r\n"
  },
  {
    "input": "2\r\n2 2\r\n2\r\n2 2\r\n",
    "output": "6:6\r\n"
  },
  {
    "input": "1\r\n7\r\n6\r\n6 7 8 9 10 11\r\n",
    "output": "2:12\r\n"
  },
  {
    "input": "1\r\n1\r\n2\r\n1 1\r\n",
    "output": "2:4\r\n"
  },
  {
    "input": "3\r\n1 2 3\r\n1\r\n1\r\n",
    "output": "9:3\r\n"
  },
  {
    "input": "3\r\n3 3 4\r\n6\r\n3 2 2 2 3 2\r\n",
    "output": "9:14\r\n"
  },
  {
    "input": "1\r\n3\r\n1\r\n3\r\n",
    "output": "3:3\r\n"
  },
  {
    "input": "1\r\n1\r\n5\r\n1 1 1 1 1\r\n",
    "output": "2:10\r\n"
  },
  {
    "input": "2\r\n1 999999999\r\n2\r\n2 4\r\n",
    "output": "5:4\r\n"
  }
]''')
SAMPLES = [{"input":"3\n1 2 3\n2\n5 6","output":"9:6"},{"input":"5\n6 7 8 9 10\n5\n1 2 3 4 5","output":"15:10"}]


class Recipe493CTests(unittest.TestCase):
    def test_interface_and_unknown_ids(self):
        self.assertEqual(recipe.IDS, ('493C',))
        self.assertEqual(set(recipe.SEMANTICS), {'493C'})
        for call in (
            lambda: recipe.parse('other', '1\n1\n1\n1\n'),
            lambda: recipe.answer('other', ([1], [1])),
            lambda: recipe.extras('other'),
            lambda: recipe.review('other', [], []),
        ):
            with self.assertRaises(ValueError):
                call()

    def test_minimum_and_crlf_layout(self):
        self.assertEqual(recipe.parse('493C', '1\r\n1\r\n1\r\n2000000000\r\n'),
                         ([1], [2000000000]))
        self.assertEqual(recipe.answer('493C', ([1], [2000000000])), '3:3')
        self.assertEqual(recipe.answer('493C', ([2000000000], [1])), '3:2')

    def test_illegal_layout_arity_and_numeric_ranges(self):
        invalid = (
            '', '1 1 1 1\n', '1\n1\n1 1\n', '1\n1\n\n1\n1\n',
            '2\n1\n1\n1\n', '1\n1 2\n1\n1\n', '1\n1\n2\n1\n',
            '0\n1\n1\n1\n', '200001\n1\n1\n1\n', '1\n1\n0\n1\n',
            '1\n0\n1\n1\n', '1\n1\n1\n2000000001\n',
            '1\n-1\n1\n1\n', '1\n+1\n1\n1\n', '1\n1_000\n1\n1\n',
            '1\n1.0\n1\n1\n', '1\n１\n1\n1\n',
        )
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('493C', text)

    def test_hand_derived_scoring_and_mutation_traps(self):
        fixtures = (
            (([1], [1, 1]), '2:4'),
            (([1], [1, 2]), '2:4'),
            (([3], [3]), '3:3'),
            (([1, 1], [1, 1]), '6:6'),
            (([2, 2, 2], [1, 1, 1]), '9:6'),
            (([1, 2000000000], [2, 4]), '5:4'),
            (([3, 3, 9], [1, 1, 7, 7]), '9:10'),
            (([2, 2, 2, 10], [1, 1, 1, 3, 3, 3, 9, 9, 9]), '9:18'),
        )
        for data, expected in fixtures:
            with self.subTest(data=data):
                self.assertEqual(recipe.answer('493C', data), expected)
                self.assertEqual(recipe._literal_best(data), expected)
        self.assertNotEqual('0:0', recipe.answer('493C', ([1], [1, 1])))
        self.assertNotEqual('2:2', recipe.answer('493C', ([3], [3])))
        self.assertNotEqual('6:6', recipe.answer('493C', ([1, 1], [1, 1, 2])))

    def test_generated_cases_are_deterministic_valid_and_literal_checked(self):
        cases = recipe.extras('493C')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('493C'))
        self.assertEqual(len({pair['input'] for pair in cases}), 160)
        self.assertEqual({pair['category'] for pair in cases},
                         {'boundary', 'adversarial', 'maxSize'})
        for pair in cases:
            data = recipe.parse('493C', pair['input'])
            self.assertEqual([len(line.split()) for line in pair['input'].splitlines()],
                             [1, len(data[0]), 1, len(data[1])])
            self.assertEqual(pair['output'].split(), [recipe.answer('493C', data)])
            self.assertEqual(pair['output'].split(), [recipe._literal_best(data)])
            self.assertTrue(pair['reason'])
        self.assertEqual(recipe.review('493C', list(enumerate(cases)), []), [])

    def test_real_maxima_have_separately_derived_scores(self):
        cases = [p for p in recipe.extras('493C') if p['category'] == 'maxSize']
        self.assertEqual(len(cases), 4)
        expected = ('600000:600000', '600000:400000', '600000:3', '2:400000')
        for pair, result in zip(cases, expected):
            a, b = recipe.parse('493C', pair['input'])
            self.assertEqual(max(len(a), len(b)), 200000)
            self.assertEqual(pair['output'].strip(), result)

    def test_real_independent_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'493C': 15260})

    def test_all_original_official_pairs_and_samples(self):
        self.assertEqual(len(OFFICIAL_PAIRS), 26)
        self.assertEqual(len(SAMPLES), 2)
        self.assertEqual(recipe.review('493C', list(enumerate(OFFICIAL_PAIRS)),
                                       [('sample-' + str(i), p) for i, p in enumerate(SAMPLES)]), [])
        for pair in OFFICIAL_PAIRS + SAMPLES:
            self.assertEqual(pair['output'].split(),
                             [recipe._literal_best(recipe.parse('493C', pair['input']))])
        report = json.loads(Path(__file__).with_name('recipe-reports').joinpath('493C.json').read_text())
        raw = json.dumps(OFFICIAL_PAIRS, sort_keys=True, separators=(',', ':'),
                         ensure_ascii=False).encode()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), report['inputBinding']['officialPairsHash'])

    def test_review_reports_each_bad_pair_without_mutating_inputs(self):
        pairs = [('bad-score', {'input': '1\n1\n1\n1\n', 'output': '2:2\n'}),
                 ('bad-layout', {'input': '1 1 1 1\n', 'output': '3:3\n'}),
                 ('bad-punctuation', {'input': '1\n1\n1\n1\n', 'output': '3 : 3\n'})]
        before = json.dumps(pairs)
        errors = recipe.review('493C', pairs, [])
        self.assertEqual([e['test'] for e in errors], [name for name, _ in pairs])
        self.assertEqual(json.dumps(pairs), before)


if __name__ == '__main__':
    unittest.main()
