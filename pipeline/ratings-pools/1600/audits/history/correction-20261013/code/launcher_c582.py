import json, subprocess, sys, tempfile, os, shutil, hashlib, uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
IMAGE = 'python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3'
ME = Path(__file__).resolve().parent
HARNESS = ME / 'harness_c582.py'
BOUND = {'495B': 5, '597A': 5, '704A': 5, '86A': 6, '741A': 6, '209A': 7, '373B': 7, '665A': 8, '678B': 8, '559A': 9, '910B': 9}
def jobs(pids):
    out = []
    for pid in pids:
        n = BOUND[pid]; base = Path(f'/home/ubuntu/audit{n}/x/1600')
        up = json.load(open(f'/home/ubuntu/audit{n}/me/upstream-subs.json'))
        for s in json.load(open(base / f'evidence/{pid}.json'))['submissions']:
            sub = up[f"{pid}/{s['submissionId']}"]
            assert hashlib.sha256(sub['source'].encode()).hexdigest() == s['sourceHash'], (pid, s['submissionId'])
            out.append((pid, str(s['submissionId']), str(base), sub, False))
            if s['expected'] != 'OK': out.append((pid, str(s['submissionId']), str(base), sub, True))
    return out
def run(job):
    pid, sid, base, sub, lf = job; B = Path(base)
    row = json.load(open(B / f'state/{pid}/source-row.json'))
    kind = 'cpp' if 'C++' in sub['programmingLanguage'] else 'py'
    d = Path(tempfile.mkdtemp(prefix='aud-')); (d / 'tests').mkdir(); names = []
    for sub_dir, pre in (('tests', ''), ('samples', 's')):
        for p in sorted((B / f'packages/{pid}/{sub_dir}').glob('*.in')):
            data = p.read_bytes()
            (d / 'tests' / (pre + p.name)).write_bytes(data.replace(b'\r\n', b'\n') if lf else data); names.append(pre + p.name)
    json.dump({'source': sub['source'], 'kind': kind, 'cpu': row['time_limit'], 'mem': int(row['memory_limit']), 'tests': names}, open(d / 'req.json', 'w'))
    os.chmod(d, 0o755)
    for f in d.rglob('*'): os.chmod(f, 0o755 if f.is_dir() else 0o644)
    cmd = ['docker', 'run', '--rm', '--pull=never', '--name', 'aud-' + uuid.uuid4().hex[:12], '--network=none', '--read-only', '--user=65534:65534', '--cap-drop=ALL',
           '--security-opt=no-new-privileges', '--pids-limit=32', '--cpus=1', '--memory=2560m', '--memory-swap=2560m',
           '--tmpfs=/w:rw,exec,nosuid,size=128m,mode=1777', '--tmpfs=/tmp:rw,nosuid,size=16m',
           '-v', f'{d}:/in:ro', '-v', f'{HARNESS}:/h.py:ro', '--env', 'HOME=/w', IMAGE, 'python3', '-I', '/h.py']
    p = subprocess.run(cmd, capture_output=True, timeout=3600, env={'PATH': '/usr/bin:/bin'})
    shutil.rmtree(d)
    if len(p.stdout) > 64 << 20: raise RuntimeError('too big')
    r = json.loads(p.stdout)
    r.update(key=f'{pid}/{sid}', lfInputs=lf, harnessSha256=hashlib.sha256(HARNESS.read_bytes()).hexdigest(), image=IMAGE,
             archiveBase=base, sourceSha256=hashlib.sha256(sub['source'].encode()).hexdigest(), stderr=p.stderr[-500:].decode(errors='replace'))
    json.dump(r, open(ME / ('replay-c582-lf' if lf else 'replay-c582') / f'{pid}-{sid}.json', 'w'), sort_keys=True)
    return f'{pid}/{sid}', lf, r['compiled']
if __name__ == '__main__':
    with ThreadPoolExecutor(4) as ex:
        for k in ex.map(run, jobs(sys.argv[1:] or list(BOUND))): print(*k, flush=True)
