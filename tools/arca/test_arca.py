#!/usr/bin/env python3
"""Self-test (synthetic data only): python3 tools/arca/test_arca.py"""
import datetime as dt, io, json, sys, tempfile
from contextlib import redirect_stdout
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import category_calc as cc, due_calendar as dc

fails = 0
def check(name, got, want):
    global fails
    ok = got == want
    fails += not ok
    print(("ok   " if ok else "FAIL ") + name + ("" if ok else f"  got {got!r} want {want!r}"))

check("amount ar", cc.parse_amount("1.234.567,89"), 1234567.89)
check("amount us", cc.parse_amount("1,234,567.89"), 1234567.89)
check("amount plain", cc.parse_amount("1234.5"), 1234.5)
check("amount thousands", cc.parse_amount("1.234"), 1234.0)
check("amount comma dec", cc.parse_amount("12,5"), 12.5)

CSV = """Fecha de Emisión;Tipo de Comprobante;Punto de Venta;Moneda;Tipo Cambio;Imp. Total
15/01/2026;11 - Factura C;1;$;1;3.000.000,00
10/02/2026;11 - Factura C;1;$;1;2.000.000,00
20/03/2026;13 - Nota de Crédito C;1;$;1;500.000,00
05/04/2026;11 - Factura C;1;DOL;1500;1000,00
01/05/2025;11 - Factura C;1;$;1;99.000.000,00
"""
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "x.csv"; p.write_text(CSV)
    buf = io.StringIO()
    with redirect_stdout(buf):
        cc.main([str(p), "--as-of", "2026-06-30", "--current", "A", "--json"])
    r = json.loads(buf.getvalue())
check("total (credit note subtracts, USD*fx, old row excluded)", r["total"], 3000000 + 2000000 - 500000 + 1500000)
check("category needed", r["category_needed"], "A")
check("window start", r["window"][0], "2025-07-01")
buf = io.StringIO()
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "y.csv"; p.write_text(CSV.replace("1000,00", "9.000.000,00"))
    with redirect_stdout(buf):
        cc.main([str(p), "--as-of", "2026-06-30", "--current", "A", "--json"])
r = json.loads(buf.getvalue())
check("under-categorised flagged", r["under_categorised"], True)
check("needed category above A", r["category_needed"] > "A", True)

buf = io.StringIO()
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / "z.csv"; p.write_text(CSV)
    with redirect_stdout(buf):
        cc.main([str(p), "--as-of", "2026-06-30", "--start", "2025-12-10", "--json"])
r = json.loads(buf.getvalue())
check("annualised months inclusive (Dec..Jun)", r["annualisation"]["months_inclusive"], 7)
check("annualised total", round(r["annualisation"]["annualised_inclusive"]["total"], 2), round(r["total"] / 7 * 12, 2))

hol = {dt.date(2026, 11, 20)}  # pretend a holiday: shift to Monday 23
check("shift past holiday+weekend", dc.next_business_day(dt.date(2026, 11, 20), hol), dt.date(2026, 11, 23))
check("no shift on a business day", dc.next_business_day(dt.date(2026, 11, 18), set()), dt.date(2026, 11, 18))
ics = dc.build(dt.date(2026, 11, 1), 3, dc.load_holidays())
check("ics has 3 quota events", ics.count("SUMMARY:Monotributo quota due"), 3)
check("ics has 3 CM03 reminders", ics.count("SUMMARY:Prepare the Convenio"), 3)
sys.exit(1 if fails else 0)
