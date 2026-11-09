# mti-akpsi — ServerAgent "Prompt as Source" workspace

**"Prompt as Source"** workspace for **high-coherence software artifacts** —
including the software itself. The canonical spec ([`spec.md`](spec.md)) and the
artifact prompts ([`prompts/`](prompts/)) are the source of truth; the generated
documents, spreadsheets, and code are *build artifacts*.

Inspired by [`mti-INTI`](../mti-INTI/README.md), where the prompts are the source
and the video is the artifact. Here the "video" is replaced by ServerAgent's
software artifacts, and "visual coherence" becomes **traceability + a controlled
vocabulary**: every artifact must trace back to `UC-01`…`UC-04` and reuse the
exact canonical names defined in `spec.md`.

## What this is

A prompt-driven pipeline for the AKPSI project **ServerAgent** (Skenario 3,
Kelompok C6) — an AI-powered digital twin that decides whether a release
candidate can take Production load before promotion, without a
Production-equivalent test environment. ServerAgent combines a **SimPy**
discrete-event digital twin ("SimPy computes") with an **LLM** agent that
composes plans, estimates out-of-scope components, and explains results ("LLM
reasons").

The authoritative description of the as-built system is
[`ServerAgent-Panduan.pdf`](ServerAgent-Panduan.pdf); [`spec.md`](spec.md)
distils it (plus the System Request and Feasibility documents) into a single,
high-coherence source of truth.

## Files

| File | Purpose |
| --- | --- |
| `spec.md` | **Single source of truth** — canonical ServerAgent spec (actors, use cases, verdicts, engine, NFRs, glossary, ID conventions). |
| `prompts/test-plan.md` | **Today's artifact** — Software Test Plan prompt (emits a spreadsheet-ready plan). |
| `prompts/srs.md` · `use-case.md` · `design.md` · `code.md` | Stub prompts for the remaining artifacts. |
| `prompts/README.md` | How to feed the prompts + coherence rules. |
| `artifacts/manifest.yaml` | Machine-readable traceability manifest (artifact → prompt → status). |
| `scripts/build_xlsx.py` | Assembles LLM output into `out/Software-Test-Plan.xlsx`. |
| `ServerAgent-Panduan.pdf` | Primary source document the spec is derived from. |
| `reference.docx` · `landscape.lua` · `Makefile` | Pandoc DOCX pipeline (portrait/landscape tables), kept. |

## Pipeline

```
spec.md ──(single source of truth)─────────────────────────────┐
   │                                                           │
   └──(feed to LLM, with)→ prompts/*.md ──(external LLM)→ out/ ├─┐
                                                               │  │
                                    make xlsx ──(assemble)─────┘  │
                                                               │  │
                                      out/Software-Test-Plan.xlsx
```

1. **Spec** — keep the canonical system description in `spec.md`.
2. **Prompt** — one prompt per artifact in `prompts/`; each instructs an LLM to
   produce an artifact that stays coherent with the spec.
3. **Generate** — paste `spec.md` + the prompt into any capable LLM; save the
   emitted blocks under `out/`.
4. **Build** — `make xlsx` assembles the blocks into the spreadsheet workbook.
5. **Curate** — promote good output into `artifacts/` and set its `status` to
   `keep` in `artifacts/manifest.yaml`.

## How to produce the Software Test Plan (today)

```sh
# 1. Copy spec.md + prompts/test-plan.md into ChatGPT / Claude / Gemini.
# 2. Save the three emitted blocks to:
#      out/plan.md          (the `## RENCANA` narrative)
#      out/test-cases.csv   (the `## TEST-CASES` CSV)
#      out/traceability.csv (the `## TRACEABILITY` CSV)
# 3. Build the workbook:
make xlsx                  # -> out/Software-Test-Plan.xlsx
```

The workbook has four sheets: **Ringkasan** (plan), **Kasus Uji** (test-case
matrix), **Traceability** (requirement coverage), and **Ringkasan Hitungan**
(auto-computed counts + coverage %).

## Conventions

- **Model-agnostic:** prompts are rich prose, not vendor-specific syntax.
- **English instructions, Indonesian deliverable:** prompts are written in
  English (best LLM fidelity); the artifacts themselves are in Bahasa Indonesia,
  keeping canonical terms verbatim (see `spec.md` §9).
- **Single source of truth:** `spec.md` is canonical; never rename or translate
  a canonical term or invent a feature in an artifact.
- **Traceability:** every test case cites a `UC-xx` / area tag; no orphan cases.
- **One job per prompt:** if a prompt tries to produce two documents, split it.
- **Numbers over adjectives:** cite concrete thresholds, not vague claims.

## DOCX pipeline (kept from the original skeleton)

```sh
make build     # build spec.md -> out/spec.docx (portrait/landscape via landscape.lua)
make check     # integrity checks on the DOCX build
```
