from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_595B as recipe

PID = '595B'

OFFICIAL = [
    ('6 2\r\n38 56 49\r\n7 3 4\r\n', '8\r\n'),
    ('8 2\r\n1 22 3 44\r\n5 4 3 2\r\n', '32400\r\n'),
    ('2 1\r\n9 9\r\n9 9\r\n', '1\r\n'),
    ('2 1\r\n9 9\r\n0 9\r\n', '1\r\n'),
    ('4 1\r\n4 3 2 1\r\n1 2 3 4\r\n', '540\r\n'),
    ('18 9\r\n2 3\r\n0 4\r\n', '505000007\r\n'),
    ('4 4\r\n1122\r\n2\r\n', '8\r\n'),
    ('10 5\r\n8378 11089\r\n7 5\r\n', '99\r\n'),
    ('10 5\r\n52057 11807\r\n0 1\r\n', '8\r\n'),
    ('10 1\r\n3 1 1 4 8 7 5 6 4 1\r\n0 0 0 5 5 6 8 8 4 0\r\n', '209952\r\n'),
    ('100 4\r\n388 2056 122 1525 2912 1465 3066 257 5708 3604 3039 6183 3035 626 1389 5393 3321 3175 2922 2024 3837 437 5836 2376 1599\r\n6 5 5 2 9 6 8 3 5 0 6 0 1 8 5 3 5 2 3 0 5 6 6 7 3\r\n', '652599557\r\n'),
    ('100 1\r\n5 3 1 5 6 2 4 8 3 3 1 1 2 8 2 3 8 2 5 2 6 2 3 5 2 1 2 1 2 8 4 3 3 5 1 4 2 2 2 5 8 2 2 6 2 9 2 4 1 8 1 5 5 6 6 1 2 7 3 3 4 2 4 1 2 6 6 4 9 4 3 2 3 8 2 3 1 4 1 4 1 3 5 3 5 5 2 3 4 1 1 8 1 5 6 9 4 2 5 1\r\n6 0 4 5 3 1 0 7 5 3 9 4 5 4 0 2 1 6 2 2 4 3 1 9 5 9 2 2 6 8 6 5 9 6 4 9 9 7 5 4 5 6 0 3 2 0 8 0 3 9 5 3 8 0 9 3 6 2 9 5 9 3 2 2 2 2 0 8 1 2 9 0 9 8 0 3 2 0 7 9 4 3 7 2 3 1 8 9 8 2 6 0 3 2 9 8 9 2 3 4\r\n', '27157528\r\n'),
    ('100 5\r\n5302 4362 11965 14930 11312 33797 17413 17850 79562 17981 28002 40852 173 23022 55762 13013 79597 29597 31944 32384\r\n9 8 7 0 6 6 7 7 5 9 1 3 4 8 7 1 1 6 4 4\r\n', '885507108\r\n'),
    ('1 1\r\n2\r\n0\r\n', '4\r\n'),
]

SAMPLES = [('6 2\n38 56 49\n7 3 4', '8'), ('8 2\n1 22 3 44\n5 4 3 2', '32400')]


