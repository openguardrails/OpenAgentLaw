#!/usr/bin/env python3
"""The bar exam (PR-401): score a judge model on the public exam set.

The judge is any OpenAI-compatible chat model (OPENAGENTLAW_LLM_URL / OPENAGENTLAW_LLM_MODEL).
To certify your own judge, replace `judge()` with a call into your model;
the only contract is: facts in, {verdict, articles} out.

  python3 bar/exam.py                 # exam set
  python3 bar/exam.py --set train     # training set
"""
import argparse
import json
import os
import sys
from scoring import score
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
from common import CASES, code_digest, code_version, judge, read_jsonl  # noqa: E402

# PR-401 thresholds (draft)
PASS = {"wrongful_block_rate": ("<=", 0.03), "miss_rate": ("<=", 0.05),
        "hard_miss_rate": ("<=", 0.01), "article_hit_rate": (">=", 0.85)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="exam", choices=["exam", "train"])
    ap.add_argument("--predictions", help="score an existing JSONL file without a model call")
    ap.add_argument("--report", help="write a machine-readable score report")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--out", help="write per-case results to this jsonl")
    ap.add_argument("--provider", choices=["orcarouter"], help="named OpenAI-compatible provider")
    ap.add_argument("--model", help="explicit model ID (recommended over mutable auto routes)")
    ap.add_argument("--base-url", help="explicit OpenAI-compatible endpoint")
    ap.add_argument("--max-tokens", type=int, help="completion token budget")
    ap.add_argument("--list-models", action="store_true", help="list a named provider's live chat models")
    ap.add_argument("--config", help="save reproducibility receipt without credentials")
    args = ap.parse_args()
    if args.workers < 1 or (args.max_tokens is not None and args.max_tokens < 1):
        ap.error("workers and max-tokens must be positive")
    if args.predictions and (args.provider or args.list_models):
        ap.error("offline scoring cannot select a provider")
    if args.list_models and not args.provider:
        ap.error("--list-models requires --provider")
    if args.provider and os.environ.get("OPENAGENTLAW_LLM_BACKEND", "openai") != "openai":
        ap.error("--provider requires the openai backend")
    receipt = {}
    if args.provider:
        from providers import resolve_provider, resolve_api_key, api_base, _check_url, discover_models, check_model, describe_catalog
        provider = resolve_provider(args.provider)
        base = _check_url(args.base_url, "--base-url") if args.base_url else api_base(provider)
        key = "" if args.list_models else resolve_api_key(provider)
        catalog = discover_models(provider, key, url=base.rstrip("/") + "/models")
        if args.list_models:
            print(json.dumps({"provider":provider.id, **describe_catalog(catalog), "models":catalog.ids()}, indent=2))
            return
        model = check_model(provider, args.model or os.environ.get("OPENAGENTLAW_LLM_MODEL") or provider.default_model, catalog.models)
        os.environ.update(OPENAGENTLAW_LLM_URL=base, OPENAGENTLAW_LLM_MODEL=model, OPENAGENTLAW_LLM_KEY=key)
        receipt = {"provider":provider.id, "model_catalog":describe_catalog(catalog)}
    else:
        if args.model:
            os.environ["OPENAGENTLAW_LLM_MODEL"] = args.model
        if args.base_url:
            os.environ["OPENAGENTLAW_LLM_URL"] = args.base_url
    if args.max_tokens:
        os.environ["OPENAGENTLAW_LLM_MAX_TOKENS"] = str(args.max_tokens)
    if not args.predictions:
        receipt.update(backend=os.environ.get("OPENAGENTLAW_LLM_BACKEND", "openai"),
                       model=os.environ.get("OPENAGENTLAW_LLM_MODEL", "dsv41-flash"),
                       base_url=os.environ.get("OPENAGENTLAW_LLM_URL", "http://localhost:8000/v1"),
                       code_version=code_version(), case_set=args.set,
                       max_tokens=int(os.environ.get("OPENAGENTLAW_LLM_MAX_TOKENS", "4000")))
        if args.config:
            Path(args.config).write_text(json.dumps(receipt, indent=2) + "\n")

    cases = read_jsonl(CASES / "casebook" / f"{args.set}.jsonl")
    if not cases:
        sys.exit("no cases; build the casebook first")
    if args.predictions:
        report = score(cases, read_jsonl(args.predictions))
        print(json.dumps(report, indent=2))
        if args.report:
            Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
        return
    digest = code_digest()

    def run(c):
        try:
            return judge(c, digest)
        except Exception as e:
            return {"verdict": None, "articles": [], "reason": f"error: {e}"}

    with ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(run, cases))

    report = score(cases, [{"id": c["id"], **r} for c, r in zip(cases, results)])
    print(json.dumps(report, indent=2))
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2) + "\n")
    passed = report["meets_draft_thresholds"]
    if args.out:
        Path(args.out).write_text("".join(
            json.dumps({"id": c["id"], "expected": c["verdict"], "expected_articles": c["articles"], **r},
                       ensure_ascii=False) + "\n" for c, r in zip(cases, results)))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
