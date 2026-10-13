from pathlib import Path
import os
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_305C as recipe

OFFICIAL = [
    ('4\r\n0 1 1 1\r\n', '0\r\n'),
    ('1\r\n3\r\n', '3\r\n'),
    ('1\r\n0\r\n', '0\r\n'),
    ('1\r\n2000000000\r\n', '2000000000\r\n'),
    ('1\r\n1\r\n', '1\r\n'),
    ('26\r\n' + ' '.join(['0'] * 24 + ['2', '2']) + '\r\n', '5\r\n'),
]
SAMPLES = [('4\n0 1 1 1', '0'), ('1\n3', '3')]


def independent_formula(a):
    total = sum(1 << x for x in a)
    return total.bit_length() - bin(total).count('1')


def mutant_print_min(a):
    return min(a)


def mutant_one_pass_merge(a):
    a = list(a)
    for i in range(len(a) - 1):
        if a[i] == a[i + 1]:
            a[i + 1] += 1
            a[i] = -1
    kept = [x for x in a if x >= 0]
    return max(kept) - len(kept) + 1


def mutant_set_without_carry_insert(a):
    s, mx, cnt = set(), 0, 0
    for k in a:
        if k in s:
            while k + 1 in s:
                s.remove(k)
                cnt -= 1
                k += 1
                mx = max(mx, k + 1)
        else:
            s.add(k)
            cnt += 1
            mx = max(mx, k)
    return mx - cnt + 1


class PowersLayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        self.assertEqual(recipe.parse('305C', '4\n0 1 1 1'), [0, 1, 1, 1])
        self.assertEqual(recipe.parse('305C', '1\r\n2000000000\r\n'), [2000000000])

    def test_rejects_bad_layout_arity_range_and_order(self):
        for text in ('', '1\n', '1 0\n', '1\n0\n\n0\n', '0\n\n', '2\n0\n', '2\n0\n0\n', '1\n0 0\n', '2\n1 0\n',
                     '1\n2000000001\n', '1\n-1\n', '1\n+1\n', '1\n01\n', '01\n0\n', '100001\n' + '0 ' * 100001 + '\n',
                     '1\n1.0\n', 'x\n0\n', '3 \n0 0\n'):
            with self.subTest(text=text[:30]), self.assertRaises(ValueError):
                recipe.parse('305C', text)


class PowersOracleTests(unittest.TestCase):
    def test_official_and_samples_pass_review(self):
        tests = [(f'{i:04d}', {'input': x, 'output': y}) for i, (x, y) in enumerate(OFFICIAL, 1)]
        samples = [(f'sample-{i}', {'input': x, 'output': y}) for i, (x, y) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review('305C', tests, samples), [])

    def test_review_reports_disagreement_and_invalid_input(self):
        failures = recipe.review('305C', [('a', {'input': '1\n3\n', 'output': '2\n'}),
                                          ('b', {'input': '2\n3 1\n', 'output': '0\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b'])
        self.assertEqual(failures[0]['expected'], ['3'])

    def test_three_references_agree_on_small_inputs(self):
        for a in ([0], [3], [0, 1, 1, 1], [0] * 24 + [2, 2], [5, 5, 6, 9, 9, 9], [0, 0, 0, 0, 0, 0, 0, 0, 1]):
            expected = independent_formula(a)
            self.assertEqual(recipe.answer('305C', a), expected)
            self.assertEqual(recipe.brute_small(a), expected)
            self.assertEqual(recipe.brute_bigint(a), expected)

    def test_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'305C': 2891})


class PowersExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('305C')

    def test_extras_layout_answers_and_size(self):
        cases = self.cases
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        sizes = set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertRegex(case['input'], r'^[1-9][0-9]*\n(0|[1-9][0-9]*)( (0|[1-9][0-9]*))*\n$')
            a = recipe.parse('305C', case['input'])
            self.assertEqual(case['output'], f'{recipe.brute_bigint(a)}\n')
            sizes.add(len(a))
            if max(a) <= 5000:
                self.assertEqual(case['output'], f'{independent_formula(a)}\n')
        self.assertIn(1, sizes)
        self.assertIn(recipe.MAX_N, sizes)
        flat = [recipe.parse('305C', c['input']) for c in cases]
        self.assertIn([recipe.MAX_A] * recipe.MAX_N, flat)
        self.assertIn([0], flat)
        self.assertIn('2000000011\n', [c['output'] for c in cases])

    def test_extras_deterministic_across_hash_seeds(self):
        code = ('import hashlib,json,sys;sys.path.insert(0,%r);import recipe_305C as r;'
                'print(hashlib.sha256(json.dumps(r.extras("305C")).encode()).hexdigest())') % str(Path(recipe.__file__).parent)
        digests = {subprocess.run([sys.executable, '-c', code], env={**os.environ, 'PYTHONHASHSEED': seed},
                                  capture_output=True, text=True, check=True).stdout for seed in ('0', '1')}
        self.assertEqual(len(digests), 1)

    def test_labelled_wrong_algorithms_fail_their_cases(self):
        mutants = {'3911483': mutant_print_min, '51991582': mutant_one_pass_merge, '39338055': mutant_set_without_carry_insert}
        for sid, mutant in mutants.items():
            labelled = [c for c in self.cases if sid in c['reason']]
            self.assertTrue(labelled, sid)
            for case in labelled:
                a = recipe.parse('305C', case['input'])
                self.assertNotEqual(f'{mutant(a)}\n', case['output'], (sid, case['reason']))
        for sid, mutant in mutants.items():
            killed = sum(f'{mutant(recipe.parse("305C", c["input"]))}\n' != c['output'] for c in self.cases)
            self.assertGreater(killed, 10, sid)


if __name__ == '__main__':
    unittest.main()
