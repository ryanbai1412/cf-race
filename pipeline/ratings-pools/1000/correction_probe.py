"""Find replacement public wrong-answer witnesses using only the pinned offline sandbox."""
import argparse
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import sys
from fractions import Fraction

from correction_triage import HERE, indexed_sources, read, triage

sys.path.insert(0, str(HERE.parents[1]))
from pool_sandbox import run


def tokens(text):
    return text.decode(errors="replace").split()


def algorithmic_shape(expected, actual, vocabulary=None):
    if len(actual) != len(expected) or actual == expected:
        return None
    if all(re.fullmatch(r"[+-]?\d+", word) for word in expected + actual):
        if [int(word) for word in actual] != [int(word) for word in expected]:
            return "different integer answer with expected arity"
    elif (len(expected) == len(actual) == 1 and expected[0].lower() in ("yes", "no")
          and actual[0].lower() in ("yes", "no")
          and actual[0].lower() != expected[0].lower()):
        return "opposite yes/no answer"
    elif (len(expected) == len(actual) == 1
          and expected[0] in ("FINITE", "INFINITE")
          and actual[0] in ("FINITE", "INFINITE")):
        return "opposite finite/infinite answer"
    elif (len(expected) == len(actual) == 1
          and re.fullmatch(r"[+-]?\d+/[+-]?\d+", expected[0])
          and re.fullmatch(r"[+-]?\d+/[+-]?\d+", actual[0])
          and int(expected[0].split("/")[1]) != 0 and int(actual[0].split("/")[1]) != 0
          and Fraction(expected[0]) != Fraction(actual[0])):
        return "different rational value with expected fraction grammar"
    elif (len(expected) == len(actual) == 1
          and re.fullmatch(r"(?:\.[a-z])+", expected[0])
          and re.fullmatch(r"(?:\.[A-Za-z])+", actual[0])
          and expected[0].lower() != actual[0].lower()):
        return "different dotted-consonant sequence"
    elif (len(expected) == len(actual) == 1 and vocabulary is not None
          and expected[0].lower() in vocabulary
          and actual[0].lower() in vocabulary
          and actual[0].lower() != expected[0].lower()):
        return "different complete answer word from the known output vocabulary"
    return None


def problem_shape(pid, expected, actual, raw, vocabulary=None):
    basic = algorithmic_shape(expected, actual, vocabulary)
    if basic:
        return basic
    if pid == "74A":
        names = {line.split()[0].decode(errors="replace").lower()
                 for line in raw.splitlines()[1:] if line.split()}
        if (len(expected) == len(actual) == 1 and expected[0].lower() in names
                and actual[0].lower() in names and expected[0] != actual[0]):
            return "different participant winner from the actual input"
    if pid not in ("583A", "660B", "118B") or expected == actual:
        return None
    if not expected or not actual or not all(re.fullmatch(r"\d+", word) for word in expected + actual):
        return None
    parameters = raw.splitlines()[0].split()
    a, e = [int(word) for word in actual], [int(word) for word in expected]
    if pid == "583A":
        limit = int(parameters[0]) ** 2
        if (all(1 <= value <= limit for value in a + e)
                and a == sorted(set(a)) and e == sorted(set(e))):
            return "different legal paving-day list; source review still required"
    if pid == "660B":
        m = int(parameters[1])
        if sorted(e) == list(range(1, m + 1)) and all(1 <= value <= m for value in a):
            return "different passenger order/cardinality; source review still required"
    if pid == "118B":
        n = int(parameters[0])
        if (len(e) == (n + 1) ** 2 + n ** 2 and 0 <= n <= 9
                and all(0 <= value <= n for value in a + e)):
            return "different numeric geometry; source review still required"
    return None


