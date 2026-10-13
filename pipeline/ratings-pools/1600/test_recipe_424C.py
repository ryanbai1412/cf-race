from functools import reduce
from itertools import accumulate
from operator import xor
from pathlib import Path
import random
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_424C as recipe


OFFICIAL = [
    ('3\r\n1 2 3\r\n',
     '3\r\n'),
    ('1\r\n0\r\n',
     '0\r\n'),
    ('2\r\n65535 0\r\n',
     '65534\r\n'),
    ('10\r\n1356106972 165139648 978829595 410669403 873711167 287346624 117863440 228957745 835903650 1575323015\r\n',
     '948506286\r\n'),
    ('20\r\n1999581813 313463235 1733614990 662007911 1789348031 1120800519 196972430 1579897311 191001928 241720485 1426288783 1103088596 839698523 1974815116 77040208 904949865 840522850 1488919296 1027394709 857931762\r\n',
     '1536068328\r\n'),
    ('25\r\n39226529 640445129 936289624 364461191 1096077769 573427707 1919403410 950067229 1217479531 455229458 1574949468 397268319 1267289585 995220637 1920919164 501015483 1815262670 1197059269 86947741 1137410885 667368575 733666398 1536581408 611239452 947487746\r\n',
     '259654661\r\n'),
]
SAMPLE = ('3\n1 2 3', '3')


def modulus_part(i, n):
    return reduce(xor, (i % k for k in range(1, n + 1)), 0)


