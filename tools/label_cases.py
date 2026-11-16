#!/usr/bin/env python3
"""Blind-label candidate cases and build the casebook.

Each candidate is judged N times by a judge that sees only the facts and
the law, never the author's label. A case enters the casebook only when
the majority verdict equals the author's verdict. Everything else goes
to cases/disputed.jsonl for human review.

Pairs are split together: ~20% of pairs form the exam, the rest train.

  python3 tools/label_cases.py --votes 3 --workers 16
  OPENAGENTLAW_LLM_BACKEND=codex python3 tools/label_cases.py --votes 1 --workers 8
"""
import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor

from common import CASES, code_digest, judge, read_jsonl, write_jsonl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--votes", type=int, default=3)
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--exam-pct", type=int, default=20)
    args = ap.parse_args()

    digest = code_digest()
    cands = read_jsonl(CASES / "raw" / "candidates.jsonl")
    if not cands:
        sys.exit("no candidates; run gen_cases.py first (casebook left untouched)")
    cache_path = CASES / "raw" / "votes.jsonl"
    cache = {r["key"]: r["votes"] for r in read_jsonl(cache_path)}

    def key(c):
        return hashlib.sha1(repr((c["messages"], c["act"], c["code_version"])).encode()).hexdigest()[:16]

    def vote(c):
        k = key(c)
        if k in cache and len(cache[k]) >= args.votes:
            return k, cache[k]
        votes = []
        for _ in range(args.votes):
            try:
                votes.append(judge(c, digest, temperature=0.7))
            except Exception as e:
                print(f"  vote error: {e}", file=sys.stderr)
        return k, votes

    with ThreadPoolExecutor(args.workers) as ex:
        for n, (k, votes) in enumerate(ex.map(vote, cands), 1):
            cache[k] = votes
            if n % 50 == 0:
                write_jsonl(cache_path, [{"key": a, "votes": b} for a, b in cache.items()])
                print(f"voted {n}/{len(cands)}", flush=True)
    write_jsonl(cache_path, [{"key": a, "votes": b} for a, b in cache.items()])

    accepted, disputed = [], []
    for c in cands:
        votes = cache.get(key(c), [])
        tally = Counter(v["verdict"] for v in votes)
        top, n = tally.most_common(1)[0] if tally else (None, 0)
        c = dict(c, votes=dict(tally))
        c.pop("batch", None)
        ok = top == c["verdict"] and n * 2 > len(votes)
        (accepted if ok else disputed).append(c)

    # A pair whose twin was disputed loses its contrast value but is still a valid case.
    seq = defaultdict(int)
    train, exam = [], []
    for c in sorted(accepted, key=lambda c: (c["article"], c["pair"], c["role"])):
        seq[c["article"]] += 1
        c = dict(id=f"AC-{c['article']}-{seq[c['article']]:04d}", **c)
        h = int(hashlib.sha1(c["pair"].encode()).hexdigest(), 16) % 100
        (exam if h < args.exam_pct else train).append(c)

    write_jsonl(CASES / "casebook" / "train.jsonl", train)
    write_jsonl(CASES / "casebook" / "exam.jsonl", exam)
    write_jsonl(CASES / "disputed.jsonl", disputed)
    print(f"candidates {len(cands)} -> accepted {len(accepted)} (train {len(train)}, exam {len(exam)}), disputed {len(disputed)}")
    print("accepted by verdict:", dict(Counter(c["verdict"] for c in accepted)))
    print("disputed by article:", dict(Counter(c["article"] for c in disputed).most_common()))


if __name__ == "__main__":
    main()
