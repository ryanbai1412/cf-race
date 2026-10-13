import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import unittest

import recipe_343B as recipe


BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1]))
from pool_contract import digest


def signed_reference(word):
    plus_even = word[::2].count('+')
    plus_odd = word[1::2].count('+')
    return 'Yes' if len(word) % 2 == 0 and plus_even == plus_odd else 'No'


class Recipe343BTests(unittest.TestCase):
    def test_interface_and_original_examples(self):
        self.assertEqual(recipe.IDS, ('343B',))
        self.assertEqual(set(recipe.SEMANTICS), {'343B'})
        for text, expected in [('-++-', 'Yes'), ('+-', 'No'), ('++', 'Yes'), ('-', 'No')]:
            with self.subTest(text=text):
                self.assertEqual(recipe.answer('343B', recipe.parse('343B', text)), [expected])

    def test_exact_one_line_layout_and_bounds(self):
        for ending in ('', '\n', '\r\n'):
            self.assertEqual(recipe.parse('343B', '+' + ending), '+')
            self.assertEqual(len(recipe.parse('343B', '-' * 100000 + ending)), 100000)
        for text in ('', '\n', ' ', ' +', '+ ', '+ -', '+\n-', '2\n++\n',
                     '+\n\n', '+\r', '++\t', '−', '+0', '+' * 100001):
            with self.subTest(text=text[:40]):
                with self.assertRaises(ValueError):
                    recipe.parse('343B', text)

    def test_foreign_pid_is_rejected(self):
        for call in (lambda: recipe.parse('343A', '++'),
                     lambda: recipe.answer('343A', '++'),
                     lambda: recipe.extras('343A'),
                     lambda: recipe.review('343A', [], [])):
            with self.assertRaises(ValueError):
                call()

    def test_real_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'343B': 4518})

    def test_every_authored_pair_is_valid_and_independently_checked(self):
        cases = recipe.extras('343B')
        self.assertEqual(len(cases), 168)
        self.assertEqual(len({pair['input'] for pair in cases}), 168)
        self.assertEqual(recipe.extras('343B'), cases)
        for pair in cases:
            with self.subTest(size=len(pair['input'])):
                self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
                self.assertIn(pair['category'], ('boundary', 'adversarial', 'maxSize'))
                self.assertTrue(pair['reason'])
                self.assertEqual(len(pair['input'].splitlines()), 1)
                word = recipe.parse('343B', pair['input'])
                self.assertEqual(pair['output'], signed_reference(word) + '\n')
                self.assertEqual(pair['output'].split(), recipe.answer('343B', word))
                if len(word) <= 18:
                    self.assertEqual(pair['output'].strip(),
                                     'Yes' if recipe._deletion_search(word) else 'No')
        recipe._deletion_search.cache_clear()
        max_cases = [p for p in cases if p['category'] == 'maxSize']
        self.assertEqual(len(max_cases), 5)
        self.assertTrue(all(len(recipe.parse('343B', p['input'])) == 100000 for p in max_cases))
        self.assertEqual({p['output'].strip() for p in max_cases}, {'Yes', 'No'})
        self.assertEqual({p['input'].strip() for p in cases if len(p['input'].strip()) == 1}, {'+', '-'})

    def test_shortcut_counterexamples_are_real(self):
        cases = {p['input'].strip(): p['output'].strip() for p in recipe.extras('343B')}
        word = '++--'
        palindrome_shortcut = len(word) % 2 == 0 and word == word[::-1]
        self.assertFalse(palindrome_shortcut)
        self.assertEqual(cases[word], 'Yes')
        word = '+-+-++'
        endpoint_shortcut = len(word) % 2 == 0 and word[0] == word[-1]
        count_shortcut = word.count('+') % 2 == 0 and word.count('-') % 2 == 0
        self.assertTrue(endpoint_shortcut)
        self.assertTrue(count_shortcut)
        self.assertEqual(cases[word], 'No')
        word = '+-++-+'
        one_pass = ''.join(word[i:i + 2] for i in range(0, len(word), 2)
                           if word[i] != word[i + 1])
        self.assertNotEqual(one_pass, '')
        self.assertEqual(cases[word], 'Yes')
        word = '+--+'
        self.assertNotEqual(word[0], word[1])
        self.assertEqual(cases[word], 'Yes')

    def test_review_preserves_bad_pairs_and_continues(self):
        pairs = [('layout', {'input': '+\n+\n', 'output': 'Yes\n'}),
                 ('wrong', {'input': '++\r\n', 'output': 'No\r\n'}),
                 ('extra-token', {'input': '++\n', 'output': 'Yes Yes\n'}),
                 ('ok', {'input': '+-\r\n', 'output': 'No\r\n'})]
        before = json.dumps(pairs)
        failures = recipe.review('343B', pairs, [('sample', {'input': '-', 'output': 'No'})])
        self.assertEqual([f['test'] for f in failures], ['layout', 'wrong', 'extra-token'])
        self.assertEqual(json.dumps(pairs), before)

    def test_hash_seed_determinism(self):
        command = [sys.executable, '-c',
                   'import json, recipe_343B; print(json.dumps(recipe_343B.extras("343B"), sort_keys=True))']
        outputs = [subprocess.check_output(command, cwd=BASE,
                                          env={**os.environ, 'PYTHONHASHSEED': seed})
                   for seed in ('1', '937')]
        self.assertEqual(outputs[0], outputs[1])

    @unittest.skipUnless(os.environ.get('CF_RECIPE_INPUT_ARCHIVE'), 'set CF_RECIPE_INPUT_ARCHIVE for pinned inputs')
    def test_pinned_source_hashes_and_every_upstream_pair(self):
        archive = Path(os.environ['CF_RECIPE_INPUT_ARCHIVE'])
        report = json.loads((BASE / 'recipe-reports' / '343B.json').read_text())
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(), report['input']['archiveSha256'])
        with tarfile.open(archive) as tar:
            manifest_bytes = tar.extractfile('inputs/MANIFEST.json').read()
            manifest = json.loads(manifest_bytes)
            original_bytes = tar.extractfile('inputs/343B.json').read()
        source = json.loads(original_bytes)
        self.assertEqual(hashlib.sha256(manifest_bytes).hexdigest(), report['input']['manifestSha256'])
        self.assertEqual(len(original_bytes), manifest['files']['inputs/343B.json']['bytes'])
        self.assertEqual(hashlib.sha256(original_bytes).hexdigest(), manifest['files']['inputs/343B.json']['sha256'])
        self.assertEqual(hashlib.sha256(original_bytes).hexdigest(), report['input']['fileSha256'])
        self.assertEqual(digest(source['sourceRow']), source['sourceRowHash'])
        self.assertEqual(source['sourceRowHash'], report['input']['sourceRowHash'])
        self.assertEqual(source['pins'], manifest['pins'])
        self.assertEqual(source['pins'], report['input']['pins'])
        row = source['sourceRow']
        before = digest(source)
        tests = [(f'official-{i:04d}', p) for i, p in enumerate(row['official_tests'], 1)]
        samples = [(f'sample-{i:04d}', p) for i, p in enumerate(row['examples'], 1)]
        self.assertEqual(recipe.review('343B', tests, samples), report['upstreamReview']['failedPairs'])
        self.assertEqual(len(tests), 45)
        self.assertEqual(len(samples), 4)
        for _, pair in itertools.chain(tests, samples):
            word = recipe.parse('343B', pair['input'])
            self.assertEqual(pair['output'].split(), [signed_reference(word)])
        self.assertEqual(digest(source), before)
        self.assertEqual(digest(row['official_tests']), report['upstreamReview']['officialPairsHash'])
        self.assertEqual(digest(row['examples']), report['upstreamReview']['samplePairsHash'])


if __name__ == '__main__':
    unittest.main()
