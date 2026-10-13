"""727B author checks; fixtures retain the pinned upstream CRLF and output bytes."""
import copy
import itertools
import json
from pathlib import Path
import sys
import unittest


sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_727B as recipe


FIXTURES = json.loads(r'''{"official": [{"input": "chipsy48.32televizor12.390\r\n", "output": "12.438.32\r\n"}, {"input": "a1b2c3.38\r\n", "output": "6.38\r\n"}, {"input": "aa0.01t0.03\r\n", "output": "0.04\r\n"}, {"input": "test0.50test0.50\r\n", "output": "1"}, {"input": "a500b500\r\n", "output": "1.000"}, {"input": "tcjbjlbtjf329.910\r\n", "output": "329.910"}, {"input": "iwpcfsmzen297.618.42ff585.209.84\r\n", "output": "882.828.26\r\n"}, {"input": "dpinb27.277fwxpdbfg709.917vocemjru16.491ade860.722tvb870.469.51wrpgy565.046gddrwv202.271.28\r\n", "output": "3.252.193.79\r\n"}, {"input": "vayscqiwpc686.919.75bwyudkz759.174kgqq444.563.54feupje806.486.78vojngmlc385.668.02jrkzbsa819.334b32.509wmjg980.332yh894.786hw356.243oiuueu662.016ychbsklfln21.860.87p836.999.94huhiiqlqoc596.917.99\r\n", "output": "8.283.810.89\r\n"}, {"input": "amhppqxei543.370.32o544.196nocwgxticn776.562nm212.195dcftrrg635.773n646.814.94vrfmjjsgoi405.114k821.983.12rb749.955.62jifmdlgs615.101hg42.083.41gdqififg908.729qrrgopyn684.451avcjul727.150s864.068bcd196.732.37jd349.984.25ghn379.763.11dw881.650.19eysthrm790.534.68gilg546.048qs648.876pdudevipn986.325jcwqq376.669.92qp169.861qyjguum254.785.35kcxgl820.940adtenavaj279.104naaxcl531.444.02jh478.042.53\r\n", "output": "16.868.306.83\r\n"}, {"input": "aasf0.01egfr0.50edfasdf0.99rwer999.999.99\r\n", "output": "1.000.001.49\r\n"}, {"input": "a1.01\r\n", "output": "1.01\r\n"}, {"input": "a0.11\r\n", "output": "0.11\r\n"}, {"input": "r0.30q0.10\r\n", "output": "0.40\r\n"}, {"input": "asd0.03sgbgfh0.27\r\n", "output": "0.30\r\n"}, {"input": "sadfa4.44f0.56\r\n", "output": "5"}, {"input": "tr999.999.99r0.01\r\n", "output": "1.000.000"}, {"input": "f999.999.99fsdf0.01wef1.10dfs2.90\r\n", "output": "1.000.004"}, {"input": "a0.01\r\n", "output": "0.01\r\n"}, {"input": "q999.10\r\n", "output": "999.10\r\n"}, {"input": "a0.40\r\n", "output": "0.40\r\n"}, {"input": "t999.000.01\r\n", "output": "999.000.01\r\n"}, {"input": "kapusta123.456\r\n", "output": "123.456"}], "samples": [{"input": "chipsy48.32televizor12.390", "output": "12.438.32"}, {"input": "a1b2c3.38", "output": "6.38"}, {"input": "aa0.01t0.03", "output": "0.04"}]}''')


def independent_price_valid(price):
    groups = price.split('.')
    cents = 0
    if len(groups) > 1 and len(groups[-1]) == 2:
        fraction = groups.pop()
        if not fraction.isascii() or not fraction.isdigit() or fraction == '00':
            return False
        cents = int(fraction)
    if not groups or any(not part or not part.isascii() or not part.isdigit() for part in groups):
        return False
    if len(groups[0]) > 3 or (len(groups[0]) > 1 and groups[0][0] == '0'):
        return False
    if any(len(part) != 3 for part in groups[1:]):
        return False
    if len(groups) > 1 and groups[0] == '0':
        return False
    dollars = 0
    for part in groups:
        dollars = dollars * 1000 + int(part)
    return 1 <= dollars * 100 + cents <= 100000000


