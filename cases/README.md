# The Casebook

The casebook supplies training data and the public evaluation set for OpenGuardrails and independent agent safety judges. All case content is in English.

- `casebook/train.jsonl`: the training set, for training judges.
- `casebook/exam.jsonl`: the exam set, for the bar exam (`bar/exam.py`). Both cases of a pair are always in the same set.
- `disputed.jsonl`: cases where the author's label and the blind vote disagree, awaiting human judgment. These usually mark articles whose text is unclear.
- `raw/`: unreviewed candidates and vote records (not committed).

## Format

One case per line:

```jsonc
{
  "id": "AC-CR-101-0003",          // AC-<article>-<serial>; AC-ALLOW-* are plain lawful cases
  "code_version": "0.2.0-draft",
  "pair": "b2-00042",              // shared by a violation and its lawful twin
  "role": "violation",             // violation | contrast | benign
  "article": "CR-101",             // the article the pair is built around
  "deployment": "private",         // private | platform | public  (decides the principal, C-4)
  "scenario": "…",
  "title": "one-line summary",

  // The facts: a judge sees only these two fields
  "messages": [                    // the trajectory, OpenAI message format
    {"role": "system", "content": "the manager's configuration"},
    {"role": "user", "content": "the user's instruction"},
    {"role": "assistant", "content": "…", "tool_calls": [{"name": "…", "arguments": {}}]},
    {"role": "tool", "name": "…", "content": "tool output (data)"}
  ],
  "act": {"type": "tool_call", "name": "…", "arguments": {}},   // the act under review
  //     {"type": "message", "content": "…"}                     // or the utterance under review

  // The judgment
  "verdict": "hard_block",         // allow | soft_block (Civil Code) | hard_block (Criminal Code)
  "articles": ["CR-101"],          // [] for allow
  "culprit": "third_party",        // who is responsible: third_party | provider | user | manager | agent | none
  "reasoning": "why this disposition",

  "source": "synthetic",           // synthetic | appeal | final (human final judgment)
  "votes": {"hard_block": 1}       // blind votes
}
```

## Why pairs

Every violation has a lawful twin that looks almost the same: same tools, similar arguments. The only difference is whether the act traces to a proper instruction and whose things it affects. A judge that rules by keywords (`rm -rf`, `curl`, "transfer") gets the twin wrong. The wrongful block rate is a hard requirement of the exam.

## Provenance and trust

The committed case files are currently empty. In the generation and review workflow, candidates are written by a model and then judged blind by a model that does not see the author's label; only agreeing cases enter the casebook. That shows the articles are *consistent* on these cases, not that the judgments are *right*. Final precedent (`source: final`) must come from people.
