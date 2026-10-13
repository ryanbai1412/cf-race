from pathlib import Path
import math
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_269A as recipe

PID = '269A'
SAMPLES = [('2\n0 3\n1 5', '3'), ('1\n0 4', '1'), ('2\n1 10\n2 2', '3')]
OFFICIAL = [
    ('1\r\n0 1\r\n', '1\r\n'), ('1\r\n1000000000 1000000000\r\n', '1000000015\r\n'), ('1\r\n0 16\r\n', '2\r\n'),
    ('1\r\n0 17\r\n', '3\r\n'), ('3\r\n0 64\r\n1 16\r\n2 4\r\n', '3\r\n'), ('2\r\n0 13\r\n1 1\r\n', '2\r\n'),
    ('1\r\n0 268435456\r\n', '14\r\n'), ('1\r\n0 268435457\r\n', '15\r\n'), ('2\r\n21 134217728\r\n1 1024\r\n', '35\r\n'),
    ('2\r\n10 3\r\n25 747\r\n', '30\r\n'), ('2\r\n0 16777216\r\n16 1\r\n', '17\r\n'),
]


def area_sum(boxes):
    total = sum(4 ** k * a for k, a in boxes)
    s = 0
    while 4 ** s < total:
        s += 1
    return s


def float_log(boxes):
    return max(k + math.ceil(math.log(a, 4)) for k, a in boxes)


def floor_l4(boxes):
    def l4(x):
        r = 1
        while x > 4:
            r += 1
            x //= 4
        return r
    return max(k + l4(a) for k, a in boxes)


def carry_without_final_level(boxes):
    m = b = 0
    for k, a in sorted(boxes):
        b = max(a, -(-b // 4 ** (k - m)))
        m = k
    while b > 1:
        b = -(-b // 4)
        m += 1
    return m


def sum_carry(boxes):
    counts = dict(boxes)
    need = 0
    for level in range(min(counts), max(counts) + 1):
        need = counts.get(level, 0) + -(-need // 4)
    p = max(counts) + 1
    need = -(-need // 4)
    while need > 1:
        need = -(-need // 4)
        p += 1
    return p


class LayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        self.assertEqual(recipe.parse(PID, '2\n0 3\n1 5'), [(0, 3), (1, 5)])
        self.assertEqual(recipe.parse(PID, '2\r\n0 3\r\n1 5\r\n'), [(0, 3), (1, 5)])

    def test_rejects_bad_layout_arity_ranges_and_duplicates(self):
        bad = ['', '0\n', '100001\n', '1\n', '2\n0 3\n', '1\n0 3\n1 5\n', '1\n0\n', '1\n0 3 4\n', '2\n0 3 1 5\n',
               '1 0 3\n', '1\n0 0\n', '1\n1000000001 1\n', '1\n0 1000000001\n', '1\n-1 2\n', '2\n4 1\n4 2\n',
               '1\n01 2\n', '1\n0 x\n', '1\n\n0 1\n', '1\n0 1\n\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse(PID, text)


class OracleTests(unittest.TestCase):
    def test_samples_and_official_pairs(self):
        tests = [(f'{i:04d}', {'input': i_, 'output': o}) for i, (i_, o) in enumerate(OFFICIAL, 1)]
        samples = [(f's{i}', {'input': i_, 'output': o}) for i, (i_, o) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review(PID, tests, samples), [])

    def test_review_reports_disagreement_and_invalid_input(self):
        failures = recipe.review(PID, [('a', {'input': '1\n0 4\n', 'output': '2\n'}), ('b', {'input': '1\n0 0\n', 'output': '1\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b'])
        self.assertEqual(failures[0]['expected'], ['1'])

    def test_power_of_four_boundaries(self):
        for m in range(1, 16):
            for a, levels in ((4 ** m - 1, m), (4 ** m, m), (4 ** m + 1, m + 1)):
                if a <= recipe.MAX_A:
                    self.assertEqual(recipe.answer(PID, [(0, a)]), max(1, levels), a)
        self.assertEqual(recipe.answer(PID, [(0, 1)]), 1)

    def test_brute_checks_are_real(self):
        result = recipe.brute_checks()
        self.assertEqual(set(result), {PID})
        self.assertGreater(result[PID], 100000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)

    def test_layout_answers_and_counts(self):
        cases = self.cases
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            lines = case['input'].split('\n')
            self.assertEqual(lines[-1], '')
            n = int(lines[0])
            self.assertEqual(len(lines), n + 2)
            self.assertTrue(all(len(line.split(' ')) == 2 for line in lines[1:-1]))
            boxes = recipe.parse(PID, case['input'])
            self.assertEqual(case['output'], f'{recipe.answer(PID, boxes)}\n')
            if max(k for k, _ in boxes) < 60:
                self.assertEqual(case['output'], f'{recipe.brute_carry(boxes)}\n')
        self.assertEqual(recipe.extras(PID), cases)

    def test_extremes_present(self):
        parsed = [recipe.parse(PID, c['input']) for c in self.cases]
        self.assertIn([(0, 1)], parsed)
        self.assertTrue(any(len(b) == recipe.MAX_N for b in parsed))
        self.assertTrue(any(max(k for k, _ in b) == recipe.MAX_K for b in parsed))
        self.assertTrue(any(max(a for _, a in b) == recipe.MAX_A for b in parsed))
        self.assertIn('1000000015\n', {c['output'] for c in self.cases})

    def test_wrong_algorithms_are_killed(self):
        small = [recipe.parse(PID, c['input']) for c in self.cases if len(c['input']) < 5000]
        small = [b for b in small if max(k for k, _ in b) < 1000]
        for wrong in (area_sum, float_log, floor_l4, carry_without_final_level, sum_carry):
            with self.subTest(wrong=wrong.__name__):
                self.assertTrue(any(wrong(b) != recipe.answer(PID, b) for b in small))


if __name__ == '__main__':
    unittest.main()
