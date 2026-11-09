---
artifact: Software Test Plan
output: out/Software-Test-Plan.xlsx
source_of_truth: ../spec.md
language:
  instructions: English
  deliverable: Bahasa Indonesia
---

# Prompt — Software Test Plan (ServerAgent)

> **How to use:** paste the *entire* content of [`../spec.md`](../spec.md) into
> the LLM, then paste this prompt below it. The spec is the single source of
> truth — the test plan you produce must stay coherent with it.

## Role

You are a **senior software quality-assurance lead** and **test manager** at PT
Mitra Integrasi Informatika, documenting the test plan for **ServerAgent**
(Skenario 3, Kelompok C6). You have deep knowledge of ISTQB-aligned test design,
discrete-event simulation, LLM-agent systems, and CI/CD.

## Task

Produce a complete **Software Test Plan** for ServerAgent, written in **Bahasa
Indonesia**, structured so it can be assembled into a spreadsheet workbook
(`Software-Test-Plan.xlsx`) with four sheets. Output **exactly three** fenced
blocks, in this order, nothing else:

1. `## RENCANA` — the plan narrative (Indonesian Markdown).
2. `## TEST-CASES` — a CSV code block (```` ```csv ````) of the test-case matrix.
3. `## TRACEABILITY` — a CSV code block (```` ```csv ````) of requirement coverage.

## Coherence rules (non-negotiable)

- **Test only what exists in `spec.md`.** Do not invent features, modules,
  roles, or verdicts. Use the exact canonical names: modules `agent.py`,
  `twin.py`, `llm.py`, `index.py`, `masking.py`, `elk.py`; layers **Core Module**
  and **Dashboard**; pages `Beranda`, `Alignment`, `Respons insiden`,
  `Sign-off`, `Report`, `Pengaturan`; verdicts `Lolos`, `Lolos Bersyarat`,
  `Tidak Lolos`, `Tidak Dapat Dinilai`.
- **Every test case cites a `Use Case ID`** from `UC-01`…`UC-04` (or an area tag
  from the list in the CSV schema) — full traceability, no orphan cases.
- **Cover everything:** each use-case sub-flow (`UC-01.a`…`UC-01.d`, UC-02,
  UC-03, UC-04), every verdict path, every engine route (DigitalTwin /
  EstimasiPenalaran / FallbackDigitalTwin), security, data, and CI/CD.
- **Keep the canonical Indonesian terms verbatim** in the deliverable (verdicts,
  page names, decision names). English may appear only for technical terms with
  no standard Indonesian equivalent.
- **Measurable expected results:** cite concrete thresholds from the spec
  (p95 within criteria, error rate, CPU/memory limits, thread pool ≥ 95%,
  utilization > 75%, confidence ≥ 0.70, seed determinism, Little's Law, 10-min
  JWT, 5-attempt lockout, 150 s / 300 s budgets).
- **Include negative, boundary, and failure-path cases** (out-of-range load,
  inactive model, LLM busy/failed, tampered HMAC, expired token, wrong role).

## Output block 1 — `## RENCANA`

Indonesian narrative with these sections (as `###` headings):

1. **Tujuan** — purpose and reference to the four use cases.
2. **Ruang Lingkup** — in scope / out of scope (SIT, UAT, performance test are
   complementary, not replaced; deployment stays in the existing pipeline).
3. **Strategi & Tingkat Pengujian** — map to the existing 3 layers (Core Module
   pytest, Dashboard Vitest, E2E Playwright) and where new cases extend them.
4. **Lingkungan Pengujian** — Core Module, Dashboard, PGlite/Neon, Vercel;
   Demo vs LLM mode; data-masking requirement.
5. **Peran & Tanggung Jawab** — the five roles (A-01…A-05) and their test duties.
6. **Kriteria Masuk & Keluar** — entry criteria (model active, load in range,
   env ready) and exit criteria (verdict rules, coverage gates ≥ 98% / 96%).
7. **Risiko & Mitigasi** — e.g. ELK unavailable, LLM nondeterminism, model
   drift, NDA data.
8. **Jadwal & Milestone** — per sprint cycle alignment + incident-driven work.
9. **Keluaran (Deliverables)** — this spreadsheet, alignment report, incident
   report, sign-off document.

## Output block 2 — `## TEST-CASES`

One CSV block. **First line is exactly this header**, then one row per test
case:

```
ID Uji,ID Use Case,Area/Modul,Jenis Uji,Prioritas,Nama Uji,Prakondisi,Data Uji,Langkah Uji,Hasil yang Diharapkan,Hasil Aktual,Status,Dieksekusi Oleh,Tanggal,Catatan
```

Column rules:

- **ID Uji** — `TC-<AREA>-<NNN>`; AREA ∈ `UC01, UC02, UC03, UC04, ENG, LLM, SEC, DATA, CI, NFR`; `NNN` zero-padded, unique.
- **ID Use Case** — `UC-01`…`UC-04` and/or the sub-flow (`UC-01.b`); for
  cross-cutting use `ENG`, `LLM`, `SEC`, `DATA`, `CI`, or `NFR`.
- **Area/Modul** — e.g. `UC-01 · Alignment Rilis`, `Core Module · twin.py`,
  `Core Module · agent.py`, `Dashboard`, `Keamanan`, `Data`, `CI/CD`.
- **Jenis Uji** — one of: `Fungsional, Integrasi, End-to-End, Performa/Beban, Keamanan, Kegunaan, Regresi, Data`.
- **Prioritas** — `Kritis`, `Tinggi`, `Sedang`, or `Rendah`.
- **Langkah Uji** — numbered `1) … 2) …` joined with `; ` on a single line (no
  literal line breaks inside a field).
- **Hasil yang Diharapkan** — concrete and verifiable.
- **Hasil Aktual, Dieksekusi Oleh, Tanggal** — leave empty.
- **Status** — `Belum Dijalankan`.
- **Catatan** — optional cross-reference or precondition note; may be empty.

CSV quoting: wrap any field containing a comma, quote, or semicolon in double
quotes and double any internal quote. Keep every row valid single-line CSV.

Target **45–65 test cases**, distributed roughly: UC-01 (alignment + all four
verdicts + what-if + out-of-range + calibration) ~14; UC-02 (reproduce →
mitigation → escalate → report → MTTR) ~7; UC-03 (filters, PDF/CSV, access/exit
control) ~5; UC-04 (publish, approve/reject, lock, PDF) ~5; ENG (SimPy
determinism, calibration ±5% p95, saturation → rejection/timeout, Little's Law
capacity) ~8; LLM (providers, confidence threshold, fallback, error paths, time
budget) ~6; SEC (auth, token, role access, masking/NDA, HMAC, lockout) ~6; DATA
(PGlite/Neon, migration, sample data, PDF/CSV) ~4; CI (hooks, coverage gates,
deploy smoke) ~4; NFR (performance, reliability, accessibility/mobile, audit,
cost) ~5.

## Output block 3 — `## TRACEABILITY`

One CSV block. **First line is exactly this header**, then one row per
requirement/area:

```
ID Use Case,Area/Modul,Uraian Singkat,ID Uji,Jumlah Cakupan,Status Cakupan
```

- One row per `UC-01`…`UC-04` **and** per sub-flow (`UC-01.a`…`UC-01.d`), plus
  one row per cross-cutting area (`ENG`, `LLM`, `SEC`, `DATA`, `CI`, `NFR`).
- **ID Uji** — comma-separated list of the `ID Uji` values that cover it.
- **Jumlah Cakupan** — integer count.
- **Status Cakupan** — `Tercakup` (≥1 test) or `Belum` (0). Aim for `Tercakup`
  on every row; if any row is `Belum`, say so explicitly.

## Quality bar (what makes this "excellent")

- 100% traceability: every requirement/area row is `Tercakup`; every test case
  cites a real `UC`/area.
- Every verdict path and every engine route is exercised at least once.
- Steps are executable as written; expected results are measurable; priorities
  are justified (a `Kritis` case blocks a release).
- No invented features and no silent renames of canonical terms.
