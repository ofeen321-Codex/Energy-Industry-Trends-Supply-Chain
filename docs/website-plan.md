# Website plan: energy supply chain decision outlook

**Planning date:** October 23, 2026. **Status:** reviewable plan and draft content model; no frontend, deployment or schedule is activated.

## Product and audience

Build a research website for procurement leaders, operations teams, energy buyers and project developers. The central question is: **What might change over the next 12 months, what evidence supports that view, and what should a buyer do differently?** Each topic must show both the global market and the consequences for a U.S. company's facilities and supplier network.

The product should make qualified future judgments visible without implying certainty. Source forecasts, our directional outlooks, planning scenarios and verified historical observations need separate labels. Company-specific savings, individual supplier failure probabilities and tariff eligibility cannot be inferred from national averages.

## Pages and reading flow

| Page | Reader's task | Minimum content |
|---|---|---|
| Home `/` | Identify decisions requiring attention | Current evidence cutoff; global/U.S./both views; six to eight decision cards; changed-since-last-release section; upcoming triggers |
| Global `/global` | Understand cross-border exposure | Regional energy benchmarks, fuel routes, equipment markets, mineral processing and trade fragmentation; links to U.S. implications |
| U.S. procurement `/us-procurement` | Translate developments into buying decisions | Power market and tariff context, delivery constraints, landed cost, customs/credit checks, contract actions and lead-time evidence |
| Topic `/topics/[topic]` | Investigate one category | Prices/availability, grid, fuel logistics, renewables, batteries, minerals, trade/regulation or supplier execution; source/metric tables |
| Outlook `/outlooks/[id]` | Assess one future judgment | Claim type, horizon, separate global/U.S. reasoning, supporting observations, assumptions, confidence, counterevidence, monitoring and procurement action |
| Sources `/sources` and `/sources/[id]` | Inspect the evidence | Publisher, original link, publication date/precision, data period, retrieval and editorial review dates, study family, limitations and access status |
| Updates `/updates` | See what changed | Dated editions; evidence-only changes versus changed outlooks; a truthful no-material-change entry when appropriate |
| Methodology `/methodology` | Understand trust and prediction limits | Definitions, source policy, comparability rules, freshness and correction policies, forecast evaluation |
| Corrections `/corrections` | Understand revisions | Corrected claim, old/new values, reason, source and effects on decisions; retain superseded editions |

Use ordinary topic names and procurement language. Put research metadata in an expandable evidence panel rather than making readers interpret IDs or schema fields. Every chart has a text summary, unit/date labels, a data table and downloadable reviewed CSV. The first mobile screen should show the decision, perspective, evidence date and uncertainty.

## Outlook card contract

Each card has:

1. A specific directional judgment, labeled **Analyst outlook**, **Source forecast**, or **Scenario**.
2. Issue date and fixed horizon. Preserve an old forecast's original horizon when updating it; a rolling homepage does not rewrite history.
3. Global implications and U.S. company implications, separately authored and cited.
4. Observations or documented provisions underlying the reasoning, with publication date, observation period and source family.
5. Assumptions, uncertainty, counterevidence and what would reverse the view.
6. Qualitative confidence in the future judgment, distinct from confidence in the observation. Do not present high evidence quality as a high chance of a price prediction succeeding.
7. A sourcing action, affected buyer categories and a measurable trigger where available.
8. Editorial review date, next review date, current/due/stale state, correction history and publication status.

`data/outlooks.json` seeds eight draft cards. The cards are directional decision outlooks, not scored numeric predictions. Each includes a review criterion. A later quantitative prediction additionally needs a precise target variable, geography, unit, baseline, target period, threshold/range, source vintage, resolution source and expected publication lag. If those cannot be defined, retain a watch item or directional outlook rather than inventing a target.

**Example presentation:** “Grid connection and execution risk likely remain material for U.S. expansions — medium confidence.” Show Berkeley Lab's generation-queue evidence and its exclusion of load requests; then explain why the buyer still needs a separate utility commitment. Never display “all factories wait five years.”

## Data model and repository layout

| Asset | Purpose | Editing rule |
|---|---|---|
| `data/sources.csv` | Canonical source registry | Append stable IDs; retain publication precision, family and access/review status |
| `data/observations.json` | Reviewed statements supporting outlooks | Observation, source forecast or document provision; explicit geography, period and caveat |
| `data/outlooks.json` | Global/U.S. decision narratives | References observation IDs and reviewed sources; draft until editorial approval |
| `data/chart_data.csv` | Reviewed numerical inputs | No direct publishing of freshly scraped numbers |
| `data/releases.json` | Edition history and changes | Append release; do not alter past issue dates to conceal revisions |
| `schemas/research-content.schema.json` | Contract for the three JSON content files | Validate before rendering; version the contract |
| `docs/sources.md` | Human-readable source catalog | Generate from the registry; do not maintain conflicting dates manually |
| `scripts/export_catalog.py` | Catalog and source export | Produces website-ready source metadata; does not approve evidence |
| `scripts/check_research.py` | Content checks | Schema, foreign keys, dates, access/review status, report links and chart assets |
| `reports/` and `charts/` | Long-form editions and figures | Retain provenance and distinguish past context from current evidence |

