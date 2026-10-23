# Twice-weekly research and website update playbook

**Recommended publication:** Tuesdays and Thursdays, **10:00 a.m. America/New_York**. **Status:** proposed process, not an activated job. Next proposed review after this edition: **Tuesday, October 27, 2026**. No automated update, email, alert or public publication is activated by this document.

Two releases a week means approximately 104 scheduled reviews a year; a review can truthfully report no material change. It does not require inventing two new forecasts every week.

## Roles and release authority

- **Research editor:** discovers changes, reads original sources, updates evidence, dates and assumptions, and proposes decision changes.
- **Reviewer:** checks material claims against source documents, challenges the forecast inference, verifies U.S./global comparisons and legal-status wording, and approves or returns the draft.
- **Release owner:** publishes only an approved edition after the user authorizes the publishing workflow. Research drafts can be versioned without being approved for public website release.

One person can hold multiple roles, but high-impact tariff, legal, numeric or operational claims need a second-person check before public release. If no reviewer is available, retain a draft and flag the delay; do not turn a missed review into apparent verification.

## Tuesday/Thursday run

Times are suggested working targets, in New York time, rather than guarantees.

| Time | Step | Concrete output and check |
|---|---|---|
| 08:00 | Fetch monitored sources and discover new documents | Retrieval outcomes and hashes; original publication date and data period; no claims approved automatically |
| 08:30 | Triage | Classify material change, background, duplicate, inaccessible lead or no change; identify buyer decision affected |
| 09:00 | Research and draft | Read source and method/footnotes; record observations and change only affected outlooks, confidence, actions and charts |
| 09:30 | Review | Check numbers, definitions, legal state and counterevidence; separate global from U.S. implications; resolve or disclose conflicts |
| 09:50 | Validate and preview | Schema/citation/date checks, link and chart review, source-family coverage, draft/publication status |
| 10:00 | Authorized release or explicit hold | Approved edition and concise change log, or a draft/late notice with reason; retain prior approved version |

Tuesday covers developments since the prior Thursday cutoff; Thursday covers developments since Tuesday. Include a 24-hour overlap for delayed indexing and use canonical URL/document ID plus content hash to deduplicate. A source edit without a new URL can be material. Retain its previous hash, observation and forecast vintage.

## Monitoring matrix

| Area | Core sources and cadence | What changes a procurement decision |
|---|---|---|
| U.S. electricity/gas/oil | EIA STEO monthly; inventory/fuel reports weekly; local utility notices and relevant ISO/RTO releases | Delivered cost, demand/basis, service interruption and contract renewal exposure |
| Global fuel and logistics | IEA monthly reports and dated commentary; World Bank monthly benchmarks; relevant UNCTAD/transport reporting; accessible original news | Product shortages, route/insurance changes, tanker or terminal constraints; keep containers and tankers distinct |
| Grid and lead times | Berkeley Lab annual queue data; PJM and other regional operators; engineering-approved supplier quotes | Connection dates, accredited versus nameplate capacity, factory slots, testing and commissioning |
| Renewables and storage | IRENA annual costs; public BNEF updates; original industry reporting and disclosed supplier data | Qualified landed costs, sample/benchmark shifts, capacity actually shipping, warranty/service risk |
| Minerals | IEA and BNEF outlooks; USGS when accessible; original official export notices and reliable event reporting | Refiner/license bottleneck, changed scope or suspension, input availability and qualification lead time |
| Tariffs/trade | Federal Register, USTR, Commerce/ITC, USITC HTS and current CBP instructions | Effective date, case/scope, producer, entry treatment, exclusion language and cash-deposit instruction |
| Tax/regulation | IRS/Treasury notices and subsequent rules, FERC decisions and applicable state/utility rules | Credit eligibility, timing, market participation, new documentation or compliance obligations |
| Supplier execution | Original filings/releases, qualified quotes, contract milestones and independent reporting | Shipment, capacity ramp, defects, service capability, credit/insurance or contractor interface risk |

Check time-sensitive trade/export/legal sources every run, even if the main article is older. For slower annual publications, check whether a new edition exists; do not relabel old observations as new data. Manufacturer and law-firm sources are useful for their own disclosures and interpretations, respectively, but are not neutral market-wide samples or controlling law.

## Local refresh commands

From this repository's root:

```bash
python scripts/research.py --fetch --ids D01 A01 A02 A03 A04 A05 B01 B03 B07 B10 B15 B16 B17 A06 A09 A10
```

