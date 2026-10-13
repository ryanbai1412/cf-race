import json, sys, hashlib
from pathlib import Path
import witness as W
ME = Path(__file__).resolve().parent
def run_full(job):
    pid, sid, base, sub, _ = job; B = Path(base)
    names = sorted(p.name[:-3] for p in (B / f'packages/{pid}/tests').glob('*.in'))
    rec = {'key': f'{pid}/{sid}', 'tests': []}
    import tempfile, os, shutil, subprocess, uuid
    row = json.load(open(B / f'state/{pid}/source-row.json'))
    kind = 'cpp' if 'C++' in sub['programmingLanguage'] else 'py'
    d = Path(tempfile.mkdtemp(prefix='witf-')); (d / 'tests').mkdir()
    for n in names: (d / 'tests' / n).write_bytes((B / f'packages/{pid}/tests/{n}.in').read_bytes().replace(b'\r\n', b'\n'))
    json.dump({'source': sub['source'], 'kind': kind, 'cpu': row['time_limit'], 'mem': int(row['memory_limit']), 'tests': names}, open(d / 'req.json', 'w'))
    os.chmod(d, 0o755)
    for f in d.rglob('*'): os.chmod(f, 0o755 if f.is_dir() else 0o644)
    cmd = ['docker', 'run', '--rm', '--pull=never', '--name', 'witf-' + uuid.uuid4().hex[:12], '--network=none', '--read-only', '--user=65534:65534', '--cap-drop=ALL',
           '--security-opt=no-new-privileges', '--pids-limit=32', '--cpus=1', '--memory=2560m', '--memory-swap=2560m',
           '--tmpfs=/w:rw,exec,nosuid,size=128m,mode=1777', '--tmpfs=/tmp:rw,nosuid,size=16m',
           '-v', f'{d}:/in:ro', '-v', f'{W.HARNESS}:/h.py:ro', '--env', 'HOME=/w', W.IMAGE, 'python3', '-I', '/h.py']
    p = subprocess.run(cmd, capture_output=True, timeout=3600, env={'PATH': '/usr/bin:/bin'}); shutil.rmtree(d)
    r = json.loads(p.stdout)
    r.update(key=f'{pid}/{sid}', harnessSha256=hashlib.sha256(W.HARNESS.read_bytes()).hexdigest(), image=W.IMAGE, archiveBase=base, lfInputs=True,
             sourceSha256=hashlib.sha256(sub['source'].encode()).hexdigest(), language=sub['programmingLanguage'])
    json.dump(r, open(ME / 'witness-full' / f'{pid}-{sid}.json', 'w'), sort_keys=True)
    return r['key'], r['compiled']
if __name__ == '__main__':
    want = set(sys.argv[1:])
    from concurrent.futures import ThreadPoolExecutor
    J = [j for j in W.jobs() if f'{j[0]}/{j[1]}' in want]; print(len(J), flush=True)
    with ThreadPoolExecutor(3) as ex:
        for k in ex.map(run_full, J): print(*k, flush=True)
