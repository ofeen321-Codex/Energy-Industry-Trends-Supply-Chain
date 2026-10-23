# Revision 2: review notes

**October 23, 2026. The user reviewed the changes and authorized repository versioning. No deployment or scheduled update job has been activated.**

## Schedule revision

The proposed publication schedule is Tuesday and Thursday at **10:00 a.m. America/New_York**, replacing Tuesday/Friday. The playbook, report, website plan and review-date validator use Tuesday/Thursday. The next proposed review remains Tuesday, October 27, 2026.

## What changed

- Reorganized the main report around buying decisions, with global and U.S. implications in each topic, conditional outlooks and sourcing actions.
- Added original World Bank benchmarks, Berkeley Lab queue research, PJM auction evidence, IRENA cost estimates, public BloombergNEF outlooks, primary Commerce/USTR documents and specialist contract analysis.
- Used BNEF's October 22 storage forecast and October 20 minerals release to qualify older numbers and shortage narratives; retained the old vintages with explicit caveats.
- Separated generation queues from load requests; equipment upper-end waits from project medians; capacity auction prices from energy prices; and auction date from delivery year.
- Added global/U.S. benchmark charts with units, periods, definitions and estimate labels.
- Added a phased website plan and a Tuesday/Thursday research/review/release process, including failures, corrections, freshness and forecast evaluation.
- Added typed draft evidence/outlook records, schema validation, a source export script and a publication-readiness guard. These are content preparation tools, not a deployed website.
- Preserved the prior local report as `reports/energy-supply-chain-outlook-2026-10-23-v1.md` for comparison.

## Main files to review

1. [Revised decision report](../reports/energy-supply-chain-outlook.md)
2. [Source catalog](sources.md) and [source assessment](source-notes.md)
3. [Website plan](website-plan.md)
4. [Twice-weekly update process](twice-weekly-updates.md)
5. [Draft outlooks](../data/outlooks.json) and [typed evidence](../data/observations.json)

## Boundaries and remaining implementation work

No frontend has been built. The recommended next implementation is a static Astro/TypeScript website consuming approved records. Hosting, a scheduler and publication tooling remain future work. The current draft has no editorial approval provenance and should fail the publication-readiness check.

Some information still needs transaction-specific verification: actual utility commitments, supplier quotes, current trade-remedy cash-deposit instructions, tax-credit treatment and any newer mineral-export-control arrangements. The report labels those gaps; a larger bibliography does not resolve them automatically.
