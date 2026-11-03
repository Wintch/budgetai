---
id: prior-art
title: "Prior art: are we reinventing the wheel? (general)"
audience: helper
country: AR
region: ""
language: en
topics: [prior-art, research]
sources: []
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Prior art: are we reinventing the wheel? (general)

Research run 2026-10-20 (six search lenses, an independent skeptic re-checking each lens, a synthesis, a completeness critic). General only, nothing about a person.
**How far to trust it:** "confirmed" below means a second agent re-opened the page; the author of this repo did not open each page, and several claims are press-only. Verify before relying on any of it.
Goal behind it: this repo collects reusable personal-finance playbooks, starting from Argentina and meant to extend to other countries, cost-first; a possible later step is a low-cost assistant bot (Hermes-style) that answers from vetted playbooks.

## 1. Short answer

- **Partly reinventing.** The directory data format, the evaluation methods and the bot runtime already exist. Do not rebuild them.
- **Likely not reinventing the content layer.** Among what was reviewed we did **not find** an open, maintained, Spanish-language, Argentina-specific set of cash-crunch playbooks, an open directory of free resources for Argentina, or an open-source Argentine benefits or crisis bot. Official assistants (Tina, Boti) exist and are closed. The search was English-first and partial, so read this as "not found", not "does not exist".
- **What we would build:** a curated, dated, vetted Argentine layer (playbooks plus a directory) with a privacy-safe public/private split.
- Prefer reusing **standards and data** over code: several repos reviewed are archived or dormant, and the main reusable codebases are AGPL or GPL.

## 2. What to reuse, integrate or learn from

| purpose | item | how to use it | notes |
|---|---|---|---|
| directory data format | Open Referral HSDS 3.x (`github.com/openreferral/specification`) | **reuse** as the schema, with a stricter minimum profile and Argentine fields | CC BY-SA 4.0; active in 2026; its optional fields are too loose to use as they are |
| directory vocabulary | OpenStreetMap tags `amenity=social_facility` with `soup_kitchen` / `food_bank` | reuse the vocabulary; seed candidates later | Argentine coverage not measured |
| directory practices | Feed America open-data manifesto; Inform USA (AIRS) standards; UK family-hubs post-mortem | **learn from**: stale-after-180-days rule, a last-verified date, curator review, a problem-report queue, minimum contact fields; the UK service was stopped over data quality | US and UK material, not copied |
| directory data (Argentina) | Territorios en Acción map (a university/CONICET project); BA Province CAJUS dataset (free legal-help centres); datos.gob.ar API | **integrate** as leads and seeds, after checking licence and freshness | the first one's licence and freshness are **unconfirmed**; the national registry of canteens (RENACOM) was **repealed** in 2025 |
| benefits engines | OpenFisca, PolicyEngine, aides-jeunes (France), MyFriendBen (US) | **learn from** their structure (rules as data, tests, per-region config); MyFriendBen is the closest analogue | mostly AGPL; no Argentine package found (not fully verified). Start with a table of conditions, not an engine |
| runtime | Hermes Agent (Nous Research, MIT): Telegram/WhatsApp gateways, skills, memory, runs on a small VPS | **integrate**, hardened (section 6) | its own security note says it is a single-tenant personal agent; a public bot for strangers is outside that posture |
| evaluation | Beagle+ (a legal-aid chatbot test with separate Safety and Value ratings); Stanford Legal Design Lab work; Vals benchmark on public-benefits questions; a caseworker study | **learn from** the methods; build our own Argentine test set | Vals suggests follow-up questions help a lot and cheap models score close to expensive ones, but on US English questions only |
| safety | VERA-MH (simulated-persona safety test, MIT); the Partnership on AI primer (no shared standard for crisis hand-off exists); NIST AI 600-1 (voluntary vocabulary) | adopt as a pre-release test and as vocabulary; **never claim compliance** | English and US-oriented |
| failure cases | NYC MyCity chatbot (wrong, illegal advice with a beta disclaimer); DoNotPay (US consumer-protection order) | use as red-team questions; do not overclaim capability | |
| Argentine privacy | Boti study (a digital-rights NGO); the national data-protection agency's responsible-AI guide | use as a privacy checklist source | the guide's text was not read directly |
| tools to recommend | Actual Budget (MIT), Firefly III (AGPL, use as a separate service) | recommend to users | |
| hand-off targets | Tina and Mi Argentina (official assistant); ERAS, ENRE, consumer window | refer people there for authenticated steps | closed systems |

Licensing in short: keep AGPL/GPL code (OpenFisca, Firefly III, Ask Izzy, Glific) as separate services or study material; **cite, do not paste** share-alike or unlicensed text (WHO guidance is NC-SA; government pages have no stated licence).

## 3. The gap this repo can fill

1. Argentine, Spanish, cost-first playbooks with front-matter: official source link, an "as of" date and an expiry date. Official pages are scattered and undated.
2. A hand-curated directory per locality where **every record has a source and a last-verified date**.
3. "What changed" notes: old advice circulates (an old energy-subsidy scheme, a dissolved consumer conciliation service, merged regulators).
4. A thin answer-from-vetted-text bot layer tested on an Argentine question set.
5. The public/private split by design (`private/` ignored, a privacy scan in the hooks).

## 4. Argentine levers worth documenting next (names only; verify every figure before writing it)

