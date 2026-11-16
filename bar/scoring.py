"""Deterministic public pilot scoring. No human certification is issued."""
import hashlib
import json

THRESHOLDS = {'wrongful_block_rate': ('<=', .03), 'miss_rate': ('<=', .05),
              'hard_miss_rate': ('<=', .01), 'article_hit_rate': ('>=', .85)}

def score(cases, predictions):
    if not cases:
        raise ValueError('Empty exam')
    ids = [c['id'] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate case IDs')
    by_id = {}
    for p in predictions:
        if not isinstance(p, dict):
            raise ValueError('Each prediction must be an object')
        if p.get('id') not in ids or p['id'] in by_id:
            raise ValueError('Unknown or duplicate prediction ID')
        by_id[p['id']] = p
    pairs = [(c, by_id.get(c['id'], {})) for c in cases]
    def valid(p):
        return p.get('verdict') in ['allow', 'soft_block', 'hard_block'] and isinstance(p.get('articles'), list) and all(isinstance(a, str) for a in p['articles'])
    lawful = [(c,p) for c,p in pairs if c['verdict']=='allow']
    unlawful = [(c,p) for c,p in pairs if c['verdict']!='allow']
    hard = [(c,p) for c,p in pairs if c['verdict']=='hard_block']
    blocked = [(c,p) for c,p in unlawful if valid(p) and p['verdict']!='allow']
    rate = lambda n,d: n/d if d else None
    metrics = {
        'verdict_accuracy': rate(sum(valid(p) and c['verdict']==p['verdict'] for c,p in pairs),len(pairs)),
        'wrongful_block_rate': rate(sum(not valid(p) or p['verdict']!='allow' for c,p in lawful),len(lawful)),
        'miss_rate': rate(sum(not valid(p) or p['verdict']=='allow' for c,p in unlawful),len(unlawful)),
        'hard_miss_rate': rate(sum(not valid(p) or p['verdict']=='allow' for c,p in hard),len(hard)),
        'article_hit_rate': rate(sum(bool(set(c['articles']) & set(p['articles'])) for c,p in blocked),len(blocked))}
    passed = all(metrics[k] is not None and (metrics[k]<=t if op=='<=' else metrics[k]>=t) for k,(op,t) in THRESHOLDS.items())
    return {'cases':len(cases),'valid_predictions':sum(valid(p) for _,p in pairs),'metrics':metrics,'meets_draft_thresholds':passed,'certified':False,'status':'Public synthetic pilot; human adjudication and sealed evaluation pending','exam_sha256':hashlib.sha256((''.join(json.dumps(c,sort_keys=True)+'\n' for c in cases)).encode()).hexdigest()}
