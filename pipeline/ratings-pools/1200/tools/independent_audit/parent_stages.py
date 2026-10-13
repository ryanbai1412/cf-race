import base64
import json
from pathlib import Path

from parent_replay import BASE, COMPILER_FLAGS, EXECUTION_VERSION, read, sha


def unwrap(data):
    return data.get('result', data)


def normal(data):
    data = unwrap(data)
    assert data['executionVersion'] == EXECUTION_VERSION and data['compilerFlags'] == COMPILER_FLAGS
    assert data['compiled'] and data['testsRun'] == len(data['runs'])
    for run in data['runs']:
        output = base64.b64decode(run['output'], validate=True)
        assert sha(output) == run['outputHash']
    return data


def main():
    replay = read(BASE / 'parent-replay.json')
    result = {'packages': {}, 'acceptedReferences': 0, 'freshPublicSourceExecutions': 0}
    for pid, row in replay['packages'].items():
        i = row['child']; root = next((BASE / f'current-child-{i}').iterdir())
        folder = root / pid / 'execution' if i == 6 else root / 'archive' / pid if i == 3 else root / 'reruns' / pid if i == 4 else root / 'fresh' / pid
        e = read(BASE / '1200/evidence' / (pid + '.json'))
        expected_tests = {p.stem for p in (BASE / '1200/packages' / pid / 'tests').glob('*.in')}
        sample_tests = {'sample-' + p.stem for p in (BASE / '1200/packages' / pid / 'samples').glob('*.in')}
        sources = []
        for s in e['submissions']:
            sid = str(s['submissionId'])
            f = folder / (('sub-' if i in [3, 6] else 'source-') + sid + '.json')
            data = read(f)
            if 'identity' in data:
                assert sha(data['identity']['code'].encode()) == s['sourceHash']
            if 'sourceHash' in data:
                assert data['sourceHash'] == s['sourceHash']
            run = normal(data)
            assert run['verdict'] == s['verdict'], (pid, sid)
            if s['expected'] == 'OK':
                assert run['verdict'] == 'AC'
                assert expected_tests <= {r['test'] for r in run['runs']} <= expected_tests | sample_tests, (pid, sid)
                assert all(r['exitCode'] == 0 and not r.get('timeout') and r['verdict'] == 'AC' for r in run['runs'])
                result['acceptedReferences'] += 1
            sources.append({'submissionId': sid, 'sourceHash': s['sourceHash'], 'freshLog': str(f.relative_to(BASE)),
                            'freshLogSha256': sha(f.read_bytes()), 'verdict': run['verdict'], 'testsRun': run['testsRun']})
            result['freshPublicSourceExecutions'] += 1
        oracle = folder / ('oracle-run.json' if i in [3, 6] else 'oracle-all.json' if i == 4 else 'oracle.json')
        run = normal(read(oracle))
        assert run['verdict'] == 'AC' and expected_tests <= {r['test'] for r in run['runs']}, pid
        assert {r['test'] for r in run['runs']} <= expected_tests | sample_tests, pid
        assert all(r['exitCode'] == 0 and not r.get('timeout') and r['verdict'] == 'AC' for r in run['runs'])
        generators = [folder / f'generator-run{n}.json' for n in [1, 2]] if i in [3, 6] else [folder / f'generator-{n}.json' for n in ([1, 2] if i == 5 else [0, 1])]
        if i in [3, 6]:
            pairs = [read(g) for g in generators]
            assert pairs[0] == pairs[1]
            summary = read(folder / 'summary.json')['generator']
            assert len(set(summary['hashes'])) == 1 and summary['identical'] and summary['matchesRecorded']
        else:
            runs = [normal(read(g))['runs'][0] for g in generators]
            assert all(r['exitCode'] == 0 and not r.get('timeout') for r in runs)
            assert runs[0]['outputHash'] == runs[1]['outputHash']
            pairs = [json.loads(base64.b64decode(r['output'])) for r in runs]
        generation = read(BASE / '1200/packages' / pid / 'qualification/generation.json')
        from pool_contract import digest
        assert pairs[0] == pairs[1] and digest(pairs[0]) == generation['pairsHash'], pid
        assert len(pairs[0]) == generation['count'], pid
        if i not in [3, 6]:
            assert [r['outputHash'] for r in runs] == generation['repeatOutputHashes'], pid
        result['packages'][pid] = {'sourceExecutions': sources,
            'oracleLog': str(oracle.relative_to(BASE)), 'oracleLogSha256': sha(oracle.read_bytes()),
            'generatorLogs': [{'path': str(g.relative_to(BASE)), 'sha256': sha(g.read_bytes())} for g in generators],
            'generatorRepeatEqual': True, 'allSuppliedPairsCheckedByFreshOracle': True,
            'fiveFreshAcceptedAllAC': True, 'suppliedTestCount': len(expected_tests)}
        print('FRESH_ALL', pid, len(expected_tests), flush=True)
    assert result['acceptedReferences'] == 190 and result['freshPublicSourceExecutions'] == 380
    (BASE / 'parent-stages.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
