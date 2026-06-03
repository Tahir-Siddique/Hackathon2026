# CPE dictionary reference

## Important: legacy XML retired (August 2025)

The hackathon guide references:

`official-cpe-dictionary_v2.3.xml`

NIST **removed** this XML feed on **20 August 2025**. Direct downloads return **403 Forbidden**.

**Replacement (official):** [NVD CPE Dictionary 2.0](https://nvd.nist.gov/vuln/data-feeds) — JSON chunks inside:

| File | Size | Purpose |
|------|------|---------|
| `data/nvdcpe-2.0.zip` | ~79 MB compressed | Official CPE dictionary (16 JSON chunks, ~840 MB uncompressed) |

Download:

```powershell
python scripts/download_datasets.py --cpe
```

## Spot-check normalisation (Step 3.4)

Do **not** load the full dictionary into memory. Search the zip:

```powershell
python scripts/lookup_cpe.py "microsoft 365"
python scripts/lookup_cpe.py "google chrome"
```

Use results to confirm `vendor:product` strings in `config/normalisation_map.json`.

## Not used by the main pipeline

CVE matching uses CPE strings embedded in **NVD CVE JSON** (`CVE-2026.json` by default), not this dictionary. The CPE zip is for **building and verifying** the normalisation map only.
