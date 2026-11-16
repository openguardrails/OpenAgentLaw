"""Run with python3 -m unittest discover -s bar -p 'test_*.py'."""
import json
from pathlib import Path
import subprocess
import unittest
from scoring import score

ROOT=Path(__file__).resolve().parent.parent
class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.cases=[json.loads(l) for l in (ROOT/'cases/casebook/exam.jsonl').read_text().splitlines()]
    def test_baselines_and_browser_parity(self):
        samples=[[],[{'id':c['id'],'verdict':'allow','articles':[]} for c in self.cases],
            [{'id':c['id'],'verdict':'hard_block','articles':['CR-101']} for c in self.cases],
            [{'id':c['id'],'verdict':c['verdict'],'articles':c['articles']} for c in self.cases],
            [{'id':c['id'],'verdict':c['verdict'],'articles':'CR-101'} for c in self.cases]]
        for i,predictions in enumerate(samples):
            result=score(self.cases,predictions)
            self.assertEqual(result['meets_draft_thresholds'],i==3)
            self.assertFalse(result['certified'])
            js="const {score}=require('./bar/space/app.js');let s='';process.stdin.on('data',d=>s+=d);process.stdin.on('end',()=>{let x=JSON.parse(s);console.log(JSON.stringify(score(x.cases,x.predictions)))})"
            browser=json.loads(subprocess.check_output(['node','-e',js],cwd=ROOT,input=json.dumps({'cases':self.cases,'predictions':predictions}).encode()))
            for k in browser:self.assertEqual(result[k],browser[k])
    def test_unknown_duplicate_and_empty(self):
        for predictions in [[{'id':'unknown'}],[{'id':self.cases[0]['id']}]*2,[None]]:
            with self.assertRaises(ValueError):score(self.cases,predictions)
        with self.assertRaises(ValueError):score([],[])
    def test_pairs_articles_and_no_answer_leak(self):
        import sys
        sys.path.insert(0,str(ROOT/'tools'))
        from common import parse_code,render_facts,code_digest
        articles={a['id']:a for a in parse_code()};pairs={}
        self.assertTrue(code_digest())
        for c in self.cases:
            pairs.setdefault(c['pair'],[]).append(c)
            self.assertIn(c['article'],articles)
            for label in ['agent-authored-unadjudicated','Expected judgment',c['id']]:
                self.assertNotIn(label,render_facts(c))
        self.assertEqual(len(pairs),24)
        for pair in pairs.values():
            self.assertEqual(len(pair),2)
            self.assertEqual(sum(c['verdict']=='allow' for c in pair),1)

if __name__=='__main__':unittest.main()
