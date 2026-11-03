# Third-party code used by tools/arca (pinned; clones live in git-ignored `vendor/`)

Nothing here is copied into git. Clone at the commit, read the diff when bumping, never run with a real key or certificate before the audit line says so.

| repo | licence | commit audited (2026-11-02) | use | audit notes (static grep only, nothing executed) |
|---|---|---|---|---|
| ralcorta/arcasdk | MIT | b0b957a41cba3a79e493f62edf6c76a58f21ae61 | invoicing + registry via web services (certificate) | monorepo whose `postinstall` builds and packs: **do not `npm install` the repo**; install the published package with `--ignore-scripts`. Only AFIP/ARCA hosts in the SOAP layer. |
| LcsGrz/arcli | MIT | 6ab2cfd51f237256a10a5d5de044ae242627ffa6 | CLI to issue and preview invoices, registry lookup | has an update check (fetches npm registry and a GitHub changelog) and spawns a PDF plugin and the clipboard: find the switch to disable the update check before use. `prepare` is husky (dev only). |
| buanzo/agentic-skill-arca-comprobantes | Apache-2.0 | 7b4f13f4033499f9e0a4d54368c2f56cb31668c7 | Playwright download of issued vouchers (Mis Comprobantes / RCEL), parsing, indexing | only `auth.afip.gob.ar` and `fe.afip.gob.ar`; credentials from env vars `AFIP_CUIT` and `CLAVE_AFIP`; says it keeps no cookies or storage state; `pdftotext` called with a list argv. **Full read of the Playwright scripts still to do** before any run; wrap it so the key comes from a prompt, not a file. Very young (2 stars). |
| Lanuti-Franco/facturador-ARCA | check LICENSE | def8763e926634eedfd7d16e496de07f3b90bc0f | reference only | depends on the Afip SDK platform (`afip.py`) and Supabase: **not adopted**. |
| reingart/pyafipws | GPL-3 | not cloned | reference only | do not copy into this repo (licence). |
