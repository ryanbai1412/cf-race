import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import normalize_statement
import run_pool
from pool_contract import digest, manifest, read_json, write_json
from pool_sources import PINS, sha_file


class SourcePolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.base_patch = patch.object(run_pool, 'BASE', self.base)
        self.base_patch.start()
        self.addCleanup(self.base_patch.stop)
        (self.base / 'submissions' / 'selected').mkdir(parents=True)
        (self.base / 'source-policies').mkdir()
        (self.base / 'collect_submissions.py').write_text('fixture')
        self.rows = [{'problem_id': '888/D', 'provenance': 'pinned-shard',
                      'submission_id': i, 'source': f'fixture {i}', 'verdict': 'WRONG_ANSWER'}
                     for i in range(1, 7)]
        write_json(self.base / 'inventory.json', {'fixture': True})
        write_json(self.base / 'submissions' / 'selected' / '888D.json', self.rows)
        write_json(self.base / 'submission-report.json', {
            'pins': PINS, 'inventoryHash': digest(read_json(self.base / 'inventory.json')),
            'recipeHash': sha_file(self.base / 'collect_submissions.py'),
            'files': {'888D.json': sha_file(self.base / 'submissions' / 'selected' / '888D.json')},
            'sourceFiles': {'pinned-shard': {'fixture': True}}})
        self.exclusion = {'submissionId': 1, 'sourceHash': hashlib.sha256(b'fixture 1').hexdigest(),
                          'reason': 'Known nonalgorithmic fixture rejection'}

    def policy(self, pid='888D', exclusions=None):
        write_json(self.base / 'source-policies' / '888D.json', {
            'id': pid, 'exclusions': [self.exclusion] if exclusions is None else exclusions})

    def select(self):
        return run_pool.selected_submissions('888/D', 'unused')[0]

    def test_canonical_alias_preserves_pinned_original(self):
        self.policy()
        before = sha_file(self.base / 'submissions' / 'selected' / '888D.json')
        self.assertEqual([r['submission_id'] for r in self.select()], [2, 3, 4, 5, 6])
        self.assertEqual(before, sha_file(self.base / 'submissions' / 'selected' / '888D.json'))

    def test_foreign_identity_is_blocked(self):
        self.policy(pid='235A')
        with self.assertRaisesRegex(ValueError, 'identity mismatch'):
            self.select()

    def test_tampered_source_binding_is_blocked(self):
        self.exclusion['sourceHash'] = '0' * 64
        self.policy()
        with self.assertRaisesRegex(ValueError, 'unbound source exclusion'):
            self.select()

    def test_missing_or_duplicate_exclusion_is_blocked(self):
        for exclusions in ([{**self.exclusion, 'submissionId': 10}], [self.exclusion] * 2):
            with self.subTest(exclusions=exclusions):
                self.policy(exclusions=exclusions)
                with self.assertRaisesRegex(ValueError, 'unbound source exclusion'):
                    self.select()


class StatementNormalizationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.base_patch = patch.object(normalize_statement, 'BASE', self.base)
        self.base_patch.start()
        self.addCleanup(self.base_patch.stop)
        self.package = self.base / 'packages' / '235A'
        (self.package / 'tests').mkdir(parents=True)
        (self.base / 'state' / '235A').mkdir(parents=True)
        (self.base / 'statement-sources').mkdir()
        (self.package / 'statement.html').write_text('<p>n (1 ≤ n ≤ 106)</p>')
        (self.package / 'tests' / '0001.in').write_bytes(b'9\r\n')
        (self.package / 'tests' / '0001.out').write_bytes(b'504\r\n')
        write_json(self.package / 'provenance.json', {'fixture': True})
        write_json(self.base / 'state' / '235A' / 'source-row.json', {'original': '≤ 106'})
        self.state = self.base / 'state' / '235A' / 'generate.json'
        self.bind()
        self.source = self.base / 'statement-sources' / '235A.json'
        write_json(self.source, {'id': '235A', 'content': {'locale': 'en', 'formatI': '10^{6}'},
                                'sourceUrl': 'https://example.com/fixture'})

    def bind(self):
        write_json(self.state, {'packageHash': digest(manifest(self.package))})

    def test_idempotent_normalization_preserves_original_and_test_bytes(self):
        original = (self.package / 'statement.html').read_bytes()
        source_row = (self.base / 'state' / '235A' / 'source-row.json').read_bytes()
        tests = {p.name: p.read_bytes() for p in (self.package / 'tests').iterdir()}
        result = normalize_statement.normalize('235A')
        self.assertEqual(result['status'], 'normalized-reexecution-required')
        self.assertEqual(result['packageHash'], digest(manifest(self.package)))
        self.assertEqual(original, (self.base / 'statement-sources' / '235A.original.html').read_bytes())
        self.assertEqual(source_row, (self.base / 'state' / '235A' / 'source-row.json').read_bytes())
        self.assertEqual(tests, {p.name: p.read_bytes() for p in (self.package / 'tests').iterdir()})
        after = manifest(self.package)
        self.assertEqual(normalize_statement.normalize('235A')['status'], 'already-normalized')
        self.assertEqual(after, manifest(self.package))

    def test_missing_attestation_is_blocked(self):
        write_json(self.source, {'id': '235A', 'content': {'locale': 'en', 'formatI': '106'}})
        with self.assertRaisesRegex(ValueError, 'attestation absent'):
            normalize_statement.normalize('235A')

    def test_ambiguous_replacement_is_blocked(self):
        (self.package / 'statement.html').write_text('≤ 106) ≤ 106)')
        self.bind()
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            normalize_statement.normalize('235A')

    def test_changed_package_is_blocked(self):
        (self.package / 'tests' / '0001.out').write_bytes(b'wrong')
        with self.assertRaisesRegex(ValueError, 'changed package'):
            normalize_statement.normalize('235A')


if __name__ == '__main__':
    unittest.main()
