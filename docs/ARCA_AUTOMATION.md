---
id: arca-automation
title: Automating the tax agency (ARCA) for a monotributista: map of tasks, routes, prior art
audience: helper
country: AR
region: ""
language: en
topics: [arca, afip, monotributo, automation, invoicing, apis]
sources:
  - {name: "ralcorta/arcasdk (MIT TypeScript SDK)", url: "https://github.com/ralcorta/arcasdk", kind: community, read_on: 2026-11-02}
  - {name: "Lanuti-Franco/facturador-ARCA (Telegram bot, type C)", url: "https://github.com/Lanuti-Franco/facturador-ARCA", kind: community, read_on: 2026-11-02}
  - {name: "LcsGrz/arcli (MIT CLI, invoicing)", url: "https://github.com/LcsGrz/arcli", kind: community, read_on: 2026-11-02}
  - {name: "Yoryoboy/ArcaMCP (MIT MCP server)", url: "https://github.com/Yoryoboy/ArcaMCP", kind: community, read_on: 2026-11-02}
  - {name: "buanzo/agentic-skill-arca-comprobantes (Apache-2.0, Playwright)", url: "https://github.com/buanzo/agentic-skill-arca-comprobantes", kind: community, read_on: 2026-11-02}
  - {name: "reingart/pyafipws (Python, GPL-3)", url: "https://github.com/reingart/pyafipws", kind: community, read_on: 2026-11-02}
  - {name: "Afip SDK docs", url: "https://docs.afipsdk.com/integracion/node.js", kind: vendor, read_on: 2026-11-02}
  - {name: "ARCA web-service catalogue", url: "https://www.arca.gob.ar/ws/documentacion/catalogo.asp", kind: official, read_on: 2026-10-19}
as_of: 2026-11-02
expires: 2027-02-02
status: draft
licence: CC-BY-4.0
verified_by: \"\"
not_verified: ["portal behaviour when automated (captcha, second factor, terms)", "Afip SDK pricing", "voucher listing through the web service by number", "every third-party repository beyond its README"]
---

# Automating ARCA for a monotributista (general)

Written 2026-11-02 from web search plus reading the GitHub pages and docs named in `sources` (READMEs and docs pages only: **no code was run, no repository audited, no portal opened**). Not tax advice. Complements `GOV_LOOKUPS.md` s.1 (what the official API covers), `MONOTRIBUTO_DIY.md` (what the regime asks), `MONOTRIBUTO_SELF_AUDIT.md` (the read-only audit, start there), `ARCA_PORTAL_MAP.md` (which service shows what) and `CONVENIO_MULTILATERAL.md` (the monthly provincial return).

## 1. The one fact that shapes everything

There are **two doors** into the agency, and they cover different things.

| door | how you get in | what it covers | cost / risk |
|---|---|---|---|
| **Web services (SOAP)** | an X.509 certificate you create once, authorised per service in "Administrador de Relaciones"; tickets last ~12 h | issuing invoices (WSFEv1), reading back vouchers, registry and registration certificate | free; the fiscal key is needed **once** (to create the certificate), never stored by your code |
| **The portal (browser)** | tax id + fiscal key, on every run | everything else: monthly-quota current account, payment voucher, recategorisation, "Mis Comprobantes" lists and exports, electronic fiscal address (notifications), delegations | no official API; the key lives wherever the script runs; terms of use **not read** |

Nothing in the official catalogue covers the monthly quota, the current account or recategorisation. So **those three can only be done by hand, by a portal robot, or reduced to a reminder**.

## 2. Task map: what a monotributista does, and the cheapest safe route

| task | frequency | route (cheapest first) | automatable? |
|---|---|---|---|
| Pay the monthly quota | monthly, ~20th | **Direct debit** (bank account or credit card), set once in the portal; fallback: the agency's mobile app or a payment voucher | yes, by the bank: set once, then only verify. A reminder with the holiday-shifted due date covers the rest |
| See what is owed (current account) | monthly | by hand in the portal or the mobile app (reported to show debt and pay). No API | portal robot only (read-only), optional |
| Issue a type C invoice | per sale | web service WSFEv1 with a certificate (`arcli`, `arcasdk`, `pyafipws`, the Telegram bot), or the agency's own free web form | yes, if invoices are frequent; with few a month the web form is enough |
| List or export issued invoices | before each recategorisation, or monthly | "Mis Comprobantes" CSV export by hand; **or** read vouchers back through the web service (query by number, from 1 to the last one on each point of sale: *memory, to verify*), which needs no fiscal key after setup | yes, locally |
| Add up the last 12 months and find the category | twice a year | local script on the exported CSV against the cap table (no model, no network) | yes, 100% local |
| Recategorise | January and July-August | portal service; reported to show the invoiced total by itself when there is electronic invoicing. Submission by hand | compute and remind: yes; submit: by hand |
| Registry and registration certificate (taxes, activities, address) | when needed | web service `ws_sr_constancia_inscripcion` (certificate) | yes |
| **Monthly provincial gross-income return (CM03) and annual (CM05), only if registered in Convenio Multilateral** | monthly, mid-month; annual | "Convenio Multilateral - SIFERE Web - DDJJ" service in the portal. **No API and no open-source tool found** (a commercial Excel helper exists for CM05). Compute the draft locally from the invoice list and the rates; file by hand | compute and remind: yes; submit: by hand |
| Notifications from the agency | continuous | electronic fiscal address in the portal (the home page shows "no notifications" or a count). No API found; the agency also notifies by email (reported) | by hand weekly, or portal robot (read-only) |
| Delegations (accountant, services) | rare | "Administrador de Relaciones" by hand | no, and it should stay manual |
| Cap table and amounts | every semester | published on the agency's site; no API found | by hand, copy into a local table with its date |
| Due-date calendar | continuous | holidays API (`INTEGRATIONS_AR.md` s.1) + a local calendar file | yes |

