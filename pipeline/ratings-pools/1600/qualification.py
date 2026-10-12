"""Generated-suite proof from authored deterministic cases and a disjoint public oracle."""
import hashlib
import json
from pathlib import Path

from pool_contract import read_json, write_json
from pool_sandbox import EXECUTION_VERSION, kind, run
from pool_sources import sha_file


def generator(pid, module):
    source = Path(module.__file__).read_text()
    return ("import json,sys,types\n"
            f"module=types.ModuleType({module.__name__!r})\n"
            f"code={source!r}\n"
            "exec(compile(code, '/work/authored-recipe.py', 'exec'), module.__dict__)\n"
            "assert int(sys.stdin.readline())==0\n"
            f"pairs=module.extras({pid!r})\n"
            "print(json.dumps([{'input':p['input'],'output':p['output']} for p in pairs],sort_keys=True))\n")


def qualify(pid, base, cache, recipe, rated_pool, arguments, review_generated):
    semantic = read_json(base / 'semantic' / f'{pid}.json')
    if semantic['status'] != 'oracle-constraints-passed' or semantic['recipeHash'] != sha_file(Path(recipe.__file__)):
        raise ValueError('authored constraints/oracle review is blocked or stale')
    evidence = read_json(base / 'evidence' / f'{pid}.json')
    if evidence['status'] != 'execution-passed' or evidence['sandbox']['executionVersion'] != EXECUTION_VERSION:
        raise ValueError('five accepted/five incorrect current-harness executions required before independent oracle selection')
    row = read_json(base / 'state' / pid / 'source-row.json')
    if row['official_tests_complete']:
        return {'id': pid, 'status': 'official-basis-already-available'}
    directory = base / 'state' / pid / 'qualification-sources'
    directory.mkdir(parents=True, exist_ok=True)
    generated_source = generator(pid, recipe)
    (directory / 'generator.py').write_text(generated_source)
    used = {s['sourceHash'] for s in evidence['submissions']}
    source_report = read_json(base / 'submission-report.json')
    selected = base / 'submissions' / 'selected' / f'{pid}.json'
    if sha_file(selected) != source_report['files'][selected.name]:
        raise ValueError('changed pinned public submission selection')
    candidates = [s for s in read_json(selected) if s['verdict'] == 'OK' and
                  hashlib.sha256(s['source'].encode()).hexdigest() not in used and kind(s['programmingLanguage'])]
    tests = [{'name': p.stem, 'input': p.read_bytes(), 'output': p.with_suffix('.out').read_bytes()}
             for p in sorted((base / 'packages' / pid / 'tests').glob('*.in'))]
    samples = [{'name': f'sample-{p.stem}', 'input': p.read_bytes(), 'output': p.with_suffix('.out').read_bytes()}
               for p in sorted((base / 'packages' / pid / 'samples').glob('*.in'))]
    attempted = []
    chosen = None
    for candidate in sorted(candidates, key=lambda s: int(s['submission_id']), reverse=True):
        result = run(candidate['source'], candidate['programmingLanguage'], tests + samples,
                     row['time_limit'], row['memory_limit'])
        attempted.append({'submissionId': candidate['submission_id'],
                          'sourceHash': hashlib.sha256(candidate['source'].encode()).hexdigest(),
                          'source': candidate['provenance'], 'result': result})
        write_json(directory / 'oracle-attempts.json', {'counted': False, 'attempts': attempted})
        if result['compiled'] is True and result['verdict'] == 'AC':
            chosen = candidate
            break
    if chosen is None:
        raise ValueError('no sixth disjoint public accepted oracle passed all supplied cases and samples')
    lang = chosen['programmingLanguage']
    path = directory / ('oracle.cpp' if kind(lang) == 'cpp' else 'oracle.py')
    path.write_text(chosen['source'])
    url = f"https://codeforces.com/contest/{chosen['contestId']}/submission/{chosen['submission_id']}"
    write_json(directory / 'source.json', {'source': chosen['provenance'], 'sourceHash': sha_file(path),
               'submissionId': chosen['submission_id'], 'language': lang, 'reviewUrl': url,
               'attribution': 'Public Codeforces accepted submission, not a different-agent audit.'})
    args = arguments(pid, cache)
    args.extra_tests = None
    args.generator_source = str(directory / 'generator.py')
    args.generator_language = 'Python 3'
    args.generator_author = args.validator
    args.oracle_source = str(path)
    args.oracle_language = lang
    args.oracle_author = f"codeforces-submission:{chosen['submission_id']}"
    args.oracle_review_url = url
    args.seed = 0
    args.exhaustive_domain_size = None
    args.exhaustive_domain = None
    generated = rated_pool.generate(args)
    extra = recipe.extras(pid)
    review_generated(pid, extra, {'officialCount': generated['official']}, generated)
    write_json(directory / 'generate-result.json', generated)
    return {'id': pid, 'status': 'generated-basis-proof-prepared', 'oracleSubmissionId': chosen['submission_id'],
            'testCount': generated['testCount'], 'qualificationBasis': generated['qualificationBasis'],
            'validated': False, 'next': 're-execute and obtain different-agent content-bound audit'}
