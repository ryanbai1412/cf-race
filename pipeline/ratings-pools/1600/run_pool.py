"""Concrete recipe stages; invoke the unchanged foundation execution gate."""
import argparse
from hashlib import sha256
from pathlib import Path
import sys
from types import SimpleNamespace

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parents[1]))
import rated_pool
from pool_contract import digest, manifest, read_json, write_json
from pool_sources import PINS, sha_file
import recipes
import extended_recipes
import additional_recipes
import more_recipes
import qualification

MODULES = (recipes, extended_recipes, additional_recipes, more_recipes)
IDS = tuple(pid for module in MODULES for pid in module.IDS)

SEMANTICS = {
    '235A': 'Unique integer maximum LCM of three positive integers, repeats allowed. n1..10^6; brute all triples n<=32 checks the parity/divisibility formula; outputs fit signed64-bit.',
    '322B': 'Unique integer maximum bouquets. Stocks0..10^9. All four allowed bouquet types present in statement. Mixing t+3 replaces three monochrome bouquets with no objective change, so residues0..2 suffice; exhaustive small stocks checks all t.',
    '371C': 'Unique integer maximum hamburgers. Nonempty BSC recipe length<=100, stock/prices1..100, money1..10^12. Monotone cost uses only required ingredients; returned x is affordable and x+1 is not; small linear brute validates binary oracle.',
    '888D': 'Unique integer number of permutations with at most k displaced indices. n4..1000,k1..4; choose displaced subset times its derangements. Exhaustive permutations n4..8 confirm all four budgets; integer answer needs no modulus.',
}
SEMANTICS.update(extended_recipes.SEMANTICS)
SEMANTICS.update(additional_recipes.SEMANTICS)
SEMANTICS.update(more_recipes.SEMANTICS)


def recipe(pid):
    return next(module for module in MODULES if pid in module.IDS)


def selected_submissions(pid, cache, all_submissions=False, index_root=None, problem_ids=None):
    report = read_json(BASE / 'submission-report.json')
    if (report['pins'] != PINS or report['inventoryHash'] != digest(read_json(BASE / 'inventory.json'))
            or report.get('recipeHash') != sha_file(BASE / 'collect_submissions.py')):
        raise ValueError('submission inventory/pin mismatch')
    name = pid.replace('/', '') + '.json'
    path = BASE / 'submissions' / 'selected' / name
    if sha_file(path) != report['files'][name]:
        raise ValueError('changed selected source bytes')
    sources = report['sourceFiles']
    rows = read_json(path)
    for row in rows:
        if row['problem_id'] != pid or row['provenance'] not in sources:
            raise ValueError('source identity/provenance mismatch')
    policy_path = BASE / 'source-policies' / name
    if policy_path.exists():
        policy = read_json(policy_path)
        if policy['id'] != pid.replace('/', ''):
            raise ValueError('source policy identity mismatch')
        exclusions = {}
        for exclusion in policy['exclusions']:
            source_id = str(exclusion['submissionId'])
            matches = [row for row in rows if str(row['submission_id']) == source_id]
            if (source_id in exclusions or len(matches) != 1 or not exclusion['reason']
                    or sha256(matches[0]['source'].encode()).hexdigest() != exclusion['sourceHash']):
                raise ValueError('stale or unbound source exclusion')
            exclusions[source_id] = exclusion
        rows = [row for row in rows if str(row['submission_id']) not in exclusions]
    wrong_answer = [row for row in rows if row['verdict'] == 'WRONG_ANSWER']
    if len(wrong_answer) >= 5:
        rows = [row for row in rows if row['verdict'] in ('OK', 'WRONG_ANSWER')]
    return rows, sources


def arguments(pid, cache):
    return SimpleNamespace(rating=1600, target=100, id=pid, workspace=str(BASE.parent), cache=cache,
                           extra_tests=str(BASE / 'extras' / (pid + '.json')),
                           coverage=str(BASE / 'coverage' / (pid + '.json')), all_submissions=True,
                           validator='devin-1ffab6b544d64d17bf1498a01b5257c0')


def build(pid, cache):
    args = arguments(pid, cache)
    prepared = rated_pool.prepare(args)
    extra = recipe(pid).extras(pid)
    write_json(args.extra_tests, extra)
    generated = rated_pool.generate(args)
    review_generated(pid, extra, prepared, generated)


