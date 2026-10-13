import json, subprocess, tempfile, os, shutil, hashlib, uuid, sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
IMAGE = 'python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3'
ME = Path(__file__).resolve().parent
HARNESS = ME / 'harness_witness.py'
H = '/home/ubuntu/'
ARCH = {'495B': 'audit5', '597A': 'audit5', '704A': 'audit5', '86A': 'audit6', '741A': 'audit6', '209A': 'audit7', '373B': 'audit7', '665A': 'audit8', '678B': 'audit8', '559A': 'audit9', '910B': 'audit9',
        '11B': 'audit12', '235A': 'audit12', '322B': 'audit12', '40B': 'audit12', '55B': 'audit12', '845B': 'audit12', '888D': 'audit12'}
SUBS = {}
for f in ['audit/me', 'audit3/me', 'audit4/me', 'audit5/me', 'audit6/me', 'audit7/me', 'audit8/me', 'audit9/me', 'audit10/me']:
    for k, v in json.load(open(H + f + '/upstream-subs.json')).items(): SUBS.setdefault((k, hashlib.sha256(v['source'].encode()).hexdigest()), v)
def jobs():
    out = []
    for pid, a in ARCH.items():
        B = Path(H + a + '/x/1600')
        for s in json.load(open(B / f'evidence/{pid}.json'))['submissions']:
            if s['expected'] == 'OK': continue
            sub = SUBS[(f"{pid}/{s['submissionId']}", s['sourceHash'])]
            out.append((pid, str(s['submissionId']), str(B), sub, s['failedTest']))
    return out
def run(job):
    pid, sid, base, sub, test = job; B = Path(base)
    row = json.load(open(B / f'state/{pid}/source-row.json'))
    kind = 'cpp' if 'C++' in sub['programmingLanguage'] else 'py'
    d = Path(tempfile.mkdtemp(prefix='wit-')); (d / 'tests').mkdir()
    raw = (B / f'packages/{pid}/tests/{test}.in').read_bytes(); lf = raw.replace(b'\r\n', b'\n')
    (d / 'tests' / test).write_bytes(lf)
    json.dump({'source': sub['source'], 'kind': kind, 'cpu': row['time_limit'], 'mem': int(row['memory_limit']), 'tests': [test]}, open(d / 'req.json', 'w'))
    os.chmod(d, 0o755)
    for f in d.rglob('*'): os.chmod(f, 0o755 if f.is_dir() else 0o644)
    cmd = ['docker', 'run', '--rm', '--pull=never', '--name', 'wit-' + uuid.uuid4().hex[:12], '--network=none', '--read-only', '--user=65534:65534', '--cap-drop=ALL',
           '--security-opt=no-new-privileges', '--pids-limit=32', '--cpus=1', '--memory=2560m', '--memory-swap=2560m',
           '--tmpfs=/w:rw,exec,nosuid,size=128m,mode=1777', '--tmpfs=/tmp:rw,nosuid,size=16m',
           '-v', f'{d}:/in:ro', '-v', f'{HARNESS}:/h.py:ro', '--env', 'HOME=/w', IMAGE, 'python3', '-I', '/h.py']
    p = subprocess.run(cmd, capture_output=True, timeout=900, env={'PATH': '/usr/bin:/bin'})
    shutil.rmtree(d)
    r = json.loads(p.stdout)
    r.update(key=f'{pid}/{sid}', test=test, harnessSha256=hashlib.sha256(HARNESS.read_bytes()).hexdigest(), image=IMAGE, archiveBase=base,
             language=sub['programmingLanguage'], sourceSha256=hashlib.sha256(sub['source'].encode()).hexdigest(),
             packageInputSha256=hashlib.sha256(raw).hexdigest(), lfInputSha256=hashlib.sha256(lf).hexdigest(), packageInputHadCRLF=b'\r\n' in raw,
             expectedOutputSha256=hashlib.sha256((B / f'packages/{pid}/tests/{test}.out').read_bytes()).hexdigest())
    json.dump(r, open(ME / 'witness' / f'{pid}-{sid}.json', 'w'), sort_keys=True)
    return f'{pid}/{sid}', test, r['compiled']
if __name__ == '__main__':
    J = jobs(); print(len(J), 'jobs', flush=True)
    with ThreadPoolExecutor(3) as ex:
        for k in ex.map(run, J): print(*k, flush=True)
