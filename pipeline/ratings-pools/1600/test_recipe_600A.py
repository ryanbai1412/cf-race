from pathlib import Path
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_600A as recipe

PID = '600A'
SAMPLES = [('aba,123;1a;0', '"123,0"\n"aba,1a"'), ('1;;01,a0,', '"1"\n",01,a0,"'), ('1', '"1"\n-'), ('a', '-\n"a"')]
OFFICIAL = [
    (',;,,;', '-', '",,,,,"'),
    ('123;abacab,123;1,sadasfas,123213132g;02131313;aaa,0,012;0;03242;1', '"123,123,1,0,0,1"', '"abacab,sadasfas,123213132g,02131313,aaa,012,03242"'),
    ('.', '-', '"."'), (';', '-', '","'), ('6;2,', '"6,2"', '""'), ('000', '-', '"000"'),
    ('100.000', '-', '"100.000"'), ('01', '-', '"01"'), (',2', '"2"', '""'), ('00', '-', '"00"'),
    ('00,0.0;00;0;,,0,0.0.0,,000,010;;', '"0,0"', '"00,0.0,00,,,0.0.0,,000,010,,"'),
    ('12345678912345', '"12345678912345"', '-'),
]


def split_words(s):
    words, cur = [], []
    for c in s:
        if c in ',;':
            words.append(''.join(cur))
            cur = []
        else:
            cur.append(c)
    words.append(''.join(cur))
    return words


def emit(nums, others, sep=',', empty='-'):
    return [('"' + sep.join(p) + '"') if p else empty for p in (nums, others)]


def mutant(is_number, drop=lambda w: False, sep=',', empty='-', swap=False):
    def run(s):
        nums, others = [], []
        for w in split_words(s):
            if drop(w):
                continue
            (nums if is_number(w) else others).append(w)
        out = emit(nums, others, sep, empty)
        return out[::-1] if swap else out
    return run


def correct_number(w):
    return w == '0' or (w[:1] in '123456789' and w != '' and all(c in '0123456789' for c in w))


def ascii_digits(w):
    return w != '' and all(c in '0123456789' for c in w)


MUTANTS = {
    'zero rejected by w[0]!="0" (109331195, 105967924, 105789683)': mutant(lambda w: ascii_digits(w) and w[0] != '0'),
    'leading zeros accepted, isdigit only (154914789)': mutant(ascii_digits),
    'int(w)==0 accepts 00/000 (111955085)': mutant(lambda w: ascii_digits(w) and (w[0] != '0' or int(w) == 0)),
    'empty and dotted words dropped (121158382)': mutant(correct_number, drop=lambda w: w == '' or '.' in w),
    'empty list printed as "" (105824496)': mutant(correct_number, empty='""'),
    'only "01" treated as leading-zero (162712627)': mutant(lambda w: ascii_digits(w) and w != '01'),
    'words joined by ";" (105811063)': mutant(correct_number, sep=';'),
    'lines swapped (105963405)': mutant(correct_number, swap=True),
    'only lowercase letters mark non-number (151263146 classification)': mutant(
        lambda w: w != '' and not any('a' <= c <= 'z' for c in w) and not (w[0] == '0' and w != '0' and set(w) <= set('0123456789'))),
}


def wrong_zero_only_last(s):
    nums, others = [], []
    words = split_words(s)
    for i, w in enumerate(words):
        if w and w[0] in '123456789' and ascii_digits(w):
            nums.append(w)
        elif w == '0' and i == len(words) - 1:
            nums.append(w)
        else:
            others.append(w)
    return emit(nums, others)


MUTANTS['"0" recognised only as last word (173914988)'] = wrong_zero_only_last


