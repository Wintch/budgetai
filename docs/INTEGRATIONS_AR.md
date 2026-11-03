---
id: integrations-ar
title: What can be integrated in Argentina (payments, prices, accounts, indices) for a personal-finance bot
audience: helper
country: AR
region: ""
language: en
topics: [integrations, apis, payments, prices, indices, bot]
sources:
  - {name: "BCRA monetary statistics API v4.0", url: "https://api.bcra.gob.ar/estadisticas/v4.0/monetarias", kind: official, read_on: 2026-11-02}
  - {name: "BCRA exchange statistics API v1.0", url: "https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones", kind: official, read_on: 2026-11-02}
  - {name: "National time-series API (datos.gob.ar)", url: "https://apis.datos.gob.ar/series/api/series", kind: official, read_on: 2026-11-02}
  - {name: "BCRA API catalogue", url: "https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp", kind: official, read_on: 2026-11-02}
  - {name: "dolarapi.com (community, unofficial)", url: "https://dolarapi.com/v1/dolares", kind: community, read_on: 2026-11-02}
  - {name: "argentinadatos.com (community)", url: "https://api.argentinadatos.com/v1/feriados/2026", kind: community, read_on: 2026-11-02}
  - {name: "WhatsApp Business pricing", url: "https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md", kind: official, read_on: 2026-11-02}
as_of: 2026-11-02
expires: 2027-02-02
status: draft
licence: CC-BY-4.0
verified_by: \"\"
not_verified: ["terms and limits of nearly all sources", "Mercado Pago access for personal accounts", "WhatsApp free window and 2026 rates", "debtor-registry path"]
---

# What can be integrated (general)

Written 2026-11-02 from three research runs (web search, fetched pages) plus direct calls to the public endpoints marked **tested**. Everything else is "snippet" (a search result, not opened) or "memory" (the model's background knowledge): **verify before building on it**. Web search was US-only and thin on Argentine sources, so "not found" is not proof of "does not exist". Terms of use and rate limits were mostly **not read**.

Principle: the cheapest, safest connectors are public and keyless (T1 in `PORTALS.md`), run on the user's machine, and need no credential from the user. Anything that needs a password, a fiscal key or a bank login is out.

## 1. Tested on 2026-11-02 (HTTP 200, no key)

| what | endpoint | note |
|---|---|---|
| Rent index (ICL), CER, UVA | `https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/{id}?limit=N` with id ICL=40, CER=30, UVA=31 | the ICL returned values dated up to 2026-11-16 (published ahead of today). Pin **v4.0**: v3.0 was announced for retirement on 2026-02-28 |
| Official FX, 39 currencies | `https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones` | returned the 2026-10-30 quote; `tipoPase` / `tipoCotizacion` are not documented in what was read (the ARS row shows 0) |
| Dollar types (official, blue, MEP, CCL, card, wholesale, crypto) | `https://dolarapi.com/v1/dolares` | community project, **unofficial**, no stated limit or SLA; each quote has `fechaActualizacion`: always show it |
| CPI (INDEC), national general level | `https://apis.datos.gob.ar/series/api/series?ids=148.3_INIVELNAL_DICI_M_26&limit=2&sort=desc` | the call redirects (HTTP 301): follow redirects. Last value was 2026-08 (about a 2-month lag). In the `meta`, start and end dates look inverted when sorted descending |
| Public holidays | `https://api.argentinadatos.com/v1/feriados/2026` | community project; also exchange-rate history under `/v1/cotizaciones/dolares` (large file: prefer the per-date endpoints) |
| A supermarket catalogue (Carrefour, a VTEX store) | `https://www.carrefour.com.ar/api/catalog_system/pub/products/search?ft=leche&_from=0&_to=2` | answered with HTTP 206 and JSON, no key. **Terms and robots.txt not read**; fragile; use only low-rate, cached, honest-client reads, and prefer the official SEPA data (`GROCERY_PLANNER.md`) |
| Address and locality lookup (Georef) | `https://apis.datos.gob.ar/georef/api/...` | reported working by a research run; licence and limits not read |
| National open-data catalogue (CKAN) | `https://datos.gob.ar/api/3/action/package_search?q=...` | reported working by a research run |

## 2. Useful calculations on top of those (no model needed)

- **Rent adjustment** = rent x index(adjustment date) / index(start or last adjustment). The same ratio works with ICL, CER or CPI. Which index a given contract uses is in the contract: **read the clause**; the national rule changed in 2023 and the parties may now agree freely (general knowledge, not verified).
- **ICL formula** (snippets of a BCRA communication, not verified): the daily factor is built from CPI and wage-index changes, 50% each, with a lag; the BCRA publishes it monthly. Use the published series, do not recompute.
- **Real change of a price or income**: divide by the CPI ratio between two dates (CPI lags about 2 months).
- **Exchange check**: compare the rate obtained at an exchange house with the official buy and sell rates of the same day (and show the community-reported alternatives as information only, with their timestamps).

## 3. What exists but is not usable by an individual today (or not confirmed)

| area | state |
|---|---|
| Open finance (reading your own bank accounts by API) | A decree created a system in 2025 (reported), but the central bank's technical standards were still pending, with a first project reported for 2027 (snippets). **Not operational.** |
| Wallets and bank apps: MODO, Ualá, Cuenta DNI, Naranja X, Brubank, Lemon | no public API for personal data found; Ualá and Naranja X have merchant APIs (memory) |
| Mercado Pago | reports of releases and account balance can be generated by API or panel, scheduled, with the user's own token (snippet; **a personal account's access was not confirmed**). Payment links and QR are for collecting money. Sending transfers is not offered to individuals (memory) |
| Transfers 3.0, DEBIN, QR schemes | reachable only through banks and registered providers; no public developer API for individuals found |
| Bill payment: Pagomiscuentas, Rapipago, Pago Facil, Link, Banelco; utility web offices | no public API found; the right path is each company's web office, direct debit, and a calendar |
| Aggregators (Prometeo and similar) | coverage and price for individuals unknown |
| Credit status | the central bank's debtor-registry API exists and is free and keyless (`GOV_LOOKUPS.md`); **two test calls by a research run returned 404, so the exact path is untested**. Anyone can query any tax id: the bot may query **only the user's own** |
| Tariffs (electricity, gas, transport), the household energy-subsidy registry, medicine prices | no open dataset or API found |
| Fuel pump prices | the energy secretary's open-data portal has wholesale data; per-station data not found; a reported rule change may have made reporting voluntary (unconfirmed) |
| Mercado Libre search | likely locked behind OAuth and app permissions (vendor claim, not confirmed) |
| Vehicle valuation | the registry's valuation tables exist (a 2026 provision, reported); it is a registry-fee valuation, not a market price |
| Basic baskets and minimum wage as series | ids not found (a basic-basket dataset exists, last update shown 2023: stale) |

