---
title: "ServerAgent — Canonical System Specification"
group: "Kelompok C6"
scenario: "Skenario 3 — ServerAgent (AI-powered digital twin for the test environment)"
repo: "mti-akpsi-task (branch main)"
source: "ServerAgent-Panduan.pdf · article/assig1.md (System Request) · article/assig2.md (Feasibility)"
version: "1.0"
status: "source-of-truth"
---

# ServerAgent — Canonical System Specification

> **This file is the single source of truth.** Every generated artifact (SRS,
> use cases, design, code, test plan) MUST trace back to the IDs and canonical
> names defined here. Do not invent features, roles, or modules that are not in
> this document. Canonical Indonesian terms are kept verbatim and glossed in
> English once, in the [Coherence Bible](#coherence-bible).

## 1. Overview

**ServerAgent** decides whether a *release candidate* is ready to take Production
load **before** it is promoted from Dev, without needing a Production-equivalent
test environment.

The problem it solves: Production runs several nodes behind a load balancer,
while Dev has a single, smaller node. Issues that depend on capacity and node
count — a **CPU spike on one node** and **request timeouts** — only appear after
go-live. Stress testing cannot be done in Production, and making Dev/Test
hardware match Production requires capital expenditure and long procurement.

ServerAgent answers this with a **digital twin**: a virtual replica of the
Integration Server built on **discrete-event simulation (SimPy)**, calibrated
from Dev test results, plus an **LLM agent** that composes the analysis plan,
estimates components outside the model's scope, and explains results in plain
language. It *complements* SIT, UAT, and performance testing — it does not
replace them. Deployment still runs through the existing pipeline.

### 1.1 Architecture (as built)

| Layer | Technology | Responsibility |
| --- | --- | --- |
| **Core Module** | Python · FastAPI · SimPy · LangChain · simulated ELK | Analysis engine, digital twin, LLM agent, data masking, HMAC-signed results, endpoints |
| **Dashboard** | Next.js · TypeScript | Role-based UI for all five roles |
| **Database** | PGlite (local) · Neon (production Postgres) | Persistence of sessions, results, reports, audit |
| **Deploy** | Vercel | Hosting; Production only updated from `main` that passed CI |

Requests and results are signed (HMAC) so the browser cannot alter parameters
or forge a verdict. The request token is a JWT valid for 10 minutes.

## 2. Actors and access

Access is enforced server-side for every page and every action; buttons that a
role may not use are hidden.

| Role (ID) | Primary tasks in ServerAgent | Pages |
| --- | --- | --- |
| **Technical Lead** (A-01) | Schedule sessions, run analysis, record cycle decisions, set analysis mode, recalibrate the twin model | All pages |
| **QA/Performance Tester** (A-02) | Fill Dev test parameters and results, run analysis and what-if tests | Beranda, Alignment, Sign-off (read), Report |
| **Integration Engineer** (A-03) | Record incidents, reproduce, test mitigation options, compile the incident report | Beranda, Respons insiden, Alignment (read), Report |
| **Project/Technical Manager** (A-04) | Approve or reject the sign-off document | Beranda, Sign-off, Alignment (read), Report |
| **Tim Support & Monitoring** (A-05) | View trends and download reports | Beranda, Respons insiden (read), Report |

## 3. Use cases

Traceability anchor for the test plan. Sub-flows are the acceptance surfaces.

### UC-01 — Jalankan Alignment Rilis Terjadwal (Run scheduled release alignment)
**Actors:** Technical Lead, QA/Performance Tester.
**Result:** a verdict per sprint cycle, a promote/return decision, and an
alignment report.

Session status stepper: `Terjadwal → Pengisian Parameter → Menunggu Hasil →
Peninjauan → Diputuskan → Ditutup`.

- **UC-01.a** Schedule session (Technical Lead): enter service, release name,
  version under test, cycle number, alignment meeting schedule (WIB). A prior
  cycle's parameters are pre-filled as a draft. The session opens automatically
  at the scheduled time, or earlier with "Buka sesi sekarang".
- **UC-01.b** Fill analysis parameters (QA/Performance Tester): load scenario
  (normal and peak TPS — typically 3–10 and 33–55 — plus what-if variants 2×,
  3×, 5×, 10× normal); release-candidate changes (version, config; naming a new
  out-of-scope component such as Kafka or Redis triggers reasoning estimation);
  acceptance criteria (p95, error rate, CPU, memory); Dev test results (tested
  TPS, p95, CPU, memory, error rate, payload size, notes); load-profile
  calibration (Dev spec: vCPU, RAM, node; Production spec: vCPU, RAM, node,
  thread pool, connection pool, bandwidth, timeout). Invalid fields are flagged
  and summarized with links; values are retained on failed validation.
- **UC-01.c** Read results: verdict, limiting resource, and narrative at top;
  per-step indicators vs criteria with the source of each number (Digital twin /
  Estimasi penalaran / Fallback); per-2-second trajectories; capacity planning
  (Little's Law); baseline-vs-simulated; previous-cycle comparison; a Dev
  verification plan; calibration/data/cost; auditable agent decision trace.
- **UC-01.d** Record cycle decision (Technical Lead): **Lanjut promosi**
  (alignment report saved, sign-off request auto-sent — unavailable for
  `Tidak Lolos` / `Tidak Dapat Dinilai`), **Kembali ke Dev** (≥1 follow-up
  required), or **Uji varian lain** (back to Pengisian Parameter, prior results
  kept in history).

### UC-02 — Tangani Respons Insiden (Handle incident response)
**Actor:** Integration Engineer.
**Result:** reproduction outside Production, tested mitigation options, incident
report with MTTR data.

Status: `Dicatat → Dalam Reproduksi → Tereproduksi | Belum Tereproduksi →
Uji Mitigasi → Mitigasi Ditemukan | Perlu Eskalasi → Terdokumentasi`.

- Record the incident: type (traffic spike, memory leak, batch job overlap,
  other), service, release, detection time, peak & average load, duration,
  payload, spec at time of incident. If ELK data is unavailable or NDA-covered,
  enter symptoms manually.
- Request reproduction: `Tidak Lolos` means the incident will recur at the
  current spec; the likely root cause is shown and root-cause time is recorded
  for MTTR.
- Test mitigation options: change vCPU, RAM, node, thread pool, connection
  pool, or timeout; submit; repeat until one option is `Lolos`.
- If none pass: "Tutup pengujian opsi", mark *perlu eskalasi*; the case enters
  the Technical Lead's task list.
- Choose the recommended mitigation, compile and save the incident report.

### UC-03 — Unduh Laporan dan Riwayat (Download reports and history)
**Actor:** Tim Support & Monitoring.
**Result:** trend summary; PDF and CSV downloads.

Filters (report type, service, release, date range) are stored in the URL so a
view can be shared. Every report is downloadable as PDF or CSV; "Unduh data
riwayat (CSV)" downloads all filtered results. Exit control: access checked
before the file is created; free text is masked; NDA-labelled reports carry
aggregate data only; every download is written to the audit log. Downloads are
restricted to Technical Lead, Project/Technical Manager, and Support.

### UC-04 — Terbitkan Dokumen Sign-Off (Publish sign-off document)
**Actor:** Project/Technical Manager (decider), Technical Lead (trigger).
**Result:** a locked sign-off document as the release-approval attachment.

The document is auto-published when the Technical Lead decides *lanjut promosi*.
It is numbered and contains: verdict + summary, release identity, conditions
(for `Lolos Bersyarat`), parameters, indicators and the source of each number,
follow-ups, and simulation limitations. The Manager chooses **Disetujui** or
**Ditolak** (reason required) and confirms. The document is then locked with a
version number and timestamp, cannot be changed, and can be downloaded as PDF.
A rejected document is kept; correction happens with a new document next cycle.

## 4. Verdict rules

Applied to the main step (peak load, or reproduction for incidents). What-if
variants never lower the main verdict; they are shown as system-limit info.

| # | Condition | Verdict |
| --- | --- | --- |
| 1 | Analysis stopped: model inactive, or normal/peak load outside the calibrated range | **Tidak Dapat Dinilai** |
| 2 | Violation at normal or peak: p95, error rate, CPU, memory exceed criteria, or thread pool ≥ 95% | **Tidak Lolos** |
| 3 | No violation, but some numbers come from reasoning estimation | **Lolos Bersyarat** (manual verification) |
| 4 | No violation, but highest utilization > 75% | **Lolos Bersyarat** (monitor 7 days) |
| 5 | Otherwise | **Lolos** |

Incident-reproduction mode: if the incident reproduces at the current spec →
`Tidak Lolos`.

**Limiting resource** at peak: if p95 is violated, no resource exceeds 85%, and
the largest wait is in database or external dependency → *Database* or
*External Dependency*. Otherwise the highest-utilization resource (if ≥ 60%);
if all below 60%, the resource that limits maximum capacity.

## 5. Analysis engine — "SimPy computes, LLM reasons"

All in-scope indicator numbers come from deterministic simulation. The LLM never
fabricates a number for a component that can be simulated.

### 5.1 Routing (per analysis step)

1. **Gates first:** model-active and load-range. Failure → `Tidak Dapat Dinilai`,
   no numbers computed.
2. After calibration, each step (normal, peak, what-if) is routed independently:
   - **What-if out of range** → only that variant is `Tidak Dapat Dinilai`.
   - **In-scope component** → SimPy **DigitalTwin** path (deterministic).
   - **Out-of-scope component** → Demo: deterministic template estimate; LLM:
     N samples in parallel → if confidence ≥ threshold (**0.70**) →
     **EstimasiPenalaran** (needs manual verification, verdict capped at
     `Lolos Bersyarat`); else → **FallbackDigitalTwin** (SimPy without the
     out-of-scope component).

### 5.2 SimPy vs LLM by step

| Step | Demo mode | LLM mode |
| --- | --- | --- |
| Data masking | Always, by code (`Penyamar`), before anything reaches an LLM | same |
| Baseline metrics | Code: ELK Stack (simulated in prototype), or last saved baseline if ELK unreachable | same |
| Analysis plan | Template | LLM composes steps; missing steps filled from template |
| Load-profile calibration | SimPy, always | same |
| In-scope scenarios | SimPy, always (DigitalTwin) | same |
| Out-of-scope component | Template estimate → threshold rules | LLM N samples → threshold; below → SimPy |
| Indicators, capacity, limiter, verdict | Always code, from SimPy + verdict rules | same |
| Verdict narrative + test plan | Template | LLM; if failed/empty → template |

### 5.3 Digital twin model (SimPy)

Discrete-event simulation of each request through the Integration Server. A
**60 s** measurement window after a **10 s** warm-up. The random seed is derived
from the request content, so identical input + model version give identical
numbers; adding a what-if variant does not change normal/peak numbers.

Request journey: **Poisson arrival (λ = TPS) → load balancer round-robin →
thread queue (reject if > 2× thread pool) → CPU 60% cpuMs → connection pool
(available within 1 s? else fail) → database (dbMs, lognormal) → external
dependency (extMs, lognormal) → CPU 40% cpuMs → latency > timeout? (timeout) →
done, latency recorded**. Nodes 2..n follow the same path.

Indicators: CPU utilization, memory, threads, connections, network; p50/p95/p99;
error rate; throughput.

**Three calculation stages:**
1. **Calibrate from Dev test.** CPU cost per request from the performance test:
   `cpuMs = CPU% × vCPU × node × 1000 / TPS`. DB/external wait re-tuned (≤ 4
   iterations) until simulated p95 is within 5% of Dev p95. DB share from the
   service registry.
2. **Simulate at Production spec** per scenario (normal, peak, what-if) with
   Production node count, thread pool, connection pool, timeout.
3. **Maximum capacity per resource**; the smallest is the capacity and limiter:
   CPU `vCPU × node × 1000 × cpuLimit / cpuMs`; threads & connections via
   **Little's Law** `L = λ × W`.

Reference example (from the guide): CPU/req `0.62 × 4 × 2 × 1000 / 40 = 124 ms`;
peak utilization `45 × 124 / (12 × 1000) ≈ 47%`; CPU capacity
`4 × 3 × 1000 × 0.80 / 124 = 77.4 TPS`; concurrent requests `45 × 0.193 ≈ 8.7`;
threads/node `8.7 / 3 × 1.3 ≈ 4` (120 available).

Load increase is **not linear**: p95 stays flat until thread/connection pools
saturate; after saturation, queuing, rejection, and timeout make p95 and error
rate spike.

### 5.4 Failure resilience

| Event | Behaviour |
| --- | --- |
| ELK Stack unreachable | Last saved baseline + its date; warning in result |
| LLM busy (HTTP 503/529) | Retry 2× (2 s apart), then fallback model (same provider); warning |
| LLM fails or output off-schema | That step uses deterministic fallback (template or SimPy); analysis completes |
| LLM time budget (150 s) exhausted | Next LLM step uses deterministic fallback; total limit 300 s |
| Result altered in transit | HMAC mismatch → rejected, not saved |

### 5.5 LLM cost control

Every analysis logs token count and estimated cost per step in the decision
trace. Demo mode is free. Feasibility estimate: ~**$0.51 USD per analysis**,
under 1% of development cost.

## 6. Non-functional requirements

- **NFR-SEC Security & privacy:** per-role access enforced server-side; data
  masking before any LLM call; NDA / UU No. 27 Tahun 2022 (PDP) compliance;
  HMAC result signing; JWT 10-minute tokens; login attempt limit (lock 10 min
  after 5 failures); no secrets in code or docs; no open redirect; no
  cross-origin forgery.
- **NFR-REL Reliability:** deterministic SimPy results (seed from request);
  graceful LLM fallback; last-saved baseline when ELK is down.
- **NFR-PERF Performance:** LLM step budget 150 s, total analysis 300 s; CI
  runs ~3 min (parallel jobs).
- **NFR-COST Cost control:** per-analysis token + cost accounting; Demo mode
  free.
- **NFR-ACC Accessibility/mobile:** login visible on mobile; password never
  shown; no horizontal scroll on 7 pages at 390 px width.
- **NFR-AUD Auditability:** decision trace per step (tool, path, confidence,
  duration, cost); download audit log; sign-off version + timestamp lock.

## 7. Existing test strategy & CI/CD (baseline)

ServerAgent already ships a 3-layer automated test pyramid (runs on every push)
and a CI/CD pipeline. The Software Test Plan formalizes and extends this into a
traceable test-case matrix.

### 7.1 Test layers and gates

| Layer | Tooling | Scope | Gate |
| --- | --- | --- | --- |
| Core Module | pytest, pytest-cov, FastAPI TestClient | `api/`: agent, SimPy, LLM, ELK, masking, endpoints | line & branch ≥ 98% |
| Dashboard | Vitest 5, coverage-v8, PGlite | `src/lib`, middleware, API routes, server actions | line/statement/function ≥ 98%; branch ≥ 96% |
| End-to-end | Playwright (Chromium) | all five role flows in the built app | all pass, no console errors |
| Types | tsc | all TS incl. tests | no errors |

Coverage achieved: Core Module **100%** (973 statements / 260 branches);
Dashboard **100% line / 96.7% branch**; **144** unit/integration tests
(81 Python, 63 TypeScript); **17** E2E scenarios.

Core Module per-file coverage: `agent.py` 528 stmt / 168 branch / 100%;
`twin.py` 204 / 30 / 100%; `llm.py` 136 / 46 / 100%; `index.py` 67 / 10 / 100%;
`masking.py` + `elk.py` 38 / 6 / 100%.

The LLM is **never called for real in tests** — LangChain is replaced by a
controllable mock (success / busy / reject / corrupt) so all fallback paths are
tested.

### 7.2 CI/CD pipeline

- **pre-commit:** black, ruff (incl. bandit security rules), sqlfluff (Postgres),
  prettier, eslint (Next.js/React Hooks/a11y/TS), NumPy docstring checker,
  detect-secrets, pre-commit-hooks (YAML/JSON/TOML validity, merge conflicts,
  large files, private keys, trailing whitespace).
- **pre-push:** tsc, vitest + coverage, pytest + coverage.
- **GitHub Actions:** lint → security (gitleaks, npm audit, pip-audit) →
  typecheck (tsc --noEmit) → test-ts (Vitest + coverage gate) → test-py (pytest
  `--cov-fail-under=98`) → build (next build) → e2e (Playwright, after the six
  preceding jobs) → CodeQL (TS + Python) → Deploy (Vercel `build`/`deploy
  --prod` + smoke tests `/api/py/sehat` and `/login`). Dependabot weekly.
- Production is only updated from `main` that passed CI.

## 8. Configuration & troubleshooting surface

Environment variables: `AUTH_SECRET` (required, ≥32 chars), `DEMO_PASSWORD`
(required, ≥8 chars), `DATABASE_URL` (recommended; Neon), `ANTHROPIC_API_KEY`,
`OPENAI_API_KEY`/`OPENAI_BASE_URL`, `GEMINI_API_KEY`/`GOOGLE_API_KEY`.

Key failure signatures (targets for test cases): login "config incomplete";
"Database belum tersambung" banner; `Tidak Dapat Dinilai` (model inactive /
out-of-range); "Permintaan kedaluwarsa" (10-min token); LLM connection-test
failure with specific causes; LLM mode slow (150 s → fallback); slow page after
idle (cold start).

## 9. Coherence Bible (canonical vocabulary)

Use these exact terms/IDs in every artifact. Do not rename or translate the
canonical column.

| Canonical term (ID) | English gloss | Notes |
| --- | --- | --- |
| UC-01 … UC-04 | Use cases 1–4 | traceability anchor |
| Lolos | Pass | verdict |
| Lolos Bersyarat | Conditional pass | verdict (manual verification / monitor 7 days) |
| Tidak Lolos | Fail | verdict (back to Dev) |
| Tidak Dapat Dinilai | Cannot be assessed | verdict (recalibrate first) |
| DigitalTwin | Digital twin path | SimPy deterministic |
| EstimasiPenalaran | Reasoning estimation | LLM, needs manual verification |
| FallbackDigitalTwin | Digital-twin fallback | SimPy without out-of-scope component |
| Penyamar | Masking component | runs before any LLM call |
| Sumber daya pembatas | Limiting resource | capacity bottleneck |
| Rentang terkalibrasi | Calibrated range | TPS range the model is fitted to |
| Jejak keputusan | Decision trace | audit log per agent step |
| MTTR | Mean time to resolution | detection → root cause |
| Little's Law | `L = λ × W` | concurrent requests |
| agent.py, twin.py, llm.py, index.py, masking.py, elk.py | Core Module files | exact module names |
| Core Module · Dashboard | Backend · Frontend | layers |
| Beranda, Alignment, Respons insiden, Sign-off, Report, Pengaturan | Page names | Dashboard pages |
| Terjadwal / Pengisian Parameter / Menunggu Hasil / Peninjauan / Diputuskan / Ditutup | UC-01 session states | exact order |
| Lanjut promosi / Kembali ke Dev / Uji varian lain | UC-01 decisions | |
| Disetujui / Ditolak | Approve / Reject | UC-04 |

## 10. ID conventions

- **Use cases:** `UC-01` … `UC-04` (sub-flows `UC-0x.a` …).
- **Test cases:** `TC-<AREA>-<NNN>` where AREA ∈ `UC01, UC02, UC03, UC04, ENG,
  LLM, SEC, DATA, CI, NFR`.
- **Actors:** `A-01` … `A-05` (see §2).
- Map to the group's SRS requirement IDs (`docs/`, "Tabel 9.30", state machine)
  when available; until then, `UC-xx` is the authoritative traceability anchor.
