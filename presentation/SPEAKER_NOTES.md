# Speaker notes — full deck (≈5 min)

Use with [SLIDES.md](SLIDES.md) (export to **PPTX/PDF**) or [slides.html](slides.html) (browser). Target **4:45** spoken + **0:15** buffer.

---

## Slide timing

| # | Slide | Time | Key message |
|---|-------|------|-------------|
| 1 | Title | 0:15 | Name, one-liner: CVEs filtered to *your* stack |
| 2 | Problem | 0:25 | Volume + relevance — 47 overnight, which 4 matter? |
| 3 | Deliver | 0:25 | Informal in → ranked table + criticality + summary out |
| 4 | Pipeline | 0:40 | Four steps; normalise is hardest; ~6 s scan |
| 5 | Data | 0:30 | CVE-2026, KEV, EPSS — all offline |
| 6 | Normalisation | 0:35 | 12/12 sample; silent miss if alias wrong |
| 7 | Ranking & criticality | 0:45 | KEV first; explain Critical on CVSS 4.3 + KEV |
| 8 | Web UI | 0:25 | Optional — show paste + filters if time |
| 9 | Live demo | 1:15 | CLI or UI — narrate while loading |
| 10 | Sample output | 0:35 | Read **one** risk_summary aloud |
| 11 | Use cases | 0:20 | SMB / school / charity |
| 12 | Limits | 0:30 | Three honest limits + 44 tests |
| 13 | Thanks | 0:10 | Questions |

---

## Before you present

- [ ] `python translate.py data/sample_asset_list.txt --brief` run once (backup CSV)
- [ ] Terminal ready **or** UI at http://127.0.0.1:8000
- [ ] Export PPTX: `marp SLIDES.md --pptx -o CVE-to-My-Stack-Slides.pptx` (see README)
- [ ] Browser deck tested: open `slides.html` (arrow keys / space)

---

## Slide 7 — Ranking & criticality (script)

> "Rows sort with **CISA KEV first** — confirmed active exploitation. Then we blend CVSS and EPSS into an urgency score. The **Criticality** column is for managers: CVE-2026-32202 has CVSS 4.3, which sounds medium, but it's on the KEV list with EPSS 0.57, so we label it **Critical**. Patch those before lower EPSS items."

---

## Slide 9 — Live demo

**CLI**

```powershell
cd c:\Users\tahir\Desktop\Hackathon2026
.\.venv\Scripts\Activate.ps1
python translate.py data\sample_asset_list.txt --brief
```

**Web UI**

```powershell
uvicorn ui.app.main:app --reload --host 127.0.0.1 --port 8000
```

While loading:

> "Loading about twenty-three thousand 2026 CVEs, KEV, and EPSS from disk — normalising twelve products, matching CPEs, ranking with KEV on top."

When done:

> "Twelve mapped, roughly a thousand matches, top fifty shown, **thirteen on the KEV list** — filter by Criticality in the UI or open the CSV."

---

## Slide 10 — Read aloud (example)

> "CVE-2026-32202 affects Windows Server 2022. EPSS 0.57 indicates high exploitation probability. Actively exploited in the wild — CISA KEV."

---

## If something breaks

- Open `output/prioritised_cves.csv` (pre-generated)
- Show web UI results from last run in `ui/output/`
- Say: "Forty-four automated pytest tests cover the pipeline."

---

## Q&A prep

| Question | Answer |
|----------|--------|
| Why offline? | Hackathon rule; works air-gapped; reproducible demo. |
| Why Python? | Guide Approach A; transparent pipeline. |
| Criticality vs CVSS? | CVSS is impact; we elevate KEV + EPSS for patch priority. |
| False positives? | No version filter — human review still needed. |
| False negatives? | Usually wrong normalisation — expand the map. |
| vs NVD website? | We filter to *your* stack and rank by KEV/EPSS. |
| Why CVE-2026? | Current-year FKIE release; auto-picks highest year in `data/`. |