## 3. Prior art found (2026-11-02)

**Invoicing and registry through web services (the mature part):**
- `ralcorta/arcasdk`: MIT, TypeScript, ~190 stars; the base for several others.
- `Lanuti-Franco/facturador-ARCA`: Telegram bot that issues type C invoices and returns a PDF with QR; Python, ~160 stars, updated Aug 2026. Its wiki **warns against any flow that asks for the fiscal key** and uses a certificate instead.
- `LcsGrz/arcli`: MIT terminal tool (A/B/C, credit and debit notes, export type E, JSON in/out, read-only queries, registry lookup); needs a certificate, a point of sale and Node 22+. No monotributo category, quota or debt features.
- `LaPyme/facturas`: TypeScript SDK and CLI, ~100 stars (not read in detail).
- `reingart/pyafipws`: the long-running Python project (WSAA, WSFEv1, a section on type C for monotributo); GPL-3 (some modules LGPL); parts are Python 2 era. Not checked against the production endpoints.
- Afip SDK (commercial platform + `afip.js`): development mode works without a certificate; for production its docs ask for an **access token from its own platform**. Pricing **not found**.

**Portal automation with the fiscal key (the part we need, and the thin one):**
- `buanzo/agentic-skill-arca-comprobantes`: Apache-2.0, 2 stars, Python and Node scripts for Claude Code or Codex; **Playwright** login with the tax id and key from environment variables; downloads issued vouchers, parses and indexes them, analyses by period and client; prepares invoices but stops before confirming; says it stores no cookies. **The closest match to "Mis Comprobantes export"; very young; not audited.**
- `Yoryoboy/ArcaMCP`: MIT MCP server (~20 tools: vouchers, PDF, registry, catalogues, sales points). Its `mis_comprobantes`, certificate creation and service authorisation run as **Afip SDK cloud automations that take the fiscal key** and need the platform's token. Using it means handing the key to a third party: not for us.
- A Selenium Telegram bot for invoicing was listed in a topic page (not opened).
- **Not found anywhere:** an open-source script that reads the monotributo current account, the quota, the category or recategorisation. Searching GitHub topics (`arca`, `monotributo`) and the web returned nothing; the search tool was US-only, so "not found" is not proof (`INTEGRATIONS_AR.md` header).

## 4. Recommended ladder (cost zero, each step independent)

1. **Direct debit for the quota**, set by hand once (and verify after the first debit). Removes the biggest risk (10 unpaid periods = removal).
2. **Calendar file** with the quota (holiday-shifted), the January and July windows, and the semester table check. Local, offline.
3. **Local category calculator**: input the CSV from "Mis Comprobantes" (exported by hand) and the cap table; output the category, the margin to the next cap and the 50%-fine risk. Writable without any network or key.
4. **Certificate + web services** (one-time, with the fiscal key typed by the owner on the agency's site, never given to a bot): then invoices (`arcli` or `arcasdk`) and the registry certificate run with no key. Worth it only if invoicing is frequent.
5. **Portal robot, read-only** (current account, notifications, vouchers): only if the owner wants it **and says yes to opening a browser** (repo rule). Run it on the owner's machine, key from a prompt or the OS keyring, never in a file or in git, never in chat. Start from reading `buanzo`'s probe script, not from running it. Check the agency's terms of use first.
6. **Never**: write operations through a robot (submitting recategorisation, creating vouchers of payment, delegating), cloud automations that take the key, or a stored key in a bot.

## 4b. Check the registration certificate first

The printable registration certificate (monotributo option certificate, and the one for provincial taxes) says which duties apply. A monotributista with a Convenio Multilateral registration has the monthly CM03 on top of the quota; one without it does not. Read both before assuming the regime is "one payment a month".

## 5. Risks

- The fiscal key is personal and non-transferable; a robot that holds it is a robot that can change contact data. Prefer certificates (revocable per service) over the key.
- The portal can change its pages or add captchas or a second factor at any time: a robot is a maintenance cost. Web services are stable by comparison.
- Advice: information and official links, not tax advice (`INTEGRATIONS_AR.md` s.7).

## 6. Not verified

Everything about the portal's behaviour when automated (captcha, second factor, session length, terms); whether the web services let an individual list vouchers by number as described; Afip SDK pricing and what the free tier allows in production; the contents of the three agency printouts the operator saved (could not be read: no PDF tool installed); the licence and maintenance of every repository above beyond what its README says.

## 7. Bringing third-party repos in (licence rule)

MIT and Apache-2.0 code may be copied with its licence and notice; **GPL-3 (`pyafipws`) may not be copied into this repo without making the combined work GPL**, so use it only as a separate tool or as a reference. Preferred shape: pinned clones in a git-ignored `vendor/` (a manifest lists repo, commit and licence), thin wrappers of our own in `tools/arca/`, and an audit of any code before it runs with a key or a certificate.

## 8. What exists in this repo (tools/arca)

- `data/monotributo_scales.json`: the cap and monthly-total table (valid from 2026-08-01, read from the official page through a summarising fetch: verify). `data/holidays_2026.json`, `holidays_2027.json`: public holidays (community API).
- `category_calc.py`: sums the 12-month window of a "Mis Comprobantes" CSV (credit notes subtract, foreign currency uses the rate column) and says which category the income needs and whether the current one is exceeded. Parser tested on **synthetic** data only: the real CSV header may differ, so run it once on the real file and fix the column names if it reports missing columns.
- `due_calendar.py`: .ics with the quota due date shifted past weekends and holidays, and the January and July reminders.
- `test_arca.py`: self-test. `VENDOR.md`: pinned third-party repos and the audit state.
