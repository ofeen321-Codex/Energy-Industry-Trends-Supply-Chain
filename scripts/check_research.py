#!/usr/bin/env python3
"""Check research integrity and publication state; does not verify factual truth."""
import argparse
import csv
from datetime import date
import json
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--publication", action="store_true", help="Require approved current content; never publishes")
args = parser.parse_args()
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


bundle = {key: json.loads((ROOT / "data" / f"{key}.json").read_text())
          for key in ["observations", "outlooks", "releases"]}
schema = json.loads((ROOT / "schemas/research-content.schema.json").read_text())
Draft202012Validator.check_schema(schema)
for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(bundle):
    errors.append(f"Schema {list(error.absolute_path)}: {error.message}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

with (ROOT / "data/sources.csv").open(newline="") as stream:
    source_rows = list(csv.DictReader(stream))
sources = {r["source_id"]: r for r in source_rows}
require(len(sources) == len(source_rows), "Duplicate source IDs")
with (ROOT / "data/retrieval_log.csv").open(newline="") as stream:
    retrieved = {r["source_id"] for r in csv.DictReader(stream)
                 if r["status"] == "retrieved_unreviewed" and r["sha256"]}
evidence = {r["id"]: r for r in bundle["observations"]}
for group, rows in bundle.items():
    require(len({r["id"] for r in rows}) == len(rows), f"Duplicate {group} IDs")
cutoff = max(r["as_of"] for r in bundle["releases"])


def check_source(sid, consumer):
    require(sid in sources, f"{consumer}: unknown source {sid}")
    if sid not in sources:
        return
    source = sources[sid]
    require(source["review_status"].startswith("reviewed"), f"{consumer}: unread source {sid}")
    require(sid in retrieved, f"{consumer}: no hashed retrieval for {sid}")
    publication = source["publication_date"]
    if publication:
        require(bool(re.fullmatch(r"\d{4}(-\d{2})?(-\d{2})?", publication)), f"{sid}: invalid publication date")
        require(publication <= cutoff[:len(publication)], f"{sid}: publication after cutoff")


for item in bundle["observations"]:
    require(item["last_reviewed"] <= cutoff, f"{item['id']}: review after cutoff")
    for sid in item["source_ids"]:
        check_source(sid, item["id"])
for item in bundle["outlooks"]:
    fid = item["id"]
    require(item["as_of"] <= item["horizon_start"] < item["horizon_end"], f"{fid}: inconsistent horizon")
    require(item["as_of"] <= cutoff, f"{fid}: issue date after cutoff")
    require(item["last_reviewed"] <= cutoff, f"{fid}: review after cutoff")
    require(item["next_review_due"] > item["last_reviewed"], f"{fid}: invalid next review date")
    require(date.fromisoformat(item["next_review_due"]).weekday() in {1, 3}, f"{fid}: review is not Tuesday/Thursday")
    expected_sources = set()
    for eid in item["observation_ids"]:
        require(eid in evidence, f"{fid}: unknown observation {eid}")
        if eid in evidence:
            expected_sources.update(evidence[eid]["source_ids"])
    require(expected_sources == set(item["source_ids"]), f"{fid}: evidence/source references disagree")
    if item["status"] == "approved":
        require(bool(item.get("approved_by") and item.get("approved_at")), f"{fid}: missing approval provenance")
for release in bundle["releases"]:
    require((ROOT / release["report_path"]).is_file(), f"{release['id']}: report missing")

report_path = ROOT / "reports/energy-supply-chain-outlook.md"
report = report_path.read_text()
refs = dict(re.findall(r"^\[([SADB]\d+)\]:\s+(\S+)", report, re.M))
for sid in set(re.findall(r"\[([SADB]\d+)\](?!:)", report)):
    check_source(sid, "current report")
    require(sid in refs and sid in sources and refs[sid] == sources[sid]["url"], f"Report citation URL mismatch: {sid}")
require(not re.search(r"\]\[(?=[SADB]\d+\])", report), "Adjacent reference citations can link to the wrong source")
for path in [ROOT / "README.md", *sorted((ROOT / "docs").glob("*.md")), *sorted((ROOT / "reports").glob("*.md"))]:
    for link in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        if not link.startswith(("https://", "http://", "#", "mailto:")):
            require((path.parent / link.split("#")[0]).exists(), f"Broken local link in {path.name}: {link}")
with (ROOT / "data/chart_data.csv").open(newline="") as stream:
    metrics = list(csv.DictReader(stream))
require(len({r["metric_id"] for r in metrics}) == len(metrics), "Duplicate chart metric IDs")
for metric in metrics:
    check_source(metric["source_id"], metric["metric_id"])
    float(metric["value"])
    for suffix in ["png", "svg"]:
        require((ROOT / "charts" / f"{metric['chart']}.{suffix}").is_file(), f"Missing chart {metric['chart']}.{suffix}")
for path in (ROOT / "charts").glob("*.svg"):
    ET.parse(path)
if args.publication:
    current = bundle["releases"][-1]
    require(current["status"] in {"approved", "published"}, "Current release is a draft; publication is blocked")
    require(bool(current.get("approved_by") and current.get("approved_at")), "Current release lacks reviewer approval")
    for item in bundle["outlooks"]:
        require(item["status"] == "approved", f"{item['id']} is not approved for publication")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"Passed: schema, {len(evidence)} evidence records, {len(bundle['outlooks'])} outlooks, citation URLs, dates, local links and {len(metrics)} chart inputs.")
print("Editorial truth/forecast accuracy still require human review. Current content remains draft; nothing published.")
