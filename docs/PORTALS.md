---
id: portals
title: "Portal map: where things are done online, and what can be automated (general)"
audience: helper
country: AR
region: ""
language: en
topics: [portals, apis, indices]
sources: []
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Portal map: where things are done online, and what can be automated (general)

Written 2026-10-20. One row per portal; the columns follow the same idea as `STANDARDS.md` (a source, a date, a status). Nothing was tested against a real account; "verify" = confirm on the official site.
Rule that comes first: **never use a browser, log in or enter a person's data without the owner asking for it, and never get past a captcha.** Automation here means official APIs and open data first, then polite read-only fetching of public pages, and otherwise a checklist for a person.

## Automation tiers

| tier | meaning | examples |
|---|---|---|
| T1 | an official API or open dataset, free, no login | BCRA debtor-registry API, national open-data portals, the official daily supermarket-price data |
| T2 | a public page read politely (low rate, cached, honest client, within the site's terms) | a province page that publishes a fixed value, a chain's public catalogue |
| T3 | a person does it (login, captcha, personal data); we only provide a checklist and the link | tax-agency accounts, fine lookups behind a captcha, appointments |
| never | bypassing a captcha, using someone else's credentials, bulk queries about other people | |

## The map

| area | portal | what it does | access | tier | notes |
|---|---|---|---|---|---|
| tax | tax agency web services (WSAA + invoicing and registry services) | electronic invoices, registry data | SOAP, a digital certificate | T1 (invoicing) | no service for quota or debt of an individual (`GOV_LOOKUPS.md`) |
| tax | tax agency current-account and payments services | what is owed, payment voucher | tax id + fiscal key | T3 | pay by hand |
| tax | province tax agency (vehicle and property taxes) | local taxes | web | T3 | find the current address; not mapped yet |
| credit | central bank debtor-registry API | a person's reported financing and days overdue, by tax id | free, **no credentials**, traffic limits per IP; the official manual is a PDF in the bank's catalogue | **T1** | only for the user's **own** id; verify the endpoint path in the manual. Third-party client libraries exist. Cheap way to see one's own credit status |
| fines | province fines lookup | fines by plate or ID | reCAPTCHA | T3 | `TRAFFIC_FINES.md` |
| fines | City fines lookup | fines by plate or ID | address unstable | T3 | find the current page |
| fines | national road-safety lookup | fines in adhered jurisdictions | web | T3 / T2? | a provincial fine did not show there in one case |
| fines | the province's published fixed-unit (UF) value | the value of the unit, updated every two months | a public page | **T2** | worth a tracker: it drives the cost of every fine |
| vehicle | province inspection (VTV) appointment and fee | book, fee schedule | web | T3 | verify the fee in force |
| vehicle | insurer's online office | policy, payments | login | T3 | private to each person |
| prices | national daily supermarket-price data (SEPA / Precios Claros) | prices by store and barcode, one zip per weekday (about 330 MB each) on the national production-open-data portal | open data, CC BY 4.0 (as read on the dataset page) | **T1** (downloaded and read on 2026-10-20) | `GROCERY_PLANNER.md` s.1a; `tools/sepa_probe.py`; the file dates inside the zips need checking |
| prices | chains' catalogues | price, promo, stock, barcode | public web (several run on the same e-commerce platform) | T2 | terms of use; rate limit |
| prices | central wholesale market | weekly wholesale reference reports (press); a retail fair with its own hours | web / on site | T3 | official publication, prices and consumer rules **not confirmed** |
| open data | national open-data portal (CKAN) | datasets, key-less API | API | **T1** | licences per dataset, often blank |
| open data | province open-data catalogue | e.g. free legal-help centres | CSV/GeoJSON | T1 | dates inconsistent |
| benefits | household energy-subsidy registry | enrol to get the subsidy | login with the person's data | T3 | `PRIOR_ART.md` s.4; no benefit before enrolling |
| benefits | consumer-claims window | file a complaint | login | T3 | |
| benefits | the state assistants (Tina, Mi Argentina) | many procedures | closed | T3 | referral target |
| utilities | electricity, gas, water companies and regulators | bills, complaints, payment plans | each company's web office | T3 | the right channel is the company first, then the regulator |
| home services | servidos.ar (marketplace for home trades, Buenos Aires and other big cities) | post a free job request, receive quotes from tradespeople; tradespeople get leads and a profile | web and Android app; no commission stated, payment arranged directly | T3 | read 2026-10-30 from its own front page, so all of it is **the site's claim, not verified**: free for both sides, income from an optional paid "Pro" account, ads and affiliates; tradespeople checked by national ID, plus licence for gas and fixed electrical work; the exact address goes only to the accepted professional. Terms at `/terminos`, privacy at `/privacidad`. Trades named: plumbing, electrical, gas, painting, cleaning, appliance repair (building trades such as masonry not named). Use: (a) a person who needs a repair compares several quotes for free; (b) a person with a trade gets free leads (`QUICK_INCOME_PLAYBOOK.md` s.4b). Read the terms before using it; check reviews and the professional yourself |
| indices and FX | BCRA monetary v4.0 (ICL, CER, UVA), BCRA exchange quotes, national time-series API (CPI), community dollar API, holidays API | indices, rates, holidays | open JSON, no key | **T1** (tested 2026-11-02) | endpoints and caveats in `INTEGRATIONS_AR.md` s.1 |
| telecom | internet and mobile providers | bills, plan changes | app or chat | T3 | no API; the chat gives retention offers (`CASH_CRUNCH_PLAYBOOK.md` s.8) |

## What to automate first (cheapest, most value)

1. **Supermarket price snapshot** from the official daily data (T1), then the planner (`GROCERY_PLANNER.md`).
2. **UF value tracker** (T2): one fetch every two months, written to a small dated file; the fine calculator reads it.
3. **Own credit check** with the central-bank API (T1), run by the owner on their own id; the assistant never stores ids.
4. **Link and freshness checker** for the repo's own pages (`STANDARDS.md` s.7).
5. Everything else stays T3 with a checklist.

## Rules for any automation

- Prefer official APIs and open data; read the terms; identify the client honestly; low rate; cache; stop on errors.
- Never store credentials, fiscal keys or ID numbers in the repo; scripts take them at run time from the owner.
- Run on the user's own machine; nothing about a person leaves it.
- A browser is used only when the owner asks, for that task; otherwise T3 means "here is the link and the steps".
