from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_154A as recipe


OFFICIAL = [
    ('ababa\r\n1\r\nab\r\n', '2'),
    ('codeforces\r\n2\r\ndo\r\ncs\r\n', '1'),
    ('nllnrlrnll\r\n1\r\nrl\r\n', '1'),
    ('aludfbjtwnkgnfl\r\n1\r\noy\r\n', '0'),
    ('pgpgppgggpbbnnn\r\n2\r\npg\r\nnb\r\n', '7'),
    ('eepeeeeppppppeepeppe\r\n1\r\npe\r\n', '10'),
    ('vefneyamdzoytemupniw\r\n13\r\nve\r\nfg\r\noi\r\nan\r\nck\r\nwx\r\npq\r\nml\r\nbt\r\nud\r\nrz\r\nsj\r\nhy\r\n', '1'),
    ('drvwfaacccwnncfwuptsorrrvvvrgdzytrwweeexzyyyxuwuuk\r\n13\r\nld\r\nac\r\nnp\r\nrv\r\nmo\r\njh\r\ngb\r\nuw\r\nfq\r\nst\r\nkx\r\nzy\r\nei\r\n', '11'),
    ('pninnihzipirpbdggrdglzdpbldtzihgbzdnrgznbpdanhnlag\r\n4\r\nli\r\nqh\r\nad\r\nbp\r\n', '4'),
    ('mbmxuuuuxuuuuhhooooxxxuxxxuxuuxuuuxxjvjvjjjjvvvjjjjjvvjvjjjvvvjjvjjvvvjjjvjvvjvjjjjjmmbmbbbbbmbbbbmm\r\n5\r\nmb\r\nho\r\nxu\r\njv\r\nyp\r\n', '37'),
    ('z\r\n0\r\n', '0'),
    ('t\r\n13\r\nzx\r\nig\r\nyq\r\nbd\r\nph\r\nar\r\nne\r\nwo\r\ntk\r\njl\r\ncv\r\nfs\r\nmu\r\n', '0'),
    ('rbnxovfcwkdjctdjfskaozjzthlcntuaoiavnbsfpuzxyvhfbxetvryvwrqetokdshadxpxijtpkrqvghsrejgnqntwiypiglzmp\r\n13\r\njr\r\nnf\r\nyk\r\ntq\r\nwe\r\nil\r\ngu\r\npb\r\naz\r\nxm\r\nhc\r\nvd\r\nso\r\n', '0'),
    ('yynynnyyyiynyniiiinyynniiyiyyyniyniyynyyyynyynnniiiniyyniiyyiynyiynnnnyiiyiyniyyininiyiiiyynnnyiyinnnnyiinnnnnyninyinyynynyiynyyyiyinyynnyyinynyinininyniniynniiyyiiyy\r\n1\r\nni\r\n', '28'),
    ('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\r\n1\r\nab\r\n', '75'),
]


class ParseTests(unittest.TestCase):
    def test_accepts_crlf_and_lf_layouts(self):
        self.assertEqual(recipe.parse('154A', 'ababa\n1\nab\n'), ('ababa', ('ab',)))
        self.assertEqual(recipe.parse('154A', 'ababa\r\n1\r\nab\r\n'), ('ababa', ('ab',)))
        self.assertEqual(recipe.parse('154A', 'z\n0\n'), ('z', ()))
        self.assertEqual(recipe.parse('154A', 'a' * 100000 + '\n0\n')[0], 'a' * 100000)

    def test_rejects_malformed_inputs(self):
        bad = ['', 'ab\n', '\n0\n', 'aB\n0\n', 'a b\n0\n', 'ab \n0\n', 'a' * 100001 + '\n0\n',
               'ab\n14\n' + ''.join(chr(97 + i) + chr(98 + i) + '\n' for i in range(0, 28, 2)),
               'ab\n-1\n', 'ab\n01\nab\n', 'ab\n1\n', 'ab\n1\nab\ncd\n', 'ab\n2\nab cd\n', 'ab\n1\naa\n',
               'ab\n2\nab\nbc\n', 'ab\n1\nabc\n', 'ab\n1\na\n', 'ab\n1\nAB\n', 'ab 1\nab\n', 'ab\n0\n\n']
        for text in bad:
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse('154A', text)


class OracleTests(unittest.TestCase):
    def test_hand_derived_answers(self):
        cases = {('abz', ('ab',)): 1, ('aab', ('ab',)): 1, ('aaab', ('ab',)): 1, ('abba', ('ab',)): 2,
                 ('abxab', ('ab',)): 2, ('abcd', ('ab', 'cd')): 2, ('acbd', ('ab', 'cd')): 0,
                 ('aaaaabbbbbaaaaa', ('ab',)): 5, ('ab', ()): 0, ('aa', ('ab',)): 0}
        for data, expected in cases.items():
            self.assertEqual(recipe.answer('154A', data), expected, data)
            self.assertEqual(recipe.exhaustive(data), expected, data)
            self.assertEqual(recipe.last_kept_dp(data), expected, data)

    def test_official_pairs(self):
        tests = [(f'{i:04d}', {'input': text, 'output': out + '\r\n'}) for i, (text, out) in enumerate(OFFICIAL, 1)]
        self.assertEqual(recipe.review('154A', tests, []), [])
        self.assertEqual(len(tests), 15)

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review('154A', [('0001', {'input': 'ab\n1\nab\n', 'output': '0\n'}),
                                          ('0002', {'input': 'ab\n1\naa\n', 'output': '0\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['0001', '0002'])
        self.assertEqual(failures[0]['expected'], ['1'])

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'154A'})
        self.assertGreaterEqual(counts['154A'], 50000)


class ExtrasTests(unittest.TestCase):
    def test_generated_cases_are_valid_and_independently_correct(self):
        cases = recipe.extras('154A')
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        self.assertEqual({c['category'] for c in cases}, {'boundary', 'adversarial', 'maxSize'})
        self.assertEqual(cases, recipe.extras('154A'))
        lengths = set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertTrue(case['reason'])
            data = recipe.parse('154A', case['input'])
            s, pairs = data
            self.assertEqual(case['input'].split('\n'), [s, str(len(pairs)), *pairs, ''])
            lengths.add(len(s))
            expected = recipe.last_kept_dp(data)
            if len(s) <= 10:
                self.assertEqual(recipe.exhaustive(data), expected)
            self.assertEqual(case['output'], f'{expected}\n')
        self.assertIn(1, lengths)
        self.assertIn(100000, lengths)
        maximum = [c for c in cases if c['category'] == 'maxSize']
        self.assertTrue(all(len(recipe.parse('154A', c['input'])[0]) == 100000 for c in maximum))
        self.assertTrue(any(len(recipe.parse('154A', c['input'])[1]) == 13 for c in maximum))


if __name__ == '__main__':
    unittest.main()
