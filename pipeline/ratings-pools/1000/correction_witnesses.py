"""Capture normal-termination wrong-answer witnesses before source-level review."""
import argparse
import base64
import hashlib
import json

from correction_replay import BASE
from correction_triage import read
from correction_probe import problem_shape, tokens
from pool_sandbox import run
from pool_contract import write_json


def inspect(pid, base=BASE):
    evidence = read(base / "evidence" / f"{pid}.json")
    package = base / "packages" / pid
    meta = read(package / "meta.json")
    outputs = {text[0].lower() for path in (package / "tests").glob("*.out")
               if (text := tokens(path.read_bytes())) and len(text) == 1}
    witnesses = []
    for reference in evidence["submissions"]:
        if reference["expected"] == "OK":
            continue
        sid = str(reference["submissionId"])
        source = read(base / "state" / pid / "sources" / f"{sid}.json")
        name = reference["failedTest"]
        raw = (package / "tests" / f"{name}.in").read_bytes()
        expected = (package / "tests" / f"{name}.out").read_bytes()
        tests = [{"name": "original", "input": raw, "output": expected},
                 {"name": "LF", "input": raw.replace(b"\r\n", b"\n"), "output": expected}]
        result = run(source["code"], source["language"], tests, meta["timeLimitMs"] / 1000,
                     int(meta["memoryLimitMb"]), capture=True)
        decoded = [base64.b64decode(row["output"]) for row in result.get("runs", [])]
        normal = (result["compiled"] and len(result["runs"]) == 2 and
                  all(row["exitCode"] == 0 and not row["timeout"] and row["verdict"] == "WA"
                      for row in result["runs"]))
        shapes = [problem_shape(pid, tokens(expected), tokens(output), raw, outputs) for output in decoded]
        witnesses.append({"submissionId": sid, "sourceHash": source["sourceHash"],
                          "test": name, "inputHash": hashlib.sha256(raw).hexdigest(),
                          "expectedOutputHash": hashlib.sha256(expected).hexdigest(),
                          "outputHashes": [hashlib.sha256(output).hexdigest() for output in decoded],
                          "normalOriginalAndLF": normal,
                          "potentialSemanticMismatch": bool(normal and all(shapes)),
                          "shape": shapes, "result": result,
                          "input": raw.decode(errors="replace")[:2000],
                          "expected": expected.decode(errors="replace")[:2000],
                          "actual": [output.decode(errors="replace")[:2000] for output in decoded],
                          "sourceReview": "REQUIRED; normal different output alone is not proof of an algorithmic source"})
        print(pid, sid, name, normal, shapes, flush=True)
    write_json(base / "review" / f"{pid}-witnesses.json", witnesses)
    return witnesses


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ids", nargs="+", required=True)
    args = parser.parse_args()
    for pid in args.ids:
        inspect(pid)


if __name__ == "__main__":
    main()
