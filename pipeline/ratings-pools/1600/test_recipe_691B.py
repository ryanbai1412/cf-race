from pathlib import Path
import itertools
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_691B as recipe

OFFICIAL = [
    ('oXoxoXo\r\n', 'TAK\r\n'), ('bod\r\n', 'TAK\r\n'), ('ER\r\n', 'NIE\r\n'), ('o\r\n', 'TAK\r\n'),
    ('a\r\n', 'NIE\r\n'), ('opo\r\n', 'NIE\r\n'), ('HCMoxkgbNb\r\n', 'NIE\r\n'), ('vMhhXCMWDe\r\n', 'NIE\r\n'),
    ('iIcamjTRFH\r\n', 'NIE\r\n'), ('WvoWvvWovW\r\n', 'TAK\r\n'), ('WXxAdbAxXW\r\n', 'TAK\r\n'),
    ('vqMTUUTMpv\r\n', 'TAK\r\n'), ('iii\r\n', 'NIE\r\n'), ('AAWW\r\n', 'NIE\r\n'), ('ss\r\n', 'NIE\r\n'),
    ('i\r\n', 'NIE\r\n'), ('ii\r\n', 'NIE\r\n'), ('mm\r\n', 'NIE\r\n'), ('LJ\r\n', 'NIE\r\n'),
    ('m\r\n', 'NIE\r\n'), ('ioi\r\n', 'NIE\r\n'), ('OA\r\n', 'NIE\r\n'), ('aaaiaaa\r\n', 'NIE\r\n'),
    ('SS\r\n', 'NIE\r\n'), ('iiii\r\n', 'NIE\r\n'), ('ssops\r\n', 'NIE\r\n'), ('ssss\r\n', 'NIE\r\n'),
    ('ll\r\n', 'NIE\r\n'), ('s\r\n', 'NIE\r\n'), ('bb\r\n', 'NIE\r\n'), ('uu\r\n', 'NIE\r\n'),
    ('ZoZ\r\n', 'NIE\r\n'), ('mom\r\n', 'NIE\r\n'), ('uou\r\n', 'NIE\r\n'), ('u\r\n', 'NIE\r\n'),
    ('JL\r\n', 'NIE\r\n'), ('mOm\r\n', 'NIE\r\n'), ('llll\r\n', 'NIE\r\n'), ('ouo\r\n', 'NIE\r\n'),
    ('aa\r\n', 'NIE\r\n'), ('olo\r\n', 'NIE\r\n'), ('S\r\n', 'NIE\r\n'), ('lAl\r\n', 'NIE\r\n'),
    ('nnnn\r\n', 'NIE\r\n'), ('ZzZ\r\n', 'NIE\r\n'), ('bNd\r\n', 'NIE\r\n'), ('ZZ\r\n', 'NIE\r\n'),
    ('oNoNo\r\n', 'NIE\r\n'), ('l\r\n', 'NIE\r\n'), ('zz\r\n', 'NIE\r\n'), ('NON\r\n', 'NIE\r\n'),
    ('nn\r\n', 'NIE\r\n'), ('NoN\r\n', 'NIE\r\n'), ('sos\r\n', 'NIE\r\n'), ('lol\r\n', 'NIE\r\n'),
    ('mmm\r\n', 'NIE\r\n'), ('YAiAY\r\n', 'NIE\r\n'), ('ipIqi\r\n', 'NIE\r\n'), ('AAA\r\n', 'TAK\r\n'),
    ('uoOou\r\n', 'NIE\r\n'), ('SOS\r\n', 'NIE\r\n'), ('NN\r\n', 'NIE\r\n'), ('n\r\n', 'NIE\r\n'),
    ('h\r\n', 'NIE\r\n'), ('blld\r\n', 'NIE\r\n'), ('ipOqi\r\n', 'NIE\r\n'), ('pop\r\n', 'NIE\r\n'),
    ('BB\r\n', 'NIE\r\n'), ('OuO\r\n', 'NIE\r\n'), ('lxl\r\n', 'NIE\r\n'), ('Z\r\n', 'NIE\r\n'),
    ('vvivv\r\n', 'NIE\r\n'), ('nnnnnnnnnnnnn\r\n', 'NIE\r\n'), ('AA\r\n', 'TAK\r\n'), ('t\r\n', 'NIE\r\n'),
    ('z\r\n', 'NIE\r\n'), ('mmmAmmm\r\n', 'NIE\r\n'), ('qlililp\r\n', 'NIE\r\n'), ('mpOqm\r\n', 'NIE\r\n'),
    ('iiiiiiiiii\r\n', 'NIE\r\n'), ('BAAAB\r\n', 'NIE\r\n'), ('UA\r\n', 'NIE\r\n'), ('mmmmmmm\r\n', 'NIE\r\n'),
    ('NpOqN\r\n', 'NIE\r\n'), ('uOu\r\n', 'NIE\r\n'), ('uuu\r\n', 'NIE\r\n'), ('NAMAN\r\n', 'NIE\r\n'),
    ('lllll\r\n', 'NIE\r\n'), ('T\r\n', 'TAK\r\n'), ('mmmmmmmmmmmmmmmm\r\n', 'NIE\r\n'), ('AiiA\r\n', 'NIE\r\n'),
    ('iOi\r\n', 'NIE\r\n'), ('lll\r\n', 'NIE\r\n'), ('N\r\n', 'NIE\r\n'), ('viv\r\n', 'NIE\r\n'),
    ('oiio\r\n', 'NIE\r\n'), ('AiiiA\r\n', 'NIE\r\n'), ('NNNN\r\n', 'NIE\r\n'), ('ixi\r\n', 'NIE\r\n'),
    ('AuuA\r\n', 'NIE\r\n'), ('AAAANANAAAA\r\n', 'NIE\r\n'), ('mmmmm\r\n', 'NIE\r\n'), ('oYo\r\n', 'TAK\r\n'),
    ('dd\r\n', 'NIE\r\n'), ('A\r\n', 'TAK\r\n'), ('ioh\r\n', 'NIE\r\n'), ('mmmm\r\n', 'NIE\r\n'),
    ('uuuu\r\n', 'NIE\r\n'), ('puq\r\n', 'NIE\r\n'), ('rrrrrr\r\n', 'NIE\r\n'), ('c\r\n', 'NIE\r\n'),
    ('AbpA\r\n', 'NIE\r\n'), ('qAq\r\n', 'NIE\r\n'), ('tt\r\n', 'NIE\r\n'), ('mnmnm\r\n', 'NIE\r\n'),
    ('sss\r\n', 'NIE\r\n'), ('yy\r\n', 'NIE\r\n'), ('bob\r\n', 'NIE\r\n'), ('NAN\r\n', 'NIE\r\n'),
    ('mAm\r\n', 'NIE\r\n'), ('tAt\r\n', 'NIE\r\n'), ('yAy\r\n', 'NIE\r\n'), ('zAz\r\n', 'NIE\r\n'),
    ('aZ\r\n', 'NIE\r\n'), ('hh\r\n', 'NIE\r\n'), ('bbbb\r\n', 'NIE\r\n'), ('ZAZ\r\n', 'NIE\r\n'),
    ('Y\r\n', 'TAK\r\n'), ('AAMM\r\n', 'NIE\r\n'), ('lml\r\n', 'NIE\r\n'), ('AZA\r\n', 'NIE\r\n'),
    ('mXm\r\n', 'NIE\r\n'), ('bd\r\n', 'TAK\r\n'), ('H\r\n', 'TAK\r\n'), ('uvu\r\n', 'NIE\r\n'),
    ('dxxd\r\n', 'NIE\r\n'), ('dp\r\n', 'NIE\r\n'), ('vV\r\n', 'NIE\r\n'), ('vMo\r\n', 'NIE\r\n'),
    ('O\r\n', 'TAK\r\n'), ('vYv\r\n', 'TAK\r\n'), ('fv\r\n', 'NIE\r\n'), ('U\r\n', 'TAK\r\n'),
    ('iAi\r\n', 'NIE\r\n'), ('I\r\n', 'TAK\r\n'), ('VxrV\r\n', 'NIE\r\n'), ('POP\r\n', 'NIE\r\n'),
    ('bid\r\n', 'NIE\r\n'), ('bmd\r\n', 'NIE\r\n'), ('AiA\r\n', 'NIE\r\n'), ('mmmmmm\r\n', 'NIE\r\n'),
    ('XHX\r\n', 'TAK\r\n'), ('llllll\r\n', 'NIE\r\n'), ('aAa\r\n', 'NIE\r\n'), ('Db\r\n', 'NIE\r\n'),
    ('lOl\r\n', 'NIE\r\n'), ('bzd\r\n', 'NIE\r\n'),
]
SAMPLES = [('oXoxoXo', 'TAK'), ('bod', 'TAK'), ('ER', 'NIE')]


