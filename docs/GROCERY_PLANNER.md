---
id: grocery-planner
title: "Grocery planner: compare prices and plan the week's shopping (design, general)"
audience: person
country: AR
region: ""
language: en
topics: [groceries, prices, sepa]
sources:
  - {name: "datos.produccion.gob.ar", url: "https://datos.produccion.gob.ar/dataset/sepa-precios", kind: unclassified}
  - {name: "datos.produccion.gob.ar", url: "https://datos.produccion.gob.ar/dataset/6f47ec76-d1ce-4e34-a7e1-621fe9b1d0b5/resource/0a9069a9-06e8-4f98-874d-da5578693290/download/sepa_lunes.zip", kind: unclassified}
as_of: 2026-10-20
expires: 2027-04-18
status: draft
licence: CC-BY-4.0
verified_by: ""
not_verified: ["see the Not verified section of the page"]
---

# Grocery planner: compare prices and plan the week's shopping (design, general)

Written 2026-10-20. Idea: query supermarket prices and offers, build the week's list, and go to buy **exactly that** at the cheapest place. A design note, not built.
Findings below come from search results and were **not tested**; the data licences and the current availability of the official data must be checked before use.
Formats follow `STANDARDS.md` (section 4: product and price tables).

## 1. Data sources, cheapest and safest first

