from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import recipe_570C as recipe

OFFICIAL = [
    ('10 3\r\n.b..bz....\r\n1 h\r\n3 c\r\n9 f\r\n', '4\r\n3\r\n1\r\n'),
    ('4 4\r\n.cc.\r\n2 .\r\n3 .\r\n2 a\r\n1 a\r\n', '1\r\n3\r\n1\r\n1\r\n'),
    ('3 3\r\n...\r\n1 .\r\n2 a\r\n3 b\r\n', '2\r\n0\r\n0\r\n'),
    ('5 1\r\n.....\r\n5 z\r\n', '3\r\n'),
    ('1 5\r\n.\r\n1 .\r\n1 w\r\n1 w\r\n1 .\r\n1 .\r\n', '0\r\n0\r\n0\r\n0\r\n0\r\n'),
    ('2 7\r\nab\r\n1 w\r\n2 w\r\n1 c\r\n2 .\r\n2 .\r\n1 .\r\n2 b\r\n', '0\r\n0\r\n0\r\n0\r\n0\r\n1\r\n0\r\n'),
]

SAMPLES = [
    ('10 3\n.b..bz....\n1 h\n3 c\n9 f', '4\n3\n1'),
    ('4 4\n.cc.\n2 .\n3 .\n2 a\n1 a', '1\n3\n1\n1'),
]


def pairs_from_scratch(chars):
    return sum(len(run) - 1 for run in re.findall(r'\.+', ''.join(chars)))


def minimum_any_occurrence(s):
    frontier, seen, depth = {s}, {s}, 0
    while True:
        if any('..' not in t for t in frontier):
            return depth
        nxt = set()
        for t in frontier:
            for i in range(len(t) - 1):
                if t[i:i + 2] == '..':
                    u = t[:i] + t[i + 1:]
                    if u not in seen:
                        seen.add(u)
                        nxt.add(u)
        frontier, depth = nxt, depth + 1


def mutant_n1_prints_one(data):
    s, queries = data
    return [1] * len(queries) if len(s) == 1 else recipe.run_answers(data)


def mutant_n1_single_line(data):
    s, queries = data
    return [0] if len(s) == 1 else recipe.run_answers(data)


def mutant_last_index(data):
    s, queries = data
    chars, n = list(s), len(s)
    for x, c in queries:
        if n > 1 and x == n and c == '.' and chars[x - 1] != '.':
            return None
        chars[x - 1] = c
    return recipe.run_answers(data)


def mutant_negative_wrap(data):
    s, queries = data
    chars, n = list(s), len(s)
    ans = sum(chars[i] == chars[i + 1] == '.' for i in range(n - 1))
    out = []
    for x, c in queries:
        i = x - 1
        if (c == '.') != (chars[i] == '.'):
            delta = (chars[i - 1] == '.') + (i + 1 < n and chars[i + 1] == '.')
            ans += delta if c == '.' else -delta
        chars[i] = c
        out.append(ans)
    return out


def mutant_no_noop_check(data):
    s, queries = data
    chars, n = list(s), len(s)
    ans = sum(chars[i] == chars[i + 1] == '.' for i in range(n - 1))
    out = []
    for x, c in queries:
        i = x - 1
        delta = (i > 0 and chars[i - 1] == '.') + (i + 1 < n and chars[i + 1] == '.')
        ans += delta if c == '.' else -delta * (chars[i] == '.')
        chars[i] = c
        out.append(ans)
    return out


