#!/usr/bin/env python3
"""Load the prices of ONE area from a daily SEPA zip (official Argentine supermarket price data) into a small SQLite file.

  python3 -I tools/sepa_ingest.py SEPA.zip OUT.db --province AR-B --area-regex 'TOWN ONE|TOWN TWO|NEIGHBOURHOOD' --postal 1234 5678

A branch is kept when its province code matches AND (its locality/neighbourhood text matches --area-regex OR its postal code starts with one of --postal).
Branch data quality is uneven (the locality is sometimes in the neighbourhood column, postal codes appear as '1638' or 'B1638AAK'), hence both tests.
Re-running with another daily file ADDS that day (primary key: snapshot_date, branch, item). Read-only on the zip; the zip is untrusted text.
Schema: see docs/DATA_ARCHITECTURE.md.
"""
import argparse
import io
import re
import sqlite3
import sys
import zipfile

SCHEMA = """
CREATE TABLE IF NOT EXISTS chain  (id_comercio INT, id_bandera INT, banner TEXT, company TEXT, PRIMARY KEY (id_comercio, id_bandera));
CREATE TABLE IF NOT EXISTS branch (id_comercio INT, id_bandera INT, id_sucursal INT, name TEXT, kind TEXT, street TEXT, number TEXT,
  lat REAL, lon REAL, neighbourhood TEXT, postal_code TEXT, locality TEXT, province TEXT, PRIMARY KEY (id_comercio, id_bandera, id_sucursal));
CREATE TABLE IF NOT EXISTS item   (item_id TEXT PRIMARY KEY, is_ean INT, description TEXT, brand TEXT, pack_qty TEXT, pack_unit TEXT);
CREATE TABLE IF NOT EXISTS price  (snapshot_date TEXT, id_comercio INT, id_bandera INT, id_sucursal INT, item_id TEXT,
  list_price REAL, ref_price REAL, ref_qty REAL, ref_unit TEXT, promo1_price REAL, promo1_text TEXT, promo2_price REAL, promo2_text TEXT,
  PRIMARY KEY (snapshot_date, id_comercio, id_bandera, id_sucursal, item_id)) WITHOUT ROWID;
CREATE INDEX IF NOT EXISTS price_item ON price (item_id, snapshot_date);
"""


def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('zip')
    ap.add_argument('db')
    ap.add_argument('--province', default='AR-B')
    ap.add_argument('--area-regex', default='')
    ap.add_argument('--postal', nargs='*', default=[])
    a = ap.parse_args()
    rx = re.compile(a.area_regex, re.I) if a.area_regex else None
    db = sqlite3.connect(a.db)
    db.executescript(SCHEMA)
    kept_rows = 0
    with zipfile.ZipFile(a.zip) as z:
        for info in z.infolist():
            if not info.filename.endswith('.zip') or info.file_size == 0:
                continue
            day = re.search(r'(\d{4}-\d{2}-\d{2})', info.filename).group(1)
            iz = zipfile.ZipFile(io.BytesIO(z.read(info)))
            m = {n.split('/')[-1]: n for n in iz.namelist()}
            if not {'comercio.csv', 'sucursales.csv', 'productos.csv'} <= set(m):
                continue
            keep = set()
            for line in iz.read(m['sucursales.csv']).decode('utf-8-sig', 'replace').splitlines()[1:]:
                p = line.split('|')
                if len(p) < 14 or p[13] != a.province:
                    continue
                postal = re.sub(r'^[A-Za-z]', '', p[11].strip())
                if (rx and (rx.search(p[12]) or rx.search(p[10]))) or any(postal.startswith(x) for x in a.postal):
                    keep.add((p[0], p[1], p[2]))
                    db.execute('INSERT OR REPLACE INTO branch VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
                               (int(p[0]), int(p[1]), int(p[2]), p[3], p[4], p[5], p[6], num(p[7]), num(p[8]), p[10], p[11], p[12], p[13]))
            if not keep:
                continue
            for line in iz.read(m['comercio.csv']).decode('utf-8-sig', 'replace').splitlines()[1:]:
                p = line.split('|')
                if len(p) >= 8 and p[0].isdigit() and (p[0], p[1]) in {(k[0], k[1]) for k in keep}:
                    db.execute('INSERT OR REPLACE INTO chain VALUES (?,?,?,?)', (int(p[0]), int(p[1]), p[4].strip(), p[3].strip()))
            batch = []
            with iz.open(m['productos.csv']) as f:
                f.readline()
                for raw in f:
                    p = raw.decode('utf-8', 'replace').rstrip('\n').split('|')
                    if len(p) < 13 or (p[0], p[1], p[2]) not in keep:
                        continue
                    price = num(p[9])
                    if price is None or price <= 0:
                        continue
                    pad = lambda i: p[i] if len(p) > i else ''
                    db.execute('INSERT OR IGNORE INTO item VALUES (?,?,?,?,?,?)', (p[3], 1 if p[4] == '1' else 0, p[5], p[8], p[6], p[7]))
                    batch.append((day, int(p[0]), int(p[1]), int(p[2]), p[3], price, num(p[10]), num(p[11]), p[12],
                                  num(pad(13)), pad(14), num(pad(15)), pad(16)))
            db.executemany('INSERT OR REPLACE INTO price VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)', batch)
            kept_rows += len(batch)
            print(f'{info.filename.split("/")[-1][:40]}: {len(keep)} branches, {len(batch)} price rows', file=sys.stderr)
    db.commit()
    print(f'done: {kept_rows} price rows -> {a.db}')


if __name__ == '__main__':
    main()
