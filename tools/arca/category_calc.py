#!/usr/bin/env python3
"""Monotributo category check from a "Mis Comprobantes" issued-invoices CSV (local, offline).

Usage: category_calc.py invoices.csv [--current A] [--as-of YYYY-MM-DD] [--activity services|goods] [--json]

Sums the pesos invoiced in the 12 months ending at --as-of (default: end of the previous month),
credit notes subtract, foreign-currency rows use the exchange-rate column. Compares with the cap
table in data/monotributo_scales.json. Only the income cap is checked (not rent, energy, etc.).
Nothing leaves the machine. Not tax advice: verify on the agency's site.
"""
import argparse, csv, datetime as dt, json, re, sys, unicodedata
from pathlib import Path

CREDIT_CODES = {3, 8, 13, 21, 53, 112, 113, 114, 119, 203, 208, 213}
PESO_TOKENS = {"", "$", "pes", "ars", "peso", "pesos", "pesos argentinos"}


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower().strip()
    return re.sub(r"\s+", " ", s)


def parse_amount(text):
    t = (text or "").strip().replace("$", "").replace(" ", "")
    if not t:
        return 0.0
    neg = t.startswith("-") or (t.startswith("(") and t.endswith(")"))
    t = t.strip("-()")
    if "," in t and "." in t:
        dec = "," if t.rfind(",") > t.rfind(".") else "."
        t = t.replace("." if dec == "," else ",", "").replace(dec, ".")
    elif "," in t:
        t = t.replace(",", ".") if re.fullmatch(r"\d+,\d{1,2}", t) else t.replace(",", "")
    elif "." in t and re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        t = t.replace(".", "")
    v = float(t)
    return -v if neg else v


def parse_date(text):
    t = (text or "").strip()[:10]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return dt.datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    raise ValueError(f"unrecognised date: {text!r}")


def find(cols, *needles):
    for n in needles:
        for c in cols:
            if n in c:
                return c
    return None


def read_rows(path):
    raw = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    delim = max(";,\t", key=lambda d: raw.split("\n", 1)[0].count(d))
    rd = csv.DictReader(raw.splitlines(), delimiter=delim)
    rows = [{norm(k): (v or "") for k, v in r.items() if k} for r in rd]
    return rows


def totals(rows, start, end):
    if not rows:
        raise SystemExit("empty CSV")
    cols = list(rows[0])
    c_date = find(cols, "fecha de emision", "fecha")
    c_type = find(cols, "tipo de comprobante", "tipo")
    c_tot = find(cols, "imp. total", "importe total", "total")
    c_cur = find(cols, "moneda")
    c_fx = find(cols, "tipo cambio", "cotizacion")
    if not (c_date and c_tot):
        raise SystemExit(f"cannot find date/total columns in: {cols}")
    monthly, used, skipped = {}, 0, 0
    for r in rows:
        try:
            d = parse_date(r[c_date])
        except ValueError:
            skipped += 1
            continue
        if not (start <= d <= end):
            continue
        amt = parse_amount(r[c_tot])
        cur = norm(r.get(c_cur, "")) if c_cur else ""
        if cur not in PESO_TOKENS:
            fx = parse_amount(r.get(c_fx, "")) if c_fx else 0.0
            amt *= fx if fx else 1.0
            if not fx:
                print(f"warning: foreign-currency row without exchange rate on {d}", file=sys.stderr)
        t = r.get(c_type, "") if c_type else ""
        m = re.match(r"\s*(\d+)", t)
        code = int(m.group(1)) if m else None
        if (code in CREDIT_CODES) or "credito" in norm(t):
            amt = -abs(amt)
        key = d.strftime("%Y-%m")
        monthly[key] = monthly.get(key, 0.0) + amt
        used += 1
    return monthly, used, skipped


def window_end(as_of):
    if as_of:
        return dt.date.fromisoformat(as_of)
    first = dt.date.today().replace(day=1)
    return first - dt.timedelta(days=1)


