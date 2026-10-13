import unittest

import recipe_603A as recipe


def blocks(bits):
    return 1 + sum(a != b for a, b in zip(bits, bits[1:]))


def runs(bits):
    out = [1]
    for a, b in zip(bits, bits[1:]):
        if a == b:
            out[-1] += 1
        else:
            out.append(1)
    return out


def doubles(bits):
    return sum(a == b for a, b in zip(bits, bits[1:]))


MUTANTS = {
    'max instead of min (14604778)': lambda s: len(s) if len(s) <= 3 else (max(blocks(s) + 2, len(s)) if doubles(s) else blocks(s)),
    'run of three only +1 (14918983)': lambda s: blocks(s) + (2 if sum(r >= 2 for r in runs(s)) >= 2 else 1 if max(runs(s)) >= 3 else 0),
    'no +1 for a single double (26640589)': lambda s: blocks(s) + (2 if doubles(s) >= 2 else 0),
    'single double counted only at an edge (26640717)': lambda s: blocks(s) + (2 if doubles(s) >= 2 else 1 if len(s) >= 2 and (s[0] == s[1] or s[-1] == s[-2]) else 0),
    'transitions without +1 (50697912)': lambda s: min(blocks(s) + 1, len(s)),
    'n minus interior doubles (55384201)': lambda s: len(s) - max(0, sum(s[i] == s[i + 1] for i in range(1, len(s) - 1)) - 2),
    'run of three or edge double (86885894)': lambda s: blocks(s) + (2 if max(runs(s)) >= 3 else 1 if runs(s)[0] == 2 or runs(s)[-1] == 2 else 0),
    'only adjacent long runs +2 (88804396)': lambda s: blocks(s) + (2 if any(a > 1 and b > 1 for a, b in zip(runs(s), runs(s)[1:])) else 1 if max(runs(s)) > 1 else 0),
    'answer is blocks only': blocks,
    'always blocks+2': lambda s: blocks(s) + 2,
}


class Recipe603ATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('603A')

    def test_samples_and_layout(self):
        samples = [('s1', {'input': '8\n10000011\n', 'output': '5\n'}), ('s2', {'input': '2\r\n01\r\n', 'output': '2\r\n'})]
        self.assertEqual(recipe.review('603A', [], samples), [])
        self.assertEqual(recipe.review('603A', [('bad', {'input': '2\n01\n', 'output': '3\n'})], [])[0]['reason'], 'independent oracle disagreement')
        for text in ('2 01\n', '2\n0 1\n', '+2\n01\n', '02\n01\n', '0\n\n', '3\n01\n', '2\n012\n', '2\n01\n1\n', '100001\n' + '0' * 100001 + '\n'):
            with self.assertRaises(ValueError, msg=text):
                recipe.parse('603A', text)

    def test_generated_suite_shape(self):
        self.assertGreaterEqual(len(self.cases), 120)
        self.assertEqual(len({c['input'] for c in self.cases}), len(self.cases))
        self.assertEqual({c['category'] for c in self.cases}, {'boundary', 'adversarial', 'maxSize'})
        lengths = set()
        for case in self.cases:
            bits = recipe.parse('603A', case['input'])
            lines = case['input'].split('\n')
            self.assertEqual(lines, [str(len(bits)), bits, ''])
            self.assertEqual(case['output'], f'{recipe.answer("603A", bits)}\n')
            lengths.add(len(bits))
        self.assertIn(1, lengths)
        self.assertIn(100000, lengths)
        self.assertEqual(recipe.extras('603A'), self.cases)

    def test_small_generated_outputs_match_exhaustive_flip_brute(self):
        checked = 0
        for case in self.cases:
            bits = recipe.parse('603A', case['input'])
            if len(bits) <= 40:
                self.assertEqual(int(case['output']), recipe.brute('603A', bits), bits)
                checked += 1
        self.assertGreater(checked, 100)

    def test_all_generated_outputs_match_independent_flip_dp(self):
        for case in self.cases:
            self.assertEqual(recipe.flip_dp(recipe.parse('603A', case['input'])), int(case['output']))
        for n in range(1, 11):
            for mask in range(1 << n):
                bits = format(mask, f'0{n}b')
                self.assertEqual(recipe.flip_dp(bits), recipe.brute('603A', bits))

    def test_subset_las_agrees_with_dp_las(self):
        for n in range(1, 11):
            for mask in range(1 << n):
                bits = format(mask, f'0{n}b')
                self.assertEqual(recipe.las_subsets(bits), recipe.las_dp(bits))

    def test_each_modeled_wrong_algorithm_is_killed(self):
        for name, mutant in MUTANTS.items():
            killed = [c['reason'] for c in self.cases if mutant(recipe.parse('603A', c['input'])) != int(c['output'])]
            self.assertTrue(killed, name)

    def test_brute_checks(self):
        self.assertGreaterEqual(recipe.brute_checks()['603A'], 8000 + len(self.cases))


if __name__ == '__main__':
    unittest.main()
