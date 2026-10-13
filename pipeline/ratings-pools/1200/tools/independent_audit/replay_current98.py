import base64
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def sha(path):
    result = hashlib.sha256()
    with path.open('rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            result.update(block)
    return result.hexdigest()


def members(tar):
    seen = set()
    total = 0
    for member in tar:
        name = Path(member.name)
        assert not name.is_absolute() and '..' not in name.parts and '\\' not in member.name
        assert member.name not in seen and (member.isfile() or member.isdir())
        seen.add(member.name)
        total += member.size
        assert len(seen) <= 120000 and total <= 8 * 1024**3 and member.size <= 2 * 1024**3
        yield member


def restore_or_compare(archive, target, restore=False):
    total = 0
    with tarfile.open(archive) as tar:
        for member in members(tar):
            destination = target / member.name
            assert not any(p.is_symlink() for p in [destination, *destination.parents])
            if member.isdir():
                if restore:
                    destination.mkdir(parents=True, exist_ok=True)
                continue
            stream = tar.extractfile(member)
            if restore and not destination.exists():
                destination.parent.mkdir(parents=True, exist_ok=True)
                with destination.open('xb') as output:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        output.write(block)
            else:
                assert destination.is_file() and destination.stat().st_size == member.size
                h = hashlib.sha256()
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    h.update(block)
                assert sha(destination) == h.hexdigest(), destination
            total += 1
    return total


def main():
    metadata = read(ROOT / 'ARCHIVE-MANIFEST.json')
    for name, record in metadata['files'].items():
        relative = Path(name)
        assert not relative.is_absolute() and '..' not in relative.parts
        path = ROOT / relative
        assert path.is_file() and not path.is_symlink()
        assert path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], name
    print('WHOLE CURRENT MANIFEST VERIFIED', len(metadata['files']), flush=True)
    originals = read(ROOT / 'SOURCE-ARCHIVES.json')
    for item in originals:
        path = ROOT / item['path']
        assert sha(path) == item['sha256'] and path.stat().st_size == item['bytes']
        if item.get('extractedPath'):
            n = restore_or_compare(path, ROOT / item['extractedPath'], item['scope'] == 'original60')
            print('IMMUTABLE SOURCE ARCHIVE VERIFIED', item['scope'], n, flush=True)
    original = ROOT / 'original60'
    subprocess.run([sys.executable, str(original / 'replay_repro.py')], check=True)
    b = ROOT / 'batch3'
    bundle = next(item for item in originals if item['scope'] == 'builder-new38')
    nested = 0
    source_bindings = 0
    selected_sources = {'1200/state/' + pid + '/sources/' + str(s['submissionId']) + '.json'
                        for pid in read(b / 'parent-replay.json')['packages']
                        for s in read(b / '1200/evidence' / (pid + '.json'))['submissions']}
    with tarfile.open(ROOT / bundle['path']) as outer:
        for member in members(outer):
            if not member.isfile() or not member.name.endswith('.tar.gz'):
                continue
            with tarfile.open(fileobj=io.BytesIO(outer.extractfile(member).read())) as tar:
                for inner in members(tar):
                    if not inner.isfile():
                        continue
                    name = inner.name
                    if name.startswith(('1200/packages/', '1200/evidence/')) or ('/sources/' in name and name.startswith('1200/state/')):
                        data = tar.extractfile(inner).read()
                        assert (b / name).read_bytes() == data, name
                        source_bindings += name in selected_sources
            nested += 1
    assert nested == 38 and source_bindings == 380
    print('IMMUTABLE BUILDER38 NESTED PACKAGES/EVIDENCE/380 SOURCES VERIFIED', flush=True)
    expected = {name: (b / name).read_bytes() for name in ['parent-replay.json', 'parent-math.json', 'parent-stages.json']}
    audits = {p.name: p.read_bytes() for p in (b / '1200/audits').glob('*.json')}
    for name in ['parent_replay.py', 'parent_math.py', 'parent_stages.py']:
        subprocess.run([sys.executable, str(b / name)], check=True)
    for name, data in expected.items():
        assert (b / name).read_bytes() == data, ('nonreproducible replay', name)
    assert audits == {p.name: p.read_bytes() for p in (b / '1200/audits').glob('*.json')}
    sys.path.insert(0, str(ROOT / 'trusted-pipeline'))
    from pool_contract import digest, manifest, publication_gate
    from pool_sandbox import EXECUTION_VERSION, COMPILER_FLAGS, IMAGE
    samples = read(b / 'parent-samples.json')
    assert samples['executionVersion'] == EXECUTION_VERSION and samples['compilerFlags'] == COMPILER_FLAGS and samples['image'] == IMAGE
    sample_suites = 0
    failures = []
    for pid, rows in samples['packages'].items():
        evidence = read(b / '1200/evidence' / (pid + '.json'))
        assert len(rows) == 6
        accepted = {str(s['submissionId']): s['sourceHash'] for s in evidence['submissions'] if s['expected'] == 'OK'}
        assert {r['submissionId'] for r in rows} == set(accepted) | {'oracle'}
        package = b / '1200/packages' / pid
        oracle = package / 'qualification/oracle.py'
        if not oracle.exists():
            oracle = package / 'qualification/oracle.cpp'
        accepted['oracle'] = sha(oracle)
        tests = [{'name': 'sample-' + p.stem, 'inputSha256': sha(p), 'inputBytes': p.stat().st_size,
                  'expectedSha256': sha(p.with_suffix('.out')), 'expectedBytes': p.with_suffix('.out').stat().st_size}
                 for p in sorted((package / 'samples').glob('*.in'))]
        for row in rows:
            log = b / row['log']
            assert sha(log) == row['logSha256'] and row['sourceHash'] == accepted[row['submissionId']]
            data = read(log)
            assert data['sourceHash'] == row['sourceHash'] and row['exactSampleByteManifest'] == tests
            result = data['result']
            assert result['executionVersion'] == EXECUTION_VERSION and result['compilerFlags'] == COMPILER_FLAGS
            assert result['compiled'] and result['verdict'] == row['verdict']
            assert result['testsRun'] == len(result['runs']) == len(tests)
            assert [r['test'] for r in result['runs']] == [t['name'] for t in tests]
            for run in result['runs']:
                output = base64.b64decode(run['output'], validate=True)
                assert hashlib.sha256(output).hexdigest() == run['outputHash']
                if row['verdict'] == 'AC':
                    assert run['exitCode'] == 0 and not run['timeout'] and run['verdict'] == 'AC'
            if row['verdict'] != 'AC':
                failures.append((pid, row['submissionId']))
                assert row['verdict'] == 'RE' and all(r['exitCode'] == -6 and not r['timeout'] and 'std::bad_alloc' in r['stderr'] for r in result['runs'])
            sample_suites += 1
    assert sample_suites == 228 and failures == [('514A', '9830350')]
    assert (b / '1200/packages/514A/samples/0001.in').read_bytes() == b'27'
    assert (b / '1200/packages/514A/samples/0002.in').read_bytes() == b'4545'
    print('EXACT ORIGINAL SAMPLE SUITES VERIFIED:228 /227AC /1KNOWN QUARANTINED RE', flush=True)
    ledger = read(ROOT / 'CURRENT98-SIGNOFF-LEDGER.json')
    aggregate = read(ROOT / 'CURRENT98-AGGREGATE.json')
    assert len(ledger['rows']) == len({r['id'] for r in ledger['rows']}) == 98
    states = {'qualified': 0, 'rejected': 0, 'held': 0}
    sources = 0
    wrong_sources = 0
    genuine = 0
    empty = ROOT / 'empty-publication-approval.json'
    empty.write_text('{}\n')
    for row in ledger['rows']:
        state = row['technicalState']
        states[state] += 1
        work = b if row['packagePath'].startswith('batch3/') else original
        package = ROOT / row['packagePath']
        assert digest(manifest(package)) == row['packageHash']
        evidence = read(ROOT / row['evidencePath'])
        assert digest(evidence) == row['evidenceHash']
        references = {str(s['submissionId']): s for s in evidence['submissions']}
        audit = read(ROOT / row['auditPath'])
        assert digest(audit) == row['auditHash'] and sha(ROOT / row['auditPath']) == row['auditFileSha256']
        assert not row['publicationApproved'] and not row['published']
        assert state != 'qualified' or audit['approved']
        for s in row['sources']:
            source = read(work / '1200/state' / row['id'] / 'sources' / (str(s['submissionId']) + '.json'))
            assert hashlib.sha256(source['code'].encode()).hexdigest() == s['sourceHash']
            sources += 1
            wrong_sources += references[str(s['submissionId'])]['expected'] != 'OK'
            genuine += bool(s['algorithmicWrongCounts'])
        try:
            publication_gate(package, work, require_approval=False)
        except ValueError:
            assert state != 'qualified', row['id']
        else:
            assert state == 'qualified', row['id']
        if state == 'qualified':
            try:
                publication_gate(package, work, approval_path=empty, require_approval=True)
            except ValueError as error:
                assert 'explicit content-bound publication approval required' in str(error)
            else:
                raise AssertionError('Empty approval accepted: ' + row['id'])
    assert states == {'qualified': 34, 'rejected': 63, 'held': 1}
    assert sources == 980 and wrong_sources == 490 and genuine == 337
    assert ledger['rightsHoldIds'] == ['63B'] and ledger['semanticHoldIds'] == ['817A'] and not ledger['publicationReadyIds']
    assert aggregate['validatedCount'] == 34 and aggregate['shortfall'] == 66 and not aggregate['targetReached']
    mathematics = read(b / 'parent-math.json')
    assert (mathematics['count'], mathematics['qualifiedCases'], mathematics['heldCases'], mathematics['rejectedCases']) == (90, 80, 5, 5)
    assert ledger['counts']['mathematicalQualificationCounterexamplesChecked'] == 170
    assert len(aggregate['publicationApprovalRejections']) == 34
    print('CURRENT98 REPLAY PASSED:34TECHNICAL /63REJECTED /1HELD /0PUBLICATION;980SOURCE BINDINGS/490SEMANTIC RECORDS/337GENUINE/153EXCLUDED/180MATHCASES;ALL34 EMPTY APPROVAL GATES REJECT', flush=True)


if __name__ == '__main__':
    assert not os.environ.get('CF_RATING1200_BATCH3_ROOT'), 'Unset workspace override for portable immutable replay'
    main()
