#!/usr/bin/env python3
"""Export reviewed metadata; this does not review, approve or publish research."""
import csv
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
with (DATA / "sources.csv").open(newline="", encoding="utf-8") as stream:
    sources = list(csv.DictReader(stream))
report = (ROOT / "reports/energy-supply-chain-outlook.md").read_text()
current_release = json.loads((DATA / "releases.json").read_text())[-1]
used = set(re.findall(r"\[([SADB]\d+)\](?!:)", report))
catalog = {"generated_utc": datetime.now(timezone.utc).isoformat(),
           "sources": sources}
(DATA / "source-catalog.json").write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
families = Counter(s["publisher_family"] for s in sources if s["source_id"] in used)
lines = ["# Source catalog and evidence diversity", "",
         f"Current edition: **{current_release['id']}**. Evidence cutoff: **{current_release['as_of']}**. Dates describe the source publication, not when a download happened. Partial dates retain their precision. See [source notes](source-notes.md) for methodology and conflicts.", "",
         f"The current report cites **{len(used)} source records across {len(families)} publisher/study families**. This measures breadth, not independence of every claim. Paired PDFs/chapters, catalogs and press coverage of another publisher's forecast are grouped; legal documents are evidence of provisions, not independent market forecasts.", "",
         "## Families used in the current report", "", "| Family | Cited records |", "|---|---:|"]
lines += [f"| {family} | {count} |" for family, count in sorted(families.items())]
lines += ["", "## Current report evidence", ""]
for source in sources:
    if source["source_id"] not in used:
        continue
    sid = source["source_id"]
    lines += [f"### {sid} — {source['publisher']}", "",
              f"[{source['working_title']}]({source['url']})", "",
              f"- **Published:** {source['publication_date'] or 'Exact date not verified'} ({source['date_precision']}). {source['date_basis']}",
              f"- **Data/effective period:** {source['data_period'] or 'See report and source notes; publication date is not the observation period.'}",
              f"- **Editorial review:** {source['last_editorial_review'] or 'Not reviewed'}; {source['review_status']}.",
              f"- **Family:** {source['publisher_family']}. {source['independence_notes']}",
              f"- **Use:** {source['research_purpose']}.", ""]
lines += ["## All registered sources and leads", "",
          "Sources below include the original nine inputs, prior-edition context, monitoring indexes, inaccessible leads and metadata cross-checks. Being listed is not an endorsement or proof that a source supports the current report.", "",
          "| ID | Publication | Publisher / original source | Review status |",
          "|---|---|---|---|"]
for source in sources:
    title = source["working_title"].replace("|", "\\|")
    lines.append(f"| {source['source_id']} | {source['publication_date'] or 'Unknown/undated'} | {source['publisher']}: [{title}]({source['url']}) | {source['review_status']} |")
lines += ["", "## Access, search and scope limits", "",
          "`data/retrieval_log.csv` retains timestamps, original/final URLs, outcomes and body hashes. `data/search_log.jsonl` records discovery attempts; `data/search_queries.csv` holds reproducible query wording. Original cached text remains ignored by Git.", "",
          "Reuters returned 401; IRENA's landing page returned 403, while the original IRENA summary PDF was accessible. These are separate access outcomes. Some attempted URLs were corrected after a 404; the failed attempts remain in the audit. A successful HTTP response can still be an index, login or challenge page and never supplies editorial verification by itself.", "",
          "Berkeley Lab's catalog says May 2026 while its PDF cover says June 2026; both are retained. IRENA's publication month is corroborated by the PNNL/Tethys catalog, whose bibliography provides month precision; its displayed day 1 is not treated as a verified exact release date. BNEF public releases do not establish access to the underlying client-only datasets.", "",
          "The source mix is reviewed per decision, not by simply counting URLs. See the [website plan](website-plan.md) and [twice-weekly process](twice-weekly-updates.md)."]
(ROOT / "docs/sources.md").write_text("\n".join(line.rstrip() for line in lines) + "\n")

outlooks = json.loads((DATA / "outlooks.json").read_text())
observations = {r["id"]: r for r in json.loads((DATA / "observations.json").read_text())}
fields = ["finding_id", "topic", "established_evidence", "conditional_12_month_outlook", "source_ids",
          "confidence_observation", "confidence_outlook", "global_perspective", "us_procurement_perspective",
          "procurement_action", "review_trigger", "as_of", "status"]
with (DATA / "findings.csv").open("w", newline="", encoding="utf-8") as stream:
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for item in outlooks:
        evidence = [observations[eid] for eid in item["observation_ids"]]
        observed = [e["text"] for e in evidence if e["claim_type"] in {"reported_observation", "documented_provision"}]
        writer.writerow(dict(finding_id=item["id"], topic=item["topic"],
                             established_evidence=" ".join(observed) or "See typed evidence records; no new observed outcome asserted.",
                             conditional_12_month_outlook=item["title"], source_ids=";".join(item["source_ids"]),
                             confidence_observation="See separate evidence_confidence for each record",
                             confidence_outlook=item["confidence"], global_perspective=item["global_view"],
                             us_procurement_perspective=item["us_view"],
                             procurement_action="; ".join(item["procurement_actions"]),
                             review_trigger="; ".join(item["review_triggers"]), as_of=item["as_of"], status=item["status"]))
print(f"Exported {len(sources)} registered sources; current report uses {len(used)} records / {len(families)} families; {len(outlooks)} draft outlook rows.")
