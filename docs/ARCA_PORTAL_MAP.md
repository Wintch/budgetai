---
id: arca-portal-map
title: ARCA portal map for a monotributista: services, what each shows, read or write
audience: person
country: AR
region: ""
language: en
topics: [arca, portal, services, monotributo, convenio-multilateral]
sources:
  - {name: "A monotributista's list of services as displayed (user-pasted screen)", url: "https://auth.afip.gob.ar/contribuyente_/login.xhtml", kind: observed, read_on: 2026-11-02}
as_of: 2026-11-02
expires: 2027-02-02
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["screen names and menu paths come from one account; they change over time", "none of the actions below was performed by the author of this page"]
---

# ARCA portal map (general)

Names as shown in one monotributista's "My services" list on 2026-11-02. A service not in your list is added in **Administrador de Relaciones** (adhere a service). The portal has two similarly named current accounts: **make sure it is the monotributo one**.

| service (as displayed) | shows or does | type | use it for |
|---|---|---|---|
| MONOTRIBUTO | adhesion, data changes, category, payment credential, recategorisation | read, and write for changes | today's category and monthly total |
| CCMA - CUENTA CORRIENTE DE CONTRIBUYENTES MONOTRIBUTISTAS Y AUTONOMOS | month-by-month obligations, payments, balances, interest; a "reassign" action on payments | read, write via reassign | debts, credits, double payments |
| CCMA - ARBA - CUENTA CORRIENTE | the **province's** current account (a different service with the same letters) | read | provincial taxes only; not the monotributo |
| COMPROBANTES EN LINEA (RCEL) | issue invoices; query issued ones (list, exports); point-of-sale registry | read and write | issued invoice list; point of sale type |
| MIS COMPROBANTES | issued and received electronic vouchers | read | CSV of issued invoices |
| FACTURADOR | issue and query simplified receipts (RG 5198/2022) | read and write | alternative to RCEL |
| DOMICILIO FISCAL ELECTRONICO | official notifications and messages | read | missed notices |
| SIACE | fiscalisation requirements notified by the agency, with answers | read, write | open requests |
| CONVENIO MULTILATERAL - SIFERE WEB - CONSULTAS / DDJJ | monthly and annual provincial returns, payment slips | read, write | `CONVENIO_MULTILATERAL.md` |
| CONVENIO MULTILATERAL - PADRON WEB | the jurisdictions registered | read | where you are registered |
| ADMINISTRADOR DE RELACIONES DE CLAVE FISCAL | add services; delegate to a representative; revoke; change profile | write | handover to an accountant |
| ACEPTACION DE DESIGNACION | accept delegations others made to you | write | working for others |
| PRESENTACION DE DDJJ Y PAGOS | filings and payment vouchers | write | paying a quota by voucher |
| APORTES EN LINEA | personal pension and health-insurance situation | read | whether the health contribution reaches an insurer |
| NUESTRA PARTE | what the agency knows about you from third parties | read | cross-check of your income as the agency sees it |
| SEGUIMIENTO DE TRAMITES | status of requests and appointments | read | pending procedures |
| SISTEMA REGISTRAL | registry changes (taxes, activities, address) | write | address or activity corrections |

Rules of thumb: read-only services are safe to explore; anything that pays, files, delegates or reassigns is a deliberate act, done by the taxpayer, not by a script holding the key (`ARCA_AUTOMATION.md`).
