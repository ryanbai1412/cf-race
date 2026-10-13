from pathlib import Path
import os
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_568A as recipe

try:
    import numpy as np
except ImportError:
    np = None

PID = '568A'
SAMPLES = [('1 1', '40'), ('1 42', '1'), ('6 4', '172')]
OFFICIAL = [
    ('1 1', 40), ('1 42', 1), ('6 4', 172), ('3 1', 2530), ('42 1', 1179858), ('10000 239', 1168638), ('5 8', 16),
    ('7 11', 16), ('16 60', 1), ('214 210', 40), ('620 35', 251262), ('940 480', 1372), ('1307 3420', 1), ('6811 5416', 66),
    ('7 267', 1), ('106 6', 250300), ('10000 10000', 40), ('10000 9999', 40), ('9999 9998', 40), ('9999 9999', 40),
    ('4 9', 10), ('1000 10000', 1), ('238 9996', 1), ('999 10000', 1), ('241 10000', 1), ('239 10000', 1), ('5858 674', 71118),
]


def tables(limit):
    sieve = np.ones(limit + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = False
    pal = np.zeros(limit + 1, dtype=bool)
    for v in range(1, limit + 1):
        s = str(v)
        if s == s[::-1]:
            pal[v] = True
    return np.cumsum(sieve, dtype=np.int64), np.cumsum(pal, dtype=np.int64)


@unittest.skipIf(np is None, 'numpy unavailable')
class Vectorized(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pi, cls.rub = tables(recipe.LIMIT)
        cls.cases = [recipe.parse(PID, c['input']) for c in recipe.extras(PID)] + [recipe.parse(PID, t) for t, _ in OFFICIAL]

    def last(self, mask, upto=None):
        idx = np.nonzero(mask[1:upto + 1 if upto else None])[0]
        return int(idx[-1]) + 1 if len(idx) else None

    def exact(self, p, q):
        return self.last(q * self.pi <= p * self.rub)

    def test_full_definition_scan_matches_oracle(self):
        for p, q in self.cases:
            self.assertEqual(self.exact(p, q), recipe.answer(PID, (p, q)), (p, q))

    def distinguished(self, wrong):
        return [(p, q) for p, q in self.cases if wrong(p, q) != recipe.answer(PID, (p, q))]

    def test_first_failure_stop_is_killed(self):
        def first_failure(p, q):
            fail = np.nonzero(q * self.pi[1:] > p * self.rub[1:])[0]
            return int(fail[0])
        self.assertGreaterEqual(len(self.distinguished(first_failure)), 20)

    def test_small_tables_are_killed(self):
        for upto, minimum in ((170, 50), (199999, 10), (999999, 5)):
            self.assertGreaterEqual(len(self.distinguished(lambda p, q: self.last(q * self.pi <= p * self.rub, upto))), minimum, upto)

    def test_float_ratio_is_killed(self):
        def floating(p, q):
            return self.last((p / q) * self.rub.astype(np.float64) >= self.pi)
        self.assertGreaterEqual(len(self.distinguished(floating)), 10)

    def test_off_by_one_palindrome_count_is_killed(self):
        self.assertGreaterEqual(len(self.distinguished(lambda p, q: self.last(q * self.pi <= p * (self.rub - 1)))), 100)

    def test_composite_prefix_bug_is_killed(self):
        is_prime = np.diff(self.pi, prepend=0).astype(bool)
        broken = np.where(is_prime, self.pi, 0)
        self.assertEqual(len(self.distinguished(lambda p, q: self.last(q * broken <= p * self.rub))), len(self.cases))

    def test_integer_division_ratio_is_killed(self):
        def floor_a(p, q):
            return self.last(self.pi <= (p // q) * self.rub)
        self.assertGreaterEqual(len(self.distinguished(floor_a)), 50)

    def test_no_qualifying_n_between_limit_and_ten_million(self):
        top = 10 ** 7
        pi, rub = tables(top)
        primes = np.nonzero(np.diff(pi, prepend=0))[0]
        n = primes[(primes - 1 >= recipe.LIMIT) & (primes - 1 <= top)] - 1
        self.assertTrue(bool(np.all(pi[n] > 42 * rub[n])))
        self.assertTrue(bool(pi[top] > 42 * rub[top]))


class Recipe(unittest.TestCase):
    def test_samples_and_official(self):
        for text, out in SAMPLES:
            self.assertEqual(str(recipe.answer(PID, recipe.parse(PID, text))), out)
        for text, out in OFFICIAL:
            self.assertEqual(recipe.answer(PID, recipe.parse(PID, text + '\r\n')), out)
        tests = [(str(i), {'input': t + '\r\n', 'output': f'{o}\r\n'}) for i, (t, o) in enumerate(OFFICIAL)]
        samples = [(f's{i}', {'input': t, 'output': o}) for i, (t, o) in enumerate(SAMPLES)]
        self.assertEqual(recipe.review(PID, tests, samples), [])
        bad = [('x', {'input': '1 1\n', 'output': '41\n'}), ('y', {'input': '43 1\n', 'output': '1\n'})]
        self.assertEqual([f['test'] for f in recipe.review(PID, bad, [])], ['x', 'y'])

    def test_parse_rejects(self):
        for text in ('', '1', '1 1 1', '1\n1', '1 1\n2', '0 1', '1 0', '43 1', '1 43', '10001 10000', '10000 10001',
                     '420 9', '+1 1', '01 1', '1 1.0', '1_0 1', '-1 1', '9996 237', '237 9996'):
            with self.assertRaises(ValueError, msg=text):
                recipe.parse(PID, text)
        self.assertEqual(recipe.parse(PID, '9996 238\r\n'), (9996, 238))
        self.assertEqual(recipe.parse(PID, '238 9996'), (238, 9996))

    def test_extras(self):
        cases = recipe.extras(PID)
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        for c in cases:
            self.assertEqual(set(c), {'input', 'output', 'reason', 'category'})
            self.assertIn(c['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertRegex(c['input'], r'^[1-9][0-9]* [1-9][0-9]*\n$')
            p, q = recipe.parse(PID, c['input'])
            self.assertEqual(c['output'], f'{recipe.brute(PID, (p, q))}\n')
        inputs = {c['input'] for c in cases}
        for text in ('1 42\n', '42 1\n', '9996 238\n', '238 9996\n', '10000 10000\n', '1 1\n'):
            self.assertIn(text, inputs)
        self.assertEqual(max(int(c['output']) for c in cases), 1179858)
        self.assertTrue(any(c['category'] == 'maxSize' for c in cases))
        self.assertEqual(cases, recipe.extras(PID))

    def test_extras_hash_seed_deterministic(self):
        code = 'import json,sys;sys.path.insert(0,%r);import recipe_568A as r;print(json.dumps(r.extras("568A")))' % str(Path(recipe.__file__).parent)
        outs = {subprocess.run([sys.executable, '-c', code], env={**os.environ, 'PYTHONHASHSEED': seed}, capture_output=True, check=True).stdout
                for seed in ('0', '1', '12345')}
        self.assertEqual(len(outs), 1)

    def test_maximum_is_prime_minus_one_or_one(self):
        for c in recipe.extras(PID):
            n = int(c['output'])
            self.assertTrue(n == 1 or recipe._is_prime_trial(n + 1), n)

    def test_literal_scan_small(self):
        for p, q in ((1, 1), (1, 42), (6, 4), (4, 9), (5, 8), (7, 11), (3, 1), (1, 2), (3, 2)):
            self.assertEqual(recipe.literal_scan(p, q, 20000), recipe.answer(PID, (p, q)))

    def test_rosser_tail_beyond_ten_million(self):
        for d in range(8, 1001):
            upto_prev = sum(9 * 10 ** ((k - 1) // 2) for k in range(1, d))
            c, f = (d + 1) // 2, d // 2
            for k in (d - 1, d):
                n = 10 ** k
                rub_bound = upto_prev + n // 10 ** f - 10 ** (c - 1) + 1
                self.assertGreater(n * 10 ** 9, 42 * rub_bound * k * 2302585094, (d, k))

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {PID})
        self.assertGreater(counts[PID], 10000)


if __name__ == '__main__':
    unittest.main()
