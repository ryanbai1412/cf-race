"""Bundle an authored recipe into a self-contained deterministic generator (seed on stdin -> JSON pairs)."""
import hashlib, importlib, json, subprocess, sys, time
from pathlib import Path

W = Path(__file__).resolve().parent
REC = W / "recipes"
sys.path.insert(0, str(REC))
import lib, rand_extra  # noqa: E402
for m in "abcdefgh":
    importlib.import_module("probs_" + m)

RUNNER = r'''
import json, random, sys, types
for _name in ("lib", "rand_extra", MODULE):
    _m = types.ModuleType(_name)
    sys.modules[_name] = _m
    exec(compile(SOURCES[_name], _name + ".py", "exec"), _m.__dict__)
lib = sys.modules["lib"]
cls = lib.REG[PID]
seed = int(sys.stdin.read().strip())
seen, cases = set(), []


def add(cat, reason, inp):
    if inp in seen:
        return
    try:
        cls.V(inp)
    except lib.Bad:
        if cat != "random":
            raise
        return
    seen.add(inp)
    cases.append((cat, reason, inp))


for cat, reason, inp in cls.G():
    add(cat, reason, inp)
if DOMAIN is not None:
    for inp in DOMAIN:
        add("domain", "exhaustive domain element", inp)
sampler = sys.modules["rand_extra"].R.get(PID) or cls.SMALL
r = random.Random(f"cf-race-1400-gen-{PID}-{seed}")
attempts = 0
while DOMAIN is None and len(cases) < TARGET and attempts < TARGET * 40:
    attempts += 1
    inp = sampler(r)
    if len(inp) <= RANDOM_MAX_BYTES:
        add("random", "seeded random valid input", inp)
pairs = [{"input": inp, "output": cls.S(inp) + "\n"} for _, _, inp in cases]
if len(cases) < MIN_DISTINCT:
    sys.exit("too few distinct inputs")
if "--manifest" in sys.argv:
    print(json.dumps([[c, r_] for c, r_, _ in cases]))
else:
    sys.stdout.write(json.dumps(pairs))
'''

DOMAINS = {"630H": [f"{n}\n" for n in range(5, 101)]}


def build(pid, target=150, random_max=20000):
    cls = lib.REG[pid]
    mod = cls.__module__
    sources = {n: (REC / f"{n}.py").read_text() for n in ("lib", "rand_extra", mod)}
    domain = DOMAINS.get(pid)
    head = (f'"""Deterministic authored generator for Codeforces {pid} (cf-race rating-1400 worker). '
            f'Reads an integer seed on stdin; writes a JSON list of {{input,output}} pairs."""\n'
            f"PID = {pid!r}\nMODULE = {mod!r}\nTARGET = {target}\nMIN_DISTINCT = {len(domain) if domain else 100}\n"
            f"RANDOM_MAX_BYTES = {random_max}\nDOMAIN = {domain!r}\nSOURCES = {json.dumps(sources, indent=0, sort_keys=True)}\n")
    code = head + RUNNER
    out = W / "gen" / pid
    out.mkdir(parents=True, exist_ok=True)
    (out / "generator.py").write_text(code)
    t = time.time()
    a = subprocess.run([sys.executable, out / "generator.py"], input=b"42\n", capture_output=True, timeout=120, cwd="/tmp")
    el = time.time() - t
    if a.returncode:
        return {"id": pid, "error": a.stderr.decode()[-300:]}
    b = subprocess.run([sys.executable, out / "generator.py"], input=b"42\n", capture_output=True, timeout=120, cwd="/tmp")
    man = subprocess.run([sys.executable, out / "generator.py", "--manifest"], input=b"42\n", capture_output=True, timeout=120, cwd="/tmp")
    pairs = json.loads(a.stdout)
    manifest = json.loads(man.stdout)
    (out / "manifest.json").write_text(json.dumps(manifest))
    res = {"id": pid, "pairs": len(pairs), "distinct": len({p["input"] for p in pairs}), "bytes": len(a.stdout),
           "seconds": round(el, 2), "deterministic": a.stdout == b.stdout,
           "sha256": hashlib.sha256(a.stdout).hexdigest(), "generatorSha256": hashlib.sha256(code.encode()).hexdigest(),
           "categories": {k: sum(1 for c, _ in manifest if c == k) for k in sorted({c for c, _ in manifest})}}
    (out / "build.json").write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    for pid in sys.argv[1:]:
        print(json.dumps(build(pid)), flush=True)
