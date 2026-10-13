import json, os, resource, subprocess, sys, time, hashlib, signal, base64
req = json.load(open('/in/req.json'))
lang, cpu, mem = req['kind'], req['cpu'], req['mem']
os.chdir('/w')
open('/w/src.' + lang, 'w').write(req['source'])
def lim(c, m):
    def f():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (c, c + 1))
        resource.setrlimit(resource.RLIMIT_AS, (m, m))
        resource.setrlimit(resource.RLIMIT_FSIZE, (16 << 20, 16 << 20))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    return f
res = {'compiled': True, 'tests': []}
if lang == 'cpp':
    p = subprocess.run(['g++', '-O2', '-std=c++17', '-DONLINE_JUDGE', 'src.cpp', '-o', 'a.out'], capture_output=True, preexec_fn=lim(60, 2 << 30), timeout=120)
    if p.returncode:
        print(json.dumps({'compiled': False, 'err': p.stderr.decode(errors='replace')[:3000]})); sys.exit()
    cmd = ['./a.out']
else:
    cmd = ['python3', 'src.py']
for name in req['tests']:
    data = open(f'/in/tests/{name}', 'rb').read()
    t0 = time.monotonic(); r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, preexec_fn=lim(int(cpu) + 1, mem << 20))
    try:
        out, _ = p.communicate(data, timeout=cpu * 3 + 2); to = False
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL); out, _ = p.communicate(); to = True
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    used = (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime)
    res['tests'].append({'name': name, 'rc': p.returncode, 'cpu': round(used, 3), 'wall': round(time.monotonic() - t0, 3), 'timeout': to or used > cpu, 'sha': hashlib.sha256(out).hexdigest(), 'out': out[:200].decode(errors='replace'), 'tokSha': hashlib.sha256(b' '.join(out.split())).hexdigest(), 'outBytes': len(out), 'outB64': base64.b64encode(out).decode()})
print(json.dumps(res))
