from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_73A as recipe

PID = '73A'
SAMPLES = [('2 2 2 3', '8'), ('2 2 2 1', '2')]
OFFICIAL = [
    ('2 2 2 3\r\n', '8'), ('2 2 2 1\r\n', '2'), ('1 1 1 1\r\n', '1'), ('1 2 3 3\r\n', '6'), ('20 4 5 12\r\n', '120'),
    ('100 500 100500 1000000000\r\n', '5025000000'), ('2 5 5 9\r\n', '50'), ('11 1 11 11\r\n', '42'),
    ('100500 5000 500 100000000\r\n', '251250000000'), ('2 2 2 0\r\n', '1'),
    ('1000000 1000000 1000000 2444441\r\n', '540974149875309150'),
    ('1000000 1000000 1000000 1000000000\r\n', '1000000000000000000'),
    ('1000000 1000000 1000000 2999996\r\n', '999999000000000000'),
    ('1000000 1000000 1000000 2999997\r\n', '1000000000000000000'),
    ('999999 1000000 999997 999999999\r\n', '999996000003000000'),
    ('500000 1000000 750000 100000\r\n', '37040370459260'), ('999999 1 999998 1333333\r\n', '444445555556'),
    ('500000 10000 1000000 29998\r\n', '1000100000000'), ('10000 500000 1000000 29999\r\n', '1000200010000'),
    ('10000 1000000 500000 29996\r\n', '999900000000'), ('999999 123456 987654 0\r\n', '1'), ('1 1 1 0\r\n', '1'),
    ('219482 801483 941695 280976\r\n', '821595067700400'), ('808994 288453 204353 580644\r\n', '7250580779648149'),
    ('428676 64403 677407 626161\r\n', '5081000961597840'), ('559002 326875 150818 157621\r\n', '145045169133102'),
    ('178008 590076 624581 201286\r\n', '302062187173952'), ('797745 854005 98703 735186\r\n', '9996502351557447'),
    ('418223 118667 573175 776998\r\n', '12857677898465963'), ('39436 384053 48008 313346\r\n', '427693170156640'),
    ('661377 149342 523189 353305\r\n', '1633415415004970'),
    ('781081 414037 495753 892089\r\n', '26294515330164544'),
    ('402353 679460 969495 930195\r\n', '29810031851367496'),
    ('593408 709898 624186 915570\r\n', '28425961712082871'), ('1000 988 1000000 3000\r\n', '1002820000'),
    ('91839 2 3 50\r\n', '288'), ('999900 999990 4 129\r\n', '16384'), ('1024 100000 4 13\r\n', '144'),
    ('1000000 1000000 1000000 1000000000\r\n', '1000000000000000000'), ('1 1000000 1 1000000000\r\n', '1000000'),
    ('2 1000 1000000 1000000000\r\n', '2000000000'), ('999999 2 1000000 1000000000\r\n', '1999998000000'),
    ('1000 1 1 1\r\n', '2'), ('1000 1 1 998\r\n', '999'), ('1000 1 1 1000\r\n', '1000'),
    ('33334 66667 1000000 100000\r\n', '37040370459260'), ('1 1000000 2 23123\r\n', '46246'),
]


