import hashlib
import json
import os
from pathlib import Path
import re
import sys
import unittest

import recipe_138A as recipe


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import digest


class Recipe138ATests(unittest.TestCase):
    def test_interface_and_unknown_id(self):
        self.assertEqual(recipe.IDS, ('138A',))
        self.assertEqual(set(recipe.SEMANTICS), {'138A'})
        for function, args in ((recipe.parse, ('1 1\na\na\na\na\n',)),
                               (recipe.answer, ((1, ('a',)*4),)),
                               (recipe.extras, ()), (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                function('139C', *args)

    def test_exact_layout_and_ranges(self):
        valid = '1 1\na\na\ne\ne\n'
        self.assertEqual(recipe.parse('138A', valid), (1, ('a', 'a', 'e', 'e')))
        self.assertEqual(recipe.parse('138A', valid.replace('\n', '\r\n')),
                         recipe.parse('138A', valid))
        self.assertEqual(recipe.parse('138A', valid.rstrip('\n')), recipe.parse('138A', valid))
        invalid = ('', '1\na\na\na\na\n', '1 1 1\na\na\na\na\n',
                   '0 1\n', '2501 1\n', '1 0\na\na\na\na\n', '1 6\na\na\na\na\n',
                   '1.0 1\na\na\na\na\n', '1 1 a a e e\n',
                   '1 1\na a\ne\ne\n', '1 1\na\na\ne\n',
                   valid+'a\n', valid+'\n', valid.replace('a\n', 'A\n', 1),
                   valid.replace('a\n', 'a \n', 1), valid.replace('a\n', '\n', 1),
                   valid.replace('a\n', 'é\n', 1), valid.replace('\n', '\v'),
                   valid.replace('\n', '\r'), '1 1\n'+'a'*9998+'\na\na\na\n')
        for text in invalid:
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                recipe.parse('138A', text)

    def test_hand_derived_schemes(self):
        cases = [('1 1\nday\nmay\nsun\nfun\n', 'aabb'),
                 ('1 1\nday\nmay\ngray\nway\n', 'aaaa'),
                 ('1 1\na\ne\na\ne\n', 'abab'),
                 ('1 1\na\ne\ne\na\n', 'abba'),
                 ('1 1\nb\nb\nb\nb\n', 'NO'),
                 ('1 2\ncommit\nhermit\ncommit\nhermit\n', 'abab'),
                 ('1 1\ncommit\nhermit\ncommit\nhermit\n', 'aaaa'),
                 ('1 1\nax\nay\nax\nay\n', 'abab'),
                 ('2 1\na\na\na\na\ne\ni\ne\ni\n', 'abab'),
                 ('2 1\na\na\ne\ne\na\ne\na\ne\n', 'NO')]
        for text, expected in cases:
            with self.subTest(expected=expected):
                self.assertEqual(recipe.answer('138A', recipe.parse('138A', text)), expected)

    def test_all_generated_pairs_are_valid_and_independently_correct(self):
        cases = recipe.extras('138A')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('138A'))
        self.assertEqual(len({case['input'] for case in cases}), 160)
        outputs = set()
        max_n = max_total = 0
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertIn(case['category'], {'boundary', 'adversarial', 'maxSize'})
                self.assertTrue(case['reason'])
                lines = case['input'].splitlines()
                n, k = map(int, lines[0].split())
                self.assertEqual(len(lines), 4*n+1)
                self.assertTrue(1 <= n <= 2500 and 1 <= k <= 5)
                self.assertTrue(all(re.fullmatch('[a-z]+', word) for word in lines[1:]))
                total = sum(map(len, lines[1:]))
                self.assertLessEqual(total, 10000)
                max_n, max_total = max(max_n, n), max(max_total, total)
                data = recipe.parse('138A', case['input'])
                self.assertEqual(case['output'].split(), [recipe._reference(data)])
                self.assertEqual(case['output'].split(), [recipe.answer('138A', data)])
                outputs.add(case['output'].strip())
        self.assertEqual(outputs, {'aaaa', 'aabb', 'abab', 'abba', 'NO'})
        self.assertEqual(max_n, 2500)
        self.assertEqual(max_total, 10000)
        self.assertEqual(recipe.review('138A', list(enumerate(cases)), []), [])

    def test_review_preserves_and_reports_bad_pairs(self):
        pairs = [('arity', {'input': '1 1\na a a a\n', 'output': 'aaaa'}),
                 ('wrong', {'input': '1 1\na\na\na\na\n', 'output': 'aabb'})]
        original = json.dumps(pairs)
        errors = recipe.review('138A', pairs[:1], pairs[1:])
        self.assertEqual([error['test'] for error in errors], ['arity', 'wrong'])
        self.assertEqual(errors[1]['expected'], 'aaaa')
        self.assertEqual(json.dumps(pairs), original)

    def test_real_exhaustive_and_random_reference_checks(self):
        self.assertEqual(recipe.brute_checks(), {'138A': 13701})

    def test_public_original_statement_binding(self):
        report = json.loads((BASE/'recipe-reports'/'138A.json').read_text())
        source = report['statementAttestation']
        body = (BASE/source['bodyPath']).read_bytes()
        self.assertEqual(hashlib.sha256(body).hexdigest(), source['bodySha256'])
        context = json.loads(re.search(r'<script id="lentille-context" type="application/json">(.*?)</script>',
                                       body.decode(), re.S).group(1))
        content = context['data']['problem']['contenu']
        self.assertEqual(content['locale'], 'en')
        self.assertEqual(content['formatI'], source['content']['formatI'])
        self.assertIn('10^{4}', content['formatI'])
        self.assertEqual(content['description'], source['content']['formatD'])
        self.assertEqual(content['formatO'], source['content']['formatO'])

    @unittest.skipUnless(os.environ.get('CF138A_SOURCE_INPUT'), 'set CF138A_SOURCE_INPUT to pinned input')
    def test_supplied_original_suite(self):
        path = Path(os.environ['CF138A_SOURCE_INPUT'])
        original = path.read_bytes()
        data = json.loads(original)
        self.assertEqual(hashlib.sha256(original).hexdigest(),
                         'c2048d11537ee877b68a43240513e43ba7d6168c488e1e4ac6d1010ddb71ad97')
        self.assertEqual(digest(data['sourceRow']), data['sourceRowHash'])
        row = data['sourceRow']
        tests = [(f'official-{i:04}', pair) for i, pair in enumerate(row['official_tests'], 1)]
        samples = [(f'sample-{i:04}', pair) for i, pair in enumerate(row['examples'], 1)]
        errors = recipe.review('138A', tests, samples)
        report = json.loads((BASE/'recipe-reports'/'138A.json').read_text())
        self.assertEqual(errors, report['upstreamReview']['errors'])
        for name, pair in tests+samples:
            if not any(error['test'] == name for error in errors):
                parsed = recipe.parse('138A', pair['input'])
                self.assertEqual(recipe.answer('138A', parsed), recipe._reference(parsed))
        self.assertEqual(path.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
