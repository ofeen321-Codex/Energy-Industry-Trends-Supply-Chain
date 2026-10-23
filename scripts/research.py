#!/usr/bin/env python3
"""Retrieve research inputs and search leads. Retrieval never constitutes source review."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import shutil
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CACHE = ROOT / ".research-cache"
MAX_BYTES = 30 * 1024 * 1024


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "noscript"}:
            self.hidden += 1
        if tag in {"p", "h1", "h2", "h3", "li", "div", "br"}:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in {"script", "style", "noscript"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, text):
        if not self.hidden:
            self.parts.append(text)


class SearchLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.results = []
        self.current = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "result__a" in attrs.get("class", ""):
            url = attrs.get("href", "")
            redirect = urllib.parse.parse_qs(urllib.parse.urlparse(url).query).get("uddg")
            if redirect:
                url = redirect[0]
            self.current = {"title": "", "url": url}

    def handle_data(self, text):
        if self.current is not None:
            self.current["title"] += text

    def handle_endtag(self, tag):
        if tag == "a" and self.current is not None:
            self.results.append(self.current)
            self.current = None


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def fetch(url):
    request = urllib.request.Request(url, headers={
        "User-Agent": "EnergySupplyChainResearch/1.0 (public-source research)",
        "Accept": "text/html,application/pdf,application/rss+xml,application/xml;q=0.9,*/*;q=0.5",
    })
    # Use the environment's normal proxy and TLS certificate verification.
    with urllib.request.urlopen(request, timeout=25) as response:
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError("Response exceeds 30 MiB; inspect and download manually")
        return body, response.url, response.headers.get("Content-Type", ""), response.status


def get_sources(ids):
    sources = read_csv(DATA / "sources.csv")
    if ids:
        selected = set(ids)
        unknown = selected - {row["source_id"] for row in sources}
        if unknown:
            raise ValueError(f"Unknown source IDs: {sorted(unknown)}")
        sources = [row for row in sources if row["source_id"] in selected]
    CACHE.mkdir(exist_ok=True)
    log_path = DATA / "retrieval_log.csv"
    rows = read_csv(log_path) if log_path.exists() else []
    for source in sources:
        sid = source["source_id"]
        row = dict(attempt_utc=datetime.now(timezone.utc).isoformat(),
                   source_id=sid, requested_url=source["url"], final_url="",
                   status="", http_status="", sha256="", text_extracted="no", detail="")
        try:
            body, final, content_type, status = fetch(source["url"])
            is_pdf = body.startswith(b"%PDF")
            suffix = ".pdf" if is_pdf else ".html"
            raw = CACHE / (sid + suffix)
            raw.write_bytes(body)
            row.update(final_url=final, status="retrieved_unreviewed", http_status=status,
                       sha256=hashlib.sha256(body).hexdigest())
            if is_pdf:
                if shutil.which("pdftotext"):
                    result = subprocess.run(["pdftotext", "-layout", str(raw),
                                             str(CACHE / (sid + ".txt"))],
                                            capture_output=True, text=True)
                    if result.returncode:
                        row["detail"] = "Downloaded; pdftotext extraction failed"
                    else:
                        row["text_extracted"] = "yes"
                else:
                    try:
                        from pypdf import PdfReader
                        reader = PdfReader(raw)
                        (CACHE / (sid + ".txt")).write_text(
                            "\n".join(page.extract_text() or "" for page in reader.pages),
                            encoding="utf-8")
                        row["text_extracted"] = "yes"
                    except ImportError:
                        row["detail"] = "Downloaded; install pypdf or pdftotext for extraction"
            elif "html" in content_type or body.lstrip().lower().startswith(b"<!doctype html"):
                parser = ArticleText()
                parser.feed(body.decode("utf-8", errors="replace"))
                text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                                 if line.strip())
                (CACHE / (sid + ".txt")).write_text(text, encoding="utf-8")
                row["text_extracted"] = "yes"
            else:
                row["detail"] = "Downloaded; inspect content type manually: " + content_type
        except Exception as error:
            row["status"] = "failed"
            row["detail"] = str(error)[:400]
            if isinstance(error, urllib.error.HTTPError):
                row["http_status"] = error.code
            elif "403" in str(error):
                row["http_status"] = "403_proxy_connect"
        rows.append(row)
        print(sid, row["status"], row["detail"])
    fields = ["attempt_utc", "source_id", "requested_url", "final_url", "status",
              "http_status", "sha256", "text_extracted", "detail"]
    write_csv(log_path, fields, rows)
    latest = {row["source_id"]: row for row in rows}
    return any(latest[source["source_id"]]["status"] == "failed" for source in sources)


def search():
    """Discover candidate URLs; search snippets are not report evidence."""
    queries = read_csv(DATA / "search_queries.csv")
    path = DATA / "search_log.jsonl"
    failed = False
    for query in queries:
        url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({
            "q": query["query"]})
        record = dict(attempt_utc=datetime.now(timezone.utc).isoformat(),
                      query_id=query["query_id"], query=query["query"], url=url,
                      status="", results=[], detail="")
        try:
            body, final, _, status = fetch(url)
            parser = SearchLinks()
            parser.feed(body.decode("utf-8", errors="replace"))
            record.update(status="retrieved_unreviewed", final_url=final, http_status=status)
            record["results"] = parser.results
            if not record["results"]:
                record["status"] = "no_results"
        except Exception as error:
            record.update(status="failed", detail=str(error)[:400])
            failed = True
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(query["query_id"], record["status"], len(record["results"]), record["detail"])
    return failed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true", help="Retrieve registered sources")
    parser.add_argument("--search", action="store_true", help="Run logged web discovery queries")
    parser.add_argument("--ids", nargs="+", help="Fetch only these source IDs")
    args = parser.parse_args()
    if not args.fetch and not args.search:
        parser.error("Choose --fetch and/or --search")
    failed = False
    if args.fetch:
        failed = get_sources(args.ids) or failed
    if args.search:
        failed = search() or failed
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