| order | source | what it gives | notes |
|---|---|---|---|
| 1 | **Precios Claros / SEPA** (**downloaded and read, see 1a**) (the national daily price system: large chains must report each item's price; one source says about 12 million prices on about 70,000 products from about 3,600 stores). **Found on 2026-10-20:** the official dataset on the national production open-data portal (`datos.produccion.gob.ar`, dataset "sepa-precios"), published by the consumer-defence office, **updated daily as one zip per weekday**, a province-codes translator and a field-description PDF (annex of a 2020 resolution); public access was ordered in 2024 | prices by branch and barcode, free | licence on the dataset page: **CC BY 4.0** (an older scrape of the web portal said CC BY 2.5 Argentina: it is a different release). Read once by a tool; **the dates inside the zips are inconsistent with the titles**: check them. Size and format of the zips not yet inspected. Maintainer contact is listed on the page |
| 2 | Community tools around it: a Scrapy crawler of the official portal (OpenDataCordoba/precios_claros), a 2018 scraped dataset (pdelboca/datasets_preciosclaros), a research archive of 2016-2018 prices | code and history | study material; old data is not for planning |
| 3 | The chains' own web catalogues (several Argentine chains run on the VTEX e-commerce platform, which exposes a public catalogue search; a community scraper exists for Dia and for Vea) | price, list price, stock, barcode, active promotion and its validity (for the chains that publish it) | **terms of use apply**: respect robots rules, rate-limit, cache, never log in. Carrefour: no scraper or documentation found. Paid scrapers exist but cost money: not first choice |
| 4 | Superprecio MCP (an MCP server for Claude comparing Argentine supermarkets by name or barcode) | an existing pattern for the same idea | early stage; read it before building |

Rule: official open data first; a chain's catalogue only to fill promotions and the gaps; never pay for what a free source gives.

## 1a. The official daily data, as downloaded and read on 2026-10-20

- **Where:** dataset page `https://datos.produccion.gob.ar/dataset/sepa-precios` (one resource per weekday). Direct file of the Monday resource, as listed on the page:
  `https://datos.produccion.gob.ar/dataset/6f47ec76-d1ce-4e34-a7e1-621fe9b1d0b5/resource/0a9069a9-06e8-4f98-874d-da5578693290/download/sepa_lunes.zip`
  (the other weekday files have their own resource ids on the page). Each weekday file looks overwritten every week, so only about the last 7 days are available: **keep your own snapshots**.
  Licence on the page: CC BY 4.0 (credit the source). **The data is not stored in this repo**: only the link, the format notes and the small reader `tools/sepa_probe.py`.
- **Size and shape:** the Monday file was **330 MB** (6 seconds to download here), holding 17 inner zips (one per retail group; one was empty that day), about **14 million price rows** (calc from the per-group counts).
  Each inner zip has three files, `|`-separated, UTF-8 with a byte-order mark: `comercio.csv` (group and banners), `sucursales.csv` (branches with address, coordinates, province code, locality, opening hours) and `productos.csv`.
- **Price columns:** `id_comercio, id_bandera, id_sucursal, id_producto, productos_ean` (the flag `1` means `id_producto` is a barcode), `productos_descripcion, productos_cantidad_presentacion, productos_unidad_medida_presentacion, productos_marca,
  productos_precio_lista, productos_precio_referencia` (the price per reference unit, for example per 1,000 ml: it gives the **unit price ready-made**), `productos_cantidad_referencia, productos_unidad_medida_referencia, productos_precio_unitario_promo1, productos_leyenda_promo1, productos_precio_unitario_promo2, productos_leyenda_promo2` (up to two promotions, with the legend text).
- **Who is in it** (Monday 19 Oct 2026): Carrefour banners, Coto, Dia, the Cencosud banners (Jumbo, Disco, Vea), Changomas, La Anonima (with Topsy and Bomba), a cooperative chain, Toledo, Comodin, Mariano Max, a pharmacy chain, fuel-station shops and some regional chains. Neighbourhood independents are not there.
- **First probe (nothing to rely on yet):** for 112 staples (rice, flour, oil, sugar, yerba, milk) sold by at least six groups, the median price differed between the cheapest and the dearest group by a **median of x1.24**, and by more than x1.2 for 62% of them; the cheapest group varied by item. **Caveat:** the median mixes every branch of a group across the whole country (some groups exist only in one region), so a real comparison must filter by province or locality first.
- **Loaded one area into SQLite** (`tools/sepa_ingest.py`, 15 s, 156,000 rows, 21.7 MB) and compared 1-litre milk: the cheapest was a low-price brand (about 13% below the leading brand at its cheapest chain); the same product varied by about 4-8% between chains; and the data needs normalising (inconsistent pack units, a wrong reference price at one group): see `DATA_ARCHITECTURE.md` s.4-5.
- **Next:** filter by the user's province or locality; match the same barcode across groups; read the promotion legends; check that the dates inside the files match the weekday titles.

## 1b. Neighbourhood shops and wholesalers

- Small neighbourhood supermarkets (many are family-run self-service stores) are **mostly not in SEPA**: one source says micro, small and medium businesses are exempt from reporting. They rarely have a web catalogue, and a map listing normally shows name, address, hours, phone, rating and photos, **not prices** (the listing page content was not readable by a tool; scraping a map service also conflicts with its terms).
- Ways to get their prices without scraping: a **shelf-price log made by the user** (a photo or a receipt turned into `price` rows with `source_kind: manual`, a date and the store), their own messaging or social posts with offers (read by a person), and a map of the shops from OpenStreetMap (`shop=supermarket`, free) to know where they are.
- Their **suppliers** are the cash-and-carry wholesalers (Maxiconsumo, Diarco, Vital, Yaguar are named in press; Makro was reported in 2024 as preparing to leave the country, and its historical customers were those same stores) and, for fruit and vegetables, the **central wholesale market** (Tapiales, province of Buenos Aires). Buying there directly can lower the unit price, usually with minimum quantities. Not found: whether each wholesaler publishes an online price list, their consumer rules and minimums, and prices of the central market's retail fair (only its opening hours were seen in press).
- **A manual price log** for the shops with no data (neighbourhood independents, greengrocers): one CSV row per observation, the same fields as the `price` table of `STANDARDS.md` s.4 plus who and where:
  `date,shop_name,shop_kind,locality,item_description,brand,pack_size,pack_unit,price,promo_text,source_kind,photo_ref` with `source_kind=manual`. Photograph the shelf tag or the receipt (the photo stays on the user's device); fresh produce is priced **per kilo**.
  A mix that works for a household: the large chains from the official data, the nearby independents from the manual log, and, for produce, the weekly wholesale reference as a benchmark of what a fair retail price looks like.
- The central market publishes **weekly wholesale reference price reports** (seen only through press); whether there is an official table or open data is **not confirmed**: look at its own site and at the open-data portals.
- To do: check each wholesaler's site for a public price list and consumer rules; check the central market's site; decide whether a price log is worth the effort against the saving.

## 2. Pipeline (offline-first)

1. **Snapshot**: a script fetches the sources on a schedule (or on demand), writes `product` and `price` rows with `retrieved_at`, keeps the last N snapshots. Without network the planner uses the last snapshot and says how old it is.
2. **Normalise**: barcode join, unit price per kg/l/unit (`STANDARDS.md` s.5).
3. **Promotions** as data, not text: kind (percent off, 2x1, second unit at X%, card or wallet discount), conditions (days, card, minimum purchase, limit per customer), validity. A promotion that needs a card the user does not have is ignored.
4. **Plan**: input = a basic list (staples by category or specific barcodes), household size, a budget, optional store limits, and what is already at home (pantry). Output = a list per store with quantities, the price of each item, the total, and the saving against the average shelf price.
5. **Route choice**: compare one store against two or three stores, charging a travel cost per extra store (transport is almost zero for some users, so a split basket often wins); the plan states the saving of the split in pesos so the user decides.
6. **Substitutions**: if an item is out of stock or much dearer, suggest an equivalent by category and unit price. A language model may phrase the explanation, never choose the price.
7. **The weekly list** is a short sheet: what, where, how much, the total, the expiry of the promotions, and the date of the prices.

## 3. Standards and tests

- Barcode (EAN/GTIN) is the key; items without a barcode are matched by name and flagged `low_confidence`.
- Golden test: a fixed basket of 10 staples with a frozen snapshot must always give the same plan.
- Tests: unit-price maths, promo rules, stale-price refusal, the offline path.
- Provenance: each price row shows its source and date; the plan shows the oldest price used.

## 4. Privacy and ethics

- Prices are public data; the **list and the household are private**: nothing about a household goes into `docs/` or git. Only `private/` or the user's device.
- Respect each site's terms; identify the client honestly; low request rate; stop on errors.
- Do not present the plan as nutritional advice.

## 5. Cost

Free data and scripts; no model is needed to plan. Storage is small (daily snapshots can be compacted). A model, if used, only phrases the explanation (cheap models first). Hosting cost: none while it runs on the user's own machine.

## 6. Hermes integration (later)

Two skills in the Agent Skills layout (`STANDARDS.md` s.6): `grocery-price-lookup` (by name or barcode, returns price, promotion, date) and `grocery-weekly-list` (builds the list from a household profile held on the user's side). The agent adds the conversation (follow-up questions, substitutions); the numbers come from the scripts.

## 7. Not verified

The current availability and licence of the official data; each chain's terms of use and catalogue endpoints (Carrefour in particular); how the chains publish promotions; how often prices really change; the accuracy of the official feed against shelf prices.
