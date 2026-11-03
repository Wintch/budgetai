---
id: data-architecture
title: "Data architecture for the price planner: start small, grow by triggers (general)"
audience: helper
country: ""
region: ""
language: en
topics: [data, architecture, privacy]
sources: []
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Data architecture for the price planner: start small, grow by triggers (general)

Written 2026-10-20 from a real test on the official daily price file (one area, one day). The first version is an MVP for **one or two concurrent users for the next months**; the plan below says when to grow, not that it must.
Figures marked (calc) are my arithmetic on the test; (guess) = an engineering estimate to be measured. The shared price data is **public**; nothing personal belongs on a shared server.

## 1. Decision

**MVP = one small SQLite file per area, built by a script from the official daily zip, read locally by the assistant. No server, no shared database.** Reasons:
- 1-2 users: a file database answers in milliseconds; there is nothing to operate or pay for.
- The data is public and the area is small: the real test (a northern Buenos Aires municipality, 27 branches of 7 groups, Monday 2026-10-19) came to **155,985 price rows in a 21.7 MB file** (calc: about 139 bytes per row with indexes) and loaded in **15 seconds**, from a 330 MB national zip of about 14 million rows.
- Offline-first and private: the user's list, household and price log stay on the user's side; only public prices are shared.
- It is the same schema that a server would use later, so nothing is thrown away when it grows.

## 2. What to store (and what not to)

- Keep: the **branches** of the user's area, and for them the latest full day plus a history of the **items the user actually buys** (a basket of a few hundred to a few thousand barcodes). Full daily history of everything is too big: at about 20 MB a day per area (calc) a year is several GB.
- Store a history row **only when a price changes** (delta storage); measure the daily change rate with two or three days of files before choosing (guess: most prices do not change daily).
- Do not mirror the national zips (330 MB a day); keep the derived file and, if wanted, the link to the official dataset (`GROCERY_PLANNER.md` s.1a).
- Rebuild is cheap: the official file can be re-read, so the database is a cache, not the source of truth.

## 3. Schema (implemented by `tools/sepa_ingest.py`)

| table | key | main columns |
|---|---|---|
| `chain` | id_comercio, id_bandera | banner name, company |
| `branch` | id_comercio, id_bandera, id_sucursal | name, kind, street, number, lat, lon, neighbourhood, postal_code, locality, province |
| `item` | item_id (a barcode when `is_ean`=1) | description, brand, pack size and unit as published |
| `price` | snapshot_date, branch, item_id | list_price, ref_price, ref_qty, ref_unit, promo1_price, promo1_text, promo2_price, promo2_text |

User-side tables (local only, never in a shared service): household profile, weekly list, pantry, manual price log (`source_kind = manual`), the memberships the user holds (`STANDARDS.md` s.4, `LOYALTY_PROGRAMS.md`).
Derived (a view or a job, not typed by hand): `unit_price` per litre, kilo or unit; the cheapest branch per item; the weekly basket per chain.

## 4. What the real test showed about data quality (so the pipeline must normalise)

1. **Pack size and unit are inconsistent**: the same 1-litre milk appears as `1UNI`, `1.00 ml.`, `1ltr`, `1000 ml` depending on the chain.
2. **One group's reference price was wrong**: its "price per reference unit" came out as 205,000 for a 1-litre carton priced 2,050 (a unit mix-up). Never trust the published reference price; **recompute the unit price from the pack size and the list price**, and check it against sanity bounds.
3. **Locality fields are messy**: some chains put the town in the neighbourhood column, use a generic "Buenos Aires" as locality, write postal codes as `1638`, `B1638AAK` or `00001638`, and at least one branch has a postal code from another district. Filter by province plus **both** text and postal code, and review the branches kept.
4. **The same barcode has different descriptions per chain**: key on the barcode, keep the descriptions per chain for display.
5. **Not every product has a barcode** (`is_ean` = 0): those need name matching and a low-confidence flag.
6. **Promotions carry their text** ("valid from..."): parse validity and conditions; a discount that needs a card or a membership is a different price.
7. Some groups were **missing on a given day** (an empty inner zip): the planner must say "no data" instead of assuming a price.

## 5. Worked example: 1-litre milk in the test area (2026-10-19, shelf prices in ARS, per litre)

| item | cheapest group in the area | others |
|---|---|---|
| a low-price UHT whole milk, 1 L | 1,790 (one hypermarket group, three formats) | - |
| the retailer's own-brand sachet, 1 L | 1,899 (a hypermarket chain's own brand) | other chains have their own brands at 1,890 to 2,390 |
| a mid-price whole milk, 3%, 1 L sachet | 1,940 (three groups) | 2,050 and 2,100 at the fifth group's two banners (about 5-8% more) |
| the leading brand's whole milk, sachet 1 L | about 2,049-2,050 (two groups) | 2,094-2,103 (one group) and 2,140 (another): a gap of about 4-5% for the **same** product |
The cheapest 1-litre milk was a low-price brand, about **13% below** the leading brand at the cheapest chain (calc: 1,790 vs 2,049). Brand choice moves the price more than chain choice here. Shelf prices only, no membership or card discounts applied. One day, one area: not a trend.

## 6. Growth plan (triggers, not dates)

| stage | what | when to move up (guess) | cost |
|---|---|---|---|
| **S0 (now)** | a daily job on the owner's machine builds the area file; the assistant or a script reads it; WAL mode; the job writes to a new file and renames it atomically | - | none |
| **S1** | publish the **per-area files** (compressed, a few MB each) with a small manifest (date, checksum, source) on static hosting or a release page; clients download the latest | a second machine or more than about 3 users | free tier of static hosting (check) |
| **S2** | a thin **read-only API** over the same files (a small VM or an edge function), with caching and rate limits; queries by barcode, list and locality | users who cannot hold files (chat bots), or more than about 10-20 concurrent | a few dollars a month (guess) |
| **S3** | **Postgres with geospatial support**, several regions, history analytics, scheduled ingestion workers, monitoring, moderated crowd-sourced prices | many regions, shared history, several writers | real hosting cost: only if the project has funding |
Rules at every stage: the shared service holds **public data only**; user data stays on the user's side (or is encrypted by the client); crowd-sourced entries are anonymous and moderated; the schema does not change between stages, only where it lives. SQLite handles many readers and one writer, so the move is driven by operations (many devices, no local storage), not by speed.

## 7. Open items

Measure the daily change rate (needs two or three daily files); define the starter basket; decide how a user's area is chosen (a postal code list or a radius around coordinates); write the attribution line for the open-data licence; a nightly job and a freshness check (`STANDARDS.md` s.7).