def cf_number(row):
    return row if row <= 12 else row + 11


def wa_19882536(s):
    n, sym = len(s), 'OoHVvXxWwMTIUY'
    if n % 2 and s[n // 2] not in sym:
        return 'NIE'
    for i in range(n // 2):
        if s[i] == s[n - 1 - i]:
            if s[i] not in sym:
                return 'NIE'
        elif s[i] != 'b' or s[n - 1 - i] != 'd':
            return 'NIE'
    return 'TAK'


def wa_20395805(s):
    n, pairs = len(s), {'b': 'd', 'd': 'b', 'p': 'q', 'q': 'p'}
    for i in range((n - 1) // 2 + 1):
        if not (s[i] in 'AHIMOTUVWXYmovwx' or pairs.get(s[i]) == s[n - 1 - i]):
            return 'NIE'
    return 'TAK'


def wa_29088316(s):
    if any(c in s for c in 'aBCcDEeFfGghJjKkLlmNnPQRrSstuyZz'):
        return 'NIE'
    for old, new in (('b', 'd'), ('d', 'b'), ('p', 'q'), ('q', 'p')):
        s = s.replace(old, new)
    return 'TAK' if s == s[::-1] else 'NIE'


def wa_35578812(s):
    image = dict(zip('AbdHIiMmnOopqTUuVvWwXxY', 'AdbHIiMmnOoqqTUuVvWwXxY'))
    n = len(s)
    return 'TAK' if all(image.get(s[i]) == s[n - 1 - i] for i in range((n + 1) // 2)) else 'NIE'


def wa_44521116(s):
    image = dict(zip('AHbdIMOoTUVvWwXxY', 'AHdbIMOoTUVvWwXxY'))
    n = len(s)
    if n % 2 and (s[n // 2] not in image or s[n // 2] in 'bd'):
        return 'NIE'
    return 'TAK' if all(s[i] in image and s[n - 1 - i] in image and image[s[i]] == s[n - 1 - i]
                        for i in range(n // 2 + (n > 1))) else 'NIE'


def wa_47806289(s):
    sym, pairs = 'AHIMmOoTUVvWwXxY', {'p': 'q', 'q': 'p', 'b': 'd', 'd': 'b'}
    for i in range(len(s) // 2):
        if s[i] in sym:
            if s[-1 - i] != s[i]:
                return 'NIE'
        elif s[i] not in pairs or pairs[s[i]] != s[-1 - i]:
            return 'NIE'
    return 'TAK'


def wa_55610602(s):
    image = dict(zip('oIHibxXVvUWwMAYTpqdO', 'oIHidxXVvUWwMAYTqpbO'))
    n = len(s)
    if n % 2 and s[n // 2] not in 'UIOTHiXxoMAWwVvY':
        return 'NIE'
    return 'TAK' if all(s[i] in image and image[s[i]] == s[n - 1 - i] for i in range(n // 2)) else 'NIE'


def wa_64421868(s):
    n = len(s)
    for i in range(n):
        x, y = s[i], s[n - 1 - i]
        if not ((x == y and x in 'xXAHIMmoOTuUVvWwYyn') or {x + y, y + x} & {'LJ', 'bd', 'pq'}):
            return 'NIE'
    return 'TAK'


MUTANTS = {
    '19882536': (wa_19882536, 10), '20395805': (wa_20395805, 24), '29088316': (wa_29088316, 5),
    '35578812': (wa_35578812, 11), '44521116': (wa_44521116, 11), '47806289': (wa_47806289, 4),
    '55610602': (wa_55610602, 23), '64421868': (wa_64421868, 28),
}


class ParseTests(unittest.TestCase):
    def test_accepts_single_line_with_lf_crlf_or_no_terminator(self):
        self.assertEqual(recipe.parse('691B', 'oXoxoXo\r\n'), 'oXoxoXo')
        self.assertEqual(recipe.parse('691B', 'bod\n'), 'bod')
        self.assertEqual(recipe.parse('691B', 'ER'), 'ER')
        self.assertEqual(recipe.parse('691B', 'z' * 1000 + '\n'), 'z' * 1000)

    def test_rejects_layout_charset_and_length(self):
        for text in ('', '\n', 'A' * 1001 + '\n', 'ab cd\n', 'ab\ncd\n', ' ab\n', 'ab \n', 'ab\n\n', 'a1\n',
                     'a-b\n', '\u00e9\n', 'ab\r\r\n', 'ab\t\n'):
            with self.assertRaises(ValueError, msg=repr(text)):
                recipe.parse('691B', text)


class OracleTests(unittest.TestCase):
    def test_official_and_sample_pairs_review_clean(self):
        self.assertEqual(len(OFFICIAL), 157)
        self.assertTrue(all(i.endswith('\r\n') for i, _ in OFFICIAL))
        tests = [('%04d' % k, {'input': i, 'output': o}) for k, (i, o) in enumerate(OFFICIAL, 1)]
        samples = [('sample%d' % k, {'input': i, 'output': o}) for k, (i, o) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review('691B', tests, samples), [])

    def test_review_flags_disagreement_and_malformed_input(self):
        failures = recipe.review('691B', [('wrong', {'input': 'mm\r\n', 'output': 'TAK\r\n'}),
                                          ('layout', {'input': 'AA\nAA\n', 'output': 'TAK\n'}),
                                          ('case', {'input': 'AA\n', 'output': 'tak\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['wrong', 'layout', 'case'])

    def test_mirror_table_matches_independent_transcription(self):
        for c in recipe.LETTERS:
            self.assertEqual(recipe.MIRROR.get(c), recipe.table_mirror(c), c)
        self.assertEqual(sorted(recipe.MIRROR), sorted('AHIMOoTUVvWwXxYbdpq'))

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'691B'})
        self.assertGreaterEqual(counts['691B'], 300000)

    def test_generative_brute_counts(self):
        for n in range(1, 5):
            found = recipe.all_s_palindromes(recipe.LETTERS, n)
            self.assertEqual(len(found), 19 ** (n // 2) * (15 if n % 2 else 1))
            self.assertTrue(all(recipe.brute('691B', s) == 'TAK' for s in found))


class ExtrasTests(unittest.TestCase):
    def test_generated_inputs_are_valid_and_independently_checked(self):
        cases = recipe.extras('691B')
        self.assertEqual(cases, recipe.extras('691B'))
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        self.assertEqual({c['category'] for c in cases}, {'boundary', 'adversarial', 'maxSize'})
        lengths = set()
        for case in cases:
            self.assertEqual(set(case), {'input', 'output', 'reason', 'category'})
            self.assertEqual(case['input'].count('\n'), 1)
            self.assertTrue(case['input'].endswith('\n') and case['output'] in ('TAK\n', 'NIE\n'))
            s = recipe.parse('691B', case['input'])
            self.assertEqual(recipe.brute('691B', s), case['output'].strip(), case['reason'])
            lengths.add(len(s))
        self.assertIn(1, lengths)
        self.assertIn(1000, lengths)
        maxima = {c['output'] for c in cases if len(c['input']) == 1001}
        self.assertEqual(maxima, {'TAK\n', 'NIE\n'})

    def test_selected_wrong_sources_modelled_and_killed(self):
        cases = recipe.extras('691B')
        for sid, (mutant, passed) in MUTANTS.items():
            outcomes = {cf_number(k): mutant(i.strip()) == o.strip() for k, (i, o) in enumerate(OFFICIAL, 1)}
            self.assertTrue(all(outcomes[k] for k in outcomes if k <= passed), sid)
            self.assertFalse(outcomes[passed + 1], sid)
            kills = [c for c in cases if mutant(c['input'].strip()) != c['output'].strip()]
            self.assertGreaterEqual(len(kills), 3, sid)

if __name__ == '__main__':
    unittest.main()
