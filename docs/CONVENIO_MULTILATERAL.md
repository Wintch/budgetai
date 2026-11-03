---
id: convenio-multilateral
title: Convenio Multilateral gross-income returns for a small independent worker
audience: person
country: AR
region: ""
language: en
topics: [convenio-multilateral, ingresos-brutos, sifere, cm03, cm05, monotributo]
sources:
  - {name: "Comision Arbitral, SIFERE due dates (example year)", url: "https://www.ca.gob.ar/descargas/sifere/vencimientos/rg_12.2024_vencimientos_SIFERE_2025.pdf", kind: official, read_on: 2026-11-02}
  - {name: "Search summary: annual return CM05 for fiscal 2025 due 2026-06-30 (Comision Arbitral RG 20/2025), no extension found", url: "https://www.ca.gob.ar", kind: official, read_on: 2026-11-02}
as_of: 2026-11-02
expires: 2027-02-02
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["2026 monthly due dates by tax-id ending", "whether the annual return is due for a registration made in December", "fines for a missed annual return", "rates and coefficients, taken from one observed draft"]
---

# Convenio Multilateral returns (general)

If a monotributista is registered in provincial gross-income tax **under the Convenio Multilateral** (typical when clients sit in other provinces), the picture "one payment a month and no returns" is wrong.

## 1. What is due

| duty | form | how often | where |
|---|---|---|---|
| Monthly return and payment of the provincial gross-income tax, split between jurisdictions | CM03 | monthly (the due date is set each year by the Comision Arbitral; historically mid-month, around the 13th to 20th; **not verified for 2026**) | "Convenio Multilateral - SIFERE Web - DDJJ" service |
| Annual return | CM05 | yearly; the one for fiscal year 2025 is reported due **2026-06-30**, extended in some past years | same service, "annual returns" tab |
| Registration of jurisdictions | registry | once, then on changes | registration certificate (provincial) lists them |

The provincial tax is **not** part of the monotributo quota in that case: the unified quota shows the simplified provincial tax as "not applicable by Convenio Multilateral".

## 2. How to check your own standing (read-only)

1. Registration certificate: "IIBB Convenio Multilateral - active", with the jurisdictions and the start month.
2. SIFERE Web, monthly list: one row per month since the start, each "presented" with a transaction number. Presentation days seen: between the 10th and the 19th of the following month.
3. SIFERE Web, annual list: an empty list for a past fiscal year means nothing was presented.
4. SIFERE Web, payment slips: unpaid vouchers.

## 3. Reading a monthly draft

A draft shows, per jurisdiction: determined tax, credits that subtract (withholdings, previous balance), credits that add, balance in your favour and amount to pay. One observed draft: income of 150,000 in a month with a determined tax of 5,250 in the seat jurisdiction, i.e. 3.5% (rate of that activity and period **not verified**), and zero in the other jurisdiction because the month's invoice belonged to a local client. A month with a credit larger than the tax gives "to pay 0" but must still be filed.

## 4. Automation status

No API and no open-source filer found for SIFERE Web (2026-11-02, US-only search, so absence is not proof). A commercial helper builds import spreadsheets for the annual return. Sensible routes: remind monthly (`tools/arca/due_calendar.py` adds a reminder on the 10th), compute the draft locally from the invoice list, file by hand.

## 5. Not verified

See the front-matter. Ask the accountant or the Comision Arbitral for the exact 2026 calendar by tax-id ending, and whether a registration made in December owes the annual return for that year.
