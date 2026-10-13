"""Portable author checks; no public submission code is executed."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest


BASE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('recipe_793B', BASE / 'recipe_793B.py')
recipe = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(recipe)
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import digest


OFFICIAL = [
    {'input': '5 5\r\n..S..\r\n****.\r\nT....\r\n****.\r\n.....\r\n', 'output': 'YES'},
    {'input': '5 5\r\nS....\r\n****.\r\n.....\r\n.****\r\n..T..\r\n', 'output': 'NO'},
    {'input': '1 2\r\nST\r\n', 'output': 'YES'},
    {'input': '3 1\r\nS\r\n*\r\nT\r\n', 'output': 'NO'},
    {'input': '3 3\r\n*..\r\n...\r\nTS.\r\n', 'output': 'YES'},
    {'input': '3 3\r\nT.*\r\n*.*\r\n*S*\r\n', 'output': 'YES'},
    {'input': '7 7\r\n.S.****\r\n...*.*.\r\n.****..\r\n.*.**.*\r\n..T*...\r\n***..*.\r\n*******\r\n', 'output': 'YES'},
    {'input': '3 3\r\n**T\r\n*S*\r\n***\r\n', 'output': 'NO'},
    {'input': '2 2\r\nST\r\n*.\r\n', 'output': 'YES'},
    {'input': '2 2\r\nS.\r\n.T\r\n', 'output': 'YES'},
    {'input': '2 2\r\nTS\r\n.*\r\n', 'output': 'YES'},
    {'input': '2 2\r\n.T\r\nS*\r\n', 'output': 'YES'},
    {'input': '2 4\r\nS.*T\r\n*...\r\n', 'output': 'NO'},
]
SAMPLES = [
    {'input': '5 5\n..S..\n****.\nT....\n****.\n.....', 'output': 'YES'},
    {'input': '5 5\nS....\n****.\n.....\n.****\n..T..', 'output': 'NO'},
]


def segment_closure_reference(rows):
    n, m = len(rows), len(rows[0])
    start, target = recipe._endpoints(rows)
    reached = bytearray(n * m)
    reached[start[0] * m + start[1]] = 1
    # Each simultaneous closure adds one straight segment, not one cell step.
    for _ in range(3):
        expanded = reached.copy()
        for r in range(n):
            for columns in (range(m), range(m - 1, -1, -1)):
                active = False
                for c in columns:
                    i = r * m + c
                    if rows[r][c] == '*':
                        active = False
                    else:
                        active = active or bool(reached[i])
                        if active:
                            expanded[i] = 1
        for c in range(m):
            for row_indices in (range(n), range(n - 1, -1, -1)):
                active = False
                for r in row_indices:
                    i = r * m + c
                    if rows[r][c] == '*':
                        active = False
                    else:
                        active = active or bool(reached[i])
                        if active:
                            expanded[i] = 1
        reached = expanded
    return 'YES' if reached[target[0] * m + target[1]] else 'NO'


class Recipe793BTests(unittest.TestCase):
    def test_interface_and_pid(self):
        self.assertEqual(recipe.IDS, ('793B',))
        self.assertIn('793B', recipe.SEMANTICS)
        for function, args in ((recipe.parse, ('other', '1 2\nST\n')),
                               (recipe.answer, ('other', ('ST',))),
                               (recipe.extras, ('other',)),
                               (recipe.review, ('other', [], []))):
            with self.subTest(function=function.__name__), self.assertRaises(ValueError):
                function(*args)

    def test_line_layout_and_newlines(self):
        for text in ('1 2\nST', '1 2\nST\n', '1 2\r\nST\r\n', ' \t1\t2 \nST\n'):
            with self.subTest(text=text):
                self.assertEqual(recipe.parse('793B', text), ('ST',))
        self.assertEqual(recipe.parse('793B', '2 1\nS\nT\n'), ('S', 'T'))

    def test_rejects_invalid_inputs(self):
        invalid = ('', '1\nST\n', '1 2 3\nST\n', '0 2\nST\n',
                   '1001 2\nST\n', '1 1001\nST\n', '2 2\nST\n',
                   '1 2\nS\nT\n', '2 1\nST\n', '1 2 ST\n',
                   '1 2\nST\n\n', '1 2\n ST\n', '1 2\nST \n',
                   '1 3\nS T\n', '1 3\nSxT\n', '1 3\nSST\n',
                   '1 3\nSTT\n', '1 2\nS.\n', '1 2\n.T\n',
                   '1 1\nS\n', '1 2\rST\r', '1 2\vST\n')
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('793B', text)

    def test_supplied_official_and_sample_pairs(self):
        tests = [(f'official-row-{i}', pair) for i, pair in enumerate(OFFICIAL, 1)]
        samples = [(f'sample-{i}', pair) for i, pair in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review('793B', tests, samples), [])
        for name, pair in tests + samples:
            with self.subTest(name=name):
                rows = recipe.parse('793B', pair['input'])
                self.assertEqual(recipe._brute(rows), pair['output'])
                self.assertEqual(recipe.answer('793B', rows), pair['output'])

    def test_review_preserves_and_reports_bad_pairs(self):
        pairs = [('wrong-token', {'input': '1 2\nST\n', 'output': 'NO'}),
                 ('bad-layout', {'input': '2 1\nST\n', 'output': 'YES'}),
                 ('extra-token', {'input': '1 2\nST\n', 'output': 'YES debug'})]
        before = json.dumps(pairs)
        errors = recipe.review('793B', pairs, [])
        self.assertEqual([entry['test'] for entry in errors], [name for name, _ in pairs])
        self.assertEqual(json.dumps(pairs), before)

    def test_real_exhaustive_and_random_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'793B': 10752})

    def test_all_generated_pairs(self):
        cases = recipe.extras('793B')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('793B'))
        self.assertEqual(len({case['input'] for case in cases}), 160)
        self.assertEqual({case['category'] for case in cases}, {'boundary', 'adversarial', 'maxSize'})
        maxima = []
        for i, case in enumerate(cases):
            with self.subTest(case=i):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertTrue(case['reason'])
                rows = recipe.parse('793B', case['input'])
                n, m = map(int, case['input'].splitlines()[0].split())
                self.assertEqual(len(rows), n)
                self.assertTrue(all(len(row) == m for row in rows))
                expected = segment_closure_reference(rows) if case['category'] == 'maxSize' else recipe._brute(rows)
                self.assertEqual(case['output'], expected + '\n')
                self.assertEqual(recipe.answer('793B', rows), expected)
                if case['category'] == 'maxSize':
                    self.assertEqual((n, m), (1000, 1000))
                    maxima.append(expected)
        self.assertEqual(maxima, ['YES', 'NO', 'YES', 'NO'])

    def test_turn_budget_and_orientation_traps(self):
        fixtures = [(('S**', '...', '**T'), 'YES'),
                    (('S.*', '*.*', '*.T'), 'YES'),
                    (('S**', '...', '**.', 'T..'), 'NO'),
                    (('*S.', '...', '.T*'), 'YES')]
        for rows, expected in fixtures:
            with self.subTest(rows=rows):
                self.assertEqual(recipe.answer('793B', rows), expected)
                self.assertEqual(recipe._brute(rows), expected)
                self.assertEqual(segment_closure_reference(rows), expected)
        rows = fixtures[0][0]
        self.assertFalse(any(all(rows[r][c] != '*' for r in range(3))
                             and all(rows[0][j] != '*' for j in range(c + 1))
                             and all(rows[2][j] != '*' for j in range(c, 3))
                             for c in range(3)))

    def test_fixture_and_attestation_bindings(self):
        report = json.loads((BASE / 'recipe-reports' / '793B.json').read_text())
        self.assertEqual(digest(OFFICIAL), report['sourceIntegrity']['officialPairsDigest'])
        self.assertEqual(digest(SAMPLES), report['sourceIntegrity']['samplePairsDigest'])
        path = BASE / report['statementAttestation']['localPath']
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                         report['statementAttestation']['problemStatementSha256'])
        self.assertEqual(report['statementNormalization']['replacements'], [])


if __name__ == '__main__':
    unittest.main()