class Recipe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras(PID)

    def test_samples_and_official_subset(self):
        for text, out in SAMPLES:
            self.assertEqual(recipe.answer(PID, recipe.parse(PID, text)), out.split('\n'))
        for text, a, b in OFFICIAL:
            self.assertEqual(recipe.answer(PID, recipe.parse(PID, text + '\r\n')), [a, b])
        tests = [(str(i), {'input': t + '\r\n', 'output': f'{a}\r\n{b}\r\n'}) for i, (t, a, b) in enumerate(OFFICIAL)]
        samples = [(f's{i}', {'input': t, 'output': o}) for i, (t, o) in enumerate(SAMPLES)]
        self.assertEqual(recipe.review(PID, tests, samples), [])

    def test_review_flags_bad_pairs(self):
        bad = [('x', {'input': '0\n', 'output': '-\n"0"\n'}), ('y', {'input': '1,\n', 'output': '"1"\n-\n'}),
               ('z', {'input': 'a b\n', 'output': '-\n"a b"\n'}), ('w', {'input': '1\n', 'output': '"1" -\n'}),
               ('v', {'input': '1\n', 'output': '"1"\n-\n'})]
        self.assertEqual([f['test'] for f in recipe.review(PID, bad, [])], ['x', 'y', 'z', 'w'])

    def test_parse_rejects(self):
        for text in ('', '\n', 'a b', 'a\nb', '1\n2\n', '-1', '+1', 'a_b', '"a"', 'é', 'a\tb', 'x' * 100001, '1' * 100001):
            with self.assertRaises(ValueError, msg=text[:20]):
                recipe.parse(PID, text)
        self.assertEqual(recipe.parse(PID, ';\r\n'), ';')
        self.assertEqual(recipe.parse(PID, 'a' * 100000), 'a' * 100000)
        with self.assertRaises(ValueError):
            recipe.parse('600B', 'a')

    def test_brute_differs_and_agrees(self):
        self.assertGreater(recipe.brute_checks()['600A'], 50000)
        for s in ('0', '00', ',', '1;;01,a0,', '0.', ';0'):
            self.assertEqual(recipe.brute(s), recipe.answer(PID, s))

    def test_extras(self):
        cases = self.cases
        self.assertGreaterEqual(len(cases), 120)
        self.assertLessEqual(len(cases), 180)
        self.assertEqual(len({c['input'] for c in cases}), len(cases))
        cats = {c['category'] for c in cases}
        self.assertEqual(cats, {'boundary', 'adversarial', 'maxSize'})
        for c in cases:
            self.assertEqual(set(c), {'input', 'output', 'reason', 'category'})
            self.assertRegex(c['input'], r'^[A-Za-z0-9.,;]{1,100000}\n$')
            s = recipe.parse(PID, c['input'])
            self.assertEqual(c['output'], '\n'.join(recipe.brute(s)) + '\n')
            self.assertEqual(c['output'], '\n'.join(split_reference(s)) + '\n')
            lines = c['output'].split('\n')
            self.assertEqual(len(lines), 3)
            self.assertEqual(lines[2], '')
            for line in lines[:2]:
                self.assertRegex(line, r'^(-|"[A-Za-z0-9.,]*")$')
            self.assertTrue(all(len(w) <= 4000 for w in re.split('[,;]', s) if set(w) <= set('0123456789')))
        lengths = [len(recipe.parse(PID, c['input'])) for c in cases]
        self.assertEqual(max(lengths), 100000)
        self.assertEqual(min(lengths), 1)
        self.assertGreaterEqual(sum(c['category'] == 'maxSize' and len(c['input']) == 100001 for c in cases), 5)
        outs = {c['output'] for c in cases}
        self.assertIn('-\n' + '"' + ',' * 100000 + '"\n', outs)

    def test_extras_hash_seed_deterministic(self):
        code = ('import json,sys;sys.path.insert(0,%r);import recipe_600A as r;'
                'print(__import__("hashlib").sha256(json.dumps(r.extras("600A")).encode()).hexdigest())') % str(Path(__file__).resolve().parent)
        digests = {subprocess.run([sys.executable, '-c', code], env={**os.environ, 'PYTHONHASHSEED': seed},
                                  capture_output=True, text=True, check=True).stdout for seed in ('0', '1', '12345')}
        self.assertEqual(len(digests), 1)
        self.assertEqual(digests.pop().strip(), hashlib.sha256(json.dumps(self.cases).encode()).hexdigest())

    def test_mutants_killed(self):
        for name, wrong in MUTANTS.items():
            killed = [c for c in self.cases if wrong(recipe.parse(PID, c['input'])) != c['output'].split('\n')[:2]]
            self.assertGreaterEqual(len(killed), 5, name)
            for c in killed:
                self.assertNotEqual(' '.join(wrong(recipe.parse(PID, c['input']))).split(), c['output'].split(), name)


def split_reference(s):
    return emit([w for w in split_words(s) if correct_number(w)], [w for w in split_words(s) if not correct_number(w)])


if __name__ == '__main__':
    unittest.main()
