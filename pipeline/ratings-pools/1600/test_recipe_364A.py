from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_364A as recipe


OFFICIAL = [
    ('10\r\n12345\r\n', '6\r\n'),
    ('16\r\n439873893693495623498263984765\r\n', '40\r\n'),
    ('0\r\n1230\r\n', '19\r\n'),
    ('8398\r\n67950927224842887617892831243606761170908507858527\r\n', '0\r\n'),
    ('2\r\n11\r\n', '4\r\n'),
    ('4\r\n111\r\n', '4\r\n'),
    ('0\r\n0\r\n', '1\r\n'),
    ('1\r\n0\r\n', '0\r\n'),
    ('0\r\n1\r\n', '0\r\n'),
    ('0\r\n0000\r\n', '100\r\n'),
    ('1\r\n00\r\n', '0\r\n'),
    ('1\r\n000\r\n', '0\r\n'),
    ('1\r\n11111\r\n', '25\r\n'),
    ('700\r\n100101011011001100111101100101000100000000011001111000111110001011011100010110000000000100100000001100000011110011101110011101101110111011011100001001101011000100000000000110001000101001100011111110011010101011010100010100001011011111001011000101001101000111010100110000100100110011111100010111100010000101001110111101110011111000111011011110111\r\n', '3390908\r\n'),
    ('1000000000\r\n769416574772919262229125278908144478541501489034872535880758612234526208997051461441045410435259231256676917086438172075984271711722261161236033705315696117638300191007208614272746181036958213963736353682247646595587613148679926094811\r\n', '0\r\n'),
    ('10000\r\n011111011000110010011010001011101100110111000100111110011100010001111010010010\r\n', '0\r\n'),
    ('5\r\n1010100010101000010101001010102020201010100101020\r\n', '14288\r\n'),
    ('0\r\n0001001001011001100101100001111111001010011111000100000000011000001010110111100100000000001110110101010010001010100110011100001010001\r\n', '3559240\r\n'),
    ('0\r\n11002201122211202102\r\n', '2484\r\n'),
    ('0\r\n3123232011321302332331322102332011002122123113023032320333332330233131131123012232200000120323200110\r\n', '322176\r\n'),
    ('2\r\n21111102201122101122\r\n', '532\r\n'),
    ('3\r\n0130301201202102033203302203131122023031112010202333033033021210331110110022230021013231130200102022\r\n', '7980\r\n'),
    ('0\r\n5054451336060064631662402176557747457153065525132775141002773502671221320017407134475306346213334141573052346075726400141731757473641\r\n', '373821\r\n'),
    ('1\r\n14230330640346634338\r\n', '1\r\n'),
    ('2\r\n5101140593483723176811719219208813520975285810392000077455984289096240663245004460322003001554026756\r\n', '800\r\n'),
    ('1000000000\r\n00000000000000000000000000000000000000000000000000\r\n', '0\r\n'),
    ('0\r\n00000000000000000000000000000000000000000000000000\r\n', '1625625\r\n'),
    ('1\r\n00000000000000000000000000000000000000000000000000000000\r\n', '0\r\n'),
    ('2\r\n000000000000000000000000000000000000000000000000000000000\r\n', '0\r\n'),
    ('0\r\n01111111011001011100010000101111101111010101110011\r\n', '75600\r\n'),
    ('1\r\n11110110111010001000100010010101001111111001100100001000\r\n', '17956\r\n'),
    ('0\r\n02102110221221211102011211200110110222121101121110\r\n', '30456\r\n'),
    ('1\r\n12200220101112112102221202012201210000010112000102121022\r\n', '2500\r\n'),
    ('0\r\n32365690899439422959451631777149229543849097266521\r\n', '5096\r\n'),
    ('1\r\n39568795337451783387623217888229492030389256605973002137\r\n', '9\r\n'),
    ('0\r\n1011101100010110010111010\r\n', '9525\r\n'),
    ('1\r\n210120001002121211101002102001010012221102201222121011102210110002222001222\r\n', '4761\r\n'),
    ('0\r\n000000000000000000000000000000000\r\n', '314721\r\n'),
    ('0\r\n32251032040000365150463055464352624561315100524465\r\n', '43061\r\n'),
    ('1\r\n43561243107434624503740444753362003764016311724140063706\r\n', '64\r\n'),
    ('0\r\n24225680092188869135902902675995827895766459740919\r\n', '15264\r\n'),
    ('0\r\n01\r\n', '5\r\n'),
    ('0\r\n101\r\n', '11\r\n'),
    ('0\r\n010\r\n', '20\r\n'),
    ('0\r\n1235456416548\r\n', '0\r\n'),
    ('0\r\n0011\r\n', '51\r\n'),
]


