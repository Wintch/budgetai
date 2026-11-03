#!/usr/bin/env python3
"""Monotributo calendar (.ics): monthly quota due date shifted past weekends and holidays, plus the
recategorisation reminders. Local and offline (holidays from data/holidays_YYYY.json).

Usage: due_calendar.py --from 2026-11 --months 14 > monotributo.ics

Dates are reminders, not official deadlines: the 20th rule and the window dates were reported by press
(docs/MONOTRIBUTO_DIY.md s.1, not verified against the regulation). Check the agency's agenda.
"""
import argparse, datetime as dt, json, sys
from pathlib import Path

DATA = Path(__file__).parent / "data"


def load_holidays():
    days = set()
    for f in DATA.glob("holidays_*.json"):
        days |= {dt.date.fromisoformat(h["fecha"]) for h in json.loads(f.read_text())}
    return days


def next_business_day(d, holidays):
    while d.weekday() >= 5 or d in holidays:
        d += dt.timedelta(days=1)
    return d


def months(start, n):
    y, m = start.year, start.month
    for _ in range(n):
        yield y, m
        m += 1
        if m == 13:
            y, m = y + 1, 1


def ev(uid, day, summary, desc, alarm_days=0):
    out = ["BEGIN:VEVENT", f"UID:{uid}@budgetai", f"DTSTAMP:{dt.datetime.now(dt.timezone.utc):%Y%m%dT%H%M%SZ}",
           f"DTSTART;VALUE=DATE:{day:%Y%m%d}", f"DTEND;VALUE=DATE:{day + dt.timedelta(days=1):%Y%m%d}",
           f"SUMMARY:{summary}", f"DESCRIPTION:{desc}"]
    if alarm_days:
        out += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{summary}", f"TRIGGER:-P{alarm_days}D", "END:VALARM"]
    return out + ["END:VEVENT"]


def build(start, n, holidays):
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//budgetai//monotributo//EN"]
    known_years = {d.year for d in holidays}
    for y, m in months(start, n):
        if y not in known_years:
            print(f"warning: no holiday file for {y}; weekends only", file=sys.stderr)
        due = next_business_day(dt.date(y, m, 20), holidays)
        lines += ev(f"quota-{y}{m:02d}", due, "Monotributo quota due (pay by hand)",
                    "Pay the monthly quota. Keep the receipt. Do not wait for the last day: payments can take up to 2 business days to apply.", 3)
    for y, m in months(start, n):
        lines += ev(f"cm03-{y}{m:02d}", dt.date(y, m, 10), "Prepare the Convenio Multilateral monthly return (CM03, SIFERE Web)",
                    "Only if registered in Convenio Multilateral. The legal due date is set each year by the Comision Arbitral (historically mid-month, around the 13th-20th): check the calendar on ca.gob.ar before relying on this reminder.", 0)
    windows = [(dt.date(y, mo, d), t, desc) for y in (start.year, start.year + 1, start.year + 2)
               for mo, d, t, desc in [
                   (1, 4, "Recategorisation window (Jan): export invoices and run category_calc.py",
                    "Export Mis Comprobantes (issued), run tools/arca/category_calc.py with the window ending 31/12, then submit in the portal. Check the deadline on the agency site (reported: early February)."),
                   (7, 1, "Recategorisation window (Jul): export invoices and run category_calc.py",
                    "Same with the window ending 30/06. Check the deadline (reported: first days of August)."),
                   (2, 1, "New semester table: refresh data/monotributo_scales.json", "Amounts change each semester."),
                   (8, 1, "New semester table: refresh data/monotributo_scales.json", "Amounts change each semester.")]]
    end = months(start, n)
    last = list(end)[-1]
    lo, hi = dt.date(start.year, start.month, 1), dt.date(last[0], last[1], 28)
    for i, (d, t, desc) in enumerate(sorted(windows)):
        if lo <= d <= hi:
            lines += ev(f"window-{d:%Y%m%d}-{i}", d, t, desc, 2)
    return "\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--from", dest="start", default=dt.date.today().strftime("%Y-%m"))
    ap.add_argument("--months", type=int, default=14)
    a = ap.parse_args(argv)
    y, m = map(int, a.start.split("-"))
    sys.stdout.write(build(dt.date(y, m, 1), a.months, load_holidays()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
