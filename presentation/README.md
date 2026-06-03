# Presentation — full deck (≈5 minutes)

## Files

| File | Purpose |
|------|---------|
| **[DEMO_SLIDES.md](DEMO_SLIDES.md)** | **Full [DEMO.md](../DEMO.md) → slides** (~20 slides, §9 hours, diagrams) |
| [SLIDES.md](SLIDES.md) | Short **4-minute** deck (7 slides) |
| [slides.html](slides.html) | Browser presenter (Reveal.js) |
| [SPEAKER_NOTES.md](SPEAKER_NOTES.md) | Timing + scripts |
| **CVE-to-My-Stack-DEMO.pptx** | PowerPoint from DEMO_SLIDES (regenerate below) |
| **CVE-to-My-Stack-4min.pptx** | PowerPoint from SLIDES.md |

---

## Export to PowerPoint (PPTX) — recommended

### Option A — Marp for VS Code

1. Install [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode).
2. Open [SLIDES.md](SLIDES.md).
3. `Ctrl+Shift+P` → **Marp: Export Slide Deck** → choose **PPTX** or **PDF**.

Output: use on projector, Teams, or Google Slides (import PPTX).

### Option B — Marp CLI

```powershell
cd c:\Users\tahir\Desktop\Hackathon2026\presentation
npx @marp-team/marp-cli DEMO_SLIDES.md --pptx -o CVE-to-My-Stack-DEMO.pptx --no-stdin
npx @marp-team/marp-cli DEMO_SLIDES.md --pdf -o CVE-to-My-Stack-DEMO.pdf --no-stdin
npx @marp-team/marp-cli SLIDES.md --pptx -o CVE-to-My-Stack-4min.pptx --no-stdin
```

---

## Present in browser (no PowerPoint)

```powershell
cd c:\Users\tahir\Desktop\Hackathon2026\presentation
start slides.html
```

Or: `python -m http.server 8765` → http://127.0.0.1:8765/slides.html

- **Space / →** next slide  
- **F** fullscreen  

---

## Slide list (13)

1. Title  
2. Problem  
3. What we deliver  
4. Pipeline  
5. Offline data  
6. Normalisation  
7. **Ranking & criticality** *(new)*  
8. **Web UI** *(new)*  
9. Live demo  
10. Sample output (with Criticality column)  
11. Use cases  
12. Limits & design  
13. Thank you / Q&A  

Spoken timing: see [SPEAKER_NOTES.md](SPEAKER_NOTES.md).

---

## What’s new in this deck (vs earlier 10-slide version)

- **CVE-2026** feed (~23k CVEs), current demo numbers  
- **Criticality** column and ranking rules explained  
- **Web UI** slide (FastAPI, filters, CSV download)  
- **44** pytest tests  
- Sample rows: CVE-2026-32202 (Critical), CVE-2026-2441 (High)

---

## Mermaid diagram not in PPTX?

If the pipeline diagram fails on export, copy the Mermaid block from [SLIDES.md](SLIDES.md) into [mermaid.live](https://mermaid.live), export PNG, and paste into slide 4.
