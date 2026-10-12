"""Generated-suite qualification; all authored programs execute offline/bounded."""
import base64
import hashlib
import re
from pathlib import Path

from pool_contract import digest, pairs, read_json
from pool_sandbox import IMAGE, COMPILER_FLAGS, EXECUTION_VERSION, kind, run
from pool_sources import sha_file


def stable_result(result):
    return {"compiled": result["compiled"], "verdict": result["verdict"],
            "testsRun": result["testsRun"], "failedTest": result.get("failedTest"),
            "runs": [{key: record[key] for key in ("test", "exitCode", "timeout", "verdict", "outputHash")}
                     for record in result["runs"]]}


def sandbox():
    return {"image": IMAGE, "network": "none", "bounded": True,
            "executionVersion": EXECUTION_VERSION, "compilerFlags": COMPILER_FLAGS,
            **{key: sha_file(Path(__file__).with_name(name)) for key, name in
               (("harnessHash", "pool_harness.py"), ("runnerHash", "pool_sandbox.py"), ("checkerHash", "checker.py"))}}


def build_generated(args, row, supplemental):
    if not args.generator_author or not args.oracle_author or args.generator_author == args.oracle_author or not args.oracle_review_url:
        raise ValueError("generated basis requires independently authored oracle, author identities and review URL")
    generator = Path(args.generator_source).read_bytes()
    oracle = Path(args.oracle_source).read_bytes()
    if generator == oracle or kind(args.generator_language) is None or kind(args.oracle_language) is None:
        raise ValueError("generator/oracle must be distinct self-contained Python3 or C++ programs")
    outputs, executions = [], []
    request = [{"name": "seed", "input": f"{args.seed}\n".encode(), "output": b""}]
    for _ in range(2):
        result = run(generator.decode("utf-8"), args.generator_language, request, 10, 1024, capture=True)
        if not result["compiled"] or result["runs"][0]["exitCode"] != 0 or result["runs"][0]["timeout"]:
            raise ValueError("generator compile/runtime/bounded-execution failure")
        outputs.append(base64.b64decode(result["runs"][0]["output"], validate=True))
        executions.append(stable_result(result))
    if outputs[0] != outputs[1]:
        raise ValueError("generator is not byte-deterministic at specified seed")
    import json
    extra = pairs(json.loads(outputs[0]))
    distinct = len({p["input"] for p in extra})
    mode = "exhaustive" if args.exhaustive_domain_size is not None else "extensive"
    if mode == "extensive" and distinct < 100:
        raise ValueError("extensive generated basis requires at least100 distinct authored inputs")
    if mode == "exhaustive" and (args.exhaustive_domain_size != distinct or distinct < 1 or not args.exhaustive_domain):
        raise ValueError("exhaustive basis requires exact declared domain size and independently auditable domain description")
    tests = [{"name": f"{i:04d}", "input": p["input"].encode(), "output": p["output"].encode()}
             for i, p in enumerate([p for _, p in supplemental] + extra, 1)]
    checked = run(oracle.decode("utf-8"), args.oracle_language, tests, row["time_limit"], row["memory_limit"])
    if checked["compiled"] is not True or checked["verdict"] != "AC":
        raise ValueError(f"oracle/constraint contradiction quarantined at {checked.get('failedTest')}; do not repair upstream tests silently")
    generation = {"schemaVersion": 1, "seed": args.seed, "author": args.generator_author,
                  "sourceHash": hashlib.sha256(generator).hexdigest(), "language": args.generator_language,
                  "pairsHash": digest(extra), "count": len(extra), "distinctInputs": distinct,
                  "mode": mode, "domainSize": args.exhaustive_domain_size, "domain": args.exhaustive_domain,
                  "repeatOutputHashes": [hashlib.sha256(o).hexdigest() for o in outputs],
                  "executions": executions, "sandbox": sandbox()}
    reference = {"schemaVersion": 1, "author": args.oracle_author, "reviewUrl": args.oracle_review_url,
                 "sourceHash": hashlib.sha256(oracle).hexdigest(), "language": args.oracle_language,
                 "result": stable_result(checked), "sandbox": sandbox()}
    return extra, generation, reference, generator, oracle


