import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
import io

sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'tools'))
import providers as P
import common

class ProviderTests(unittest.TestCase):
    def test_catalog_filters_output_without_input_metadata(self):
        models=P.parse_catalog({'data':[{'id':'image','architecture':{'output_modalities':['image']}},
            {'id':'chat','supported_endpoint_types':['openai']},{'id':'embed','supported_endpoint_types':['embeddings']},
            {'id':'chat'},None]})
        self.assertEqual(P.filter_models(models),['chat'])
        with self.assertRaises(P.ProviderError):P.check_model(P.resolve_provider('orcarouter'),'image',models)
    def test_outage_does_not_invent_catalog(self):
        def fail(*args):raise P.ProviderError('unavailable')
        with self.assertRaises(P.ProviderError):P.discover_models(P.resolve_provider('orcarouter'),fetch=fail)
    def test_urls_and_credentials(self):
        p=P.resolve_provider('orcarouter')
        for url in ['http://external.example/v1','https://user:pass@example.com/v1','https://example.com/v1?key=secret','https://example.com/v1#fragment']:
            with self.assertRaises(P.ProviderError):P._check_url(url,'base')
        self.assertEqual(P._check_url('http://127.0.0.1:9000/v1','base'),'http://127.0.0.1:9000/v1')
        self.assertEqual(P.resolve_api_key(p,{'ORCAROUTER_API_KEY':'fake-orca','OPENAGENTLAW_LLM_KEY':'fake-other'}),'fake-orca')
        with self.assertRaises(P.ProviderError):P.resolve_api_key(p,{})
    def test_transport_and_token_budget(self):
        captured={}
        def open_(req,timeout):
            captured['url']=req.full_url;captured['auth']=req.get_header('Authorization');captured['body']=json.loads(req.data)
            return io.BytesIO(json.dumps({'choices':[{'message':{'content':'{"verdict":"allow","articles":[]}'}}]}).encode())
        with patch.dict(os.environ,{'OPENAGENTLAW_LLM_URL':'https://api.orcarouter.ai/v1','OPENAGENTLAW_LLM_MODEL':'test/chat','OPENAGENTLAW_LLM_KEY':'fake-key','OPENAGENTLAW_LLM_MAX_TOKENS':'8192'}),patch('urllib.request.urlopen',open_):
            common._chat_openai([{'role':'user','content':'facts'}],0,4000)
        self.assertEqual(captured['url'],'https://api.orcarouter.ai/v1/chat/completions')
        self.assertEqual(captured['auth'],'Bearer fake-key')
        self.assertEqual(captured['body']['max_tokens'],8192)

if __name__=='__main__':unittest.main()