Tags: **O** official page read; **P** press only. Amounts and thresholds change monthly: store a link to where to look them up, not the number.

| lever | tag | what it may cut |
|---|---|---|
| energy-subsidy registry for households (income-based; registration is required and no benefit is paid before enrolling) | O, details conflict | electricity, gas, bottled gas |
| national consumer-claims window (the older conciliation service was dissolved in 2025) | O | indirect: disputes with providers |
| cancellation button and the consumer-law rule to cancel through the same channel you contracted | O (2018 resolution), P (later scope) | subscriptions |
| free legal help: Centres of Access to Justice, national line 137 | O | legal costs |
| tax-agency payment plans for small taxpayers (a plan had an adhesion deadline in late Oct 2026) | O existence, P terms | financing only; verify |
| social tariff for water via the regulator ERAS (AMBA); social monotributo; family allowance and food card | P mostly | recurring costs, income support |
| free job portal and municipal employment offices | O | income side |
| food banks (supply organisations, not individuals); municipal registries | O/P | food |

## 5. Staged path to a low-cost assistant (nothing is built; costs mostly unknown)

| stage | what | cost known so far |
|---|---|---|
| 0. docs only | playbooks in Markdown with the front-matter above; a contributing guide; optionally packaged as agent skills | unknown (effort, not money) |
| 1. vetted directory | HSDS-shaped CSV/YAML in git; mandatory fields (name, description, one contact, source, last-verified date, method); stale entries hidden; a human-reviewed problem queue | public APIs seen need no keys; the rest unknown |
| 2. bot answers from vetted text | retrieval-only answers showing source and date; contacts, numbers and links **rendered from records, never generated**; a deterministic check for any number or URL not in the retrieved text; ask follow-up questions first; cheap models first; a 30-50 question Argentine test set | a small VPS is the README claim for the runtime only (**model cost excluded**); a cheap model was about 3 cents per benchmark test run; no cost model exists yet |
| 3. escalation and safety | crisis protocol (stop advising, give verified hotlines, stay bounded); human review of drafts before going public; a safety test as a gate; a privacy notice and a complaint channel | unknown |

## 6. Safety and governance rules to adopt

1. No authoritative standard for crisis hand-off exists: write a conservative protocol of our own; never claim compliance with a standard.
2. Isolate the runtime: one instance per audience, in a container; shell and file tools off; memory and profile-building off; read-only playbook store; an allowlist or pairing.
3. Answer **only** from vetted playbooks; show the source and its date; refuse and refer when nothing matches.
4. Never generate contact details or amounts; render them from structured records.
5. Ask follow-up questions before answering.
6. Say at the first message that it is an AI and never imply it is a lawyer, doctor or adviser (two statutes were seen only in summaries: verify their text).
7. Hotlines come from the official source with a verified date (the status of some national lines was not confirmed).
8. Directory hygiene: minimum fields, a last-verified date, review before merge, a fast path for urgent resources, an expiry rule.
9. Human in the loop first: draft-for-review mode before the public.
10. Test before launch: an Argentine test set, red-team questions from known failures, a safety test; keep the test log.
11. Privacy by design: no personal data in the corpus, screen incoming queries for it, minimal retention, a published notice.
12. Imminent risk (violence, hunger, no shelter) needs a human route and a hotline, not a playbook.
13. Be conservative with evidence: most positive figures are self-reported by builders.

## 7. Not yet covered (next research rounds, in order)

1. **First audience:** a person, or a helper/adviser using the bot? It changes licence, safety and channels.
2. **User groups with their own levers:** older adults (free medicines through the pension health fund), disability pensions, debt and over-indebtedness (card rights, credit-bureau listings, phone collection, no personal-bankruptcy path), tenants and the rent law, informal workers and popular-economy registries, unemployment insurance, students (scholarship), people facing gender violence (hotlines 144/135: verify first).
3. **Scams and predatory lending:** online loans, wallets, informal lenders.
4. **Abuse and cost of a public bot:** spam, cost-draining use, rate limits (cost is this project's core concern).
5. **Channels:** WhatsApp rules and pricing for general chatbots, Telegram share, SMS or voice, printed one-pagers.
6. **Latin American counterparts** (Chile, Brazil, Colombia, Mexico, Uruguay) in Spanish and Portuguese.
7. **Spanish-language model quality** (an open leaderboard for Spanish varieties; open regional models).
8. **Community data:** a national survey of canteens (2024), a city map of canteens (Rosario), city open-data portals.
9. **Sustainability:** who keeps playbooks current, funding, a stale-by-default rule.
10. **Legal exposure:** advice by a bot under Argentine rules, and the data-protection law (registering a database).

Integrations (payments, prices, accounts, indices) researched on 2026-11-02: `INTEGRATIONS_AR.md`.

## 8. Open decisions

Audience; licence for playbooks (for example CC BY) and for directory data (CC BY, CC0 or CC BY-SA: conflicting advice, **decide with a lawyer**); Hermes or a thin custom layer; which first city or province to curate.

## 9. Caveats from the critic

"Not found" rests on limited searching; the benchmark evidence is English and US; some "official" pages are undated, so anything quoted to a person in crisis (hours, hotlines, deadlines) needs a date-read stamp; the energy-subsidy page was read inconsistently by two agents; self-reported results (Caddy, Signpost, MyFriendBen) are builders' claims.