def verify_generated(package, files, records, evidence, audit):
    package = Path(package)
    gen = read_json(package / "qualification/generation.json")
    oracle = read_json(package / "qualification/oracle.json")
    if gen.get("schemaVersion") != 1 or oracle.get("schemaVersion") != 1:
        raise ValueError("generated proof version mismatch")
    for name, record in (("generator", gen), ("oracle", oracle)):
        language = kind(record.get("language", ""))
        source = f"qualification/{name}.{'cpp' if language == 'cpp' else 'py'}"
        if language is None or files.get(source, {}).get("sha256") != record.get("sourceHash"):
            raise ValueError("changed/missing generated qualification source")
        if record.get("sandbox") != evidence.get("sandbox"):
            raise ValueError("generated proof differs from bounded validator implementation")
    if (not gen.get("author") or not oracle.get("author") or gen["author"] == oracle["author"] or
            oracle["author"] == evidence.get("validator") or not oracle.get("reviewUrl") or
            oracle["sourceHash"] == gen["sourceHash"] or any(r["sourceHash"] == oracle["sourceHash"] for r in evidence["submissions"])):
        raise ValueError("oracle is not independent from generator/validator/external references")
    authored = [r for r in records if r.get("origin") == "worker-generated"]
    extra = [{"input": (package / f"tests/{r['name']}.in").read_text(),
              "output": (package / f"tests/{r['name']}.out").read_text()} for r in authored]
    if gen.get("count") != len(extra) or gen.get("pairsHash") != digest(extra):
        raise ValueError("generator proof does not bind every authored pair")
    distinct = len({p["input"] for p in extra})
    if gen.get("distinctInputs") != distinct or not isinstance(gen.get("seed"), int):
        raise ValueError("generated diversity/seed mismatch")
    if gen.get("mode") == "extensive":
        if distinct < 100:
            raise ValueError("generated suite is not extensive")
    elif gen.get("mode") == "exhaustive":
        if gen.get("domainSize") != distinct or distinct < 1 or not gen.get("domain") or audit.get("checks", {}).get("exhaustiveDomain") is not True:
            raise ValueError("exhaustive generated domain lacks independent signoff")
    else:
        raise ValueError("missing extensive/exhaustive generated basis")
    hashes = gen.get("repeatOutputHashes", [])
    executions = gen.get("executions", [])
    if len(hashes) != 2 or any(not isinstance(h, str) or not re.fullmatch(r"[a-f0-9]{64}", h) for h in hashes) or hashes[0] != hashes[1] or len(executions) != 2:
        raise ValueError("missing reproducible generator executions")
    for expected, execution in zip(hashes, executions):
        results = execution.get("runs", [])
        if execution.get("compiled") is not True or execution.get("testsRun") != 1 or len(results) != 1 or results[0].get("test") != "seed" or results[0].get("outputHash") != expected or results[0].get("exitCode") != 0 or results[0].get("timeout") is not False:
            raise ValueError("generator execution failure/hash mismatch")
    result = oracle.get("result", {})
    if (result.get("compiled") is not True or result.get("verdict") != "AC" or result.get("testsRun") != len(records) or
            [r.get("test") for r in result.get("runs", [])] != [r["name"] for r in records] or
            any(r.get("verdict") != "AC" or r.get("exitCode") != 0 or r.get("timeout") is not False or not re.fullmatch(r"[a-f0-9]{64}", r.get("outputHash", "")) for r in result.get("runs", []))):
        raise ValueError("independent oracle did not check every supplied pair")
    authored_names = {r["name"] for r in authored}
    for key in ("boundary", "adversarial", "maxSize"):
        if not any(c["test"] in authored_names for c in evidence["coverage"][key]):
            raise ValueError("generated coverage must name authored boundary/max/adversarial pairs")
    if evidence.get("qualificationBasis") != "generated" or audit.get("qualificationBasis") != "generated":
        raise ValueError("generated basis not explicitly declared in evidence/audit")
    for key in ("deterministicGeneration", "independentOracle", "generatedBasis", "algorithmicallyWrong", "inputConstraints"):
        if audit.get("checks", {}).get(key) is not True:
            raise ValueError(f"generated audit did not sign off {key}")
    for submission in evidence["submissions"]:
        if submission["expected"] == "OK":
            continue
        analysis = audit.get("incorrectAnalysis", {}).get(str(submission["submissionId"]), {})
        if not analysis.get("reason") or analysis.get("test") != submission["failedTest"] or analysis.get("kind") not in ("wrong-answer", "complexity"):
            raise ValueError("missing independently reviewed algorithmic defect/counterexample")
