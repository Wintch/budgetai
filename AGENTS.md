# Guide for AI assistants and contributors

This repository is a toolkit and a library of personal-finance playbooks, Argentina only for now and designed to extend to other countries, built to spend as little as possible (on AI too). Humans and assistants read it the same way: plain files, checked by scripts.

## Where to start

1. `README.md`: what is here and how the cost ladder works.
2. `docs/INDEX.md`: every playbook with its topic, status and expiry (generated from each page's front-matter).
3. `docs/STANDARDS.md`: the format every page and record follows.
4. `tools/`: small stdlib-only scripts, each with a self-test.

## Layout

- `router/router.py` (+ `router_selftest.py`, `router_smoke.py`): OpenAI-compatible proxy; the home model answers first, the cloud only on explicit consent, images included.
- `providers.py`: providers, keys and the preference order (free tiers first).
- `tools/`: `privacy_scan.sh` (+ `private_pattern.sh`), `check_docs.py`, `sepa_probe.py` and `sepa_ingest.py` (official daily supermarket-price data into a small local SQLite; the data itself is never committed), `arca/` (monotributo category calculator, due-date calendar, self-tests).
- `docs/`: playbooks (generated index in `docs/INDEX.md`); `docs/COST_LADDER.md` lists what is left to extract.
- `presets.example/`: invented example presets. Real presets live in git-ignored `presets/`.

## Rules (follow them exactly)

- **English only in the repo**: docs, comments, commit messages, code identifiers. User-facing text is produced in the user's language at answer time (a few router messages are Spanish on purpose, as runtime strings).
- **No personal data in git**: no names, tax ids, addresses, phone numbers, emails, plates, account or invoice numbers, amounts of a real person's life, chat exports, keys or passwords. Personal material lives in `private/` and `presets/`, both git-ignored. Worked examples use invented data.
- **Never reproduce a secret** found in something the user shares (passwords, fiscal keys, tokens). Redact local copies and tell the user to rotate it.
- **Every fact carries a source and a date.** Volatile numbers (taxes, caps, fees, prices) are stored with where to look them up. Mark anything not read from an official page as not verified, in the page and in the front-matter `not_verified` list.
- **Read-only first.** Anything that pays, files, delegates, reassigns or submits is done by the user, not by a script holding their credentials. No browser or portal session is opened without asking.
- **Cheapest first**: scripts and data before a model; a model only to phrase an answer, never to invent a number, a link or a contact.
- **Information, not advice**: tax, legal and medical topics give official links and questions to ask a professional.
- **Author e-mail**: git publishes the author and committer e-mail of every commit in a public repo. Use the platform's `noreply` address (on GitHub, `ID+username@users.noreply.github.com`, with "Keep my email addresses private" and "Block command line pushes that expose my email" turned on), never a personal address. Rewriting history afterwards does not remove copies already cloned or cached.
- Commit only when asked. Never push unless asked.

## Commit attribution (several AIs work here)

- Several AI tools contribute. **Each tool names itself in a trailer when it writes a commit**; a person never has to retype it.
- Use what the tool writes by default (for example `Co-Authored-By: <tool> <noreply address the vendor documents>`), or, when it writes nothing, the kernel-style line `Assisted-by: AGENT:MODEL_VERSION` (version optional if unknown).
- **Never invent an email address** for a co-author trailer: GitHub links a trailer to whatever account owns that address. Never add `Signed-off-by` on behalf of an AI; only a person signs off.
- Commit messages are English.

## Checks (run before proposing a change)

```
python3 tools/check_docs.py              # front-matter, dates, sources, stale pages
python3 tools/check_docs.py --index      # also regenerates docs/INDEX.md
python3 tools/arca/test_arca.py          # tax tools self-test (synthetic data)
python3 router/router_selftest.py        # router unit checks
tools/privacy_scan.sh --tree             # secrets and private strings in tracked files
```

## Adding or changing a playbook

Copy the front-matter shape from `docs/STANDARDS.md` section 2, fill `sources` with official links and the date you read them, set `expires`, list what you could not verify, then run the checks. A page past `expires` is stale and must be re-checked before it is quoted.