class Recipe727BTests(unittest.TestCase):
    def test_interface_and_unknown_problem(self):
        self.assertEqual(recipe.IDS, ('727B',))
        self.assertEqual(set(recipe.SEMANTICS), {'727B'})
        for function, args in ((recipe.parse, ('a1\n',)),
                               (recipe.answer, (('1',),)),
                               (recipe.extras, ()),
                               (recipe.review, ([], []))):
            with self.assertRaises(ValueError):
                function('727A', *args)

    def test_all_pinned_official_and_sample_pairs(self):
        tests = [(f'official/{i:04d}', pair) for i, pair in enumerate(FIXTURES['official'], 1)]
        samples = [(f'samples/{i:04d}', pair) for i, pair in enumerate(FIXTURES['samples'], 1)]
        before = copy.deepcopy(FIXTURES)
        self.assertEqual((len(tests), len(samples)), (23, 3))
        self.assertEqual(recipe.review('727B', tests, samples), [])
        for name, pair in tests + samples:
            with self.subTest(pair=name):
                self.assertEqual(recipe.answer('727B', recipe.parse('727B', pair['input'])),
                                 pair['output'].strip())
                self.assertEqual(recipe._reference_bill(pair['input']), pair['output'].strip())
        self.assertEqual(FIXTURES, before)

    def test_layout_and_name_rejection(self):
        invalid = ('', '\n', 'a1\n\n', 'a1\nb2\n', 'a1\rb2',
                   ' a1\n', 'a1 \n', 'a1\tb2\n', 'a1\u00a0b2',
                   'A1', 'á1', 'a١', '1', 'a', 'a1b', 'abcdefghijk1',
                   'a1' * 501 + '\n', 'a1\v', 'a1\r')
        for text in invalid:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('727B', text)
        for text in ('a1', 'a1\n', 'a1\r\n', 'abcdefghij1\n'):
            self.assertEqual(recipe.answer('727B', recipe.parse('727B', text)), '1')

    def test_price_rejection_and_valid_examples(self):
        invalid = ('.333', '3.33.11', '12.00', '.33', '0.1234', '1.2',
                   '0', '0.00', '01', '00.01', '1.000.000.01',
                   '1.000.001', '1000', '1.00', '0.000.01', '01.001',
                   '1..001', '1.000.', '1.000.000.99')
        for price in invalid:
            with self.subTest(price=price), self.assertRaises(ValueError):
                recipe.parse('727B', 'a' + price + '\n')
        for price in ('234', '1.544', '149.431.10', '0.99', '123.05',
                      '1.001', '1.000.01', '999.999.99', '1.000.000'):
            with self.subTest(price=price):
                self.assertEqual(recipe.answer('727B', recipe.parse('727B', 'a' + price)), price)

    def test_small_lexical_space_independently(self):
        for size in range(1, 7):
            for chars in itertools.product('01.', repeat=size):
                price = ''.join(chars)
                with self.subTest(price=price):
                    if independent_price_valid(price):
                        data = recipe.parse('727B', 'a' + price)
                        self.assertEqual(recipe.answer('727B', data), recipe._reference_bill('a' + price))
                    else:
                        with self.assertRaises(ValueError):
                            recipe.parse('727B', 'a' + price)

    def test_all_generated_pairs_are_unique_valid_and_independently_correct(self):
        cases = recipe.extras('727B')
        self.assertEqual(len(cases), 160)
        self.assertEqual(cases, recipe.extras('727B'))
        self.assertEqual(len({case['input'] for case in cases}), 160)
        for index, case in enumerate(cases):
            with self.subTest(index=index):
                self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
                self.assertIn(case['category'], ('boundary', 'adversarial', 'maxSize'))
                self.assertTrue(case['reason'])
                self.assertEqual(case['input'].count('\n'), 1)
                self.assertTrue(case['input'].endswith('\n'))
                data = recipe.parse('727B', case['input'])
                self.assertEqual(case['output'], recipe.answer('727B', data) + '\n')
                self.assertEqual(case['output'], recipe._reference_bill(case['input']) + '\n')

    def test_real_maximum_dimension_and_minimum(self):
        maxima = [c for c in recipe.extras('727B') if c['category'] == 'maxSize']
        self.assertEqual(len(maxima), 4)
        for case in maxima:
            self.assertEqual(len(case['input'].rstrip('\n')), 1000)
        self.assertEqual(len(recipe.parse('727B', maxima[0]['input'])), 500)
        self.assertEqual(maxima[1]['output'], '100.000.000\n')
        self.assertEqual(maxima[2]['output'], '2\n')
        self.assertEqual(maxima[3]['output'], '90.999.999.10\n')
        self.assertEqual(recipe.answer('727B', recipe.parse('727B', 'a0.01')), '0.01')

    def test_arithmetic_defect_models_not_downloaded_programs(self):
        repeated = recipe.parse('727B', 'same0.01same0.01same0.01\n')
        deduplicated_cents = sum({recipe._price_cents(value) for value in repeated})
        self.assertEqual(recipe.answer('727B', repeated), '0.03')
        self.assertEqual(deduplicated_cents, 1)
        final_price = recipe.parse('727B', 'a1b2\n')
        dropped_last_cents = sum(recipe._price_cents(value) for value in final_price[:-1])
        self.assertEqual(recipe.answer('727B', final_price), '3')
        self.assertEqual(dropped_last_cents, 100)
        self.assertEqual(recipe.answer('727B', recipe.parse('727B', 'a10\n')), '10')
        misread_undotted_two_digits_cents = 10
        self.assertNotEqual(misread_undotted_two_digits_cents, 1000)

    def test_review_reports_failures_without_repairing_bytes(self):
        pairs = [('bad-layout', {'input': 'a1\nb2\n', 'output': '3\n'}),
                 ('bad-format', {'input': 'a1\n', 'output': '1.00\n'}),
                 ('bad-value', {'input': 'a1b2\n', 'output': '1\n'})]
        before = copy.deepcopy(pairs)
        errors = recipe.review('727B', pairs, [])
        self.assertEqual([e['test'] for e in errors], ['bad-layout', 'bad-format', 'bad-value'])
        self.assertEqual(pairs, before)

    def test_real_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'727B': 1874})


if __name__ == '__main__':
    unittest.main()
