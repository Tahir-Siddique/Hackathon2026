/** Client-side UX: loading overlay, sample assets, results filters */

(function () {
  const form = document.getElementById("analyze-form");
  const overlay = document.getElementById("loading-overlay");
  const textarea = document.getElementById("assets_text");
  const sampleBtn = document.getElementById("load-sample");
  const sampleData = document.getElementById("sample-assets-data");

  if (form && overlay) {
    form.addEventListener("submit", () => {
      overlay.classList.remove("hidden");
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        btn.disabled = true;
        btn.dataset.originalText = btn.textContent;
        btn.textContent = "Analysing…";
      }
    });
  }

  if (sampleBtn && textarea && sampleData) {
    sampleBtn.addEventListener("click", () => {
      textarea.value = sampleData.textContent.trim();
      textarea.focus();
    });
  }

  const filterPanel = document.getElementById("results-filters");
  if (!filterPanel) return;

  const rows = document.querySelectorAll(".cve-result-row");
  const critChips = document.querySelectorAll("[data-filter-criticality]");
  const assetChips = document.querySelectorAll("[data-filter-asset]");
  const assetSelect = document.getElementById("filter-asset-select");
  const visibleCountEl = document.getElementById("filter-visible-count");
  const totalRows = parseInt(filterPanel.dataset.totalRows || String(rows.length), 10);

  let activeCriticality = "all";
  let activeAsset = "all";

  function applyFilters() {
    let visible = 0;
    rows.forEach((row) => {
      const crit = row.dataset.rowCriticality || "";
      const asset = row.dataset.rowAsset || "";
      const critOk = activeCriticality === "all" || crit === activeCriticality;
      const assetOk = activeAsset === "all" || asset === activeAsset;
      const show = critOk && assetOk;
      row.classList.toggle("table-row-hidden", !show);
      if (show) visible += 1;
    });
    if (visibleCountEl) {
      visibleCountEl.textContent = `Showing ${visible} of ${totalRows}`;
    }
  }

  function setActiveAsset(value) {
    activeAsset = value;
    assetChips.forEach((chip) => {
      chip.classList.toggle("active", chip.dataset.filterAsset === value);
    });
    if (assetSelect && assetSelect.value !== value) {
      assetSelect.value = value;
    }
    applyFilters();
  }

  critChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      activeCriticality = chip.dataset.filterCriticality || "all";
      critChips.forEach((c) => c.classList.toggle("active", c === chip));
      applyFilters();
    });
  });

  assetChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      setActiveAsset(chip.dataset.filterAsset || "all");
    });
  });

  if (assetSelect) {
    assetSelect.addEventListener("change", () => {
      setActiveAsset(assetSelect.value || "all");
    });
  }

  applyFilters();
})();