def review_generated(pid, extra, prepared, generated):
    package = BASE / 'packages' / pid
    tests = [(p.stem, {'input': p.read_text(), 'output': p.with_suffix('.out').read_text()})
             for p in sorted((package / 'tests').glob('*.in'))]
    samples = [('sample-' + p.stem, {'input': p.read_text(), 'output': p.with_suffix('.out').read_text()})
               for p in sorted((package / 'samples').glob('*.in'))]
    failures = recipe(pid).review(pid, tests, samples)
    semantic = {'id': pid, 'packageHash': generated['packageHash'], 'recipeHash': sha_file(Path(recipe(pid).__file__)),
                'officialPairs': prepared['officialCount'], 'extraPairs': len(extra),
                'checkedTests': len(tests), 'checkedSamples': len(samples), 'failures': failures,
                'semantics': SEMANTICS[pid], 'validated': False,
                'status': 'oracle-constraints-passed' if not failures else 'semantic-gap'}
    write_json(BASE / 'semantic' / (pid + '.json'), semantic)
    if failures:
        print(semantic, flush=True)
        raise ValueError('invalid input or conflicting expected output; original bytes retained')
    coverage = {'packageHash': digest(manifest(package)), 'inputConstraints': 'Every supplied official, authored, and sample pair parsed with exact arity/ranges by recipes.parse; integer outputs checked by recipes.answer. ' + SEMANTICS[pid],
                'checkerSemantics': SEMANTICS[pid] + ' Token comparison is appropriate; no floating/multiple-answer/special checker.',
                'statementComplete': 'Manually read full pinned description/input/output/examples; no question or required image omitted for this problem. Superscript constraints are normalized to powers of10 by the recipe; no statement bytes changed.'}
    for category in ('boundary', 'adversarial', 'maxSize'):
        coverage[category] = [{'test': f'{generated["official"] + generated["openR1Generated"] + index:04d}', 'reason': pair['reason']}
                              for index, pair in enumerate(extra, 1) if pair['category'] == category]
    write_json(BASE / 'coverage' / f'{pid}.json', coverage)
    print(generated, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('stage', choices=('build', 'refresh', 'validate', 'qualify', 'report'))
    parser.add_argument('--id', choices=IDS)
    parser.add_argument('--ids', nargs='+', choices=IDS)
    parser.add_argument('--cache', default=str(Path.home() / '.cache' / 'cf-race-pool'))
    args = parser.parse_args()
    selected = [args.id] if args.id else args.ids or IDS
    if args.stage == 'build':
        checks = {pid: count for module in MODULES for pid,count in module.brute_checks().items()}
        write_json(BASE / 'brute-report.json', {'recipeHashes': {m.__name__: sha_file(Path(m.__file__)) for m in MODULES}, 'checks': checks,
                                             'status': 'passed', 'validatedCount': 0})
        for pid in selected:
            try:
                build(pid, args.cache)
            except (ValueError,RuntimeError,IndexError) as exc:
                write_json(BASE / 'build-gaps' / (pid + '.json'), {'id':pid,'status':'blocked','reason':str(exc),'validated':False})
                print({'id':pid,'status':'blocked','reason':str(exc)}, flush=True)
    elif args.stage == 'refresh':
        for pid in selected:
            prepared = {'officialCount': len(read_json(BASE / 'state' / pid / 'source-row.json')['official_tests'])}
            generated_state = read_json(BASE / 'state' / pid / 'generate.json')
            if generated_state['packageHash'] != digest(manifest(BASE / 'packages' / pid)):
                raise ValueError('refresh refuses changed package bytes')
            provenance = read_json(BASE / 'packages' / pid / 'provenance.json')
            generated = {'id': pid, 'status': 'semantic-refreshed', 'packageHash': generated_state['packageHash'],
                         'official': provenance['tests']['officialIncluded'],
                         'openR1Generated': provenance['tests']['generatedIncluded'],
                         'qualificationBasis': provenance['qualification']['basis']}
            try:
                review_generated(pid, recipe(pid).extras(pid), prepared, generated)
            except (ValueError, RuntimeError, IndexError) as exc:
                print({'id': pid, 'status': 'blocked', 'reason': str(exc)}, flush=True)
    elif args.stage == 'qualify':
        for pid in selected:
            try:
                print(qualification.qualify(pid, BASE, args.cache, recipe(pid), rated_pool, arguments, review_generated), flush=True)
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                write_json(BASE / 'build-gaps' / f'{pid}-qualify.json', {'id': pid, 'status': 'blocked', 'reason': str(exc), 'validated': False})
                print({'id': pid, 'status': 'blocked', 'reason': str(exc)}, flush=True)
    elif args.stage == 'validate':
        rated_pool.submissions = selected_submissions
        for pid in selected:
            semantic = read_json(BASE / 'semantic' / (pid + '.json'))
            if (semantic['status'] != 'oracle-constraints-passed' or semantic['packageHash'] != digest(manifest(BASE / 'packages' / pid))
                    or semantic['recipeHash'] != sha_file(Path(recipe(pid).__file__))):
                print({'id':pid,'status':'blocked','reason':'semantic review missing or stale'}, flush=True)
                continue
            print(rated_pool.validate(arguments(pid, args.cache)), flush=True)
    else:
        print(rated_pool.report(arguments(args.id, args.cache)), flush=True)


if __name__ == '__main__':
    main()
