from pathlib import Path
import json
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_722C as recipe

PID = '722C'
SAMPLES = [('4\n1 3 2 5\n3 4 1 2', '5\n4\n3\n0'), ('5\n1 2 3 4 5\n4 2 3 5 1', '6\n5\n5\n1\n0'),
           ('8\n5 5 4 4 6 6 5 5\n5 2 8 7 1 3 4 6', '18\n16\n11\n8\n8\n6\n6\n0')]
OFFICIAL_SAMPLE_CRLF = ('4\r\n1 3 2 5\r\n3 4 1 2\r\n', '5\r\n4\r\n3\r\n0\r\n')
OFFICIAL_17 = ('17\r\n12 9 17 5 0 6 5 1 3 1 17 17 2 14 5 1 17\r\n3 7 5 8 12 9 15 13 11 14 6 16 17 1 10 2 4\r\n',
               '94\r\n78\r\n78\r\n77\r\n39\r\n39\r\n21\r\n21\r\n21\r\n21\r\n21\r\n21\r\n21\r\n9\r\n9\r\n5\r\n0\r\n')


def kadane_sentinel(data):
    values, order = data
    arr = list(values)
    out = []
    for position in order[:-1]:
        arr[position - 1] = -512
        best = cur = 0
        for v in arr:
            cur = max(0, cur + v)
            best = max(best, cur)
        out.append(best)
    return out + [0]


def dsu_neighbour_value(data):
    values, order = data
    n = len(values)
    aa = [0, *values, 0]
    clusters = [0] * (n + 2)

    def find(x):
        while clusters[x] != x:
            x = clusters[x]
        return x

    best = 0
    res = []
    for a in reversed(order):
        res.append(best)
        clusters[a] = a
        for i in (a - 1, a + 1):
            if clusters[i]:
                j = find(i)
                aa[a] += aa[i]
                clusters[i] = clusters[j] = a
        best = max(best, aa[a])
    return res[::-1]


def digit_split(data):
    values, order = data
    arr = list(values)
    out = []
    for position in order:
        arr[position - 1] = 0
        pieces = ''.join(map(str, arr)).split('0')
        out.append(max(sum(map(int, piece)) for piece in pieces))
    return out


def zero_sentinel_no_tail(data):
    values, order = data
    arr = list(values)
    out = []
    for position in order:
        arr[position - 1] = 0
        sums, run = [], 0
        for v in arr:
            if v == 0:
                sums.append(run)
                run = 0
            else:
                run += v
        out.append(max(sums))
    return out


def zero_sentinel(data):
    values, order = data
    arr = list(values)
    out = []
    for position in order:
        arr[position - 1] = 0
        best = run = 0
        for v in arr:
            run = 0 if v == 0 else run + v
            best = max(best, run)
        out.append(best)
    return out


def multiset_erase_all(data):
    values, order = data
    n = len(values)
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    cuts = [0, n + 1]
    sums = {prefix[n]: 1}
    out = []
    for position in order:
        k = next(i for i, c in enumerate(cuts) if c > position)
        left, right = cuts[k - 1], cuts[k]
        cuts.insert(k, position)
        sums.pop(prefix[right - 1] - prefix[left], None)
        for s in (prefix[position - 1] - prefix[left], prefix[right - 1] - prefix[position]):
            sums[s] = sums.get(s, 0) + 1
        out.append(max(sums))
    return out


def last_split_only(data):
    values, order = data
    n = len(values)
    prefix = [0]
    for v in values:
        prefix.append(prefix[-1] + v)
    cuts = [0, n + 1]
    out = []
    for position in order:
        k = next(i for i, c in enumerate(cuts) if c > position)
        left, right = cuts[k - 1], cuts[k]
        cuts.insert(k, position)
        out.append(max(prefix[position - 1] - prefix[left], prefix[right - 1] - prefix[position]))
    return out


def int32_wrap(data):
    return [(x + 2 ** 31) % 2 ** 32 - 2 ** 31 for x in recipe.answer(PID, data)]


MUTANTS = {'kadane_sentinel': kadane_sentinel, 'dsu_neighbour_value': dsu_neighbour_value, 'digit_split': digit_split,
           'zero_sentinel_no_tail': zero_sentinel_no_tail, 'zero_sentinel': zero_sentinel,
           'multiset_erase_all': multiset_erase_all, 'last_split_only': last_split_only, 'int32_wrap': int32_wrap}


class LayoutTests(unittest.TestCase):
    def test_accepts_lf_crlf_and_missing_final_newline(self):
        expected = ([1, 3, 2, 5], [3, 4, 1, 2])
        self.assertEqual(recipe.parse(PID, SAMPLES[0][0]), expected)
        self.assertEqual(recipe.parse(PID, OFFICIAL_SAMPLE_CRLF[0]), expected)

    def test_rejects_bad_layout_arity_ranges_and_permutations(self):
        bad = ['', '0\n\n\n', '100001\n1\n1\n', '1\n1\n', '1\n1 1\n', '1 1\n1\n', '2\n1 2 1 2\n', '2\n1\n2\n1 2\n',
               '2\n1 2\n1\n2\n', '2\n1 2\n1 1\n', '2\n1 2\n0 1\n', '2\n1 2\n2 3\n', '1\n1000000001\n1\n', '1\n-1\n1\n',
               '1\n01\n1\n', '1\n+1\n1\n', '1\nx\n1\n', '1\n1\n1\n\n', '\n1\n1\n1\n', '2\n1 2\n1 2 3\n', '1\n1\n1 1\n']
        for text in bad:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse(PID, text)


