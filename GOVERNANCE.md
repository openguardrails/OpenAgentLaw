# Governance

Basis: Constitution, Chapters 6 and 7.

## Now: the founding period

- The founding maintainers of OpenGuardrails legislate, and the founder serves as the first Executive (C-71).
- The founding period ends when five certified judges independent of OpenGuardrails exist, or four years after first public release, whichever comes first. A constitutional convention follows (C-72).
- Everything enacted during the founding period is provisional and may be reconsidered as a whole by the convention.

## Changing the law

1. **Propose**: open a pull request that edits the articles in `code/` directly, with your reasoning in the description. Anyone, and any agent, may propose (C-73); an agent must name its manager.
2. **Attach cases**: a change to any article that can block must come with at least one pair of cases (one that should be blocked, one that looks similar but should be allowed) showing how the new text decides them. An article without cases can be neither learned by judges nor tested by the exam.
3. **Discuss**: public discussion lasts at least 14 days.
4. **Decide**: during the founding period the maintainers decide and publish their reasons.
5. **Release**: after merging, update `code/VERSION`. Wording fixes bump the patch version; adding or repealing articles, or moving one between the Civil and Criminal Codes, bumps the minor version; changes to the Constitution bump the major version. Judges must recertify after a major version change (PR-402).

## Changing the casebook

- New cases enter `cases/casebook/` after agreeing blind review or human review.
- To challenge a case, open an issue citing its ID. That is an appeal (PR-302).
- A reversed case keeps its ID and records the reason for reversal; cases are never deleted.

## Language and participation

English is the sole language of this repository, including articles, documentation, cases, and generated judgments. The English text in `code/` is authoritative. People worldwide are invited to propose legislation, build enforcement integrations, train independent judges, review cases, and hear appeals. OpenGuardrails maintains the founding draft through the public process above.

## Article numbers

Once released, an article number is never reused. A repealed article keeps its number and is marked "Repealed".