def multiples(lo, hi, a):
    return max(0, hi // a - (lo - 1) // a) if lo <= hi else 0


def _product(data, count, modulus=True, wrap32=False):
    _, k, a, b = data
    result = 1
    for x, y in zip(a, b):
        result *= count(k, x, y)
        if wrap32:
            result = (result + 2 ** 31) % 2 ** 32 - 2 ** 31
            result = result - recipe.MOD * int(result / recipe.MOD)
        elif modulus:
            result %= recipe.MOD
        elif result > recipe.MOD ** 2:
            return -1
    return result


def ceil_total(k, a, b):
    p = 10 ** (k - 1)
    return -(-(10 * p - 1) // a) - multiples(b * p, (b + 1) * p - 1, a)


def power_total(k, a, b):
    p = 10 ** (k - 1)
    return 10 * p // a + 1 - multiples(b * p, (b + 1) * p - 1, a)


def clamped_zero(k, a, b):
    p = 10 ** (k - 1)
    return (10 * p - 1) // a + 1 - (((b + 1) * p - 1) // a - max(b * p - 1, 0) // a)


def times_typo(k, a, b):
    p = 10 ** (k - 1)
    if b == 0:
        return multiples(10 * (k - 1), 10 * p - 1, a)
    return multiples(0, b * p - 1, a) + multiples((b + 1) * p, 10 * p - 1, a)


def unpadded(k, a, b):
    p = 10 ** (k - 1)
    if b == 0:
        bad = 1
    else:
        bad = sum(multiples(b * 10 ** e, (b + 1) * 10 ** e - 1, a) for e in range(k))
    return (10 * p - 1) // a + 1 - bad


MUTANTS = {
    'ceil((10^k-1)/a) total (14161391)': (lambda d: _product(d, ceil_total), 2),
    '10^k//a+1 total (14194649)': (lambda d: _product(d, power_total), 2),
    'b=0 floor(-1/a) clamped to 0 (14208904)': (lambda d: _product(d, clamped_zero), 4),
    'b=0 band starts at 10*(k-1) (26065128)': (lambda d: _product(d, times_typo), 4),
    'final product not reduced (14607985 14892841 15822359 17341355 17568290 27281495 119099937)':
        (lambda d: _product(d, recipe.block_count, modulus=False), 6),
    'hypothetical: 32-bit product overflow': (lambda d: _product(d, recipe.block_count, wrap32=True), None),
    'hypothetical: leading digit of unpadded value': (lambda d: _product(d, unpadded), None),
}


def official_pairs():
    return [(f'{i:04d}', {'input': text, 'output': out}) for i, (text, out) in enumerate(OFFICIAL, 1)]


def sample_pairs():
    return [(f's{i}', {'input': text, 'output': out}) for i, (text, out) in enumerate(SAMPLES, 1)]


class ParseTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        expected = (6, 2, (38, 56, 49), (7, 3, 4))
        self.assertEqual(recipe.parse(PID, '6 2\n38 56 49\n7 3 4\n'), expected)
        self.assertEqual(recipe.parse(PID, '6 2\r\n38 56 49\r\n7 3 4\r\n'), expected)
        self.assertEqual(recipe.parse(PID, '6 2\n38 56 49\n7 3 4'), expected)
        self.assertEqual(recipe.parse(PID, '1 1\n9\n0\n'), (1, 1, (9,), (0,)))
        self.assertEqual(recipe.parse(PID, '9 9\n999999999\n9\n'), (9, 9, (999999999,), (9,)))
        self.assertEqual(recipe.parse(PID, '100000 1\n' + '1 ' * 99999 + '1\n' + '0 ' * 99999 + '0\n')[:2], (100000, 1))

    def test_rejects_malformed_inputs(self):
        bad = ['', '6 2\n38 56 49\n', '6 2\n38 56 49 7 3 4\n', '6 2 38 56 49 7 3 4\n', '6 2\n38 56\n7 3\n',
               '6 2\n38 56 49\n7 3 4\n\n', '6 2\n38 56 49\n7 3 4\n1\n', '6  2\n38 56 49\n7 3 4\n', ' 6 2\n38 56 49\n7 3 4\n',
               '6 2\n38 56 49 \n7 3 4\n', '6 2\n38\t56 49\n7 3 4\n', '6 2\n+38 56 49\n7 3 4\n', '6 2\n038 56 49\n7 3 4\n',
               '6 2\n3_8 56 49\n7 3 4\n', '6 2\n100 56 49\n7 3 4\n', '6 2\n0 56 49\n7 3 4\n', '6 2\n38 56 49\n7 3 10\n',
               '6 2\n38 56 49\n7 3 -1\n', '7 2\n38 56 49\n7 3 4\n', '0 1\n\n\n', '100002 1\n1\n1\n', '9 10\n1\n1\n',
               '2 3\n1\n1\n', '6 2\r38 56 49\r7 3 4\r', '6 2\n38 56 49\r\n7 3 4\r\r\n', '6 2\n\n7 3 4\n']
        for text in bad:
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse(PID, text)


class OracleTests(unittest.TestCase):
    def test_hand_derived_block_counts(self):
        cases = {(1, 1, 0): 9, (1, 1, 9): 9, (1, 9, 0): 1, (1, 9, 9): 1, (1, 2, 0): 4, (2, 38, 7): 2,
                 (2, 56, 3): 2, (2, 49, 4): 2, (2, 1, 5): 90, (2, 99, 0): 1, (2, 99, 9): 1, (2, 10, 3): 9,
                 (9, 1, 0): 900000000, (9, 999999999, 0): 1, (9, 999999999, 9): 1, (9, 100000000, 4): 9}
        for (k, a, b), expected in cases.items():
            self.assertEqual(recipe.block_count(k, a, b), expected, (k, a, b))
            self.assertEqual(recipe.band_count(k, a, b), expected, (k, a, b))
            if k <= 4:
                self.assertEqual(recipe.enumerated_count(k, a, b), expected, (k, a, b))

    def test_first_sample_note_lists_exactly_the_good_numbers(self):
        n, k, a, b = recipe.parse(PID, SAMPLES[0][0])
        per_block = [[str(v).zfill(k) for v in range(10 ** k) if v % x == 0 and str(v).zfill(k)[0] != str(y)]
                     for x, y in zip(a, b)]
        good = sorted(''.join(parts) for parts in __import__('itertools').product(*per_block))
        self.assertEqual(good, ['000000', '000098', '005600', '005698', '380000', '380098', '385600', '385698'])
        self.assertEqual(recipe.answer(PID, (n, k, a, b)), len(good))

    def test_official_pairs_and_samples(self):
        tests, samples = official_pairs(), sample_pairs()
        self.assertEqual(len(tests), 14)
        self.assertEqual(recipe.review(PID, tests, samples), [])
        for _, pair in tests + samples:
            data = n, k, a, b = recipe.parse(PID, pair['input'])
            expected = pair['output'].split()
            self.assertEqual(expected, [str(recipe.band_oracle(data))])
            if k <= 5:
                product = 1
                for x, y in zip(a, b):
                    product = product * recipe.enumerated_count(k, x, y) % recipe.MOD
                self.assertEqual(expected, [str(product)])
            if n <= 4:
                self.assertEqual(expected, [str(recipe.phone_brute(data))])

    def test_official_bytes_are_crlf_canonical(self):
        for text, out in OFFICIAL:
            n, k, a, b = recipe.parse(PID, text)
            self.assertEqual(text, f'{n} {k}\r\n' + ' '.join(map(str, a)) + '\r\n' + ' '.join(map(str, b)) + '\r\n')
            self.assertRegex(out, r'^[1-9][0-9]*\r\n$')

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review(PID, [('0001', {'input': '1 1\n9\n0\n', 'output': '2\n'}),
                                       ('0002', {'input': '1 1\n10\n0\n', 'output': '1\n'}),
                                       ('0003', {'input': '1 1\n9\n0\n', 'output': '1\n1\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['0001', '0002', '0003'])
        self.assertEqual(failures[0]['expected'], ['1'])

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {PID})
        self.assertGreaterEqual(counts[PID], 110000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)

    def test_generated_cases_are_valid_and_independently_correct(self):
        cases = self.cases
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        self.assertEqual({c['category'] for c in cases}, {'boundary', 'adversarial', 'maxSize'})
        sizes, ks = set(), set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertTrue(case['reason'])
            data = n, k, a, b = recipe.parse(PID, case['input'])
            self.assertEqual(case['input'], f'{n} {k}\n' + ' '.join(map(str, a)) + '\n' + ' '.join(map(str, b)) + '\n')
            self.assertEqual(case['output'], f'{recipe.band_oracle(data)}\n')
            if k <= 4 and len(a) <= 50:
                product = 1
                for x, y in zip(a, b):
                    product = product * recipe.enumerated_count(k, x, y) % recipe.MOD
                self.assertEqual(case['output'], f'{product}\n')
            if n <= 4:
                self.assertEqual(case['output'], f'{recipe.phone_brute(data)}\n')
            sizes.add(n)
            ks.add(k)
        self.assertIn(1, sizes)
        self.assertIn(100000, sizes)
        self.assertEqual(ks, set(range(1, 10)))
        maximum = [recipe.parse(PID, c['input']) for c in cases if c['category'] == 'maxSize']
        self.assertTrue(all(n == 100000 or (k == 9 and n == 99999) for n, k, _, _ in maximum))
        self.assertTrue(any(k == 9 and n == 99999 for n, k, _, _ in maximum))

    def test_deterministic_across_hash_seeds(self):
        digests = set()
        for seed in ('1', '2'):
            code = ('import json,hashlib,recipe_595B as r;'
                    'print(hashlib.sha256(json.dumps(r.extras("595B"),sort_keys=True).encode()).hexdigest())')
            env = dict(os.environ, PYTHONHASHSEED=seed)
            digests.add(subprocess.run([sys.executable, '-c', code], cwd=Path(__file__).resolve().parent, env=env,
                                       capture_output=True, text=True, check=True).stdout.strip())
        expected = sha256(json.dumps(self.cases, sort_keys=True).encode()).hexdigest()
        self.assertEqual(digests, {expected})

    def test_selected_wrong_algorithms_are_killed(self):
        cases = [recipe.parse(PID, c['input']) for c in self.cases]
        for label, (mutant, _) in MUTANTS.items():
            killed = [d for d in cases if mutant(d) != recipe.answer(PID, d)]
            self.assertTrue(killed, label)

    def test_mutants_reproduce_recorded_failed_official_test(self):
        tests = [recipe.parse(PID, text) for text, _ in OFFICIAL]
        for label, (mutant, failed) in MUTANTS.items():
            if failed is None:
                continue
            outcomes = [mutant(d) == recipe.answer(PID, d) for d in tests[:failed]]
            self.assertEqual(outcomes, [True] * (failed - 1) + [False], label)


if __name__ == '__main__':
    unittest.main()
