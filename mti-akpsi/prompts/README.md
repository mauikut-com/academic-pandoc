# Prompts

One artifact prompt per deliverable. Each prompt is **model-agnostic rich
prose** — you paste [`../spec.md`](../spec.md) first, then the prompt, into any
capable LLM (ChatGPT, Claude, Gemini, …). The LLM's output is the *draft*; after
you curate it, it becomes the committed source for that artifact.

## How to feed a prompt

1. Copy the **whole** of [`../spec.md`](../spec.md).
2. Copy the prompt (e.g. [`test-plan.md`](test-plan.md)).
3. Paste spec + prompt into the LLM, in that order.
4. Save the emitted blocks to `out/` per the prompt's instructions.
5. Build the final artifact (`make xlsx` for the test plan).
6. When satisfied, promote the curated files into `artifacts/` and set its
   `status` to `keep` in [`artifacts/manifest.yaml`](../artifacts/manifest.yaml).

## Coherence rules (apply to every artifact)

- **Single source of truth:** `spec.md` is canonical. Every ID, module, role,
  verdict, and page name must match it exactly. Never rename or translate a
  canonical term.
- **Traceability:** artifacts cite `UC-xx` / area tags and actor IDs; no
  invented requirements.
- **Language:** instructions are English (best LLM fidelity); the *deliverable*
  is Bahasa Indonesia, keeping canonical terms verbatim (see `spec.md` §9).
- **One artifact per prompt:** if a prompt tries to produce two documents, split
  it.
- **Numbers over adjectives:** cite concrete thresholds from the spec, not
  vague statements.

## Files

| File | Artifact | Status |
| --- | --- | --- |
| [`test-plan.md`](test-plan.md) | Software Test Plan (spreadsheet, XLSX) | ✅ ready |
| [`srs.md`](srs.md) | Software Requirements Specification | stub |
| [`use-case.md`](use-case.md) | Use-case specifications | stub |
| [`design.md`](design.md) | Design / architecture | stub |
| [`code.md`](code.md) | Source code (the software itself) | stub |
