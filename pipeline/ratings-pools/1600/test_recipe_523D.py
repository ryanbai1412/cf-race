"""Functional recipe checks, not external-submission validation or signoff."""
import hashlib
import json
from pathlib import Path
import unittest

import recipe_523D as recipe


OFFICIAL = (
    ('3 2\r\n1 5\r\n2 5\r\n3 5\r\n', '6\r\n7\r\n11\r\n'),
    ('6 1\r\n1 1000000000\r\n2 1000000000\r\n3 1000000000\r\n4 1000000000\r\n5 1000000000\r\n6 3\r\n', '1000000001\r\n2000000001\r\n3000000001\r\n4000000001\r\n5000000001\r\n5000000004\r\n'),
    ('1 1\r\n1 1\r\n', '2\r\n'),
    ('1 1\r\n1000000000 10000\r\n', '1000010000\r\n'),
    ('10 6\r\n1 1\r\n2 1\r\n3 1\r\n4 1\r\n5 1\r\n6 1\r\n7 1\r\n8 1\r\n9 1\r\n10 1\r\n', '2\r\n3\r\n4\r\n5\r\n6\r\n7\r\n8\r\n9\r\n10\r\n11\r\n'),
    ('10 4\r\n1 1\r\n2 2\r\n3 1\r\n4 1\r\n5 1\r\n6 1\r\n7 1\r\n8 2\r\n9 1\r\n10 1\r\n', '2\r\n4\r\n4\r\n5\r\n6\r\n7\r\n8\r\n10\r\n10\r\n11\r\n'),
    ('10 2\r\n1 5650\r\n2 4753\r\n3 7632\r\n4 688\r\n5 8853\r\n6 284\r\n7 4659\r\n8 5650\r\n9 9768\r\n10 3905\r\n', '5651\r\n4755\r\n12387\r\n6339\r\n15192\r\n12671\r\n17330\r\n20842\r\n27098\r\n24747\r\n'),
    ('10 8\r\n1 5036\r\n7 9294\r\n8 6011\r\n10 8273\r\n11 9203\r\n12 7037\r\n14 383\r\n16 4568\r\n18 8136\r\n19 8288\r\n', '5037\r\n9301\r\n6019\r\n8283\r\n9214\r\n7049\r\n397\r\n4584\r\n8533\r\n12872\r\n'),
    ('10 2\r\n4 2\r\n7 2\r\n8 2\r\n9 1\r\n10 2\r\n12 2\r\n14 1\r\n15 2\r\n17 2\r\n19 1\r\n', '6\r\n9\r\n10\r\n10\r\n12\r\n14\r\n15\r\n17\r\n19\r\n20\r\n'),
    ('10 7\r\n195901104 7859\r\n265432683 5489\r\n290824505 5754\r\n346976046 4969\r\n406206484 8390\r\n522669517 6810\r\n800443397 4979\r\n839536223 1825\r\n918231479 8117\r\n941210310 1322\r\n', '195908963\r\n265438172\r\n290830259\r\n346981015\r\n406214874\r\n522676327\r\n800448376\r\n839538048\r\n918239596\r\n941211632\r\n'),
    ('10 4\r\n126995987 385321200\r\n195616854 752754110\r\n197489309 899442094\r\n285439286 247570387\r\n308620877 957032819\r\n428385669 227675453\r\n673115425 94614781\r\n766412355 105231165\r\n943783548 855684033\r\n994356572 699602107\r\n', '512317187\r\n948370964\r\n1096931403\r\n533009673\r\n1469350006\r\n760685126\r\n855299907\r\n960531072\r\n1804054997\r\n1693958679\r\n'),
    ('10 10\r\n999999991 1000000000\r\n999999992 1000000000\r\n999999993 1000000000\r\n999999994 1000000000\r\n999999995 1000000000\r\n999999996 1000000000\r\n999999997 1000000000\r\n999999998 1000000000\r\n999999999 1000000000\r\n1000000000 1000000000\r\n', '1999999991\r\n1999999992\r\n1999999993\r\n1999999994\r\n1999999995\r\n1999999996\r\n1999999997\r\n1999999998\r\n1999999999\r\n2000000000\r\n'),
)
SAMPLES = (
    ('3 2\n1 5\n2 5\n3 5', '6\n7\n11'),
    ('6 1\n1 1000000000\n2 1000000000\n3 1000000000\n4 1000000000\n5 1000000000\n6 3', '1000000001\n2000000001\n3000000001\n4000000001\n5000000001\n5000000004'),
)


def named(pairs, prefix):
    return [(f'{prefix}/{i:04d}', {'input': text, 'output': output})
            for i, (text, output) in enumerate(pairs, 1)]