def mutant_unstored_prepend(data):
    s, queries = data
    groups, assoc, gid, cur = {}, {}, 0, []
    for j, c in enumerate(s):
        if c == '.':
            cur.append(j)
        elif cur:
            groups[gid], cur, gid = cur, [], gid + 1
    if cur:
        groups[gid], gid = cur, gid + 1
    for k, g in groups.items():
        for e in g:
            assoc[e] = k
    out = []
    try:
        for x, c in queries:
            x -= 1
            if x in assoc and c != '.':
                group = groups[assoc[x]]
                idx = group.index(x)
                for part in (group[:idx], group[idx + 1:]):
                    if part:
                        groups[gid] = part
                        for e in part:
                            assoc[e] = gid
                        gid += 1
                del groups[assoc[x]]
                del assoc[x]
            elif x not in assoc and c == '.':
                if x - 1 in assoc:
                    group = groups[assoc[x - 1]]
                    group.append(x)
                    assoc[x] = assoc[x - 1]
                    if x + 1 in assoc:
                        old = assoc[x + 1]
                        group += groups[old]
                        for e in groups[old]:
                            assoc[e] = assoc[x - 1]
                        del groups[old]
                elif x + 1 in assoc:
                    assoc[x] = assoc[x + 1]
                else:
                    groups[gid] = [x]
                    assoc[x] = gid
                    gid += 1
            out.append(sum(len(g) - 1 for g in groups.values()))
    except (KeyError, ValueError):
        return None
    return out


MUTANTS = {
    'n=1 prints 1 per query (39752211)': mutant_n1_prints_one,
    'n=1 prints a single 0 and exits (57922619)': mutant_n1_single_line,
    'IndexError assigning period at x=n (57922619)': mutant_last_index,
    'left-edge prepend not stored in run list (60179927)': mutant_unstored_prepend,
    'x=1 reads s[-1] through negative index': mutant_negative_wrap,
    'no check that the old character already had the new class': mutant_no_noop_check,
}


