# Updating the energy supply chain outlook

The report is a dated research product, not an automated market feed. Revision 2 uses an October 23, 2026 cutoff and a 12-month horizon. Use the proposed [Tuesday/Thursday process](twice-weekly-updates.md), with off-cycle review after a material event. No schedule has been activated. Move issue dates deliberately; preserve an existing prediction's original horizon. Do not let a download date become a publication date.

## Reproduce the current charts

From `/workspace/Energy-Industry-Trends-Supply-Chain` (or this repository's root on another machine):

```bash
python scripts/charts.py
```

The script reads reviewed inputs in `data/chart_data.csv` and writes six PNG and six editable SVG files under `charts/`. Four are used in the revised report; the original transformer and utilization figures remain available with edition 1. It makes no network requests and uses an ignored cache for Matplotlib configuration. Saved images need no software installation.

If the Python dependencies are missing, use an isolated environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-research.txt
.venv/bin/python scripts/charts.py
```

Retrieval/search uses the Python standard library; PDF text extraction uses `pdftotext` if installed, otherwise `pypdf`. TLS verification and the environment's normal network proxy remain enabled. No credentials are required for the public sources used here. Paywalled or blocked sources are logged, not bypassed.

## Refresh research

1. Check Git status and preserve user changes. Cloud tasks already have isolated environments: use the existing checkout; do not create a worktree unless requested.
2. Review `data/sources.csv`. It includes all nine user inputs, additional documents, and discovery-only pages. A page being downloaded does not mean that its text, date, or findings have been reviewed.
3. Retrieve selected inputs to avoid unnecessary downloads:

   ```bash
   python scripts/research.py --fetch --ids D01 A01 A02 A03 A04 A05 A06 A09 A10 A19 A20
   ```

   To retrieve the entire register, use `python scripts/research.py --fetch`. Expected blockers such as the USGS PDF and Reuters may make a full retrieval exit nonzero. Inspect `data/retrieval_log.csv`; the script preserves failures instead of claiming success. Hashes identify the downloaded content. A successful HTTP response can still be a consent, challenge, error, index, or login page: inspect `.research-cache/<ID>.txt` and the original document.
4. Update the queries in `data/search_queries.csv` for the new cutoff, then run:

   ```bash
   python scripts/research.py --search
   ```

   `data/search_log.jsonl` preserves search attempts and candidate URLs. Initial Bing searches returned poor matches; DuckDuckGo and direct publisher indexes produced better discovery. Search can return challenges or no usable matches. Review relevance, open the original publisher's article, and verify its date before using it. Search snippets are not evidence. If search is unreliable, use EIA Today in Energy, IEA news/reports, and official regulator indexes to discover dated articles.
5. Add new article URLs to the source register with stable IDs. Do not relabel a publisher homepage as a dated article. Distinguish publication date, modification date, underlying data cutoff, and access date. Prefer primary data and operative legal documents; use independent news for corroboration and events.
6. Read relevant sections, including methodology and footnotes. Edit `data/observations.json`, `data/outlooks.json` and `docs/source-notes.md`: distinguish observations from source forecasts, add global/U.S. reasoning, confidence and reversal triggers. `data/findings.csv` is now derived by the export script; do not edit it independently. Record conflicting estimates rather than averaging them.
7. Update `data/chart_data.csv` manually from reviewed sources. Keep observations, estimates, forecasts, and optimization benchmarks distinct. Preserve the old edition in Git history if committing the update. Do not combine Ember's January and April U.S. snapshots, or different global battery estimates, as if they were an unchanged dataset.
8. Rewrite the report, update `data/releases.json`, and run `python scripts/export_catalog.py` to refresh `docs/sources.md`, the website-ready source catalog and findings CSV. A download does not update the analysis. Recheck laws, IRS guidance, tariff classifications, licenses and effective dates before transaction-specific recommendations.
9. Run `python scripts/charts.py` and `python scripts/check_research.py`; inspect images and units. The checker covers schema, dates, references and assets, not factual truth. `python scripts/check_research.py --publication` additionally requires approved content and intentionally fails on this draft. Confirm annual forecasts beyond the report horizon are context. Inspect changes and follow the current commit/push authorization; website publication approval is separate.

## Company exposure worksheet

`data/company_exposure_template.csv` is intentionally empty. Use one row per facility or separately metered contract. Record annual MWh, gas MMBtu and diesel gallons, the exposed/unhedged share of each, energy location, and renewal dates. Use delivered prices with consistent units. Keep sensitive completed worksheets outside the public repository.

For an approved scenario, incremental variable energy cost is the sum of:

```text
electricity_MWh × electricity_unhedged_share × change_in_delivered_dollars_per_MWh
+ gas_MMBtu × gas_unhedged_share × change_in_delivered_dollars_per_MMBtu
+ diesel_gallons × diesel_unhedged_share × change_in_delivered_dollars_per_gallon
```

Shares are fractions between 0 and 1. Add capacity/demand charges, transport commitments, tariffs, interruption losses, and credit changes separately. Model both rising and falling prices; do not treat a scenario as a forecast. For indirect supplier exposure, confirm contract pass-throughs before including them. Separate the fuel already in carrier rates to avoid double counting.

## Research limits to retain

- Forecast confidence is a qualitative assessment, not a probability or investment return.
- Site availability and supplier readiness require evidence beyond national statistics.
- Trade and tax analysis must distinguish enacted law, interim guidance, proposals, suspensions, and uncertain future action.
- Some publisher pages lack a reliable exact date; retain that uncertainty.
- `.research-cache/` is ignored. Public-source text can be downloaded again; the repository retains citations, hashes, access records, reviewed data and analysis rather than redistributing complete third-party articles.
- Network access was initially blocked and later succeeded. By revision 2, environment metadata reported unrestricted access, but individual publishers still returned access errors. Use actual retrieval outcomes, not configuration alone, to diagnose failures. Do not bypass publisher access restrictions.