## 4. Statement import is the realistic account feed

No parser for Argentine bank or wallet exports was found. Budget tools (Firefly III, Actual Budget) import CSV and some EU/US bank feeds, none Argentine (snippets). Plan: the user exports a CSV/PDF from the bank or wallet, a local parser (written here, tested on a synthetic sample) maps it to the ledger; nothing leaves the machine. Categories and subscriptions detection use the same ledger.

## 5. Channel for the bot

- **Telegram**: free and without a business account (memory): first channel.
- **WhatsApp**: per-message billing since 2025-07-01; messages from the user to the business are free, the business pays for its replies by category; a free window applies in some cases (page read 2026-11-02; whether replies inside the 24-hour window are free, and the 2026 rates, were not confirmed). A Business account, a phone number and templates are needed outside the window. Unofficial WhatsApp connectors risk a ban: avoid.
- Never ask the user for a password, a fiscal key, a card number or a bank PIN in chat: it is indistinguishable from phishing. Use delegation (the tax agency's relations service) instead of storing a key.

## 6. Existing tools around (all snippet-level, not evaluated)

| tool | what | note |
|---|---|---|
| ARCA SDK libraries (an MIT TypeScript SDK with about 190 stars; a commercial "Afip SDK" platform) | invoicing, registry lookups | read-only registry lookups are the safest use; issuing invoices with someone's key is high risk (`GOV_LOOKUPS.md` s.1) |
| An MCP server for ARCA e-invoicing | 10 tools, 0 stars | untrusted |
| WhatsApp expense-logging bots (several Argentine and Latin American products) | log purchases by chat | closed products; no open-source Argentine one found |
| A monotributo category calculator site | category and simulator | the claim of an MIT licence on its source was not checked |
| Scrapers of the Precios Claros portal and metadata of the official dataset | prices | mostly stale; our route is the official daily zip |
| Official pointers to link, not reimplement | the consumer-protection claim portal; the cancellation ("baja") button rules for telephony, internet, cable, gyms, streaming, insurance (`CANCEL_GUIDE.md`) | page read 2026-11-02 (dated 2021); a 2026 provision on identity checks was only a snippet |

## 7. Risks

- **Advice**: give information with official links, not tax or legal advice; say so.
- **Personal data**: financial data is sensitive; keep it local, minimise, and look up the data-protection law's duties (database registration, consent, deletion) before holding any user's data (`PRIOR_ART.md` s.7 item 10; not checked here).
- **Staleness**: rates, thresholds and categories change; every answer shows its source date, and a page past `expires` is treated as stale.
- **Community APIs**: no SLA; keep a fallback (official BCRA endpoints) and cache.

## 8. Integrate first (ranked)

1. BCRA monetary v4.0 (ICL, CER, UVA) + official FX: rent-adjustment and exchange checks.
2. Dollar types from the community API with the BCRA official rate as the fallback and sanity check.
3. CPI from the national series API.
4. Holidays (due-date shifting in the calendar).
5. Statement import (CSV) into the local ledger.
6. Telegram channel; WhatsApp second, after the pricing is confirmed.
7. Own-id debtor check, after testing the endpoint.

## 9. Not verified

Terms and limits of nearly all sources; Mercado Pago access for personal accounts; WhatsApp free-window and 2026 rates; the debtor-registry path; the status of the open-finance rules after mid-2026; every item marked snippet or memory.