class Recipe570CTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = recipe.extras('570C')

    def test_official_and_samples_match_independent_oracles(self):
        named = [(f'official-{i}', {'input': a, 'output': b}) for i, (a, b) in enumerate(OFFICIAL, 1)]
        samples = [(f'sample-{i}', {'input': a, 'output': b}) for i, (a, b) in enumerate(SAMPLES, 1)]
        self.assertEqual(recipe.review('570C', named, samples), [])
        for text, output in OFFICIAL + SAMPLES:
            data = recipe.parse('570C', text)
            expected = [int(v) for v in output.split()]
            self.assertEqual(recipe.literal_answers(data), expected)
            self.assertEqual(recipe.run_answers(data), expected)

    def test_review_reports_wrong_and_short_outputs(self):
        text, output = OFFICIAL[0]
        failures = recipe.review('570C', [('bad', {'input': text, 'output': '4\n3\n2\n'}),
                                           ('short', {'input': text, 'output': '4 3 1\n'})], [])
        self.assertEqual([f['test'] for f in failures], ['bad', 'short'])

    def test_parse_rejects_constraint_and_layout_violations(self):
        bad = ['', '1 1\n.\n', '1 1\n.\n1 .\n1 .\n', '2 1\n.\n1 .\n', '2 1\n...\n1 .\n', '1 1\nA\n1 .\n',
               '1 1\n.\n0 .\n', '1 1\n.\n2 .\n', '1 1\n.\n01 .\n', '1 1\n.\n+1 .\n', '1 1\n.\n1 ab\n',
               '1 1\n.\n1 . x\n', '1 1\n.\n1 ,\n', '1 0\n.\n', '300001 1\n' + '.' * 300001 + '\n1 .\n',
               '1 2\n.\n1 . 1 .\n', '1 2\n.\n1 .\n\n1 .\n', '2 1\n. .\n1 .\n', '1 1 1\n.\n1 .\n',
               '1 1\n.\n1\n', '1 1\n.\n1 1\n']
        for text in bad:
            with self.subTest(text=text[:40]):
                with self.assertRaises(ValueError):
                    recipe.parse('570C', text)
        self.assertEqual(recipe.parse('570C', '2 1\r\n.a\r\n2 .\r\n'), ('.a', ((2, '.'),)))

    def test_extras_count_layout_and_categories(self):
        self.assertGreaterEqual(len(self.cases), 100)
        counts = Counter(case['category'] for case in self.cases)
        self.assertEqual(set(counts), {'boundary', 'adversarial', 'maxSize'})
        dims = set()
        for case in self.cases:
            self.assertTrue(case['reason'])
            s, queries = recipe.parse('570C', case['input'])
            lines = case['input'].split('\n')
            self.assertEqual(lines[-1], '')
            self.assertEqual(len(lines) - 1, len(queries) + 2)
            self.assertEqual(lines[0], f'{len(s)} {len(queries)}')
            self.assertTrue(all(re.fullmatch(r'[1-9][0-9]* [a-z.]', line) for line in lines[2:-1]))
            self.assertEqual(len(case['output'].splitlines()), len(queries))
            self.assertTrue(case['output'].endswith('\n'))
            dims.add((len(s), len(queries)))
        self.assertIn((300000, 300000), dims)
        self.assertIn((1, 1), dims)
        self.assertIn((1, 300000), dims)
        self.assertIn((300000, 1), dims)

    def test_extras_outputs_agree_with_independent_oracles(self):
        literal = 0
        for case in self.cases:
            data = recipe.parse('570C', case['input'])
            output = [int(v) for v in case['output'].split()]
            self.assertEqual(output, recipe.run_answers(data))
            s, queries = data
            self.assertTrue(all(0 <= v <= len(s) - 1 for v in output))
            if len(s) * len(queries) <= 400:
                self.assertEqual(output, recipe.literal_answers(data))
                literal += 1
            chars = list(s)
            step = max(1, len(queries) // 50)
            for k, (x, c) in enumerate(queries):
                chars[x - 1] = c
                if k % step == 0 or k == len(queries) - 1:
                    self.assertEqual(output[k], pairs_from_scratch(chars))
        self.assertGreaterEqual(literal, 100)

    def test_known_maximum_answers(self):
        by_reason = {case['reason']: case for case in self.cases}
        first = by_reason['maximum n=m all periods, maximum answer 299999 then alternating removals']
        self.assertEqual(first['output'].split()[:2], ['299998', '299998'])
        climb = by_reason['maximum n=m letters turned into one 300000 run, answer climbs to n-1']
        self.assertEqual(climb['output'].split()[-1], '299999')
        last = by_reason['maximum n=300000 with m=1 last-position period']
        self.assertEqual(last['output'], '299999\n')

    def test_minimum_interpretation_equals_forced_first_occurrence(self):
        for n in range(1, 9):
            for s in itertools.product('.a', repeat=n):
                s = ''.join(s)
                self.assertEqual(minimum_any_occurrence(s), recipe.literal_f(s))
                self.assertEqual(recipe.literal_f(s), pairs_from_scratch(s))

    def test_brute_checks(self):
        counts = recipe.brute_checks()
        self.assertEqual(set(counts), {'570C'})
        self.assertGreater(counts['570C'], 10000)

    def test_each_selected_wrong_algorithm_is_killed(self):
        for name, mutant in MUTANTS.items():
            with self.subTest(mutant=name):
                kills = 0
                for case in self.cases:
                    data = recipe.parse('570C', case['input'])
                    if len(data[0]) * len(data[1]) > 10**6 and name.startswith('left-edge'):
                        continue
                    if mutant(data) != [int(v) for v in case['output'].split()]:
                        kills += 1
                self.assertGreater(kills, 0)

    def test_extras_deterministic_across_hash_seeds(self):
        code = ('import hashlib,json,recipe_570C as r;'
                'print(hashlib.sha256(json.dumps(r.extras("570C"),sort_keys=True).encode()).hexdigest())')
        here = str(Path(__file__).resolve().parent)
        digests = {subprocess.run([sys.executable, '-c', code], cwd=here, capture_output=True, text=True, check=True,
                                  env={'PYTHONHASHSEED': seed, 'PATH': '/usr/bin:/bin'}).stdout
                   for seed in ('1', '2')}
        self.assertEqual(len(digests), 1)
        self.assertEqual(digests.pop().strip(),
                         hashlib.sha256(json.dumps(self.cases, sort_keys=True).encode()).hexdigest())


if __name__ == '__main__':
    unittest.main()
