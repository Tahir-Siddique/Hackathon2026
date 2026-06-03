# Requirements & Use Cases Verification

Cross-check against **CVE-to-My-Stack Translator Hackathon Project Guide v01** (CyberHack 2026).

**Verification date:** Project as built in `Hackathon2026/`  
**Verdict:** **MVP and evaluation criteria met.** A few use-case examples and stretch items are partial — see gaps below.

---

## 1. Core aim (§3.1)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Input: list of software assets | ✅ | [parse_asset_list()](src/loaders.py#L57), UI paste/upload [ui/app/main.py](ui/app/main.py#L83) |
| Output: prioritised plain-English CVE list | ✅ | [run_pipeline()](src/pipeline.py#L16) → [add_summaries()](src/summarise.py#L30) |
| Ranked by real-world exploitability | ✅ | [enrich_and_rank()](src/rank.py#L17) — KEV first, then urgency/EPSS/CVSS |

---

## 2. Objectives (§3.2)

| # | Objective | Status | Evidence |
|---|-----------|--------|----------|
| 1 | Load/parse ≥1 offline feed (NVD, KEV, EPSS) | ✅ **All 3** (+ CPE reference) | [load_kev](src/loaders.py#L13), [load_epss](src/loaders.py#L23), [load_nvd](src/loaders.py#L41) |
| 2 | Normalisation: 15–20 product names → CPE | ✅ **19 products** | [config/normalisation_map.json](config/normalisation_map.json) |
| 3 | Matching function for user's assets | ✅ | [match_cves_to_assets()](src/match.py#L66) |
| 4 | EPSS + KEV applied; rank by urgency | ✅ | [enrich_and_rank()](src/rank.py#L17) |
| 5 | CSV or table: CVE, asset, EPSS, KEV, risk summary | ✅ | [OUTPUT_COLUMNS](src/export.py#L11) — includes **CVSS** (§4 also requires it) |
| 6 | Demo on facilitator sample list | ✅ | [data/sample_asset_list.txt](data/sample_asset_list.txt) — **12/12 mapped**, 40 tests pass |

**Note on objective 5:** Guide §3.2 lists five columns; §4 “Anticipated outcomes” also requires **CVSS** — you include both (exceeds minimum).

---

## 3. Anticipated outcomes (§4)

| Deliverable | Status | Location |
|-------------|--------|----------|
| Prioritised CVE table (all columns) | ✅ | [output/prioritised_cves.csv](output/prioritised_cves.csv) |
| Normalisation dictionary (15–20 SMB titles) | ✅ | [config/normalisation_map.json](config/normalisation_map.json) (JSON; guide allows “dictionary or CSV”) |
| Working script, sample list, no errors | ✅ | [translate.py](translate.py) |
| Demo presentation (5 min) | ✅ | [DEMO.md](DEMO.md) with script + diagrams |

---

## 4. Stretch goals (§3.3)

| Stretch | Status | Evidence |
|---------|--------|----------|
| One-page summary brief | ✅ | [write_brief()](src/export.py#L51) → `--brief` → [output/executive_brief.md](output/executive_brief.md) |
| Combined CVSS + EPSS urgency score | ✅ | [combined_urgency_score()](src/rank.py#L8) |
| Version range matching | ❌ Not built | MVP: [match_cves_to_assets()](src/match.py#L66) ignores version ranges (documented in DEMO) |
| CLI with asset list file argument | ✅ | [translate.py](translate.py) |
| Web UI (beyond guide) | ✅ Extra | [ui/](ui/) FastAPI + Jinja + Tailwind |

---

## 5. Hard constraints (§7)

| Constraint | Status | Notes |
|------------|--------|-------|
| No external vulnerability APIs at runtime | ✅ | No HTTP in [src/](src/); offline files only |
| 5.5 h scope / demo-ready | ✅ | Pipeline ~6s on full NVD |
| Current-year NVD unless needed | ✅ | Default [CVE-2025.json](data/CVE-2025.json); [CVE-2024.json](data/CVE-2024.json) also present |
| 15–20 products, not exhaustive | ✅ | 19 products, quality over breadth |
| No version matching in core MVP | ✅ | By design |

---

## 6. Data feeds (§6) — four feeds

| Feed | Guide file | Your project | Status |
|------|------------|--------------|--------|
| NVD CVE | `CVE-2024.json` / `CVE-2025.json` (FKIE) | [data/CVE-2025.json](data/CVE-2025.json), [data/CVE-2024.json](data/CVE-2024.json) | ✅ |
| CISA KEV | `known_exploited_vulnerabilities.json` | [data/known_exploited_vulnerabilities.json](data/known_exploited_vulnerabilities.json) | ✅ |
| EPSS | `epss_scores-[date].csv` | [data/epss_scores-2026-06-02.csv](data/epss_scores-2026-06-02.csv) | ✅ |
| CPE dictionary | `official-cpe-dictionary_v2.3.xml` | [data/nvdcpe-2.0.zip](data/nvdcpe-2.0.zip) (NIST retired XML Aug 2025) | ✅ Equivalent — [data/CPE_DICTIONARY.md](data/CPE_DICTIONARY.md) |

**Evaluation:** “≥2 of 4 feeds” — you load **all four** (CPE for reference/lookup only).

**Event-day resources (§12):**

| Resource | Status |
|----------|--------|
| `sample_asset_list.txt` | ✅ |
| `starter_notebook.ipynb` | ✅ |
| Download script | ✅ [scripts/download_datasets.py](scripts/download_datasets.py) |

---

## 7. Evaluation criteria (§11)

| Criterion | Status | How to show in demo |
|-----------|--------|---------------------|
| Data pipeline (≥2 feeds) | ✅ | `python translate.py --smoke` or UI status cards |
| Normalisation quality | ✅ | 12/12 sample products; explain [normalise_assets()](src/normalise.py#L88) |
| Matching accuracy | ✅ | Relevant CVEs per product; mention no version filter (some false positives possible) |
| Prioritisation (EPSS + KEV, KEV on top) | ✅ | Top rows in CSV have `kev=yes`; [tests/test_rank.py](tests/test_rank.py) |
| Output clarity (Use Case 1 sysadmin) | ✅ | Read one [risk_summary](output/prioritised_cves.csv) aloud |
| Limitations explained | ✅ | [DEMO.md](DEMO.md) § Limitations |

---

## 8. Use cases (§5)

### Use Case 1 — Solo SMB sysadmin (Alex)

| Need | Status | Notes |
|------|--------|-------|
| Informal asset list input | ✅ | File, CLI, **UI paste** [ui/templates/index.html](ui/templates/index.html) |
| Short actionable list + urgency | ✅ | Top 50 cap, KEV highlighted |
| Plain language | ✅ | [build_risk_summary()](src/summarise.py#L16) |
| Example: “Office 365 Business” | ✅ | Maps → `microsoft:365_apps` |
| Example: “Windows Server 2019” | ✅ | Alias in map |
| Example: “Sage Payroll 22” | ⚠️ **Unmapped** | Third-party payroll not in dictionary — silent miss risk |
| Example: “Cisco router” | ✅ | Alias → `cisco:ios_xe` (added) |
| Patch one KEV item first | ✅ | KEV-sorted output supports this |

### Use Case 2 — School / university IT

| Need | Status | Notes |
|------|--------|-------|
| Mixed Windows + Linux estate | ✅ Partial | Moodle, Apache, nginx + generic `linux:linux_kernel` alias for Linux OS |
| Moodle | ✅ | Sample list + map |
| Weekly CSV for CISO report | ✅ | [write_csv()](src/export.py#L21), UI download |
| Structured CMDB-style input | ✅ | Tab/comma file format supported |

### Use Case 3 — Charity / volunteer

| Need | Status | Notes |
|------|--------|-------|
| Non-expert readable output | ✅ | Risk sentences, no jargon required |
| Informal names + rough versions | ✅ | Fuzzy matching |
| Quarterly check posture | ✅ | Same tool; re-run when feeds updated |

---

## 9. Sample asset list (§10)

| Product (facilitator) | Maps correctly | CPE target |
|----------------------|----------------|------------|
| Microsoft 365 Apps for Business | ✅ | `microsoft:365_apps` |
| Windows Server 2022 | ✅ | `microsoft:windows_server_2022` |
| Windows 10 Pro | ✅ | `microsoft:windows_10` |
| Adobe Acrobat Reader DC | ✅ | `adobe:acrobat_reader` |
| Cisco IOS XE | ✅ | `cisco:ios_xe` |
| VMware vSphere | ✅ | `vmware:vsphere` |
| Google Chrome | ✅ | `google:chrome` |
| OpenSSL | ✅ | `openssl:openssl` |
| Apache HTTP Server | ✅ | `apache:http_server` |
| Zoom | ✅ | `zoom:zoom` |
| WordPress | ✅ | `wordpress:wordpress` |
| Moodle | ✅ | `moodle:moodle` |

**Required:** ≥10 of 12 — **you have 12/12 (100%).**

---

## 10. Gaps and partial items (honest)

| Item | Severity | Recommendation |
|------|----------|----------------|
| **Version range matching** | Stretch only | State in demo; not required for MVP |
| **Sage Payroll / generic third-party apps** | Use Case 1 example | Add aliases as you discover CPEs, or explain unmapped warning |
| **“Cisco router” (generic)** | Use Case 1 example | ✅ Fixed — alias → `cisco:ios_xe` |
| **NVD patch/reference links** | Overview “what to do” | Risk text implies priority; no CVE advisory URLs in CSV |
| **EPSS percentile in output** | Terminology only | Loaded in [enrich_and_rank](src/rank.py#L17) but not exported to CSV |
| **KEV `knownRansomwareCampaignUse`** | KEV field exists in feed | Not shown in output (optional column) |
| **Normalisation map as CSV file** | §4 “dictionary or CSV” | JSON only — trivial to export if asked |
| **official-cpe-dictionary_v2.3.xml** | Event USB may still have it | You use **2.0 zip** — document replacement |

None of the above block MVP submission or §11 evaluation if limitations are explained.

---

## 11. Summary scorecard

| Area | Result |
|------|--------|
| §3.2 Objectives (6) | **6/6** |
| §4 Anticipated outcomes (4) | **4/4** |
| §3.3 Stretch goals | **3/4** (no version ranges) |
| §6 Data feeds | **4/4** (CPE via 2.0 zip) |
| §10 Sample list | **12/12** |
| §11 Evaluation criteria | **6/6** |
| §5 Use cases | **Core met**; Sage Payroll–style third-party apps still need manual aliases |

**Ready to present:** Yes — lead with facilitator sample (12/12), CLI + UI, tests, limitations, and optional UC1 alias improvements.

---

## 12. Quick verification commands

```powershell
python translate.py --smoke
python translate.py data/sample_asset_list.txt --brief
pytest -q
uvicorn ui.app.main:app --host 127.0.0.1 --port 8000
```

---

*Generated for hackathon compliance review — see also [PLAN.md](PLAN.md) and [DEMO.md](DEMO.md).*
