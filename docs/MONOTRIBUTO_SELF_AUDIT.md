---
id: monotributo-self-audit
title: Self-audit of a monotributo standing in one evening (read-only)
audience: person
country: AR
region: ""
language: en
topics: [monotributo, arca, category, recategorisation, current-account, convenio-multilateral, accountant-handover]
sources:
  - {name: "ARCA monotributo category table (valid from 2026-08-01)", url: "https://www.arca.gob.ar/monotributo/categorias.asp", kind: official, read_on: 2026-11-02}
  - {name: "Press summaries of the activity-age rules (annualisation, 6-month exemption); contradictory in details", url: "https://www.perfil.com/noticias/canal-e/arca-habilito-la-recategorizacion-del-monotributo-2026-todo-tenes-saber.phtml", kind: press, read_on: 2026-11-02}
  - {name: "Comision Arbitral (Convenio Multilateral) site", url: "https://www.ca.gob.ar", kind: official, read_on: 2026-11-02}
as_of: 2026-11-02
expires: 2027-02-02
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["annualisation rule for 6 to 11 months of activity (press only)", "whether a payment can be reassigned to a not-yet-due period", "legal due dates of the Convenio Multilateral returns for 2026", "every screen name was taken from one user's portal, others may differ"]
---

# Self-audit of a monotributo standing (general)

Method distilled from one real case (2026-11-02), with every personal fact removed. Not tax advice: it tells you **what to look at, in what order, and what to ask**. Everything below is read-only until step 7.

## 1. Why do it

A monotributista can sit in the wrong category for months with nobody noticing, miss a provincial return, pay a month twice, or leave the fiscal key in a chat. Each of these costs money or exposes the account, and each is visible in about ten screens.

## 2. What to gather (and which question each answers)

| item | where | question it answers |
|---|---|---|
| Adhesion form (F.184) and the monotributo option certificate | the monotributo service, printed | category at the start, start date, activity code |
| Registration certificate (provincial) | the registry service | is a **Convenio Multilateral** gross-income registration active, in which jurisdictions |
| Payment credential (F.1520) | the monotributo service | **today's category** and the monthly total |
| List of issued invoices with dates and totals | invoicing service (RCEL) or "Mis Comprobantes" | the real income of the last 12 months |
| Monotributo current account | service "CCMA - Cuenta Corriente de Contribuyentes Monotributistas y Autonomos" | debts, credits, double payments, interest |
| Monthly and annual lists of the Convenio Multilateral returns | "SIFERE Web - DDJJ" | is every month filed, is the annual one filed |
| Electronic fiscal address | "Domicilio Fiscal Electronico" | notifications you never saw |
| Fiscalisation requirements | "SIACE" | open requests from the agency |
| Delegations | "Administrador de Relaciones" | who can act in your name |

See `ARCA_PORTAL_MAP.md` for what each service is. Put the files in a private folder (never in git).

## 3. Steps

1. **Read the registration facts.** Note the start date, the category (the credential's total identifies it against the current table), the activity code, and whether the provincial registration is Convenio Multilateral. If it is, the monotributo is **not** "one payment a month": see `CONVENIO_MULTILATERAL.md`.
2. **Compute the real category.** Export issued invoices, then:
   `python3 tools/arca/category_calc.py invoices.csv --current <letter> --as-of <YYYY-MM-DD> [--start <activity start>]`
   `--as-of` is the end of the window (31/12 for the January recategorisation, 30/06 for July). Credit notes subtract; only the income cap is checked.
3. **Apply the activity-age rule** (reported by press, **verify**): under 6 months at the end of the window = keeps the initial category; 6 to 11 months = income since the start, divided by the months elapsed, times 12 (the tool prints two ways of counting months); 12 months or more = the actual last 12 months. The agency also recategorises by itself at 12 months (reported).
4. **Compare with what you pay.** If the payment equals the monthly total of a category lower than the calculated one, you are probably under-categorised. Check the current account for any recategorisation entry. Reported consequences: automatic recategorisation notified in the electronic fiscal address, differences owed from the date it applies, and a fine; none of it verified here.
5. **Read the current account** (see section 4).
6. **Check the Convenio Multilateral lists** if registered: the monthly returns for every month since the start must be "presented"; the annual return for the first fiscal year is due the following June (reported).
7. **Only now act**, with the accountant's OK if unsure: reassign credits, file late returns, request the recategorisation in the next window.

## 4. Reading the monotributo current account

- Three lines per month: integrated tax, pension contribution, health-insurance contribution. The sum is the quota.
- A **duplicate payment** shows as two payment lines for one obligation and a credit (positive balance) equal to a full month. Each payment line has a "reassign" action; reassigning **one** of the duplicates to a later obligation lets you pay only the difference. Do not reassign both. Keep the full amount ready until the reassignment is visible: a payment can take up to two business days to apply.
- Small leftover interest (cents to a few hundred pesos) comes from paying a day or two late. Pay it when convenient.
- Lines older than your registration date mean a previous registration left periods open: ask.

## 5. Credentials and exports

- The fiscal key is personal and not transferable. An accountant acts through **delegation** (Administrador de Relaciones: you choose the services, they accept). Delegate first, **then change the key** and check the contact email and phone.
- Chat exports, screenshots and PDFs from a professional often contain a password or a tax id. Scan before sharing, redact copies, and delete the original export after rotating the key. Never paste a key to an assistant.

## 6. Message template for the accountant (translate to your language)

> Hi, to organise the handover: (1) please file next month's Convenio Multilateral return as a last favour; (2) I will delegate the services you need in Administrador de Relaciones and then change my key, tell me which services; (3) my payments correspond to category X but my invoices since <start date> add up to about N: how was the July/August recategorisation handled, and does the annualisation for under-12-months activity apply to me? (4) I see no annual Convenio Multilateral return: was it due, and can it be filed now? (5) Could we spend half an hour on a shared screen so I can file the monthly return myself? (6) I have your last fee in mind and will pay as soon as I can.

## 7. Decision table

| finding | action |
|---|---|
| payment matches a lower category than the calculated one | ask the accountant in writing; prepare the next window (January or July) with the tool |
| annual Convenio Multilateral return missing | ask whether it was due; file late if so; ask about fines |
| credit in the current account | reassign (step 7), or ask the accountant |
| key found in a chat | delegate, rotate, delete the export |
| notifications or open fiscalisation requests | read and answer before anything else |
| health-insurance enrolment unfinished | finish it, or confirm coverage in the pension and health services ("Aportes en linea") |

## 8. Not verified

The annualisation and 6-month rules; fines and their amounts; whether reassignment accepts a future period; the legal return due dates of the year; and the screen names, taken from one portal (they may differ by taxpayer type).
