---
id: cost-ladder
title: "The cost ladder, and what is left to extract"
audience: helper
country: ""
region: ""
language: en
topics: [cost, architecture, ai-spend]
sources: []
as_of: 2026-10-19
expires: 2027-04-17
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# The cost ladder, and what is left to extract

Principle (2026-10-19): the system exists to spend as little as possible. Free and local first; paid only when a person decides.

See also: `CANCEL_GUIDE.md` (how to cancel a paid subscription and check it took effect), `CASH_CRUNCH_PLAYBOOK.md` (several bills due at once, bills, seasonality, CV to money map),
`FUNDING_LINKS.md` (how donations link to git, and what to weigh).

## Already here

- **Router** (`router/router.py`): per turn, home model → classify (LOCAL/NUBE) → cloud only after a consent message that says why,
  which model and what travels. "siempre" is remembered on disk for 24 h and survives a restart; a delegated subagent rides on the
  last consent for 15 min. With the home model out, a call with an image (Hermes's vision call, or video frames) uses a cloud
  vision model on that same consent; without it, a 503 says how to give it.
- **Providers** (`providers.py`): NVIDIA NIM, Gemini, Hugging Face, OpenRouter, Groq; free ones first; models that share one free
  daily cap are flagged so probing does not spend it.

## Not built here yet (in this order)

1. **Model menu**: probes every candidate the way the client calls it (one tool defined, plus an image for vision models)
   and lists only what answers 200. Saves the time and the calls spent on models with no credit. Coupled to Hermes's config.
2. **Key usage and key check**: tokens and calls used per key, expiry, free quota nearly gone. Coupled to Hermes's
   `state.db`.
3. **Waker**: stacks sleep after idle minutes and wake on a visit, a Telegram message or a due cron (RAM guard included).
4. **Telemetry**: usage reports with no personal data.

## Measured, for choosing the order of the cloud chain

Image description through the cloud on 2026-10-19: NVIDIA gemma-4-31b 5 s, Gemini flash-lite 6 s, NVIDIA nemotron-3-nano-omni 28 s.
Gemini's free tier is about 5 requests/min, so it is the backup, not the front. `VISION_CLOUD` in the router still lists
nemotron-3-nano-omni first; gemma-4-31b first would be 5x faster.
