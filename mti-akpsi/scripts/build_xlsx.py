#!/usr/bin/env python3
"""Assemble ServerAgent's Software Test Plan into a spreadsheet workbook.

Reads the three blocks emitted by an LLM (via prompts/test-plan.md):
    out/plan.md           -> "Ringkasan" sheet (plan narrative)
    out/test-cases.csv    -> "Kasus Uji" sheet (test-case matrix)
    out/traceability.csv  -> "Traceability" sheet (requirement coverage)

and writes out/Software-Test-Plan.xlsx with a computed "Ringkasan Hitungan"
(summary) sheet.

Requires: pip install openpyxl
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:  # pragma: no cover
    sys.exit(
        "openpyxl is not installed. Run:  pip install openpyxl\n"
        "Then re-run:  make xlsx"
    )

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, color="FFFFFF")
TITLE_FONT = Font(bold=True, size=13)
SECTION_FONT = Font(bold=True)

# Columns whose content is long prose -> wide + wrapped.
LONG_COLS = {
    "prakondisi", "data uji", "langkah uji",
    "hasil yang diharapkan", "catatan", "uraian singkat",
}


def read_md(path: Path) -> list[str]:
    if not path.exists():
        sys.exit(f"missing {path} — save the LLM's `## RENCANA` block there first.")
    return path.read_text(encoding="utf-8").splitlines()


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    if not path.exists():
        sys.exit(f"missing {path} — save the LLM's CSV block there first.")
    text = path.read_text(encoding="utf-8-sig")
    # Drop markdown code-fence markers and surrounding blank lines.
    rows = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("```"):
            continue
        rows.append(line)
    reader = csv.reader(rows)
    parsed = [r for r in reader if any(c.strip() for c in r)]
    if not parsed:
        sys.exit(f"{path} has no data rows.")
    return parsed[0], parsed[1:]


def col_index(header: list[str], name: str) -> int | None:
    norm = name.strip().lower()
    for i, h in enumerate(header):
        if h.strip().lower() == norm:
            return i
    return None


def autosize(ws, rows: list[list[str]], header: list[str]):
    ncols = len(header)
    widths = [max(len(str(c)) for c in [header[i]]) for i in range(ncols)]
    for row in rows:
        for i in range(ncols):
            val = row[i] if i < len(row) else ""
            # Cap contribution from long text; LONG_COLS get fixed width below.
            if header[i].strip().lower() in LONG_COLS:
                continue
            widths[i] = max(widths[i], min(len(str(val)), 40))
    for i in range(ncols):
        name = header[i].strip().lower()
        if name in LONG_COLS:
            widths[i] = 48
        else:
            widths[i] = min(widths[i] + 2, 40)
        ws.column_dimensions[get_column_letter(i + 1)].width = widths[i]


def write_header_row(ws, header: list[str]):
    for c, value in enumerate(header, start=1):
        cell = ws.cell(row=1, column=c, value=value)
        cell.font = HEADER_FONT
        cell.fill = HEADER_FILL
        cell.alignment = Alignment(vertical="center", wrap_text=True)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(header))}1"


def build_summary_sheet(wb: Workbook, cases_header, cases_rows, trace_header, trace_rows):
    ws = wb.create_sheet("Ringkasan Hitungan")
    ws.cell(row=1, column=1, value="Ringkasan Hitungan").font = TITLE_FONT

    def header_for(h):
        idx = col_index(cases_header, h)
        if idx is None:
            sys.exit(f"test-cases.csv is missing the '{h}' column.")
        return idx

    i_type = header_for("Jenis Uji")
    i_prio = header_for("Prioritas")
    i_area = header_for("Area/Modul")

    r = 3
    ws.cell(row=r, column=1, value="Total Kasus Uji").font = SECTION_FONT
    ws.cell(row=r, column=2, value=len(cases_rows))
    r += 2

    def table(title: str, counter: Counter):
        nonlocal r
        ws.cell(row=r, column=1, value=title).font = SECTION_FONT
        r += 1
        ws.cell(row=r, column=1, value="Kategori").font = HEADER_FONT
        ws.cell(row=r, column=1).fill = HEADER_FILL
        ws.cell(row=r, column=2, value="Jumlah").font = HEADER_FONT
        ws.cell(row=r, column=2).fill = HEADER_FILL
        r += 1
        for key, count in sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])):
            ws.cell(row=r, column=1, value=key)
            ws.cell(row=r, column=2, value=count)
            r += 1
        r += 2

    table("Berdasarkan Jenis Uji", Counter(
        (row[i_type] if i_type < len(row) else "") for row in cases_rows))
    table("Berdasarkan Prioritas", Counter(
        (row[i_prio] if i_prio < len(row) else "") for row in cases_rows))
    table("Berdasarkan Area/Modul", Counter(
        (row[i_area] if i_area < len(row) else "") for row in cases_rows))

    # Coverage from traceability.csv.
    ws.cell(row=r, column=1, value="Cakupan Kebutuhan").font = SECTION_FONT
    r += 1
    if trace_header and trace_rows:
        i_status = col_index(trace_header, "Status Cakupan")
        i_req = col_index(trace_header, "ID Use Case")
        if i_status is not None:
            covered = sum(
                1 for row in trace_rows
                if i_status < len(row) and row[i_status].strip().lower().startswith("tercakup")
            )
            total = len(trace_rows)
            ws.cell(row=r, column=1, value="Baris kebutuhan (dari Traceability)")
            ws.cell(row=r, column=2, value=total)
            r += 1
            ws.cell(row=r, column=1, value="Tercakup")
            ws.cell(row=r, column=2, value=covered)
            r += 1
            ws.cell(row=r, column=1, value="Cakupan (%)")
            ws.cell(row=r, column=2, value=round(100 * covered / total, 1) if total else 0)
            r += 1
            if i_req is not None:
                missing = [row[i_req] for row in trace_rows
                           if i_status < len(row)
                           and not row[i_status].strip().lower().startswith("tercakup")]
                if missing:
                    ws.cell(row=r, column=1, value="Belum tercakup")
                    ws.cell(row=r, column=2, value=", ".join(missing))
    ws.column_dimensions["A"].width = 34
    ws.column_dimensions["B"].width = 22


def main() -> None:
    ap = argparse.ArgumentParser(description="Build ServerAgent Software Test Plan XLSX")
    ap.add_argument("--plan", default=str(BASE / "out" / "plan.md"))
    ap.add_argument("--cases", default=str(BASE / "out" / "test-cases.csv"))
    ap.add_argument("--trace", default=str(BASE / "out" / "traceability.csv"))
    ap.add_argument("--out", default=str(BASE / "out" / "Software-Test-Plan.xlsx"))
    args = ap.parse_args()

    plan_path = Path(args.plan)
    cases_path = Path(args.cases)
    trace_path = Path(args.trace)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    wb = Workbook()

    # 1) Ringkasan — plan narrative.
    ws = wb.active
    ws.title = "Ringkasan"
    ws.cell(row=1, column=1, value="Rencana Pengujian — ServerAgent").font = TITLE_FONT
    row = 2
    for line in read_md(plan_path):
        stripped = line.strip()
        if not stripped:
            continue
        cell = ws.cell(row=row, column=1, value=stripped)
        if stripped.startswith("#"):
            cell.font = Font(bold=True)
            # Flatten headings to readable text.
            cell.value = stripped.lstrip("#").strip()
        elif stripped.startswith("- "):
            cell.value = "• " + stripped[2:]
        row += 1
    ws.column_dimensions["A"].width = 120

    # 2) Kasus Uji.
    cases_header, cases_rows = read_csv(cases_path)
    ws = wb.create_sheet("Kasus Uji")
    write_header_row(ws, cases_header)
    for r, data in enumerate(cases_rows, start=2):
        for c in range(len(cases_header)):
            cell = ws.cell(row=r, column=c + 1, value=(data[c] if c < len(data) else ""))
            if cases_header[c].strip().lower() in LONG_COLS:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
    autosize(ws, cases_rows, cases_header)

    # 3) Traceability.
    trace_header, trace_rows = read_csv(trace_path)
    ws = wb.create_sheet("Traceability")
    write_header_row(ws, trace_header)
    for r, data in enumerate(trace_rows, start=2):
        for c in range(len(trace_header)):
            cell = ws.cell(row=r, column=c + 1, value=(data[c] if c < len(data) else ""))
            if trace_header[c].strip().lower() in LONG_COLS:
                cell.alignment = Alignment(vertical="top", wrap_text=True)
    autosize(ws, trace_rows, trace_header)

    # 4) Ringkasan Hitungan.
    build_summary_sheet(wb, cases_header, cases_rows, trace_header, trace_rows)

    wb.save(out_path)
    print(f"wrote {out_path}")
    print(f"  sheets: {', '.join(wb.sheetnames)}")
    print(f"  test cases: {len(cases_rows)}")


if __name__ == "__main__":
    main()
