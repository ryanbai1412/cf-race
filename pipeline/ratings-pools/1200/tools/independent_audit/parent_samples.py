import concurrent.futures
import json

from parent_replay import BASE, read, sha
from pool_sandbox import run, IMAGE, COMPILER_FLAGS, EXECUTION_VERSION


def task(pid):
    package = BASE / '1200/packages' / pid
    meta = read(package / 'meta.json')
    tests = [{'name': 'sample-' + p.stem, 'input': p.read_bytes(), 'output': p.with_suffix('.out').read_bytes()}
             for p in sorted((package / 'samples').glob('*.in'))]
    sources = [read(BASE / '1200/state' / pid / 'sources' / (str(s['submissionId']) + '.json'))
               for s in read(BASE / '1200/evidence' / (pid + '.json'))['submissions'] if s['expected'] == 'OK']
    oracle = package / 'qualification/oracle.py'
    if not oracle.exists():
        oracle = package / 'qualification/oracle.cpp'
    sources.append({'code': oracle.read_text(), 'programmingLanguage': 'Python 3' if oracle.suffix == '.py' else 'GNU C++17', 'id': 'oracle'})
    rows = []
    for s in sources:
        sid = str(s.get('id', s.get('submissionId')))
        language = s.get('programmingLanguage', s.get('language'))
        f = BASE / 'parent-samples' / (pid + '-' + sid + '.json')
        if f.exists():
            previous = read(f)
            assert previous['sourceHash'] == sha(s['code'].encode())
            result = previous['result']
            assert {r['test'] for r in result['runs']} == {t['name'] for t in tests}
        else:
            result = run(s['code'], language, tests, meta['timeLimitMs'] / 1000, meta['memoryLimitMb'], capture=True)
            f.write_text(json.dumps({'sourceHash': sha(s['code'].encode()), 'result': result}, indent=2) + '\n')
        rows.append({'submissionId': sid, 'sourceHash': sha(s['code'].encode()), 'log': str(f.relative_to(BASE)),
                     'logSha256': sha(f.read_bytes()), 'verdict': result['verdict'], 'testsRun': result['testsRun'],
                     'failedTest': result['failedTest'], 'exactSampleByteManifest': [
                         {'name': t['name'], 'inputSha256': sha(t['input']), 'inputBytes': len(t['input']),
                          'expectedSha256': sha(t['output']), 'expectedBytes': len(t['output'])} for t in tests]})
    print('SAMPLES', pid, [(r['submissionId'], r['verdict']) for r in rows], flush=True)
    return pid, rows


if __name__ == '__main__':
    (BASE / 'parent-samples').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        packages = dict(executor.map(task, sorted(read(BASE / 'parent-replay.json')['packages'])))
    record = {'executionVersion': EXECUTION_VERSION, 'compilerFlags': COMPILER_FLAGS, 'image': IMAGE,
              'purpose': 'Fresh exact original sample bytes, five accepted references and independent oracle per candidate; no LF repair',
              'packages': packages, 'allPassed': all(r['verdict'] == 'AC' for rows in packages.values() for r in rows)}
    (BASE / 'parent-samples.json').write_text(json.dumps(record, indent=2) + '\n')
    print('SAMPLE_CONTRADICTIONS', [(pid, r['submissionId'], r['verdict']) for pid, rows in packages.items() for r in rows if r['verdict'] != 'AC'], flush=True)
