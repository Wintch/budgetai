# budgetai — personal finances, spending as little as possible

A collection of **how things are done**: practical playbooks and small offline tools for the money side of everyday life (taxes of a small independent worker, utilities, fines, groceries, debt, quick income), written from real cases with the personal details removed. The rule everywhere is **cheapest first**: free official sources and plain scripts before a model, and a model only when it adds something, with every outward or paid step a conscious choice.

**Scope today: Argentina only.** The content, the official sources and the tools are Argentine. The structure is meant to grow to other countries: every page declares its `country` (and optionally `region`) in its front-matter, and the format in `docs/STANDARDS.md` does not depend on the country. Work and the job search are out of scope; this repo is about **finances**.

> Information, not advice. Every page says what it read, when, and what it could not verify. Tax, legal and money decisions are yours (or a professional's); the pages tell you where to check and what to ask.

## Integration side: a module for any personal assistant

budgetai is meant to be **added to a personal assistant as a module**, whichever assistant that is. In that picture this repo is the **knowledge base and the skills**, not a set of loose scripts: the playbooks are what the assistant reads and quotes (each page with its sources, dates and what is unverified), the tools are what a skill calls so that a number comes from a script and not from the model, and the router and `providers.py` are the cost side between the assistant and the models. The skill layout follows the open Agent Skills format (`docs/STANDARDS.md` section 6), so it is not tied to one product.

**Worked example:** [`bridgeai`](https://github.com/Wintch/bridgeai), which deploys one private Hermes Agent per person. If you want to integrate it with another assistant, you are welcome to: the code is MIT, the page text CC-BY-4.0 (see Licence below), so use it.

It also **runs standalone**: read the pages, run the checks and the offline tools with no assistant and no model. Nothing here needs an assistant; an assistant just makes it conversational.

The router also exists in bridgeai (`aibridge/router.py`, the live one). This copy **has diverged** and has not been reconciled; treat bridgeai's as the deployed one.

## Where to start

- **`docs/INDEX.md`**: every playbook with topic, status and expiry date (generated from each page's front-matter). A page past its `expires` date is stale and must be re-checked before it is quoted.
- Good first reads: `docs/MONOTRIBUTO_DIY.md` and `docs/ARCA_RULES_MAP.md` (small-taxpayer regime: duties, recategorisation, fines), `docs/CASH_CRUNCH_PLAYBOOK.md`, `docs/GROCERY_PLANNER.md`.
- `docs/STANDARDS.md`: the one format every page follows (sources, dates, what is not verified).

## What is here

| path | what |
|---|---|
| `docs/` | the playbooks. Argentina-specific, English text, official links first |
| `tools/arca/` | offline helpers for a monotributista: category calculator from an invoice export, due-date calendar, self-tests (synthetic data) |
| `tools/sepa_*.py` | read the official daily supermarket-price file into a small local database; the data itself is never committed |
| `tools/check_docs.py` | checks every playbook's front-matter, dates and sources; regenerates `docs/INDEX.md` |
| `tools/privacy_scan.sh` | blocks secrets, personal strings and anything under `private/` or `presets/` from being committed (runs as a git hook) |
| `router/router.py`, `providers.py` | the AI-cost side, for an assistant that answers from the playbooks: an OpenAI-compatible proxy that tries a home model first and goes to the cloud only on consent (free tiers in order, images included) |
| `presets.example/` | invented example presets; real ones live in the git-ignored `presets/` |
| `AGENTS.md` | rules for AI assistants and contributors, including how commits credit the AIs that helped |

The cost ladder behind the AI side (home model, idle sleep, free tiers with consent, never pay for a probe, know what is left) is in `docs/COST_LADDER.md`, with what is still to build.

## Run the checks

```
python3 tools/check_docs.py
python3 tools/arca/test_arca.py
python3 router/router_selftest.py
ROUTER_DIR=router python3 router/router_smoke.py
```

## Privacy rule

No personal data in this repo: no names, tax ids, addresses, phone numbers, chat exports, chat ids, personal domains, LAN addresses, keys or amounts of a real person's life. Personal notes live in the ignored `private/`, real presets in the ignored `presets/`. `tools/privacy_scan.sh --install` sets the git hooks; it also reads your own private list of forbidden strings from a file outside the repo (path set with `PRIVATE_REPLACEMENTS`; see the script), which never enters git. Worked examples use invented data.

## Status

Early and in motion. Pages are drafts with their gaps listed; the tools are small and stdlib-only; the router's paths are overridable by environment variables and some defaults still reflect the setup it was first written for. Contributions that add a source, correct a rule or flag a stale page are welcome: read `AGENTS.md` first.

Licence: MIT for the code (`LICENSE`); the text of the pages is CC-BY-4.0 (see each page's front-matter).