Before future runs, update `data/search_queries.csv` to the intended cutoff and run selected discovery queries as appropriate:

```bash
python scripts/research.py --search
```

Some pages may be blocked, removed, an index, a challenge, or an HTTP-200 error page. Inspect actual content. The scripts log retrieval, not editorial approval. Avoid repeatedly downloading a large unchanged PDF when a source index or release notice establishes that there is no newer edition.

After editorial changes:

```bash
python scripts/export_catalog.py
python scripts/charts.py
python scripts/check_research.py
```

These commands prepare local files. They do not schedule, commit, push, approve or publish anything. For missing dependencies see `requirements-research.txt` and the [update guide](updating.md).

## Materiality and editorial rules

Publish a changed judgment when new evidence changes an actionable price/availability assumption, a sourcing/lead-time decision, a legal requirement or effective date, a supplier's ability to deliver, confidence, or a previously cited fact. Preserve the old claim with a superseded/corrected state and explain why it changed.

For unchanged material, record that it was reviewed, not that the underlying data were re-measured. A change to a download timestamp alone must not refresh an observation date or forecast issue date. Keep at least one explicit counterargument or reversal trigger for every outlook.

Use these evidence states:

| State | Meaning | Public behavior |
|---|---|---|
| Retrieved, unreviewed | A response was downloaded | Cannot substantiate a new public claim |
| Reviewed | Editor read the relevant content, date, unit and scope | May support a draft; reviewer still approves the release |
| Inaccessible | Source content could not be read | Lead only; no inferred facts from URL/title/snippet |
| Contradicted or superseded | Better evidence, correction or a newer incompatible vintage exists | Show the revision; do not silently overwrite the old record |
| Insufficient evidence | Plausible view without adequate support | Watchlist/scenario or omit; do not call it a verified prediction |

Maintain jurisdiction and legal state separately: proposal, announcement, final determination, final rule/order, effective, suspended, litigated or status not reverified. A customs entry must not be priced from a generic news headline. Preserve primary document links and obtain applicable broker/legal advice for a real transaction.

## Freshness and failure handling

- Each active card is due on the next Tuesday/Thursday review. After its due date, display **review due**. If it remains unreviewed after the following scheduled review, display **stale** and remove it from “new/verified” promotional placement.
- Evidence age and review freshness are separate. An annual queue observation can still be useful with its 2025 period visible; checking it today does not make it an October observation.
- Treat a changed law, route disruption or major source correction as an off-cycle draft trigger. Off-cycle publication still needs the normal authorized review; no automatic external notification is assumed.
- On partial source failure, continue independent categories and show the affected evidence gap. Retain the last approved content with its age and a failed-check flag; never show a failed retrieval as a fresh verification.
- On invalid data, wrong units, broken evidence references or unexplained source conflict, hold affected claims. If a forecast assumption changes, downgrade or withdraw the forecast rather than hiding the problem.
- On build failure, retain the previous approved website artifact. Publication and rollback tooling are implemented only in a later authorized phase.

## Automation design for later implementation

Start with scheduled **collection and draft generation**, not unattended public interpretation of articles. Prefer official APIs/RSS and conditional HTTP requests when supported. A later scheduler should use the IANA `America/New_York` zone. If only UTC cron is available, run at both 14:00 and 15:00 UTC on Tuesday/Thursday with a local-time guard so exactly one run targets 10:00 New York time across daylight-saving transitions. Do not configure an external workflow now.

Use a per-date run ID, idempotent deduplication, retained logs, bounded retries only for transient failures, and separate validation/review/publication stages. New numeric extractions require human confirmation; new source domains require an ordinary credibility review. Keep credentials in environment settings, never in repository content.

## Release checklist and forecast evaluation

Before a release, confirm original links and dates, country/region, unit and denominator, sample/population, data versus forecast period, source independence, current legal state, chart labels, global/U.S. narratives and who approved it. Record unresolved limitations and what changed since the previous edition. Append a release record; a no-change review is not a newly successful forecast.

For a quantitative forecast, store its original target, horizon, assumptions and evaluation source before publication. Resolve only after the whole target period and source lag end; keep observed outcomes separate from revised forecasts. Report abstentions, unresolved cases and withdrawn forecasts as well as successes. Directional cards in this revision require documented reassessment rather than an invented hit-rate statistic.