def m14407647(x, y, z, k):
    sides = sorted([x, y, z])
    product = 1
    for i in reversed(range(3)):
        a = min(sides[i] - 1, k // (i + 1))
        k -= a
        product *= a + 1
    return [product]


def m14927908(x, y, z, k):
    out = []
    if k == 1:
        out.append(2)
    if k == 2:
        out.append(4)
    if k == 3:
        out.append(8)
    if k > (x - 1) + (y - 1) + (z - 1):
        out.append(x * y * z)
    if 3 < k <= (x - 1) + (y - 1) + (z - 1):
        out.append(4 * k - 4)
    return out


def m26485196(x, y, z, k):
    dim = sorted([x, y, z])
    ans = [0, 0, 0]
    for i in range(3):
        dimi = dim[i]
        if dimi * (3 - i) <= k:
            k -= dimi * (3 - i)
            for j in range(i, 3):
                ans[j] += dimi
            for j in range(3):
                dim[j] -= dimi
        else:
            for j in range(i, 3):
                ans[j] += k // (3 - i)
            for j in range(i, k % (3 - i)):
                ans[j] += 1
            break
    product = 1
    for v in ans:
        product *= v + 1
    return [product]


def m27476502(x, y, z, k):
    x, y, z = sorted([x, y, z])
    x = min(k // 3 + 1, x)
    y = min((k - x + 1) // 2 + 2, y)
    z = min(k - x - y + 3, z)
    return [x * y * z]


def m34780255(x, y, z, k):
    w = x + y + z - 3
    resp = 1
    while w > 0 and k > 0:
        resp *= 2
        w -= 1
        k -= 1
    return [resp]


def m43416779(x, y, z, k):
    c = [1, 1, 1]
    for i in range(k):
        c[i % 3] += 1
    return [c[0] * c[1] * c[2]]


def m43418008(x, y, z, k):
    a = b = c = 1
    for _ in range(k):
        if a < x:
            a += 1
        if b < y:
            b += 1
        if c < z:
            c += 1
    return [a * b * c]


def m49807273(text):
    k = int(text.splitlines()[0][6])
    ans = 1
    for i in range(3):
        a = k // 3 + (1 if i < k % 3 else 0)
        ans *= a + 1
    return [ans]


def m58111838(x, y, z, k):
    return [2 ** k]


def m58118698(x, y, z, k):
    return [2 ** k if 2 ** k <= x * y * z else x * y * z]


def m58118761(x, y, z, k):
    return [x ** k]


def m86757103(x, y, z, k):
    a = [0, 0, 0]
    caps = (x, y, z)
    while sum(a) != k:
        if all(a[i] >= caps[i] for i in range(3)):
            return ['<hang>']
        for i in range(3):
            if a[i] < caps[i]:
                a[i] += 1
            if sum(a) == k:
                break
    return [(a[0] + 1) * (a[1] + 1) * (a[2] + 1)]


def m87220102(x, y, z, k):
    if x == y == z == 1:
        return [1]
    s = sorted([x, y, z])
    if s[0] == s[1] == 1:
        return [k + 1]
    if s[0] == 1:
        return [k * 2]
    return [k ** 2]


def m89876096(x, y, z, k):
    return [8]


def m143630229(x, y, z, k):
    x, y, z = sorted([x, y, z])
    d = x + y + z - 3 - k
    if d <= 0:
        return [x * y * z]
    e, c = divmod(d, 3)
    x1, y1, z1 = x - e, y - e, z - e
    if c > 0:
        x1 -= 1
    if c > 1:
        y1 -= 1
    return [x1 * y1 * z1]


def round_robin_372737(x, y, z, k):
    a, b, c = x, y, z
    na = nb = nc = 1
    while a > 1 or b > 1 or c > 1:
        if k == 0:
            break
        if a > 1 and k > 0:
            a, na, k = a - 1, na + 1, k - 1
        if b > 1 and k > 0:
            b, nb, k = b - 1, nb + 1, k - 1
        if c > 1 and k > 0:
            c, nc, k = c - 1, nc + 1, k - 1
    return [na * nb * nc]


def unsorted_greedy(x, y, z, k):
    a = min(x - 1, k // 3)
    b = min(y - 1, (k - a) // 2)
    c = min(z - 1, k - a - b)
    return [(a + 1) * (b + 1) * (c + 1)]


def no_rebalance(x, y, z, k):
    product = 1
    for side in (x, y, z):
        product *= min(side - 1, k // 3) + 1
    return [product]


def int32_product(x, y, z, k):
    value = recipe.answer(PID, (x, y, z, k)) % 2 ** 32
    return [value - 2 ** 32 if value >= 2 ** 31 else value]


WA_MUTANTS = [
    (m14407647, 3), (m14927908, 2), (m26485196, 2), (m27476502, 9), (m34780255, 3), (m43416779, 2),
    (m43418008, 1), (m58111838, 2), (m58118698, 4), (m58118761, 3), (m86757103, 2), (m87220102, 0),
    (m89876096, 1), (m143630229, 4),
]
SLOW = {m43416779, m43418008, m86757103, round_robin_372737}
EXPONENTIAL = {m34780255, m58111838, m58118698, m58118761}


def tokens(values):
    return [str(v) for v in values]


class LayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        for text in ('2 2 2 3', '2 2 2 3\n', '2 2 2 3\r\n', ' 2 2  2 3 \n'):
            self.assertEqual(recipe.parse(PID, text), (2, 2, 2, 3))

    def test_rejects_bad_layout_arity_and_ranges(self):
        bad = ['', '\n', '2 2 2\n', '2 2 2 3 4\n', '2 2\n2 3\n', '2 2 2 3\n\n', '\n2 2 2 3\n', '0 2 2 3\n',
               '2 0 2 3\n', '2 2 0 3\n', '1000001 1 1 0\n', '1 1000001 1 0\n', '1 1 1000001 0\n',
               '1 1 1 1000000001\n', '1 1 1 -1\n', '01 1 1 0\n', '1 1 1 x\n', '1.0 1 1 0\n', '+1 1 1 0\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse(PID, text)
        self.assertEqual(recipe.parse(PID, '1000000 1000000 1000000 1000000000\n'), (10 ** 6, 10 ** 6, 10 ** 6, 10 ** 9))


class OracleTests(unittest.TestCase):
    def test_samples_and_official_pairs(self):
        self.assertEqual(len(OFFICIAL), 47)
        tests = [(f'{i:04d}', {'input': i_, 'output': o}) for i, (i_, o) in enumerate(OFFICIAL, 1)]
        samples = [(f's{i}', {'input': i_, 'output': o}) for i, (i_, o) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review(PID, tests, samples), [])

    def test_official_pairs_match_brute_scan(self):
        for text, out in OFFICIAL:
            x, y, z, k = recipe.parse(PID, text)
            s = sorted((x, y, z))
            self.assertEqual(recipe.brute_scan((s[0], s[1], s[2], k)), int(out), text)

    def test_review_reports_disagreement_and_invalid_input(self):
        failures = recipe.review(PID, [('a', {'input': '2 2 2 3\n', 'output': '9\n'}),
                                       ('b', {'input': '0 2 2 3\n', 'output': '1\n'}),
                                       ('c', {'input': '2 2 2 3\n', 'output': '8\n8\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b', 'c'])
        self.assertEqual(failures[0]['expected'], ['8'])

    def test_hand_values(self):
        cases = {(2, 2, 2, 3): 8, (1, 2, 3, 3): 6, (2, 5, 5, 9): 50, (1, 1, 1, 10 ** 9): 1,
                 (10 ** 6, 10 ** 6, 10 ** 6, 10 ** 9): 10 ** 18, (10 ** 6, 10 ** 6, 10 ** 6, 2999996): 999999 * 10 ** 12,
                 (2, 1000, 1000, 4): 2 * 2 * 3, (3, 3, 1000, 100): 9 * 97}
        for data, expected in cases.items():
            self.assertEqual(recipe.answer(PID, data), expected, data)
            if max(data[:3]) <= 1000 and data[3] <= 1000:
                self.assertEqual(recipe.brute_exhaustive(data), expected, data)

    def test_brute_checks_are_real(self):
        result = recipe.brute_checks()
        self.assertEqual(set(result), {PID})
        self.assertGreater(result[PID], 20000)


class SelectedSourceMutantTests(unittest.TestCase):
    def run_mutant(self, mutant, text):
        if mutant is m49807273:
            return tokens(mutant(text))
        return tokens(mutant(*recipe.parse(PID, text)))

    def test_mutants_pass_prefix_and_fail_next_official_test(self):
        for mutant, passed in WA_MUTANTS + [(m49807273, 2)]:
            with self.subTest(mutant=mutant.__name__):
                for text, out in OFFICIAL[:passed]:
                    self.assertEqual(self.run_mutant(mutant, text), out.split(), text)
                text, out = OFFICIAL[passed]
                self.assertNotEqual(self.run_mutant(mutant, text), out.split(), text)

    def test_accepted_round_robin_agrees(self):
        for text, out in OFFICIAL:
            x, y, z, k = recipe.parse(PID, text)
            if min(k, x + y + z) <= 300000:
                self.assertEqual(round_robin_372737(x, y, z, k), [int(out)], text)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)
        cls.parsed = [recipe.parse(PID, c['input']) for c in cls.cases]

    def test_layout_answers_and_counts(self):
        cases = self.cases
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        official_inputs = {recipe.parse(PID, t) for t, _ in OFFICIAL}
        for case, data in zip(cases, self.parsed):
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            self.assertTrue(case['reason'])
            self.assertRegex(case['input'], r'\A[1-9][0-9]* [1-9][0-9]* [1-9][0-9]* (0|[1-9][0-9]*)\n\Z')
            self.assertRegex(case['output'], r'\A[1-9][0-9]*\n\Z')
            self.assertEqual(case['output'], f'{recipe.answer(PID, data)}\n')
            self.assertLessEqual(int(case['output']), 10 ** 18)
        self.assertGreater(len(set(self.parsed) - official_inputs), 120)
        self.assertEqual(recipe.extras(PID), cases)

    def test_every_extra_matches_independent_brutes(self):
        exhaustive = 0
        for case, (x, y, z, k) in zip(self.cases, self.parsed):
            s = sorted((x, y, z))
            self.assertEqual(recipe.brute_scan((s[0], s[1], s[2], k)), int(case['output']), case['input'])
            if x * y * z <= 20000 and k <= 200:
                self.assertEqual(recipe.brute_exhaustive((x, y, z, k)), int(case['output']), case['input'])
                exhaustive += 1
        self.assertGreater(exhaustive, 60)

    def test_extremes_present(self):
        parsed = set(self.parsed)
        m = recipe.MAX_SIDE
        self.assertIn((1, 1, 1, 0), parsed)
        self.assertIn((m, m, m, recipe.MAX_K), parsed)
        self.assertIn((m, m, m, 0), parsed)
        self.assertIn((1, 1, 1, recipe.MAX_K), parsed)
        self.assertIn('1000000000000000000\n', {c['output'] for c in self.cases})
        self.assertGreaterEqual(sum(c['category'] == 'maxSize' for c in self.cases), 10)

    def test_extras_kill_selected_wrong_sources_and_known_bugs(self):
        mutants = [m for m, _ in WA_MUTANTS] + [unsorted_greedy, no_rebalance, int32_product]
        for mutant in mutants:
            with self.subTest(mutant=mutant.__name__):
                killed = 0
                for case, data in zip(self.cases, self.parsed):
                    if mutant in SLOW and data[3] > 10 ** 5:
                        continue
                    if mutant in EXPONENTIAL and data[3] > 2000:
                        continue
                    if tokens(mutant(*data)) != case['output'].split():
                        killed += 1
                self.assertGreater(killed, 0)

    def test_extras_agree_with_accepted_round_robin(self):
        checked = 0
        for case, data in zip(self.cases, self.parsed):
            if min(data[3], sum(data[:3])) <= 100000:
                self.assertEqual(tokens(round_robin_372737(*data)), case['output'].split(), case['input'])
                checked += 1
        self.assertGreater(checked, 100)

    def test_labels_are_true(self):
        for case, data in zip(self.cases, self.parsed):
            if 'largest-first' in case['reason']:
                self.assertEqual((m14407647(*data), int(case['output'])), ([4], 6))
            if 'exceeds 32-bit' in case['reason'] or '32-bit with uncapped' in case['reason'] or 'just above 2^31' in case['reason']:
                self.assertNotEqual(int32_product(*data), [int(case['output'])], case['input'])
            if 'just below 2^31' in case['reason']:
                self.assertEqual(int32_product(*data), [int(case['output'])])
            if 'greedy must sort' in case['reason'] and data[3] >= 6:
                self.assertNotEqual(unsorted_greedy(*data), [int(case['output'])], case['input'])


if __name__ == '__main__':
    unittest.main()
