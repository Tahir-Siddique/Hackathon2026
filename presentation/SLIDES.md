---
marp: true
theme: default
paginate: true
header: "CVE-to-My-Stack Translator"
footer: "CyberHack 2026 · 4 min presentation"
style: |
  section { font-size: 26px; }
  h1 { color: #1e3a8a; }
  h2 { color: #2563eb; }
  table { font-size: 20px; }
  blockquote { border-left: 4px solid #2563eb; }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# CVE-to-My-Stack Translator

Prioritised CVE list for **your** software stack

*[Your name / team]*

---

## Why · Who

**Why:** Too many CVEs — need **stack-specific** patch order

**Who:** SMB sysadmins · school/uni IT · charity volunteers

> Which CVEs matter to **us**?

---

## What we built

- **In:** informal asset list (CLI or web UI)
- **Out:** top 50 CVEs — criticality, CVSS, EPSS, KEV, risk text, CSV
- **Offline:** CVE-2026 + CISA KEV + EPSS

---

## Pipeline

Normalise → Match NVD → KEV + EPSS → Rank + Criticality → CSV

- 12/12 sample products mapped · ~6 s scan · **44** tests

---

## Innovation

1. **KEV-first** ranking  
2. **Criticality** badge (KEV + EPSS elevate low CVSS)  
3. Plain-English **risk_summary**  
4. Web UI filters (app + criticality)

---

## Demo result

- ~996 matches → top **50** · **13 KEV**  
- Example: **CVE-2026-32202** — Critical, KEV, EPSS 0.57

`python translate.py data/sample_asset_list.txt --brief`

---

## Limits · Thanks

- Bad alias → missed CVE · no version matching yet  
- Feeds updated **manually** (`download_datasets.py`)

**Questions?**

---

*Full demo deck: [DEMO_SLIDES.md](DEMO_SLIDES.md) · Source: [DEMO.md](../DEMO.md)*