class Recipe523DTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.generated = recipe.extras('523D')
        cls.report = json.loads((Path(__file__).parent / 'recipe-reports/523D.json').read_text())

    def test_exported_interface(self):
        self.assertEqual(recipe.IDS, ('523D',))
        self.assertEqual(set(recipe.SEMANTICS), {'523D'})

    def test_decimal_and_line_endings(self):
        for text in ('1 2\n10 3\n', '1 2\r\n10 3\r\n', '1 2\n10 3', '01\t02\n010 03\n'):
            self.assertEqual(recipe.parse('523D', text), (2, [(10, 3)]))

    def test_rejects_wrong_layout_arity_and_ranges(self):
        invalid = (
            '', '0 1\n', '1 0\n1 1\n', '500001 1\n1 1\n', '1 500001\n1 1\n',
            '1\n1 1\n', '1 1 1\n1 1\n', '1 1\n', '1 1 1 1\n',
            '1 1\n1\n1\n', '2 1\n1 1 2 1\n', '1 1\n1 1\n2 1\n',
            '1 1\n\n1 1\n', '\n1 1\n1 1\n', '1 1\n1 1\n\n',
            '2 1\n1 1\n1 2\n', '2 1\n2 1\n1 2\n', '1 1\n0 1\n',
            '1 1\n1 0\n', '1 1\n1000000001 1\n', '1 1\n1 1000000001\n',
            '1 1\n-1 1\n', '1 1\n+1 1\n', '1 1\n1_000 1\n',
            '1 1\n1.0 1\n', '1 1\n١ 1\n', '1 1\n1 1 junk\n',
        )
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('523D', text)

    def test_unknown_problem_fails_closed(self):
        for function, args in ((recipe.parse, ('1 1\n1 1\n',)),
                               (recipe.answer, ((1, [(1, 1)]),)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                function('523E', *args)

    def test_known_queue_ties_order_and_overflow(self):
        cases = (
            ((2, [(1, 5), (2, 5), (3, 5)]), [6, 7, 11]),
            ((1, [(1, 1), (2, 1)]), [2, 3]),
            ((2, [(1, 10), (2, 1)]), [11, 3]),
            ((1, [(1, 5), (2, 1), (3, 2)]), [6, 7, 9]),
            ((2, [(1, 4), (2, 3), (3, 2), (4, 1), (5, 3)]), [5, 5, 7, 6, 9]),
            ((1, [(i, 10**9) for i in range(1, 5)]), [1000000001, 2000000001, 3000000001, 4000000001]),
        )
        for data, expected in cases:
            self.assertEqual(recipe.answer('523D', data), expected)

    def test_original_official_and_sample_review(self):
        self.assertEqual(recipe.review('523D', named(OFFICIAL, 'tests'), named(SAMPLES, 'samples')), [])
        for text, output in (*OFFICIAL, *SAMPLES):
            self.assertEqual(recipe._event_reference(recipe.parse('523D', text)), list(map(int, output.split())))

    def test_original_fixture_bytes_bound_to_report(self):
        for field, fixtures in (('officialPairs', OFFICIAL), ('samplePairs', SAMPLES)):
            records = self.report['upstreamReview'][field]
            self.assertEqual(len(records), len(fixtures))
            for record, (text, output) in zip(records, fixtures):
                for key, original in (('input', text), ('output', output)):
                    self.assertEqual(record[key + 'Sha256'], hashlib.sha256(original.encode()).hexdigest())

    def test_generated_layout_and_oracle_outputs(self):
        self.assertEqual(len(self.generated), 160)
        self.assertEqual(len({p['input'] for p in self.generated}), 160)
        self.assertEqual({p['category'] for p in self.generated}, {'boundary', 'adversarial', 'maxSize'})
        for pair in self.generated:
            with self.subTest(reason=pair['reason']):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                data = recipe.parse('523D', pair['input'])
                lines = pair['input'].splitlines()
                self.assertEqual(len(lines), len(data[1]) + 1)
                self.assertTrue(all(len(line.split()) == 2 for line in lines))
                self.assertEqual(pair['output'], '\n'.join(map(str, recipe.answer('523D', data))) + '\n')

    def test_every_generated_pair_against_independent_reference(self):
        for pair in self.generated:
            data = recipe.parse('523D', pair['input'])
            k, videos = data
            if k >= len(videos):
                expected = [s + m for s, m in videos]
            else:
                expected = recipe._event_reference(data)
            self.assertEqual(list(map(int, pair['output'].split())), expected, pair['reason'])

    def test_maximum_dimensions_and_minima_are_real(self):
        headers = [tuple(map(int, pair['input'].split('\n', 1)[0].split())) for pair in self.generated]
        self.assertIn((500000, 500000), headers)
        self.assertIn((1, 500000), headers)
        self.assertIn((1, 1), headers)
        maximum = self.generated[headers.index((500000, 500000))]
        self.assertEqual(maximum['category'], 'maxSize')
        self.assertEqual(maximum['output'].split()[-1], '500001')

    def test_exhaustive_and_random_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'523D': 6386})

    def test_selected_wa_mutant_targets_are_semantic(self):
        witnesses = (
            ('1 2\n10 3\n', [5]),
            ('2 1\n1 1\n100 2\n', [2, 4]),
            ('4 2\n1 100\n2 1\n3 1\n4 1\n', [101, 3, 4, 102]),
        )
        for text, predicted_wrong in witnesses:
            self.assertIn(text, {pair['input'] for pair in self.generated})
            expected = recipe._event_reference(recipe.parse('523D', text))
            self.assertNotEqual(expected, predicted_wrong)

    def test_review_preserves_and_reports_bad_pairs(self):
        bad = [('bad-layout', {'input': '1 1 1 1\n', 'output': '2\n'}),
               ('bad-range', {'input': '1 1\n0 1\n', 'output': '1\n'}),
               ('bad-answer', {'input': '1 1\n1 1\n', 'output': '3\n'}),
               ('missing-output', {'input': '1 1\n1 1\n'})]
        before = json.dumps(bad)
        self.assertEqual([e['test'] for e in recipe.review('523D', bad, [])], [name for name, _ in bad])
        self.assertEqual(json.dumps(bad), before)

    def test_public_statement_copy_is_hash_bound(self):
        source = self.report['statementAttestation']
        body = (Path(__file__).parent / source['copyPath']).read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), source['copySha256'])
        self.assertEqual(hashlib.sha256(body[:-1]).hexdigest(), source['elementSha256'])
        self.assertIn(b'5\xc2\xb710<sup class="upper-index">5</sup>', body)
        self.assertIn(b'10<sup class="upper-index">9</sup>', body)
        self.assertEqual(len(self.report['normalizationProposals']), 2)


if __name__ == '__main__':
    unittest.main()