def classify(total, scales, current, activity):
    cats = scales["categories"]
    key = "total_services" if activity == "services" else "total_goods"
    needed = next((k for k, v in cats.items() if total <= v["cap"]), None)
    out = {"category_needed": needed or "over K (outside the regime)", "total": round(total, 2)}
    if needed:
        out["margin_to_cap"] = round(cats[needed]["cap"] - total, 2)
        out["monthly_total_needed"] = cats[needed][key]
    if current:
        cur = cats[current]
        out["current"] = current
        out["current_cap"] = cur["cap"]
        out["under_categorised"] = total > cur["cap"]
        out["over_cap_by"] = round(max(0.0, total - cur["cap"]), 2)
        if needed:
            out["monthly_difference"] = round(cats[needed][key] - cur[key], 2)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--current")
    ap.add_argument("--as-of")
    ap.add_argument("--start", help="activity start date (YYYY-MM-DD) if under 12 months old at --as-of: reports the annualised figures")
    ap.add_argument("--activity", choices=["services", "goods"], default="services")
    ap.add_argument("--scales", default=str(Path(__file__).parent / "data" / "monotributo_scales.json"))
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    scales = json.loads(Path(a.scales).read_text())
    if a.current and a.current.upper() not in scales["categories"]:
        raise SystemExit("unknown category")
    end = window_end(a.as_of)
    # 12 months ending at `end`: from the first day of the month after `end`, one year earlier
    start = dt.date(end.year, 1, 1) if end.month == 12 else dt.date(end.year - 1, end.month + 1, 1)
    monthly, used, skipped = totals(read_rows(a.csv), start, end)
    total = sum(monthly.values())
    res = classify(total, scales, a.current.upper() if a.current else None, a.activity)
    if a.start:
        st = dt.date.fromisoformat(a.start)
        if st > start:
            days = (end - st).days + 1
            m_incl = (end.year - st.year) * 12 + end.month - st.month + 1
            m_exact = days / 365.25 * 12
            ann = {"activity_days": days, "months_inclusive": m_incl, "months_exact": round(m_exact, 2)}
            if m_exact < 6:
                ann["rule"] = "under 6 months of activity (reported): exempt, keeps the initial category"
            else:
                for label, m in (("inclusive", m_incl), ("exact", m_exact)):
                    t = total / m * 12
                    ann[f"annualised_{label}"] = classify(t, scales, a.current.upper() if a.current else None, a.activity)
                ann["rule"] = "6 to 11 months of activity (reported by press, UNVERIFIED): income / months * 12"
            res["annualisation"] = ann
    res.update(window=[start.isoformat(), end.isoformat()], rows_used=used, rows_skipped=skipped,
               scales_as_of=scales["as_of"], monthly={k: round(v, 2) for k, v in sorted(monthly.items())})
    if a.json:
        print(json.dumps(res, indent=2))
        return 0
    print(f"window {start} .. {end}  rows used {used}  skipped {skipped}  scales as of {scales['as_of']}")
    for k, v in sorted(monthly.items()):
        print(f"  {k}  {v:>16,.2f}")
    print(f"TOTAL 12 months: {total:,.2f}")
    print(f"category needed: {res['category_needed']}" + (f"  (margin to its cap {res['margin_to_cap']:,.2f})" if "margin_to_cap" in res else ""))
    if "annualisation" in res:
        an = res["annualisation"]
        print(f"-- activity since {a.start}: {an['rule']}")
        for k in ("annualised_inclusive", "annualised_exact"):
            if k in an:
                x = an[k]
                print(f"   {k}: {x['total']:,.2f} -> category {x['category_needed']}" + (f", monthly total {x['monthly_total_needed']:,.2f}" if "monthly_total_needed" in x else ""))
    if a.current:
        if res["under_categorised"]:
            print(f"!! current {res['current']} cap {res['current_cap']:,.2f} is EXCEEDED by {res['over_cap_by']:,.2f}: recategorise upward"
                  + (f"; monthly total would differ by {res['monthly_difference']:,.2f}" if "monthly_difference" in res else ""))
        else:
            print(f"ok: within current category {res['current']}")
    print("Only the income cap is checked. Verify on the agency's site; not tax advice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