def tests(pid, audit):
    path = HERE / "packages" / pid / "tests"
    witnesses = {name for reference in audit["problems"][pid]["references"]
                 if reference.get("algorithmicWrongAnswer") and reference.get("witness")
                 for name in reference["witness"].get("matchingPackageTests", [])[:1]}
    records = sorted(path.glob("*.in"))
    for item in records:
        if item.stat().st_size < 1024:
            witnesses.add(item.stem)
            if len(witnesses) >= 8:
                break
    return [{"name": name, "input": (path / f"{name}.in").read_bytes().replace(b"\r\n", b"\n"),
             "output": (path / f"{name}.out").read_bytes()}
            for name in sorted(witnesses)]


def candidates(pid, audit):
    references = audit["problems"][pid]["references"]
    used_ids = {str(r["submissionId"]) for r in references}
    used_hashes = {r["sourceHash"] for r in references}
    return [row for row in indexed_sources(pid)
            if str(row["submission_id"]) not in used_ids
            and hashlib.sha256(row["source"].encode()).hexdigest() not in used_hashes
            and row.get("testset") == "TESTS"
            and row.get("programmingLanguage", "").startswith("Python 3")
            and row.get("verdict") == "WRONG_ANSWER"]


def probe(pid, audit, limit, stop_after):
    short_suite = tests(pid, audit)
    meta = read(HERE / "packages" / pid / "meta.json")
    vocabulary = {text[0].lower() for path in (HERE / "packages" / pid / "tests").glob("*.out")
                  if (text := tokens(path.read_bytes())) and len(text) == 1}
    hits, attempted, errors = [], 0, []
    for row in candidates(pid, audit)[:limit]:
        attempted += 1
        try:
            result = run(row["source"], row["programmingLanguage"], short_suite,
                         meta["timeLimitMs"] / 1000, int(meta["memoryLimitMb"]), capture=True)
        except (RuntimeError, ValueError) as exc:
            errors.append({"submissionId": str(row["submission_id"]), "error": str(exc)})
            if "infrastructure" in str(exc) or "unavailable" in str(exc):
                break
            continue
        for test, outcome in zip(short_suite, result.get("runs", [])):
            if outcome["verdict"] != "WA" or outcome["exitCode"] != 0 or outcome["timeout"]:
                continue
            output = base64.b64decode(outcome["output"])
            expected, actual = tokens(test["output"]), tokens(output)
            shape = algorithmic_shape(expected, actual, vocabulary)
            if shape:
                hits.append({"submissionId": str(row["submission_id"]),
                             "sourceHash": hashlib.sha256(row["source"].encode()).hexdigest(),
                             "source": row["provenance"], "language": row["programmingLanguage"],
                             "test": outcome["test"], "input": test["input"].decode(errors="replace"),
                             "expected": test["output"].decode(errors="replace")[:250],
                             "actual": output.decode(errors="replace")[:250],
                             "shape": shape, "result": "potential, requires source-level review/full-suite rerun/different-agent audit"})
                break
        if len(hits) >= stop_after:
            break
    return {"id": pid, "attempted": attempted, "totalUnused": len(candidates(pid, audit)),
            "potentialWitnesses": hits, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ids", nargs="*")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--stop-after", type=int, default=2)
    args = parser.parse_args()
    audit = read(args.audit)
    priority = [row["id"] for row in triage(audit) if row["missingProvenWrong"] == 1]
    ids = args.ids or priority
    if any(pid not in audit["excludedIds"] for pid in ids):
        raise ValueError("only held packages may be probed")
    if args.output.exists():
        prior = read(args.output)
        if prior["auditHead"] != audit["builderHead"]:
            raise ValueError("cannot resume a different audit")
    else:
        prior = {"auditHead": audit["builderHead"], "results": {}}
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(probe, pid, audit, args.limit, args.stop_after): pid
                   for pid in ids if pid not in prior["results"]}
        for future in as_completed(futures):
            result = future.result()
            prior["results"][result["id"]] = result
            tmp = args.output.with_suffix(".partial")
            tmp.write_text(json.dumps(prior, indent=2, sort_keys=True) + "\n")
            tmp.replace(args.output)
            print(result["id"], result["attempted"], "potential", len(result["potentialWitnesses"]),
                  "errors", len(result["errors"]), flush=True)


if __name__ == "__main__":
    main()
