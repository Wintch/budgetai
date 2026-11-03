#!/usr/bin/env python3
"""Summarise a daily SEPA price zip (official Argentine supermarket price data) without extracting it to disk.

  python3 -I tools/sepa_probe.py path/to/sepa_lunes.zip            # chains, branches, row counts
  python3 -I tools/sepa_probe.py path/to/sepa_lunes.zip --staples  # median shelf price of staples per chain

The zip holds one inner zip per retail group; each has comercio.csv, sucursales.csv and productos.csv ('|' separated, UTF-8 with BOM).
Read-only; reads the data as untrusted text. Medians mix every branch of a chain in the whole country: filter by province or
locality (sucursales_provincia / sucursales_localidad) before comparing prices for one household.
"""
import io
import re
import statistics
import sys
import zipfile
from collections import defaultdict

STAPLES = re.compile(r'^(LECHE (ENTERA|DESCREMADA)|ARROZ|FIDEOS|HARINA|ACEITE|AZUCAR|YERBA)', re.I)


def inner_zips(z):
    for info in z.infolist():
        if info.filename.endswith('.zip') and info.file_size > 0:
            yield info.filename, zipfile.ZipFile(io.BytesIO(z.read(info)))


def members(iz):
    return {n.split('/')[-1]: n for n in iz.namelist()}


def chains(z):
    for fname, iz in inner_zips(z):
        m = members(iz)
        if 'comercio.csv' not in m or 'productos.csv' not in m:
            print(f'{fname}: missing files {sorted(m)}')
            continue
        rows = [r.split('|') for r in iz.read(m['comercio.csv']).decode('utf-8-sig', 'replace').splitlines()[1:] if r.count('|') >= 7]
        branches = len(iz.read(m['sucursales.csv']).decode('utf-8-sig', 'replace').splitlines()) - 1
        with iz.open(m['productos.csv']) as f:
            f.readline()
            n = sum(1 for _ in f)
        print(f"{', '.join(sorted({r[4].strip() for r in rows}))[:70]:70s} branches={branches:4d} price_rows={n}")


def staples(z):
    data = defaultdict(lambda: defaultdict(list))
    desc = {}
    for fname, iz in inner_zips(z):
        m = members(iz)
        if 'productos.csv' not in m or 'comercio.csv' not in m:
            continue
        com = [r.split('|') for r in iz.read(m['comercio.csv']).decode('utf-8-sig', 'replace').splitlines()[1:] if r.count('|') >= 7]
        label = com[0][4].strip() if com else fname
        with iz.open(m['productos.csv']) as f:
            f.readline()
            for raw in f:
                p = raw.decode('utf-8', 'replace').rstrip('\n').split('|')
                if len(p) < 13 or p[4] != '1' or not STAPLES.match(p[5]):  # p[4] == '1': id_producto is an EAN
                    continue
                try:
                    data[p[3]][label].append(float(p[9]))
                except ValueError:
                    continue
                desc[p[3]] = p[5]
    rows = []
    for ean, by_chain in data.items():
        if len(by_chain) >= 5:
            med = {k: statistics.median(v) for k, v in by_chain.items()}
            rows.append((max(med.values()) / min(med.values()), desc[ean], med))
    rows.sort(reverse=True)
    for spread, d, med in rows[:15]:
        print(f'{d[:50]:50s} x{spread:.2f}  ' + '  '.join(f'{k[:12]}:{v:,.0f}' for k, v in sorted(med.items(), key=lambda kv: kv[1])))
    if rows:
        print(f'median spread x{statistics.median(r[0] for r in rows):.2f} over {len(rows)} staples')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    with zipfile.ZipFile(sys.argv[1]) as z:
        staples(z) if '--staples' in sys.argv else chains(z)
