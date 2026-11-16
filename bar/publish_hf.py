#!/usr/bin/env python3
"""Build and publish the public exam using an explicit file allowlist."""
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parent.parent
SPACE = ROOT / 'bar/space'
TARGET = 'openguardrails/OpenAgentLaw-Bar'

def build():
    cases = ROOT / 'cases/casebook/exam.jsonl'
    SPACE.joinpath('exam.jsonl').write_bytes(cases.read_bytes())
    SPACE.joinpath('VERSION').write_bytes((ROOT/'code/VERSION').read_bytes())
    SPACE.joinpath('code.json').write_text(json.dumps({p.stem:p.read_text() for p in sorted((ROOT/'code').glob('*.md'))}))
    SPACE.joinpath('methodology.md').write_bytes((ROOT/'bar/README.md').read_bytes())
    SPACE.joinpath('OGB-LICENSE').write_bytes((ROOT/'bar/sources/OGB-LICENSE').read_bytes())
    kit = ['bar/exam.py','bar/scoring.py','bar/README.md','bar/sources/OGB-LICENSE','tools/common.py','tools/providers.py','CONTRIBUTORS.md','cases/casebook/exam.jsonl','cases/README.md','code/VERSION','LICENSE.md']
    kit += [str(p.relative_to(ROOT)) for p in sorted((ROOT/'code').glob('*.md'))]
    with zipfile.ZipFile(SPACE/'exam-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
        for path in kit:z.write(ROOT/path,path)
    return ['README.md','index.html','app.js','exam.jsonl','VERSION','code.json','methodology.md','OGB-LICENSE','exam-kit.zip']

def request(path, body, content_type='application/json'):
    data = json.dumps(body).encode() if content_type=='application/json' else body
    req=urllib.request.Request('https://huggingface.co'+path,data=data,headers={'Authorization':'Bearer '+os.environ['HF_TOKEN'],'Content-Type':content_type})
    with urllib.request.urlopen(req,timeout=180) as response:return json.load(response)

def commit(repo, files):
    ops=[{'key':'header','value':{'summary':'Publish OpenAgentLaw Bar public pilot'}}]
    ops += [{'key':'file','value':{'path':name,'encoding':'base64','content':base64.b64encode(raw).decode()}} for name,raw in files.items()]
    return request('/api/spaces/'+repo+'/commit/main',('\n'.join(map(json.dumps,ops))+'\n').encode(),'application/x-ndjson')

def main():
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--build-only',action='store_true');args=ap.parse_args()
    files=build()
    if args.build_only:return
    try:request('/api/repos/create',{'type':'space','name':'OpenAgentLaw-Bar','organization':'openguardrails','private':False,'sdk':'static'})
    except urllib.error.HTTPError as error:
        if error.code!=409:raise
    result=commit(TARGET,{name:(SPACE/name).read_bytes() for name in files})
    print(json.dumps({'repo':TARGET,'commit':result.get('commitOid'),'exam_sha256':hashlib.sha256((SPACE/'exam.jsonl').read_bytes()).hexdigest()}),flush=True)

if __name__=='__main__':main()