def missing_last_modulus(p):
    n = len(p)
    pre = list(accumulate(range(n), xor))
    total = reduce(xor, p, 0)
    for k in range(1, n):
        if (n // k) & 1:
            total ^= pre[k]
        total ^= pre[n % k]
    return total


def corrupted_zero_prefix(p):
    n = len(p)
    f = list(range(n + 1))
    for i in range(n + 1):
        f[i] ^= f[i - 1]
    total = reduce(xor, p, 0)
    for k in range(1, n + 1):
        total ^= (f[k - 1] ^ f[n % k]) if (n // k) & 1 else f[n % k]
    return total


def summed_q(p):
    n = len(p)
    return sum(v ^ modulus_part(i, n) for i, v in enumerate(p, 1))


def wrapped_negative_index(p):
    n = len(p)
    x = [1] + [0] * (n - 1)
    for i in range(1, n):
        x[i] = x[i - 1] ^ (i + 1)
    total = reduce(xor, p, 0)
    for i in range(n):
        a, r = divmod(n, i + 1)
        total ^= x[r - 1] ^ (x[i - 1] if a % 2 else 0)
    return total


def without_last_q(p):
    n = len(p)
    return recipe.answer('424C', p) ^ p[-1] ^ modulus_part(n, n)


MUTANTS = {
    'k loop stops at n-1 (6473617)': (missing_last_modulus, 10 ** 6),
    'prefix table f[0] overwritten by f[-1]=n (6544288)': (corrupted_zero_prefix, 10 ** 6),
    'q_i combined with + instead of xor (10255184)': (summed_q, 300),
    'X[r-1] wraps to X[-1] when r=0 (29555463)': (wrapped_negative_index, 10 ** 6),
    'upstream text Q stops at q_{n-1}': (without_last_q, 10 ** 6),
}


class ParseTests(unittest.TestCase):
    def test_accepts_official_layouts(self):
        self.assertEqual(recipe.parse('424C', '3\r\n1 2 3\r\n'), [1, 2, 3])
        self.assertEqual(recipe.parse('424C', SAMPLE[0]), [1, 2, 3])
        self.assertEqual(recipe.parse('424C', '1\n2000000000\n'), [2000000000])

    def test_rejects_invalid_inputs(self):
        for text in ['', '3\n', '3\n1 2\n', '3\n1 2 3 4\n', '3\n1\n2\n3\n', '3 1 2 3\n',
                     '0\n\n', '1\n2000000001\n', '1\n-1\n', '1\n+1\n', '1\n01\n', '01\n1\n',
                     '1\n1_0\n', '1\n1.0\n', '2\n1 x\n', '1000001\n' + '0 ' * 1000001 + '\n',
                     '1\n1\n\n']:
            with self.assertRaises(ValueError, msg=repr(text[:40])):
                recipe.parse('424C', text)
        with self.assertRaises(ValueError):
            recipe.parse('424D', '1\n1\n')


class OracleTests(unittest.TestCase):
    def test_official_and_sample(self):
        for text, output in OFFICIAL + [SAMPLE]:
            self.assertEqual(str(recipe.answer('424C', recipe.parse('424C', text))), output.strip())
            self.assertEqual(str(recipe.literal(recipe.parse('424C', text))), output.strip())
        tests = [(f'official/{i}', {'input': t, 'output': o}) for i, (t, o) in enumerate(OFFICIAL, 1)]
        self.assertEqual(recipe.review('424C', tests, [('sample/1', {'input': SAMPLE[0], 'output': SAMPLE[1]})]), [])

    def test_review_reports_disagreement_and_constraint_violation(self):
        failures = recipe.review('424C', [('bad', {'input': '3\n1 2 3\n', 'output': '1\n'}),
                                          ('range', {'input': '1\n2000000001\n', 'output': '0\n'}),
                                          ('layout', {'input': '1\n5\n', 'output': '5\n5\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['bad', 'range', 'layout'])

    def test_prefix_xor_closed_form(self):
        running = 0
        for x in range(5000):
            running ^= x
            self.assertEqual(recipe.prefix_xor(x), running)

    def test_against_literal_double_loop(self):
        rng = random.Random(4240)
        for n in range(1, 80):
            for _ in range(3):
                p = [rng.randint(0, recipe.MAX_P) for _ in range(n)]
                self.assertEqual(recipe.answer('424C', p), recipe.literal(p))

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'424C'})
        self.assertGreaterEqual(counts['424C'], 5000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('424C')

    def test_count_categories_and_determinism(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual({c['category'] for c in self.cases}, {'boundary', 'adversarial', 'maxSize'})
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        again = recipe.extras('424C')
        self.assertEqual([c['input'] for c in again], [c['input'] for c in self.cases])
        self.assertEqual([c['output'] for c in again], [c['output'] for c in self.cases])
        for c in self.cases:
            self.assertEqual(set(c), {'input', 'output', 'reason', 'category'})
            self.assertTrue(c['reason'])

    def test_layout_and_answers(self):
        sizes = []
        for c in self.cases:
            p = recipe.parse('424C', c['input'])
            sizes.append(len(p))
            self.assertEqual(c['input'], f'{len(p)}\n' + ' '.join(map(str, p)) + '\n')
            self.assertRegex(c['output'], r'^(0|[1-9][0-9]*)\n$')
            self.assertEqual(c['output'], f"{recipe.answer('424C', p)}\n")
            if len(p) <= 400:
                self.assertEqual(c['output'], f'{recipe.literal(p)}\n')
        self.assertIn(1, sizes)
        self.assertIn(recipe.MAX_N, sizes)
        self.assertTrue(all(len(recipe.parse('424C', c['input'])) == recipe.MAX_N
                            for c in self.cases if c['category'] == 'maxSize'))
        self.assertIn(recipe.MAX_P, [v for c in self.cases for v in recipe.parse('424C', c['input'])])
        self.assertTrue({n % 4 for n in sizes} == {0, 1, 2, 3})

    def test_wrong_algorithms_are_killed(self):
        for label, (mutant, limit) in MUTANTS.items():
            killed = 0
            for c in self.cases:
                p = recipe.parse('424C', c['input'])
                if len(p) <= limit and str(mutant(p)) != c['output'].strip():
                    killed += 1
            self.assertGreaterEqual(killed, 5, label)


if __name__ == '__main__':
    unittest.main()
