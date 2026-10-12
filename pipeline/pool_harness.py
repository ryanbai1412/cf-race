"""Trusted container entrypoint. Never run this on the credential-bearing host."""
import base64
import json
import math
import os
from pathlib import Path
import resource
import signal
import subprocess
import time

EXECUTION_VERSION = 2
COMPILER_FLAGS = ["-O2", "-std=c++17", "-DONLINE_JUDGE"]


def execute(command, data, cpu, memory, wall):
    def limits():
        os.setsid()
        resource.setrlimit(resource.RLIMIT_CPU, (math.ceil(cpu), math.ceil(cpu) + 1))
        resource.setrlimit(resource.RLIMIT_AS, (int(memory * 1024 * 1024),) * 2)
        resource.setrlimit(resource.RLIMIT_FSIZE, (8 * 1024 * 1024,) * 2)
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    Path("/work/input").write_bytes(data)
    before = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    with open("/work/input", "rb") as inp, open("/work/output", "wb") as out, open("/work/error", "wb") as err:
        process = subprocess.Popen(command, stdin=inp, stdout=out, stderr=err,
                                   cwd="/work", env={"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "/work", "LANG": "C.UTF-8"},
                                   preexec_fn=limits)
        timed_out = False
        try:
            process.wait(timeout=wall)
        except subprocess.TimeoutExpired:
            timed_out = True
        finally:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()
    after = resource.getrusage(resource.RUSAGE_CHILDREN)
    used = after.ru_utime + after.ru_stime - before.ru_utime - before.ru_stime
    output = Path("/work/output").read_bytes()
    error = Path("/work/error").read_bytes()
    return {"exitCode": process.returncode, "timeout": timed_out or used > cpu or process.returncode == -signal.SIGXCPU,
            "cpuSeconds": used, "wallSeconds": time.monotonic() - start,
            "output": base64.b64encode(output).decode(), "stderr": error[:2000].decode(errors="replace")}


def main():
    request = json.loads(Path("/payload/request.json").read_text())
    ext = "cpp" if request["kind"] == "cpp" else "py"
    source = Path(f"/work/main.{ext}")
    source.write_text(request["source"])
    if ext == "cpp":
        compile_result = execute(["g++", *COMPILER_FLAGS, str(source), "-o", "/work/main"], b"", 30, 1024, 60)
        if compile_result["exitCode"] != 0 or compile_result["timeout"]:
            print(json.dumps({"executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS, "compiled": False, "compile": compile_result, "runs": []}))
            return
        command = ["/work/main"]
    else:
        command = ["python3", "-I", str(source)]
    runs = []
    for test in request["tests"]:
        result = execute(command, base64.b64decode(test["input"]), request["cpu"], request["memory"], request["cpu"] * 2 + 2)
        result["test"] = test["name"]
        runs.append(result)
    print(json.dumps({"executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS, "compiled": True, "runs": runs}))


if __name__ == "__main__":
    main()