class OracleTests(unittest.TestCase):
    def test_samples_and_official_pairs(self):
        tests = [('0001', {'input': OFFICIAL_SAMPLE_CRLF[0], 'output': OFFICIAL_SAMPLE_CRLF[1]}),
                 ('0005', {'input': OFFICIAL_17[0], 'output': OFFICIAL_17[1]})]
        samples = [(f's{i}', {'input': i_, 'output': o}) for i, (i_, o) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review(PID, tests, samples), [])

    def test_review_reports_disagreement_layout_and_invalid_input(self):
        failures = recipe.review(PID, [('a', {'input': '1\n5\n1\n', 'output': '5\n'}),
                                       ('b', {'input': '2\n1 2\n1 1\n', 'output': '0\n0\n'}),
                                       ('c', {'input': '2\n1 2\n1 2\n', 'output': '2 0\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['a', 'b', 'c'])
        self.assertEqual(failures[0]['expected'], ['0'])
        self.assertIn('layout', failures[2]['reason'])

    def test_brutes_agree_on_official_pairs(self):
        for text, out in [*SAMPLES, OFFICIAL_17]:
            data = recipe.parse(PID, text)
            expected = list(map(int, out.split()))
            self.assertEqual(recipe.brute_scan(data), expected)
            self.assertEqual(recipe.brute_segments(data), expected)
            self.assertEqual(recipe.forward_tree(data), expected)

    def test_mutants_reproduce_recorded_failures_on_row_tests(self):
        data = recipe.parse(PID, SAMPLES[0][0])
        self.assertNotEqual(zero_sentinel_no_tail(data), recipe.answer(PID, data))
        data = recipe.parse(PID, OFFICIAL_17[0])
        self.assertNotEqual(digit_split(data), recipe.answer(PID, data))
        self.assertNotEqual(zero_sentinel(data), recipe.answer(PID, data))
        for text, _ in SAMPLES:
            data = recipe.parse(PID, text)
            for wrong in (kadane_sentinel, digit_split, zero_sentinel, multiset_erase_all, int32_wrap):
                self.assertEqual(wrong(data), recipe.answer(PID, data), wrong.__name__)

    def test_brute_checks_are_real(self):
        result = recipe.brute_checks()
        self.assertEqual(set(result), {PID})
        self.assertGreater(result[PID], 60000)


class ExtrasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)
        cls.parsed = [recipe.parse(PID, c['input']) for c in cls.cases]

    def test_layout_answers_and_counts(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertLessEqual(len(self.cases), 180)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        for case, data in zip(self.cases, self.parsed):
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
            lines = case['input'].split('\n')
            n = len(data[0])
            self.assertEqual(len(lines), 4)
            self.assertEqual(lines[3], '')
            self.assertEqual(lines[0], str(n))
            self.assertEqual([len(lines[1].split(' ')), len(lines[2].split(' '))], [n, n])
            out_lines = case['output'].split('\n')
            self.assertEqual(len(out_lines), n + 1)
            self.assertEqual(out_lines[-1], '')
            self.assertEqual(out_lines[:-1], [str(x) for x in recipe.answer(PID, data)])
            self.assertEqual(out_lines[:-1], [str(x) for x in recipe.forward_tree(data)])
            if n <= 1000:
                self.assertEqual(out_lines[:-1], [str(x) for x in recipe.brute_scan(data)])
            if n <= 10:
                self.assertEqual(out_lines[:-1], [str(x) for x in recipe.brute_segments(data)])
        self.assertEqual(recipe.extras(PID), self.cases)
        self.assertEqual(json.dumps(recipe.extras(PID)), json.dumps(self.cases))

    def test_extremes_present(self):
        sizes = [len(v) for v, _ in self.parsed]
        self.assertIn(1, sizes)
        self.assertGreaterEqual(sizes.count(recipe.MAX_N), 3)
        self.assertTrue(any(min(v) == max(v) == recipe.MAX_A and len(v) == recipe.MAX_N for v, _ in self.parsed))
        outputs = [int(c['output'].split('\n')[0]) for c in self.cases]
        self.assertEqual(max(outputs), (recipe.MAX_N - 1) * recipe.MAX_A)
        self.assertIn(0, outputs)

    def test_labelled_cases_kill_their_mutants(self):
        labels = {'sentinels split 1 0 1': zero_sentinel, 'string split on "0"': digit_split,
                  'Kadane gives 1488': kadane_sentinel, 'neighbour value instead of its root total': dsu_neighbour_value,
                  'erasing a multiset value removes both': multiset_erase_all, 'multiset erase-by-value': multiset_erase_all,
                  'not one of the two halves just split': last_split_only, 'reaches the array end': zero_sentinel_no_tail,
                  'exceeds signed 32-bit': int32_wrap, 'exceed unsigned 32-bit': int32_wrap,
                  'zero inside the surviving run': zero_sentinel, 'sentinel solutions undercount': zero_sentinel}
        for fragment, wrong in labels.items():
            matching = [d for c, d in zip(self.cases, self.parsed) if fragment in c['reason']]
            with self.subTest(fragment=fragment):
                self.assertEqual(len(matching), 1)
                self.assertNotEqual(wrong(matching[0]), recipe.answer(PID, matching[0]))

    def test_every_mutant_is_killed(self):
        small = [d for d in self.parsed if len(d[0]) <= 1000]
        for name, wrong in MUTANTS.items():
            with self.subTest(wrong=name):
                self.assertTrue(any(wrong(d) != recipe.answer(PID, d) for d in small))


if __name__ == '__main__':
    unittest.main()