Keep downloaded full articles in ignored `.research-cache/`. Store citations, hashes, brief paraphrases, reviewed numbers and the analysis in the repository. Treat inaccessible articles as leads, not support. A website search result should link the original publication, not redistribute its full text. Use publisher-approved RSS/APIs where practical and respect licenses and request limits.

## Recommended implementation

Use **Astro + TypeScript with static generation** for the first release. Read the reviewed JSON/CSV at build time. This fits a small editorial publication, supports fast pages and straightforward previews, and avoids a database or live scraping service for the MVP. Use lightweight client-side filters and a simple chart library only where interaction adds value; retain accessible static charts/data tables.

Suggested future app location: `site/`. Use the Node LTS and package-manager versions selected when implementation begins; pin them and the dependency lockfile then. Do not invent an untested package setup as part of this planning task. Local preview and a deployment provider can be chosen during implementation; publication requires the user's later authorization.

A small Git-backed editing workflow is sufficient initially. Add a CMS only if nontechnical editors need it after the workflow is established. Discovery runs separately from production builds. The public site reads approved content and never scrapes live sources when a reader opens a page.

## Implementation sequence and acceptance criteria

Indicative effort assumes one developer, a research editor and access to a second reviewer; it is a planning estimate, not a committed delivery date.

| Phase | Indicative effort | Deliverable | Acceptance criteria |
|---|---|---|---|
| 1. Content contract and editorial process | 1–2 working days | Finalize source, observation and outlook records; complete two practice update runs | Each claim has correct type, scope, period and source; no inaccessible evidence or unexplained numeric conflict |
| 2. Website MVP | 3–5 working days | Home, both perspective pages, topic/outlook pages, source/methodology pages and charts | Global/U.S. views work on mobile; links/filters/keyboard navigation work; every chart exposes data and uncertainty |
| 3. Review and release tooling | 2–3 working days | Validation, draft preview, change log, stale-state display and reproducible build | A bad source ID, future-dated source, invalid status or missing cited chart fails validation; draft content cannot enter production |
| 4. Pilot publication | At least two Tuesday/Thursday cycles | Controlled editorial releases and corrections rehearsal | Reviewer can compare editions, mark no-change reviews and reproduce charts; recovery to the last approved edition works |
| 5. Optional expansion | After pilot evidence | Search, subscriptions, more regions, quantitative prediction tracking | Added features support reader decisions without weakening source or review controls |

The user authorized committing and pushing the reviewed project files. Website publication, deployment and schedule activation remain separate future steps.

## Trust, measurement and maintenance

- Measure citation coverage, independent study-family coverage by decision, broken links, overdue reviews and correction turnaround. More URLs do not necessarily mean more evidence.
- Require a primary document for a legal assertion. Prefer two independent evidence families for a material market judgment; if only one is available, disclose it and narrow confidence/scope. A journalist quoting BNEF is not a second forecast.
- Make disagreements visible: source vintage, sample, geography and metric may explain differences; never average incompatible forecasts just to create a “consensus.”
- Preserve numeric forecast records until their target period and publication lag have ended. Compare with the specified realization series. Do not score a 2027 annual forecast using October 2027 partial-year data.
- Initially evaluate directional outlooks through documented editorial review. Add statistical calibration only after enough genuinely comparable resolved predictions exist; avoid an invented accuracy percentage from a handful of cases.
- Reassess the source mix monthly and methodology quarterly. Include U.S. regional operators, international agencies, original commercial research, primary trade documents, independent reporting and disclosed supplier evidence where relevant.

This plan draws on the current report's source distinctions: [Berkeley Lab, May 2026](https://emp.lbl.gov/publications/queued-2026-edition-characteristics), [World Bank Pink Sheet, October 2, 2026](https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Pink-Sheet-October-2026.pdf), [BloombergNEF, October 22, 2026](https://about.bnef.com/insights/commodities/energy-storage-growth-surge-goes-global-three-things-to-know/), and [USTR notice, September 2, 2026](https://www.federalregister.gov/documents/2026/09/02/2026-17925/notice-of-conforming-amendments-to-product-exclusions-chinas-acts-policies-and-practices-related-to). The architecture and editorial schedule are recommendations, not conclusions asserted by those sources.
