import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'pipeline'))
import select_problems
import rated_pool
from pool_contract import digest, manifest, pairs, row_gate, verify_evidence, write_json, publication_gate
from pool_sources import PINS
from pool_sandbox import IMAGE, COMPILER_FLAGS, EXECUTION_VERSION


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.package = self.base / '1200/packages/999999A'
        self.package.mkdir(parents=True)
        self.rating = 1200
        write_json(self.package/'meta.json', {'id':'999999A','rating':1200,'specialJudge':False,'floatEps':None,'poolPipeline':1})
        (self.package/'statement.html').write_text('<p>statement</p>')
        (self.package/'tests').mkdir()
        (self.package/'tests/0001.in').write_text('1\n')
        (self.package/'tests/0001.out').write_text('2\n')
        (self.package/'samples').mkdir()
        (self.package/'samples/0001.in').write_text('0\n')
        (self.package/'samples/0001.out').write_text('1\n')
        a=hashlib.sha256(b'1\n').hexdigest();b=hashlib.sha256(b'2\n').hexdigest()
        write_json(self.package/'provenance.json', {'pins':PINS,'apiRating':1200,'tests':{'officialIncluded':1,'officialComplete':True,'officialAdvertised':1,'generatedIncluded':0,'generatedAdvertised':0,'pairs':[{'name':'0001','origin':'official','inputHash':a,'outputHash':b}]}})
        files=manifest(self.package);ph=digest(files)
        coverage={k:[{'test':'0001','reason':k+' constraint check'}] for k in ['boundary','adversarial','maxSize']}
        coverage.update({'packageHash':ph,'inputConstraints':'reviewed','checkerSemantics':'unique output','statementComplete':'reviewed'})
        runs=[]
        for i in range(10):
            runs.append({'submissionId':str(i),'sourceHash':hashlib.sha256(str(i).encode()).hexdigest(),'expected':'OK' if i<5 else 'WRONG_ANSWER','compiled':True,'verdict':'AC' if i<5 else 'WA','failedTest':None if i<5 else '0001','testsRun':1,'source':{'dataset':'open-r1/codeforces-submissions','revision':PINS['open-r1/codeforces-submissions']},'runs':[{'test':'0001','verdict':'AC' if i<5 else 'WA','exitCode':0,'timeout':False,'outputHash':b}]})
        self.evidence={'schemaVersion':1,'id':'999999A','rating':1200,'files':files,'packageHash':ph,'status':'execution-passed','stages':['prepare','generate','validate'],'coverage':coverage,'submissions':runs,'testCount':1,'validator':'worker','acceptedContradiction':False,'sandbox':{'image':IMAGE,'network':'none','bounded':True,'harnessHash':'a'*64,'runnerHash':'b'*64,'checkerHash':'c'*64}}
        self.audit={'evidenceHash':digest(self.evidence),'packageHash':ph,'approved':True,'reviewer':'auditor','reviewUrl':'https://review.example','checks':{k:True for k in ['sourceAttribution','fullTests','coverage','fiveAcceptedFiveIncorrect','noSpecialChecker','hashes']}}
        self.evidence['sandbox'].update(executionVersion=EXECUTION_VERSION,compilerFlags=COMPILER_FLAGS)
        for run in self.evidence['submissions']:run.update(executionVersion=EXECUTION_VERSION,compilerFlags=COMPILER_FLAGS)
        self.audit['evidenceHash']=digest(self.evidence)

    def tearDown(self):
        self.tmp.cleanup()

    def valid_row(self):
        return {'id':'1/A','description':'task','input_format':'n','output_format':'answer','title':'title','input_mode':'stdio','time_limit':1,'memory_limit':256,'official_tests':[{'input':'1','output':'2'},{'input':'2','output':'3'}],'examples':[{'input':'1','output':'2'}],'official_tests_complete':True,'testset_size':2,'generated_tests':0}

    def test_selector_default_and_rating(self):
        problems=[{'contestId':1,'index':'A','rating':r,'type':'PROGRAMMING','name':str(r),'tags':['math']} for r in [800,1200]]
        def api(method,**kwargs):
            return [{'id':1,'name':'Contest','phase':'FINISHED','startTimeSeconds':1000}] if method=='contest.list' else {'problems':problems}
        with patch.object(select_problems,'api',api):
            self.assertEqual(select_problems.candidates(now=1000)[0]['rating'],800)
            self.assertEqual(select_problems.candidates(rating=1200,now=1000)[0]['rating'],1200)

    def test_cli_default(self):
        result=subprocess.run([sys.executable,str(ROOT/'pipeline/rated_pool.py'),'prepare','--workspace',str(self.base)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertEqual(json.loads(result.stdout)['rating'],800)

    def test_missing_empty_truncated_pairs(self):
        for candidate in [None,[],[{'input':'','output':'1'}],[{'input':'1'}],[{'input':'...\n','output':'1'}],[{'input':'1','output':'[truncated]'}]]:
            with self.subTest(candidate=candidate),self.assertRaises(ValueError):pairs(candidate)

    def test_samples_only(self):
        row=self.valid_row();row['official_tests']=row['examples'];row['testset_size']=1
        with self.assertRaisesRegex(ValueError,'samples-only'):row_gate(row)

    def test_missing_incomplete_tests(self):
        row=self.valid_row();row['official_tests_complete']=False
        with self.assertRaises(ValueError):row_gate(row)

    def test_completeness_count(self):
        row=self.valid_row();row['testset_size']=3
        with self.assertRaises(ValueError):row_gate(row)

    def test_metadata_boolean_not_validation(self):
        row=self.valid_row();row['official_tests']=[];row['executable']=True
        with self.assertRaises(ValueError):row_gate(row)

    def test_special_checker(self):
        row=self.valid_row();row['generated_checker']='print(1)'
        with self.assertRaises(ValueError):row_gate(row)

    def test_valid_evidence(self):
        self.assertEqual(verify_evidence(self.package,self.evidence,self.audit),self.evidence['files'])

    def test_changed_hash(self):
        (self.package/'tests/0001.in').write_text('3\n')
        with self.assertRaisesRegex(ValueError,'changed package'):verify_evidence(self.package,self.evidence,self.audit)

    def test_unpaired_empty_tests(self):
        (self.package/'tests/0001.out').unlink()
        with self.assertRaises(ValueError):manifest(self.package)
        (self.package/'tests/0001.out').write_text('')
        with self.assertRaises(ValueError):manifest(self.package)

    def test_unexpected_files_and_symlinks(self):
        (self.package/'extra.txt').write_text('x')
        with self.assertRaises(ValueError):manifest(self.package)
        (self.package/'extra.txt').unlink();(self.package/'tests/0002.in').symlink_to(self.package/'tests/0001.in')
        with self.assertRaises(ValueError):manifest(self.package)

    def test_interrupted_stages(self):
        e=copy.deepcopy(self.evidence);e['stages']=['prepare','generate']
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_missing_quota(self):
        e=copy.deepcopy(self.evidence);e['submissions'].pop()
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_compile_error_is_not_kill(self):
        e=copy.deepcopy(self.evidence);e['submissions'][-1]['compiled']=False
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_duplicate_sources(self):
        e=copy.deepcopy(self.evidence);e['submissions'][-1]['sourceHash']=e['submissions'][0]['sourceHash']
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_unresolved_accepted_contradiction(self):
        e=copy.deepcopy(self.evidence);e['acceptedContradiction']=True
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_incomplete_per_test_evidence(self):
        e=copy.deepcopy(self.evidence);e['submissions'][0]['runs']=[]
        with self.assertRaises(ValueError):verify_evidence(self.package,e,self.audit)

    def test_stale_audit_and_self_approval(self):
        for field,value in [('evidenceHash','wrong'),('reviewer','worker'),('approved',False)]:
            a=copy.deepcopy(self.audit);a[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):verify_evidence(self.package,self.evidence,a)

    def test_gate_bypass_and_explicit_approval(self):
        write_json(self.base/'1200/evidence/999999A.json',self.evidence)
        write_json(self.base/'1200/audits/999999A.json',self.audit)
        self.assertFalse(publication_gate(self.package,self.base,require_approval=False)['legacy'])
        with self.assertRaises((ValueError,OSError)):publication_gate(self.package,self.base,self.base/'missing-approval.json')
        approval={'action':'publish','approvedBy':'operator','approvalUrl':'https://approval.example','packages':{'999999A':{'packageHash':self.evidence['packageHash'],'evidenceHash':digest(self.evidence),'auditHash':digest(self.audit)}}}
        write_json(self.base/'approval.json',approval)
        self.assertFalse(publication_gate(self.package,self.base,self.base/'approval.json')['legacy'])
        approval['packages']['999999A']['packageHash']='wrong';write_json(self.base/'approval.json',approval)
        with self.assertRaises(ValueError):publication_gate(self.package,self.base,self.base/'approval.json')

    def test_new_harder_and_new_800_no_legacy_bypass(self):
        (self.base/'1200/evidence').mkdir(exist_ok=True)
        with self.assertRaises(OSError):publication_gate(self.package,self.base,require_approval=False)
        meta={'id':'999999A','rating':800};write_json(self.package/'meta.json',meta)
        with self.assertRaises(OSError):publication_gate(self.package,self.base,require_approval=False)

    def test_inventory_change_interrupts_generation(self):
        args=type('Args',(),{'workspace':str(self.base),'rating':1200,'id':'999999A'})()
        write_json(self.base/'1200/state/999999A/prepare.json',{'inventoryHash':'old'})
        write_json(self.base/'1200/inventory.json',{'items':[]})
        with self.assertRaisesRegex(ValueError,'inventory changed'):rated_pool.generate(args)

    def rebind(self):
        self.evidence['files']=manifest(self.package)
        self.evidence['packageHash']=digest(self.evidence['files'])
        self.evidence['coverage']['packageHash']=self.evidence['packageHash']
        self.audit['packageHash']=self.evidence['packageHash']
        self.audit['evidenceHash']=digest(self.evidence)

    def test_incomplete_official_never_validates(self):
        provenance=json.loads((self.package/'provenance.json').read_text())
        provenance['tests'].update({'officialComplete':False,'officialAdvertised':83})
        write_json(self.package/'provenance.json',provenance);self.rebind()
        with self.assertRaisesRegex(ValueError,'incomplete official'):verify_evidence(self.package,self.evidence,self.audit)

    def test_wrong_test_origin_fails(self):
        provenance=json.loads((self.package/'provenance.json').read_text())
        provenance['tests']['pairs'][0]['origin']='worker-generated'
        write_json(self.package/'provenance.json',provenance);self.rebind()
        with self.assertRaisesRegex(ValueError,'origin/count'):verify_evidence(self.package,self.evidence,self.audit)

    def test_dev_cannot_bypass_rated_gate(self):
        import pool_contract
        with patch.object(pool_contract,'ROOT',self.base):
            p=self.base/'problems/dev/fake';p.mkdir(parents=True)
            write_json(p/'meta.json',{'id':'999999A','rating':1200})
            with self.assertRaises(OSError):publication_gate(p,self.base,require_approval=False)
            write_json(p/'meta.json',{'id':'dev/fake','rating':None})
            with self.assertRaises(OSError):publication_gate(p,self.base,require_approval=False)

    def test_archive_byte_reproducible(self):
        import os
        (self.base/'1200/state/999999A').mkdir(parents=True)
        write_json(self.base/'1200/state/999999A/source.json',{'example':'source'})
        args=type('Args',(),{'workspace':str(self.base),'rating':1200,'id':'999999A','output':str(self.base/'first.tar.gz')})()
        first=rated_pool.archive(args)
        for p in self.package.rglob('*'):os.utime(p,(100000,100000))
        args.output=str(self.base/'second.tar.gz');second=rated_pool.archive(args)
        self.assertEqual(first['sha256'],second['sha256'])
        self.assertTrue(any('state/999999A/source.json' in n for n in second['archiveFiles']))

    def test_missing_checker_checksum_fails(self):
        self.evidence['sandbox'].pop('checkerHash')
        self.audit['evidenceHash']=digest(self.evidence)
        with self.assertRaisesRegex(ValueError,'checksum'):verify_evidence(self.package,self.evidence,self.audit)

    def test_unpinned_image_fails(self):
        self.evidence['sandbox']['image']='python@sha256:'+'a'*64
        self.audit['evidenceHash']=digest(self.evidence)
        with self.assertRaisesRegex(ValueError,'sandbox'):verify_evidence(self.package,self.evidence,self.audit)

    def test_samples_only_hard_gate(self):
        (self.package/'tests/0001.in').write_text('0\n')
        (self.package/'tests/0001.out').write_text('1\n')
        with self.assertRaisesRegex(ValueError,'samples-only'):manifest(self.package)

    def test_missing_samples_and_whitespace_tests(self):
        (self.package/'samples/0001.out').unlink()
        with self.assertRaisesRegex(ValueError,'unpaired samples'):manifest(self.package)
        (self.package/'samples/0001.out').write_text('1\n')
        (self.package/'tests/0001.in').write_text('  \n')
        with self.assertRaisesRegex(ValueError,'empty'):manifest(self.package)

    def test_python_upload_blocks_before_remote(self):
        import os
        with patch.dict(os.environ,{'SUPABASE_URL':'https://invalid.local','SUPABASE_SERVICE_ROLE_KEY':'local-test-placeholder'}):
            import upload_supabase
        with patch.object(upload_supabase,'PROBLEMS_DIR',str(self.base/'1200/packages')), patch.object(upload_supabase.requests,'post',side_effect=AssertionError('remote writes forbidden')) as remote:
            for operation in [upload_supabase.upload_package,upload_supabase.upsert_row]:
                with self.assertRaises(OSError):operation('999999A')
            remote.assert_not_called()

    def test_typescript_seed_blocks_before_remote(self):
        import os,shutil
        node=shutil.which('node')
        if not node:self.fail('Node is required to test TypeScript seed preflight')
        seed=self.base/'seed-fixture';(seed/'scripts').mkdir(parents=True)
        (seed/'pipeline').mkdir()
        for name in ['pool_contract.py','pool_sources.py','pool_sandbox.py','checker.py','legacy_800.json']:
            shutil.copy2(ROOT/'pipeline'/name,seed/'pipeline'/name)
        shutil.copy2(ROOT/'scripts/seed.ts',seed/'scripts/seed.ts')
        (seed/'scripts/env.ts').write_text('export function loadDotEnvLocal(_: string) {}\n')
        (seed/'scripts/supabase.ts').write_text("import fs from 'node:fs';\nfunction forbidden() { fs.writeFileSync(process.env.REMOTE_MARKER!, 'called'); throw new Error('remote forbidden'); }\nexport const ensureBucket=forbidden, uploadObject=forbidden, upsertRows=forbidden;\n")
        pkg=seed/'problems/999999A';pkg.mkdir(parents=True)
        write_json(pkg/'meta.json',{'id':'999999A','rating':1200,'poolPipeline':1})
        marker=self.base/'remote-called'
        result=subprocess.run([node,str(ROOT/'node_modules/tsx/dist/cli.mjs'),str(seed/'scripts/seed.ts'),'--only','999999A'],cwd=ROOT,env={**os.environ,'REMOTE_MARKER':str(marker)},capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertIn('1200/evidence/999999A.json',result.stderr)
        self.assertFalse(marker.exists(),'seed made a remote call before preflight')


class GeneratedTests(unittest.TestCase):
    setUp=PipelineTests.setUp
    tearDown=PipelineTests.tearDown
    valid_row=PipelineTests.valid_row
    def generated_fixture(self):
        from pool_generation import stable_result
        directory=self.package/'qualification';directory.mkdir()
        (directory/'generator.py').write_text('import json\nprint(json.dumps([{\"input\":str(i)+\"\\n\",\"output\":str(i+1)+\"\\n\"} for i in range(2,102)]))\n')
        (directory/'oracle.py').write_text('import sys\nn=int(sys.stdin.read());assert 1<=n<=101\nprint(n+1)\n')
        prov=json.loads((self.package/'provenance.json').read_text())
        prov['qualification']={'basis':'generated'}
        prov['tests'].update(officialComplete=False,officialAdvertised=83,officialRole='supplementary')
        extra=[]
        for i in range(2,102):
            pair={'input':f'{i}\n','output':f'{i+1}\n'};extra.append(pair)
            for ext,key in [('in','input'),('out','output')]:
                (self.package/f'tests/{i:04d}.{ext}').write_text(pair[key])
            prov['tests']['pairs'].append({'name':f'{i:04d}','origin':'worker-generated','inputHash':hashlib.sha256(pair['input'].encode()).hexdigest(),'outputHash':hashlib.sha256(pair['output'].encode()).hexdigest()})
        write_json(self.package/'provenance.json',prov)
        execution={'compiled':True,'verdict':'WA','testsRun':1,'failedTest':'seed','runs':[{'test':'seed','exitCode':0,'timeout':False,'verdict':'WA','outputHash':'d'*64}]}
        gen={'schemaVersion':1,'seed':42,'author':'unit-generator','sourceHash':hashlib.sha256((directory/'generator.py').read_bytes()).hexdigest(),'language':'Python 3','count':100,'distinctInputs':100,'mode':'extensive','pairsHash':digest(extra),'repeatOutputHashes':['d'*64]*2,'executions':[execution]*2,'sandbox':self.evidence['sandbox']}
        oracle={'schemaVersion':1,'author':'unit-oracle','sourceHash':hashlib.sha256((directory/'oracle.py').read_bytes()).hexdigest(),'language':'Python 3','reviewUrl':'https://unit-test.invalid/independent','sandbox':self.evidence['sandbox'],'result':{'compiled':True,'verdict':'AC','testsRun':101,'failedTest':None,'runs':[{'test':p['name'],'exitCode':0,'timeout':False,'verdict':'AC','outputHash':p['outputHash']} for p in prov['tests']['pairs']]}}
        write_json(directory/'generation.json',gen);write_json(directory/'oracle.json',oracle)
        for execution in gen['executions']:execution.update(executionVersion=EXECUTION_VERSION,compilerFlags=COMPILER_FLAGS)
        oracle['result'].update(executionVersion=EXECUTION_VERSION,compilerFlags=COMPILER_FLAGS)
        oracle['sampleResult']={'compiled':True,'verdict':'AC','testsRun':1,'failedTest':None,'runs':[{'test':'sample-0001','exitCode':0,'timeout':False,'verdict':'AC','outputHash':hashlib.sha256(b'1\n').hexdigest()}]}
        write_json(directory/'oracle.json',oracle)
        oracle['sampleResult'].update(executionVersion=EXECUTION_VERSION,compilerFlags=COMPILER_FLAGS)
        write_json(directory/'oracle.json',oracle);write_json(directory/'generation.json',gen)
        self.evidence.update(qualificationBasis='generated',testCount=101)
        for source in self.evidence['submissions']:
            source['testsRun']=101
            source['runs']=[{'test':p['name'],'exitCode':0,'timeout':False,'verdict':source['verdict'],'outputHash':p['outputHash']} for p in prov['tests']['pairs']]
        for key in ['boundary','adversarial','maxSize']:self.evidence['coverage'][key][0]['test']='0002'
        self.audit['qualificationBasis']='generated'
        for key in ['deterministicGeneration','independentOracle','generatedBasis','algorithmicallyWrong','inputConstraints']:self.audit['checks'][key]=True
        self.audit['incorrectAnalysis']={str(i):{'reason':'synthetic wrong algorithm fixture','kind':'wrong-answer','test':'0001'} for i in range(5,10)}
        self.rebind()

    def rebind(self):
        self.evidence['files']=manifest(self.package);self.evidence['packageHash']=digest(self.evidence['files'])
        self.evidence['coverage']['packageHash']=self.evidence['packageHash']
        self.audit.update(evidenceHash=digest(self.evidence),packageHash=self.evidence['packageHash'])

    def change_proof(self,name,mutate):
        path=self.package/f'qualification/{name}.json';record=json.loads(path.read_text());mutate(record);write_json(path,record);self.rebind()

    def test_generated_incomplete_official_positive(self):
        self.generated_fixture();verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_missing_explicit_basis(self):
        self.generated_fixture();self.evidence.pop('qualificationBasis');self.rebind()
        with self.assertRaisesRegex(ValueError,'explicitly'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_missing_oracle_pair(self):
        self.generated_fixture();self.change_proof('oracle',lambda x:x['result']['runs'].pop())
        with self.assertRaisesRegex(ValueError,'every supplied pair'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_oracle_contradiction(self):
        self.generated_fixture();self.change_proof('oracle',lambda x:x['result']['runs'][0].update(verdict='WA'))
        with self.assertRaisesRegex(ValueError,'oracle'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_changed_source(self):
        self.generated_fixture();(self.package/'qualification/oracle.py').write_text('print(0)');self.rebind()
        with self.assertRaisesRegex(ValueError,'source'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_basis_pair_hash(self):
        self.generated_fixture();self.change_proof('generation',lambda x:x.update(pairsHash='f'*64))
        with self.assertRaisesRegex(ValueError,'authored pair'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_repeated_output_mismatch(self):
        self.generated_fixture();self.change_proof('generation',lambda x:x['repeatOutputHashes'].__setitem__(1,'f'*64))
        with self.assertRaisesRegex(ValueError,'reproducible'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_self_authored_oracle(self):
        self.generated_fixture();self.change_proof('oracle',lambda x:x.update(author='unit-generator'))
        with self.assertRaisesRegex(ValueError,'independent'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_upstream_only_coverage(self):
        self.generated_fixture();self.evidence['coverage']['maxSize'][0]['test']='0001';self.rebind()
        with self.assertRaisesRegex(ValueError,'authored'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_missing_extra_audit(self):
        self.generated_fixture();self.audit['checks'].pop('independentOracle')
        with self.assertRaisesRegex(ValueError,'independentOracle'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_algorithmic_defect_required(self):
        self.generated_fixture();self.audit['incorrectAnalysis'].pop('5')
        with self.assertRaisesRegex(ValueError,'algorithmic'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_official_role_explicit(self):
        self.generated_fixture();p=self.package/'provenance.json';v=json.loads(p.read_text());v['tests'].pop('officialRole');write_json(p,v);self.rebind()
        with self.assertRaisesRegex(ValueError,'supplementary'):verify_evidence(self.package,self.evidence,self.audit)

    def test_authored_prepare_still_rejects_malformed(self):
        row=self.valid_row();row.update(official_tests_complete=False,official_tests=[])
        row_gate(row,allow_authored=True)
        row['official_tests']=[{'input':'1','output':'...'}]
        with self.assertRaises(ValueError):row_gate(row,allow_authored=True)

    def test_generated_exhaustive_requires_domain_signoff(self):
        self.generated_fixture();self.change_proof('generation',lambda x:x.update(mode='exhaustive',domainSize=100,domain='finite100-input synthetic unit domain'))
        with self.assertRaisesRegex(ValueError,'domain'):verify_evidence(self.package,self.evidence,self.audit)
        self.audit['checks']['exhaustiveDomain']=True
        verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_quota_not_weakened(self):
        self.generated_fixture();self.evidence['submissions'].pop();self.rebind()
        with self.assertRaisesRegex(ValueError,'fewer'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_contradictions_remain_blocked(self):
        self.generated_fixture();self.evidence['acceptedContradiction']=True;self.rebind()
        with self.assertRaisesRegex(ValueError,'contradiction'):verify_evidence(self.package,self.evidence,self.audit)

    def test_old_inventory_exclusion_migration(self):
        self.assertEqual(rated_pool.inventory_blockers({'exclusions':['incomplete-tests-no-generated-suite']}),[])
        self.assertEqual(rated_pool.inventory_blockers({'exclusions':['unaudited-special-checker','incomplete-tests-no-generated-suite']}),['unaudited-special-checker'])

    def test_generated_no_official_pairs_positive(self):
        self.generated_fixture();(self.package/'tests/0001.in').unlink();(self.package/'tests/0001.out').unlink()
        p=self.package/'provenance.json';prov=json.loads(p.read_text());prov['tests']['officialIncluded']=0;prov['tests']['pairs']=prov['tests']['pairs'][1:];write_json(p,prov)
        self.evidence['testCount']=100
        for sub in self.evidence['submissions']:
            sub['testsRun']=100;sub['runs']=sub['runs'][1:]
            if sub['expected']!='OK':sub['failedTest']='0002';self.audit['incorrectAnalysis'][sub['submissionId']]['test']='0002'
        self.change_proof('oracle',lambda x:x['result'].update(testsRun=100,runs=x['result']['runs'][1:]))
        verify_evidence(self.package,self.evidence,self.audit)

    def test_generator_must_execute_twice_and_match(self):
        from pool_generation import build_generated
        from types import SimpleNamespace
        gen=self.base/'g.py';gen.write_text('print(1)');oracle=self.base/'o.py';oracle.write_text('print(2)')
        args=SimpleNamespace(generator_author='unit-g',oracle_author='unit-o',oracle_review_url='https://unit.invalid',generator_source=str(gen),oracle_source=str(oracle),generator_language='Python 3',oracle_language='Python 3',seed=42,exhaustive_domain_size=None)
        import base64
        def result(data):return {'executionVersion':EXECUTION_VERSION,'compilerFlags':COMPILER_FLAGS,'compiled':True,'verdict':'WA','testsRun':1,'failedTest':'seed','runs':[{'test':'seed','output':base64.b64encode(data).decode(),'exitCode':0,'timeout':False,'verdict':'WA','outputHash':hashlib.sha256(data).hexdigest()}]}
        with patch('pool_generation.run',side_effect=[result(b'[]'),result(b'[1]')]) as runner:
            with self.assertRaisesRegex(ValueError,'deterministic'):build_generated(args,self.valid_row(),[])
            self.assertEqual(runner.call_count,2)

    def test_generator_insufficient_diversity_blocked(self):
        from pool_generation import build_generated
        from types import SimpleNamespace
        gen=self.base/'g.py';gen.write_text('print(1)');oracle=self.base/'o.py';oracle.write_text('print(2)')
        args=SimpleNamespace(generator_author='unit-g',oracle_author='unit-o',oracle_review_url='https://unit.invalid',generator_source=str(gen),oracle_source=str(oracle),generator_language='Python 3',oracle_language='Python 3',seed=42,exhaustive_domain_size=None)
        import base64
        data=json.dumps([{'input':'1\n','output':'2\n'}]*100).encode()
        result={'executionVersion':EXECUTION_VERSION,'compilerFlags':COMPILER_FLAGS,'compiled':True,'verdict':'WA','testsRun':1,'failedTest':'seed','runs':[{'test':'seed','output':base64.b64encode(data).decode(),'exitCode':0,'timeout':False,'verdict':'WA','outputHash':hashlib.sha256(data).hexdigest()}]}
        with patch('pool_generation.run',return_value=result):
            with self.assertRaisesRegex(ValueError,'distinct'):build_generated(args,self.valid_row(),[])

    def test_generated_samples_missing_rejected(self):
        self.generated_fixture();self.change_proof('oracle',lambda x:x.pop('sampleResult'))
        with self.assertRaisesRegex(ValueError,'oracle'):verify_evidence(self.package,self.evidence,self.audit)

    def test_generated_crlf_bytes_preserved(self):
        self.generated_fixture();(self.package/'tests/0002.in').write_bytes(b'2\r\n')
        p=self.package/'provenance.json';prov=json.loads(p.read_text());prov['tests']['pairs'][1]['inputHash']=hashlib.sha256(b'2\r\n').hexdigest();write_json(p,prov)
        extra=[{'input':(self.package/f'tests/{i:04d}.in').read_bytes().decode(),'output':(self.package/f'tests/{i:04d}.out').read_bytes().decode()} for i in range(2,102)]
        self.change_proof('generation',lambda x:x.update(pairsHash=digest(extra)))
        verify_evidence(self.package,self.evidence,self.audit)

    def test_old_compiler_context_rejected(self):
        self.evidence['sandbox'].update(executionVersion=1,compilerFlags=['-O2','-std=c++17']);self.rebind()
        with self.assertRaisesRegex(ValueError,'compiler context'):verify_evidence(self.package,self.evidence,self.audit)

    def test_online_judge_flag_sandbox(self):
        from pool_sandbox import run
        code='#include <bits/stdc++.h>\nusing namespace std;int main(){\n#ifndef ONLINE_JUDGE\nfreopen("missing-local-input","r",stdin);freopen("local-output","w",stdout);\n#endif\nint n;cin>>n;cout<<n+1<<"\\n";}\n'
        result=run(code,'GNU C++17',[{'name':'0001','input':b'1\n','output':b'2\n'}],1.0,256.0)
        self.assertEqual(result['verdict'],'AC');self.assertEqual(result['executionVersion'],2);self.assertEqual(result['compilerFlags'],COMPILER_FLAGS)

    def test_mixed_submission_compiler_context(self):
        self.evidence['submissions'][0]['executionVersion']=1;self.rebind()
        with self.assertRaisesRegex(ValueError,'submission execution'):verify_evidence(self.package,self.evidence,self.audit)

    def test_mixed_generator_compiler_context(self):
        self.generated_fixture();self.change_proof('generation',lambda x:x['executions'][0].update(executionVersion=1))
        with self.assertRaisesRegex(ValueError,'generator execution'):verify_evidence(self.package,self.evidence,self.audit)

    def test_mixed_oracle_compiler_context(self):
        self.generated_fixture();self.change_proof('oracle',lambda x:x['result'].update(compilerFlags=['-O2']))
        with self.assertRaisesRegex(ValueError,'oracle execution'):verify_evidence(self.package,self.evidence,self.audit)

    def test_oracle_author_cannot_audit_package(self):
        self.generated_fixture();self.audit['reviewer']='unit-oracle'
        with self.assertRaisesRegex(ValueError,'auditor must differ'):verify_evidence(self.package,self.evidence,self.audit)


if __name__=='__main__':unittest.main(verbosity=2)
