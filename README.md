This project analyzes energy industry trends and their supply chain impacts from a global and US standpoint.

## Current report

[Read the revised energy supply chain outlook](reports/energy-supply-chain-outlook.md) — **revision 2**, research cutoff **October 23, 2026**, covering decisions through **October 23, 2027**. The report and planning files are maintained here for review.

The revised report cites 28 records across 13 publisher/study families, including World Bank, Berkeley Lab, PJM, IRENA, BloombergNEF and primary U.S. trade documents. Each topic connects the global market to U.S. procurement decisions. Observations, source forecasts, analyst outlooks and legal-status limits are distinguished. The original nine inputs remain assessed, and [edition 1](reports/energy-supply-chain-outlook-2026-10-23-v1.md) is preserved for comparison.

## Website and twice-weekly updates

- [Website plan](docs/website-plan.md): audience, pages, content model, proposed architecture, implementation phases and acceptance criteria.
- [Tuesday/Thursday update process](docs/twice-weekly-updates.md): 10 a.m. New York publication target, research, review, freshness, corrections and forecast evaluation.
- [Revision review notes](docs/revision-notes.md): changes and remaining implementation work.

The website is planned; no frontend, deployment or scheduled job has been activated. Repository versioning does not activate website publication.

## Supporting files

- [Source list, dates and access status](docs/sources.md)
- [Source analysis and conflicting estimates](docs/source-notes.md)
- [Update and reproduction guide](docs/updating.md)
- [Six charts, in PNG and SVG](charts/), including regional gas benchmarks and global/U.S. solar generation costs
- [Reviewed chart inputs](data/chart_data.csv) and [findings register](data/findings.csv)
- [Blank company exposure worksheet](data/company_exposure_template.csv)
- [Source registry](data/sources.csv), [retrieval audit](data/retrieval_log.csv), [search queries](data/search_queries.csv) and [search results](data/search_log.jsonl)
- [Typed evidence](data/observations.json), [eight draft outlooks](data/outlooks.json), [local edition history](data/releases.json) and [content schema](schemas/research-content.schema.json)

Export the catalog, rebuild charts and check content from the repository root:

```bash
python scripts/export_catalog.py
python scripts/charts.py
python scripts/check_research.py
```

See the update guide for dependencies and refresh commands. Checks cover data structure and references, not factual truth or editorial approval. The optional `--publication` check intentionally rejects this unapproved draft. Downloads and chart regeneration do not revise findings automatically. Full third-party articles remain in an ignored local cache; the repository stores analysis, citations, reviewed data and provenance.
