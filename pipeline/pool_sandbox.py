"""Run public programs only in disposable offline resource-bounded containers."""
import base64
import json
import os
import resource
from pathlib import Path
import subprocess
import tempfile
import uuid

from checker import check
from pool_harness import COMPILER_FLAGS, EXECUTION_VERSION

IMAGE = "python@sha256:5887f265d8d44d8b4734d3658b21d668edf5aaf92e4945bc0c984afbfab105d3"
SAFE_ENV = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(Path.home())}


def kind(language):
    if "C++" in language and "Diagnostics" not in language:
        return "cpp"
    if language.startswith("Python 3"):
        return "py"
    return None


def run(source, language, tests, cpu, memory, capture=False):
    language_kind = kind(language)
    if language_kind is None:
        raise ValueError("unsupported language (PyPy timing is not equivalent to Python)")
    if not 0 < cpu <= 20 or not 0 < memory <= 1024:
        raise ValueError("resource limit outside supported sandbox range")
    inspect = subprocess.run(["docker", "image", "inspect", IMAGE], env=SAFE_ENV,
                             capture_output=True, timeout=15)
    if inspect.returncode:
        raise RuntimeError(f"sandbox image unavailable; explicitly pull {IMAGE}")
    with tempfile.TemporaryDirectory(prefix="cf-pool-") as tmp:
        path = Path(tmp)
        path.chmod(0o755)
        request = {"source": source, "kind": language_kind, "cpu": cpu, "memory": memory,
                   "tests": [{"name": t["name"], "input": base64.b64encode(t["input"]).decode()} for t in tests]}
        (path / "request.json").write_text(json.dumps(request))
        (path / "request.json").chmod(0o644)
        name = "cf-pool-" + uuid.uuid4().hex
        harness = Path(__file__).with_name("pool_harness.py")
        command = ["docker", "run", "--rm", "--pull=never", "--name", name,
                   "--network=none", "--read-only", "--user=65534:65534", "--cap-drop=ALL",
                   "--security-opt=no-new-privileges", "--pids-limit=64", "--cpus=1",
                   "--memory=1280m", "--memory-swap=1280m", "--ulimit=nofile=128:128",
                   "--tmpfs=/work:rw,exec,nosuid,size=256m,mode=1777", "--tmpfs=/tmp:rw,noexec,nosuid,size=32m",
                   "--mount", f"type=bind,source={path},target=/payload,readonly",
                   "--mount", f"type=bind,source={harness},target=/harness.py,readonly",
                   IMAGE, "python3", "-I", "/harness.py"]
        with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
            def host_output_bound():
                resource.setrlimit(resource.RLIMIT_FSIZE, (128 * 1024 * 1024,) * 2)
            try:
                proc = subprocess.run(command, env=SAFE_ENV, stdout=stdout, stderr=stderr,
                                      timeout=65 + len(tests) * (cpu * 2 + 3), preexec_fn=host_output_bound)
                stdout.seek(0)
                stderr.seek(0)
                if proc.returncode:
                    raise RuntimeError("sandbox infrastructure failure: " + stderr.read(4000).decode(errors="replace"))
                data = stdout.read(128 * 1024 * 1024 + 1)
                if len(data) > 128 * 1024 * 1024:
                    raise RuntimeError("sandbox output exceeds evidence limit")
                result = json.loads(data)
            finally:
                subprocess.run(["docker", "rm", "-f", name], env=SAFE_ENV, capture_output=True, timeout=15)
    context = {"executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS}
    if any(result.get(key) != value for key, value in context.items()):
        raise RuntimeError("sandbox execution/compiler context mismatch")
    if not result.get("compiled"):
        return {**context, "compiled": False, "verdict": "CE", "testsRun": 0, "runs": result.get("runs", [])}
    runs = result.get("runs", [])
    if len(runs) != len(tests) or [r["test"] for r in runs] != [t["name"] for t in tests]:
        raise RuntimeError("interrupted/malformed sandbox result")
    verdict, failed = "AC", None
    summaries = []
    import hashlib
    for test, result in zip(tests, runs):
        encoded = result.pop("output")
        output = base64.b64decode(encoded, validate=True)
        if capture:
            result["output"] = encoded
        result["outputHash"] = hashlib.sha256(output).hexdigest()
        current = ("TLE" if result["timeout"] else "RE" if result["exitCode"] != 0 else
                   "AC" if check(test["output"].decode(), output.decode(errors="replace")) else "WA")
        result["verdict"] = current
        summaries.append(result)
        if verdict == "AC" and current != "AC":
            verdict, failed = current, test["name"]
    return {**context, "compiled": True, "verdict": verdict, "failedTest": failed, "testsRun": len(runs), "runs": summaries}
