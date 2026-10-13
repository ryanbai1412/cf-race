"""Deterministic whole-current-pool archive: every package (incl. tests), evidence, current + revoked audits, manifest."""
import gzip, hashlib, io, json, sys, tarfile
from pathlib import Path
sys.path.insert(0, str(Path.home() / "repos/cf-race/pipeline"))
import pool_contract as pc
WS = Path.home() / "Documents/cf-pools/1400"
REPO = Path.home() / "repos/cf-race/pipeline/ratings-pools/1400"
out = Path(sys.argv[1])
sha = lambda b: hashlib.sha256(b).hexdigest()
files = {}
for root, pre in ((WS, ""), (REPO, "repo-owned/")):
    for f in sorted(root.rglob("*")):
        rel = f.relative_to(root)
        if not f.is_file() or rel.parts[0] in ("state", "submissions") or "__pycache__" in rel.parts:
            continue
        if pre and rel.parts[0] in ("packages", "evidence", "audits-revoked") :
            continue
        files[pre + str(rel)] = f
status = {}
for d in sorted((WS / "packages").iterdir()):
    pid = d.name; e = WS / "evidence" / f"{pid}.json"; a = WS / "audits" / f"{pid}.json"
    s = {"packageHash": None, "evidenceStatus": None, "evidenceHash": None, "audit": a.exists(), "gate": None}
    try: s["packageHash"] = pc.digest(pc.manifest(d))
    except Exception as x: s["packageError"] = str(x)[:200]
    if e.exists():
        ev = json.loads(e.read_text()); s["evidenceStatus"] = ev.get("status"); s["evidenceHash"] = pc.digest(ev)
        s["evidencePackageHashMatches"] = ev.get("packageHash") == s["packageHash"]
    if a.exists():
        try: pc.publication_gate(d, evidence_root=WS.parent, require_approval=False); s["gate"] = "pass"
        except Exception as x: s["gate"] = "fail: " + str(x)[:200]
    status[pid] = s
approved = sorted(p for p, s in status.items() if s["gate"] == "pass")
execp = sorted(p for p, s in status.items() if s["evidenceStatus"] == "execution-passed" and s.get("evidencePackageHashMatches"))
MAINJ = Path.home() / "attachments/b2502c27-8f01-44e1-9099-6cf9e728f43c/independent-audit.json"
main = json.loads(MAINJ.read_text())["problems"]
mainv = sorted(p for p, m in main.items() if m["verdict"] == "VALIDATED")
manifest = {"rating": 1400, "primaryGateJsonSha256": sha(MAINJ.read_bytes()), "worker": "devin-7733398037234c53afd9ded68a6e407d",
    "counts": {"packages": len(status), "executionPassedCurrent": len(execp),
               "currentAuditApprovedGatePass": len(approved),
               "primaryGateValidated": len(mainv), "primaryGateReviewed": len(main)},
    "currentAuditApproved": approved, "executionPassedCurrent": execp,
    "executionPassedUnaudited": sorted(set(execp) - set(approved)),
    "mainGateValidated": mainv,
    "mainGateValidatedCurrentBytes": sorted(p for p in mainv if status.get(p, {}).get("packageHash") == main[p]["packageHash"]),
    "approvedNotYetMainGateReviewed": sorted(set(approved) - set(main)),
    "perPackage": status,
    "files": {k: sha(v.read_bytes()) for k, v in files.items()}}
mb = json.dumps(manifest, indent=1, sort_keys=True).encode()
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w", format=tarfile.PAX_FORMAT) as t:
    def add(name, data):
        ti = tarfile.TarInfo("rating1400-pool/" + name); ti.size = len(data); ti.mtime = 0; ti.mode = 0o644
        ti.uid = ti.gid = 0; ti.uname = ti.gname = ""; t.addfile(ti, io.BytesIO(data))
    add("MANIFEST.json", mb)
    add("SHA256SUMS", "".join(f"{h}  {k}\n" for k, h in sorted(manifest["files"].items())).encode())
    for k in sorted(files): add(k, files[k].read_bytes())
with open(out, "wb") as fh:
    with gzip.GzipFile(fileobj=fh, mode="wb", compresslevel=6, mtime=0, filename="") as g: g.write(buf.getvalue())
print(json.dumps(manifest["counts"]), "files", len(files), sha(out.read_bytes()))
print("approved", approved); print("unaudited", manifest["executionPassedUnaudited"])
print("mainCur", manifest["mainGateValidatedCurrentBytes"]); print("notMain", manifest["approvedNotYetMainGateReviewed"])
