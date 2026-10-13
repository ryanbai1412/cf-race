import hashlib
import itertools
import json
import os
from pathlib import Path
import string
import sys
import tarfile
import unittest

import recipe_59C as recipe


def lookahead_reference(k, template):
    alphabet = set(string.ascii_lowercase[:k])
    domains = []
    for i in range((len(template) + 1) // 2):
        known = set(template[i] + template[-1 - i]) - {'?'}
        if len(known) > 1:
            return 'IMPOSSIBLE'
        domains.append(known or alphabet)
    prefix = []
    for i, domain in enumerate(domains):
        for c in sorted(domain):
            covered = set(prefix + [c])
            mandatory = set().union(*(d for d in domains[i + 1:] if len(d) == 1))
            flexible = sum(len(d) > 1 for d in domains[i + 1:])
            if len(alphabet - covered - mandatory) <= flexible:
                prefix.append(c)
                break
        else:
            return 'IMPOSSIBLE'
    half = ''.join(prefix)
    return half + (half[:-1] if len(template) % 2 else half)[::-1]


class Recipe59CTests(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(recipe.IDS, ('59C',))
        self.assertEqual(set(recipe.SEMANTICS), {'59C'})
        for fn, args in [(recipe.parse, ('1\n?\n',)), (recipe.answer, ((1, '?'),)),
                         (recipe.extras, ()), (recipe.review, ([], []))]:
            with self.assertRaises(ValueError):
                fn('59D', *args)

    def test_valid_layout(self):
        for text, data in [('1\n?', (1, '?')), ('26\r\n' + '?' * 100 + '\r\n', (26, '?' * 100)),
                           (' 2 \n abba \n', (2, 'abba')), ('02\n??\n', (2, '??'))]:
            self.assertEqual(recipe.parse('59C', text), data)

    def test_invalid_inputs(self):
        for text in ['', '1 ?', '1\n\n?', '\n1\n?', '1\n?\n\n', '1\n?\na',
                     '1 2\n?', '1\n? a', '+1\n?', '1_0\n?', '１\n?', '0\n?',
                     '-1\n?', '27\n?', '1\n', '1\nb', '2\nA', '26\n0',
                     '1\n' + '?' * 101, '1\n?\x00']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                recipe.parse('59C', text)

    def test_known_answers(self):
        for k, word, expected in [(3, 'a?c', 'IMPOSSIBLE'), (2, 'a??a', 'abba'),
                                  (2, '?b?a', 'abba'), (2, '???', 'aba'),
                                  (2, '?a?', 'bab'), (3, '??b??', 'acbca'),
                                  (2, '??????', 'aabbaa'), (3, '???????', 'aabcbaa'),
                                  (1, '?', 'a'), (2, '?', 'IMPOSSIBLE'),
                                  (3, 'ab?ba', 'abcba'), (2, 'aaaa', 'IMPOSSIBLE')]:
            self.assertEqual(recipe.answer('59C', (k, word)), [expected])

    def test_real_brute_checks(self):
        self.assertEqual(recipe.brute_checks(), {'59C': 6978})

    def test_separate_reference_matches_literal_enumeration(self):
        for k in range(1, 4):
            for length in range(1, 5):
                for template in itertools.product(string.ascii_lowercase[:k] + '?', repeat=length):
                    word = ''.join(template)
                    self.assertEqual(lookahead_reference(k, word), recipe._literal_brute(k, word))

    def test_generated_pairs(self):
        cases = recipe.extras('59C')
        self.assertEqual(cases, recipe.extras('59C'))
        self.assertEqual(len(cases), 160)
        self.assertEqual(len({p['input'] for p in cases}), 160)
        self.assertEqual({p['category'] for p in cases}, {'boundary', 'adversarial', 'maxSize'})
        self.assertTrue(any(len(recipe.parse('59C', p['input'])[1]) == 100 for p in cases))
        for pair in cases:
            k, word = recipe.parse('59C', pair['input'])
            self.assertEqual(set(pair), {'input', 'output', 'reason', 'category'})
            self.assertEqual(pair['output'].split(), recipe.answer('59C', (k, word)))
            self.assertEqual(pair['output'], lookahead_reference(k, word) + '\n')
            self.assertTrue(pair['reason'])
            if len(word) <= 9 and word.count('?') <= 5:
                self.assertEqual(pair['output'], recipe._literal_brute(k, word) + '\n')
        self.assertEqual(recipe.review('59C', list(enumerate(cases)), []), [])

    def test_review_preserves_pairs_and_reports_errors(self):
        pairs = [('bad-layout', {'input': '2 ???\n', 'output': 'aba\n'}),
                 ('wrong-title', {'input': '2\n??????\n', 'output': 'abaaba\n'}),
                 ('missing-output', {'input': '1\n?\n'}),
                 ('wrong-case', {'input': '2\n?\n', 'output': 'impossible\n'})]
        original = json.dumps(pairs)
        self.assertEqual(len(recipe.review('59C', pairs, [])), 4)
        self.assertEqual(json.dumps(pairs), original)
        self.assertEqual(recipe.review('59C', [], [('crlf', {'input': '2\r\n???\r\n', 'output': 'aba\r\n'})]), [])

    @unittest.skipUnless(os.environ.get('CF59C_INPUT_ARCHIVE'), 'set CF59C_INPUT_ARCHIVE to the pinned author input')
    def test_all_imported_pairs_and_bindings(self):
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
        from pool_contract import digest
        archive = Path(os.environ['CF59C_INPUT_ARCHIVE'])
        self.assertEqual(hashlib.sha256(archive.read_bytes()).hexdigest(),
                         'b5d674a6b75b1a5faeaccb187f45c787b70c71508f2e00a3fff922298761d98f')
        with tarfile.open(archive) as tar:
            raw = tar.extractfile('inputs/59C.json').read()
            manifest = json.load(tar.extractfile('inputs/MANIFEST.json'))
        self.assertEqual(manifest['files']['inputs/59C.json'],
                         {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
        data = json.loads(raw)
        row = data['sourceRow']
        self.assertEqual(data['sourceRowHash'], digest(row))
        self.assertEqual(len(row['official_tests']), 76)
        self.assertEqual(len(row['examples']), 3)
        original = digest(data)
        tests = [(f'tests/{i:04d}', p) for i, p in enumerate(row['official_tests'], 1)]
        samples = [(f'samples/{i:04d}', p) for i, p in enumerate(row['examples'], 1)]
        self.assertEqual(recipe.review('59C', tests, samples), [])
        for _, pair in tests + samples:
            k, word = recipe.parse('59C', pair['input'])
            self.assertEqual(pair['output'].split(), [lookahead_reference(k, word)])
        self.assertEqual(digest(data), original)


if __name__ == '__main__':
    unittest.main()