def mutants():
    def counts(s):
        return recipe.histogram(s)

    def generic(a, s, zero_rule=None, unit_once=False, cap=None):
        cnt = counts(s)
        if cap is not None:
            cnt = cnt[:cap]
        every = len(s) * (len(s) + 1) // 2
        if a == 0:
            return zero_rule(cnt[0], every, len(s))
        total = sum(cnt[x] * cnt[a // x] for x in range(1, len(cnt)) if a % x == 0 and a // x < len(cnt))
        if unit_once and 1 < a < len(cnt):
            total -= cnt[1] * cnt[a]
        return total

    exact_zero = lambda c0, every, n: 2 * c0 * every - c0 * c0
    wrap = lambda v: (v + 2 ** 31) % 2 ** 32 - 2 ** 31
    return {
        'a=0 prints |s|^2 (19763711)': lambda a, s: generic(a, s, lambda c0, every, n: n * n),
        'a=0 prints 0 (33535913, 5338173)': lambda a, s: generic(a, s, lambda c0, every, n: 0),
        'a=0 counts only zero*zero (33530016)': lambda a, s: generic(a, s, lambda c0, every, n: c0 * c0),
        'a=0 counts one order only': lambda a, s: generic(a, s, lambda c0, every, n: c0 * every),
        'pair (1,a) counted once (33536046)': lambda a, s: generic(a, s, exact_zero, unit_once=True),
        'interval sums capped below 36000': lambda a, s: generic(a, s, exact_zero, cap=36000),
        '32-bit answer': lambda a, s: wrap(generic(a, s, exact_zero)),
    }


class ParseTests(unittest.TestCase):
    def test_accepts_crlf_and_lf_layouts(self):
        self.assertEqual(recipe.parse('364A', '10\n12345\n'), (10, '12345'))
        self.assertEqual(recipe.parse('364A', '10\r\n12345\r\n'), (10, '12345'))
        self.assertEqual(recipe.parse('364A', '0\n0'), (0, '0'))
        self.assertEqual(recipe.parse('364A', '1000000000\n' + '9' * 4000 + '\n'), (10 ** 9, '9' * 4000))
        self.assertEqual(recipe.parse('364A', '5\n0012\n'), (5, '0012'))

    def test_rejects_malformed_inputs(self):
        bad = ['', '10\n', '\n123\n', '10 12345\n', '10\n123 45\n', '10\n12345 \n', ' 10\n12345\n',
               '+10\n12345\n', '1_0\n12345\n', '010\n12345\n', '-1\n12345\n', '1000000001\n1\n',
               '10\n' + '1' * 4001 + '\n', '10\n12a45\n', '10\n12345\n\n', '10\n12345\n1\n', '10\n\n']
        for text in bad:
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse('364A', text)


class OracleTests(unittest.TestCase):
    def test_hand_derived_answers(self):
        cases = {(0, '0'): 1, (1, '0'): 0, (0, '1'): 0, (1, '1'): 1, (0, '01'): 5, (2, '11'): 4,
                 (5, '15'): 2, (25, '5'): 1, (0, '00'): 9, (36, '123'): 1, (10, '12345'): 6}
        for data, expected in cases.items():
            self.assertEqual(recipe.answer('364A', data), expected, data)
            self.assertEqual(recipe.literal_rectangles(data), expected, data)
            self.assertEqual(recipe.histogram_oracle(data), expected, data)
            self.assertEqual(recipe.quadratic_oracle(data), expected, data)

    def test_official_pairs(self):
        tests = [(f'{i:04d}', {'input': text, 'output': out}) for i, (text, out) in enumerate(OFFICIAL, 1)]
        samples = [('s1', {'input': '10\n12345', 'output': '6'}), ('s2', {'input': '16\n439873893693495623498263984765', 'output': '40'})]
        self.assertEqual(recipe.review('364A', tests, samples), [])
        self.assertEqual(len(tests), 46)
        for _, pair in tests:
            data = recipe.parse('364A', pair['input'])
            self.assertEqual(pair['output'], f'{recipe.quadratic_oracle(data)}\r\n')
            self.assertEqual(pair['input'], f'{data[0]}\r\n{data[1]}\r\n')

    def test_review_reports_disagreement_and_malformed(self):
        failures = recipe.review('364A', [('0001', {'input': '0\n0\n', 'output': '0\n'}),
                                          ('0002', {'input': '0\n0 \n', 'output': '1\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['0001', '0002'])
        self.assertEqual(failures[0]['expected'], ['1'])

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'364A'})
        self.assertGreaterEqual(counts['364A'], 10000)


class ExtrasTests(unittest.TestCase):
    def test_generated_cases_are_valid_and_independently_correct(self):
        cases = recipe.extras('364A')
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        self.assertEqual({c['category'] for c in cases}, {'boundary', 'adversarial', 'maxSize'})
        self.assertEqual(cases, recipe.extras('364A'))
        lengths, values = set(), set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertTrue(case['reason'])
            a, s = data = recipe.parse('364A', case['input'])
            self.assertEqual(case['input'].split('\n'), [str(a), s, ''])
            lengths.add(len(s))
            values.add(a)
            expected = recipe.histogram_oracle(data)
            if len(s) <= 8:
                self.assertEqual(recipe.literal_rectangles(data), expected, data)
            if len(s) <= 300:
                self.assertEqual(recipe.quadratic_oracle(data), expected, data)
            self.assertEqual(case['output'], f'{expected}\n')
        self.assertIn(1, lengths)
        self.assertIn(4000, lengths)
        self.assertIn(0, values)
        self.assertIn(10 ** 9, values)
        maximum = [c for c in cases if c['category'] == 'maxSize']
        self.assertTrue(all(len(recipe.parse('364A', c['input'])[1]) == 4000 for c in maximum))
        self.assertTrue(any(int(c['output']) >= 2 ** 31 for c in maximum))

    def test_selected_wrong_algorithms_are_killed(self):
        cases = [recipe.parse('364A', c['input']) for c in recipe.extras('364A')]
        for label, mutant in mutants().items():
            killed = [d for d in cases if mutant(*d) != recipe.histogram_oracle(d)]
            self.assertTrue(killed, label)


if __name__ == '__main__':
    unittest.main()
