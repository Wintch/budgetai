---
id: gov-lookups
title: "Government lookups in Argentina: tax (ARCA) and a pointer to the traffic-fines guide (general)"
audience: person
country: AR
region: ""
language: en
topics: [government, tax, arca, lookups]
sources: []
as_of: 2026-10-19
expires: 2027-04-17
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Government lookups in Argentina: tax (ARCA) and a pointer to the traffic-fines guide (general)

Method notes from looking around, 2026-10-19. Nothing here is about a person. Found by search and by reading the public pages; **not tested against a real account**.

## 1. ARCA (ex AFIP): is there an API?

Yes, but it covers invoicing and registry data, not a taxpayer's own debt or payments.
- **What exists:** SOAP web services. Authentication goes through WSAA with an X.509 certificate that is then associated to each service; the access ticket lasts about 12 hours.
  - Electronic invoicing (WSFEv1): local vouchers, including the type C invoice a monotributista issues.
  - Registry and registration certificate: `ws_sr_constancia_inscripcion`, `ws_sr_padron_a4/a10/a13`.
  - Filing of sworn tax declarations ("Presentacion de DDJJ") exists as a service.
- **What does not exist for a small taxpayer:** nothing in the official catalogue covers monotributo quotas or the current account. "Deuda por CUIT" is reserved for banks. The VEP creation API (`SETIWS-PAGO-API`) is for external bodies, not for an individual.
- **Manual path:** the "Cuenta Corriente de Monotributistas y Autonomos" service shows what is owed (with a debt calculator); "Presentacion de DDJJ y Pagos" generates the VEP. Both need the tax id and the fiscal key. Payment by VEP, transfer, direct debit or wallet can take up to two business days to be applied.
- **Third parties:** `afip.py` (Afip SDK) covers invoices and registry; for production its docs ask for a token from its own platform, so it is not fully self-hosted (cost and licence **not verified**). Community projects exist (a Telegram bot for type C invoices, an MCP server for ARCA); not evaluated.
- **Cheap-first reading:** only automate invoicing if you invoice often; keep paying the quota by hand.
- Catalogue: `arca.gob.ar/ws/documentacion/catalogo.asp`; WSAA: `arca.gob.ar/ws/documentacion/wsaa.asp`.

## 2. Traffic fines

Moved to its own guide: `TRAFFIC_FINES.md` (where to check, how the amount is calculated, laws and time limits, how to pay the least).

## 3. Rule for any browser lookup

Do not open or drive someone's browser for a lookup without asking first, even a read-only one. A plate or id handed over in chat is not permission. Prefer web fetch or search; when a captcha or a login is needed, say so and let the owner do it.
