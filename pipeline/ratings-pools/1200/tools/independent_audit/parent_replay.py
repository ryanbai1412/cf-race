import base64
import hashlib
import json
import os
import sys
from pathlib import Path

BASE = Path(os.environ.get('CF_RATING1200_BATCH3_ROOT', Path(__file__).resolve().parent)).resolve()
REPO = next((p for p in Path(__file__).resolve().parents if (p / 'pipeline/pool_contract.py').is_file()), Path('/home/ubuntu/repos/cf-race'))
sys.path.insert(0, str(BASE.parent / 'trusted-pipeline' if (BASE.parent / 'trusted-pipeline').is_dir() else REPO / 'pipeline'))
from pool_contract import digest, manifest, publication_gate
from pool_sandbox import EXECUTION_VERSION, COMPILER_FLAGS


def read(p):
    return json.loads(p.read_bytes())


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pick(d, *keys):
    for k in keys:
        if k in d:
            return d[k]
    raise KeyError(keys)


def resolve(root, name):
    p = Path(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    roots = [root, root / 'run', root / 'semantic']
    candidates = [r / p for r in roots if (r / p).is_file()]
    if not candidates and len(p.parts) == 3 and p.parts[0] == 'archive':
        mapped = root / p.parts[1] / 'execution' / p.parts[2]
        if mapped.is_file():
            candidates.append(mapped)
    assert candidates, (root, name)
    assert len({sha(p.read_bytes()) for p in candidates}) == 1
    return candidates[0]


def checked(root, path, expected):
    p = resolve(root, path)
    assert sha(p.read_bytes()) == expected, (p, expected)
    return p


def audit_file(root, i, pid):
    if i == 3:
        return root / 'semantic/new-audits' / (pid + '.json')
    if i == 6:
        return root / pid / 'audit.current.json'
    prefix = 'workspace/1200' if i == 2 else '1200'
    return root / prefix / 'audits' / (pid + '.json')


def verify():
    assignments = read(BASE.parent / 'batch3-assignments.json')
    print('ASSIGNMENT_SCHEMA', type(assignments).__name__, flush=True)
    groups = [['151B','344B','47B','514A','552B','55A','560B'],
              ['592A','732C','743A','743B','765C','774C','779C'],
              ['787A','79A','803B','811B','812A','817A'],
              ['854B','870B','875A','879B','892B','895A'],
              ['902B','903C','911B','913B','914B','928A'],
              ['931B','958C1','960A','985B','990B','998B']]
    result = {'executionVersion': 2, 'publicationApproved': 0, 'packages': {},
              'sourceBindings': 0, 'semanticRecords': 0, 'genuineRecords': 0,
              'primaryWitnesses': [], 'acceptedSourceWarnings': []}
    sample_record = read(BASE / 'parent-samples.json')
    (BASE / '1200/audits').mkdir(exist_ok=True)
    for i, ids in enumerate(groups, 1):
        root = next((BASE / f'current-child-{i}').iterdir())
        for pid in ids:
            path = audit_file(root, i, pid)
            a = read(path)
            pkg = BASE / '1200/packages' / pid
            e = read(BASE / '1200/evidence' / (pid + '.json'))
            assert digest(manifest(pkg)) == a['packageHash'] == e['packageHash'], pid
            assert digest(e) == a['evidenceHash'], pid
            assert e['sandbox']['executionVersion'] == EXECUTION_VERSION
            src = {str(s['submissionId']): s for s in e['submissions']}
            assert len(src) == 10
            wrong = {sid: s for sid, s in src.items() if s['expected'] != 'OK'}
            assert len(wrong) == 5 and set(wrong) == set(a['incorrectAnalysis']), pid
            for sid, s in src.items():
                meta = read(BASE / '1200/state' / pid / 'sources' / (sid + '.json'))
                assert sha(meta['code'].encode()) == s['sourceHash'], (pid, sid)
                result['sourceBindings'] += 1
                if s['expected'] == 'OK' and 'int x[0]' in meta['code']:
                    result['acceptedSourceWarnings'].append({'id': pid, 'submissionId': sid,
                        'sourceHash': s['sourceHash'], 'reason': 'zero-length global x[0] followed by x[0]/x[1] writes and reads; undefined behavior; no observed contradiction is not proof of source validity'})
            genuine = 0
            for sid, row in a['incorrectAnalysis'].items():
                review = row['semanticReview']
                code = read(BASE / '1200/state' / pid / 'sources' / (sid + '.json'))['code']
                source_hash = sha(code.encode())
                assert review['sourceHash'] == source_hash == wrong[sid]['sourceHash']
                for key in ['implementedAlgorithm', 'faultyLogic', 'excludedNonAlgorithmicCauses']:
                    assert isinstance(review[key], str) and review[key].strip(), (pid, sid, key)
                lines = code.splitlines()
                for excerpt in pick(review, 'sourceLines', 'faultySourceLines'):
                    start, end = excerpt['start'], excerpt['end']
                    assert 1 <= start <= end <= len(lines)
                    assert '\n'.join(lines[start - 1:end]) == excerpt['code'], (pid, sid)
                counted = row['kind'] == 'wrong-answer'
                assert not counted or review['algorithmicWrong'], (pid, sid)
                result['semanticRecords'] += 1
                if not counted:
                    continue
                c = review['counterexample']
                raw = pick(c, 'validLFInput', 'validLF', 'input', 'validLfInput').encode()
                ih = sha(raw)
                assert b'\r' not in raw and ih == pick(c, 'validLFInputSha256', 'inputSHA256', 'inputHash', 'validLfInputSha256')
                test = pick(c, 'test', 'includedTest')
                assert isinstance(test, str)
                f = pkg / ('samples' if test.startswith('sample-') else 'tests') / (test.removeprefix('sample-') + '.in')
                assert raw == f.read_bytes().replace(b'\r\n', b'\n'), (pid, sid, test)
                constraints = pick(c, 'constraintsExplanation', 'constraints', 'constraintValidity')
                assert constraints
                assert pick(c, 'mathematicalDerivation', 'derivation').strip()
                correct, actual = str(c['correctAnswer']), str(c['actualAnswer'])
                assert correct.split() == f.with_suffix('.out').read_text().split(), (pid, sid)
                assert correct.lower().split() != actual.lower().split(), (pid, sid, 'case-only')
                log = c.get('executionLog') or c.get('proof') or review.get('lfExecution')
                if isinstance(log, str):
                    log = {'path': log, 'sha256': c['executionLogSha256']}
                if not log:
                    log = {'path': pick(c, 'executionLogPath', 'proofLog'),
                           'sha256': pick(c, 'executionLogSha256', 'proofLogHash')}
                log_path = checked(root, log['path'], log['sha256'])
                data = read(log_path)
                if 'identity' in data:
                    assert sha(data['identity']['code'].encode()) == source_hash
                if 'result' in data:
                    data = data['result']
                assert data['executionVersion'] == EXECUTION_VERSION and data['compilerFlags'] == COMPILER_FLAGS
                assert data['testsRun'] == len(data['runs']) and data.get('compiled', True)
                oh = pick(c, 'actualOutputHash', 'outputHash', 'actualOutputSha256')
                matches = [r for r in data['runs'] if r['outputHash'] == oh and
                           (r.get('test') in [test, test + '-LF', 'LF-' + test, 'lf-' + test] or len(data['runs']) == 1)]
                assert matches, (pid, sid, log_path, test)
                r = matches[0]
                assert r['exitCode'] == 0 and not r.get('timeout') and r['verdict'] == 'WA', (pid, sid)
                output = base64.b64decode(r['output'], validate=True)
                assert sha(output) == oh and output.decode().split() == actual.split()
                receipt = c.get('sourceBoundReceipt') or c.get('sourceBindingReceipt')
                if isinstance(receipt, str):
                    receipt = {'path': receipt, 'sha256': pick(c, 'sourceBoundReceiptHash', 'sourceBindingReceiptSha256')}
                if not receipt and 'sourceBoundReceiptPath' in c:
                    receipt = {'path': c['sourceBoundReceiptPath'], 'sha256': c['sourceBoundReceiptSha256']}
                binding_paths = []
                if receipt:
                    rp = checked(root, receipt['path'], receipt['sha256'])
                    binding = read(rp)
                    serialized = json.dumps(binding)
                    assert all(h in serialized for h in [source_hash, ih, oh, log['sha256']]), (pid, sid, 'receipt binding')
                    binding_paths.append(str(rp.relative_to(BASE)))
                else:
                    source_file = review.get('sourceFile')
                    if not source_file:
                        rec = log['receipt']
                        source_file = {'path': rec['sourcePath'], 'sha256': rec['sourceFileSha256']}
                        summary = checked(root, rec['summaryPath'], rec['summarySha256'])
                        assert source_hash in json.dumps(read(summary)), (pid, sid)
                        binding_paths.append(str(summary.relative_to(BASE)))
                    sp = checked(root, source_file['path'], source_file['sha256'])
                    assert sp.read_bytes() == code.encode() and sha(sp.read_bytes()) == source_hash, (pid, sid)
                    binding_paths.append(str(sp.relative_to(BASE)))
                witness = {'id': pid, 'submissionId': sid, 'sourceHash': source_hash,
                           'test': test, 'inputHash': ih, 'outputHash': oh,
                           'executionLog': str(log_path.relative_to(BASE)), 'executionLogSha256': log['sha256'],
                           'sourceBindingPaths': binding_paths, 'normalExit': True,
                           'diagnosticCopyPrimary': False, 'caseOnly': False,
                           'recordedFailedTest': wrong[sid]['failedTest']}
                result['primaryWitnesses'].append(witness)
                genuine += 1
            assert not a['approved'] or genuine == 5, pid
            (BASE / '1200/audits' / (pid + '.json')).write_bytes(path.read_bytes())
            try:
                gate = publication_gate(pkg, BASE, require_approval=False)
                gate = {'passed': True, 'auditHash': gate['auditHash']}
            except ValueError as exc:
                gate = {'passed': False, 'reason': str(exc)}
            assert gate['passed'] == a['approved'], (pid, gate)
            state = 'held' if pid == '817A' else 'qualified' if a['approved'] else 'rejected'
            contradictions = [r for r in sample_record['packages'][pid] if r['verdict'] != 'AC']
            if contradictions:
                state = 'rejected'
            current = dict(a)
            if state == 'held' or contradictions:
                current['approved'] = False
                current['parentDecision'] = {'reviewer': 'devin-4f9e83a9b1ff45288014bd469b4fa8ad',
                    'state': state, 'reason': 'Accepted reference27796232 declares int x[0] and writes/reads x[0]/x[1]; undefined behavior; passing tests does not establish validity' if not contradictions else
                    'Accepted reference9830350 loops on getchar EOF when exact original sample has no trailing whitespace; both original samples cause std::bad_alloc/RE. Original sample bytes are unchanged; runtime/sample contradiction quarantines this package.',
                    'sampleContradictions': contradictions}
                current['reasons'] = list(a.get('reasons', [])) + [current['parentDecision']['reason']]
            current_path = BASE / '1200/audits' / (pid + '.json')
            current_path.write_text(json.dumps(current, indent=2) + '\n')
            if state == 'held' or contradictions:
                try:
                    publication_gate(pkg, BASE, require_approval=False)
                except ValueError:
                    pass
                else:
                    raise AssertionError('Held parent audit unexpectedly passes gate')
            result['packages'][pid] = {'child': i, 'technicalState': state,
                'packageHash': a['packageHash'], 'evidenceHash': digest(e),
                'auditHash': digest(current), 'auditFileSha256': sha(current_path.read_bytes()),
                'childAuditHash': digest(a), 'childAuditFileSha256': sha(path.read_bytes()),
                'childAuditPath': str(path.relative_to(BASE)), 'genuineWrongReferences': genuine,
                'sourceSemanticRecords': 5, 'childGate': gate,
                'publicationApproved': False, 'publicationReady': False,
                'reasons': a.get('reasons', []), 'reviewer': a['reviewer']}
            result['genuineRecords'] += genuine
            print('REPLAY', i, pid, state, genuine, flush=True)
    assert len(result['packages']) == 38 and result['semanticRecords'] == 190 and result['sourceBindings'] == 380
    (BASE / 'parent-replay.json').write_text(json.dumps(result, indent=2) + '\n')
    print('ALL38SOURCE/SEMANTIC/LOG/GATESVERIFIED', result['genuineRecords'], flush=True)
    return result


if __name__ == '__main__':
    verify()
