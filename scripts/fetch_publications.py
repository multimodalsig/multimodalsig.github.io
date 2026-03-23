#!/usr/bin/env python3
"""
Semantic Scholar -> BibTeX Pipeline for al-folio
================================================
Fetches publications for specified author(s) from the Semantic Scholar API
and generates a .bib file compatible with al-folio (Jekyll Scholar).

Usage:
    python scripts/fetch_publications.py
    python scripts/fetch_publications.py --author-id 2245053
    python scripts/fetch_publications.py --output _bibliography/papers.bib

Run locally or via GitHub Action on a monthly schedule.
"""

import argparse
import json
import re
import time
import sys
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("ERROR: 'requests' required. Install: pip install requests")
    sys.exit(1)

DEFAULT_AUTHOR_IDS = ["2245053"]  # Derek D. Lichti
DEFAULT_OUTPUT = "_bibliography/papers.bib"
API_BASE = "https://api.semanticscholar.org/graph/v1"
FIELDS = (
    "title,authors,year,venue,publicationVenue,"
    "externalIds,abstract,citationCount,url,"
    "publicationTypes,journal,openAccessPdf"
)
PAPERS_PER_REQUEST = 500
REQUEST_DELAY = 1.1


def fetch_author_info(author_id, api_key=None):
    url = f"{API_BASE}/author/{author_id}"
    params = {"fields": "name,affiliations,paperCount,citationCount,hIndex"}
    headers = {"x-api-key": api_key} if api_key else {}
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_all_papers(author_id, api_key=None):
    all_papers = []
    offset = 0
    headers = {"x-api-key": api_key} if api_key else {}
    while True:
        url = f"{API_BASE}/author/{author_id}/papers"
        params = {"fields": FIELDS, "limit": PAPERS_PER_REQUEST, "offset": offset}
        resp = requests.get(url, params=params, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        papers = data.get("data", [])
        all_papers.extend(papers)
        print(f"  Fetched {len(all_papers)} / ~{data.get('total', '?')} papers...")
        if len(papers) < PAPERS_PER_REQUEST:
            break
        offset += PAPERS_PER_REQUEST
        time.sleep(REQUEST_DELAY)
    return all_papers


def sanitize_key(text):
    return re.sub(r"[^a-zA-Z0-9]", "", text)


def make_citation_key(paper):
    authors = paper.get("authors", [])
    year = paper.get("year") or "unknown"
    title = paper.get("title") or "untitled"
    if authors:
        last_name = authors[0].get("name", "Unknown").split()[-1].lower()
    else:
        last_name = "unknown"
    stop_words = {"a","an","the","of","in","on","for","and","to","with","from","by"}
    title_words = re.findall(r"[a-zA-Z]+", title.lower())
    first_word = next((w for w in title_words if w not in stop_words), "untitled")
    return f"{sanitize_key(last_name)}{year}{sanitize_key(first_word)}"


def escape_bibtex(text):
    if not text:
        return ""
    for char, repl in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_")]:
        text = text.replace(char, repl)
    return text


def format_authors(authors):
    formatted = []
    for a in authors:
        name = a.get("name", "")
        if not name:
            continue
        parts = name.split()
        if len(parts) >= 2:
            formatted.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        else:
            formatted.append(name)
    return " and ".join(formatted)


def entry_type(paper):
    pub_types = paper.get("publicationTypes") or []
    venue = (paper.get("venue") or "").lower()
    if "Conference" in pub_types:
        return "inproceedings"
    if "JournalArticle" in pub_types or "Review" in pub_types:
        return "article"
    if any(kw in venue for kw in ["conference","proceedings","symposium","workshop"]):
        return "inproceedings"
    return "article"


def paper_to_bibtex(paper, key):
    etype = entry_type(paper)
    lines = [f"@{etype}{{{key},"]

    if paper.get("title"):
        lines.append(f"  title = {{{escape_bibtex(paper['title'])}}},")
    if paper.get("authors"):
        lines.append(f"  author = {{{format_authors(paper['authors'])}}},")
    if paper.get("year"):
        lines.append(f"  year = {{{paper['year']}}},")

    journal_info = paper.get("journal") or {}
    venue = paper.get("venue", "")
    pub_venue = paper.get("publicationVenue") or {}
    venue_name = pub_venue.get("name") or venue or journal_info.get("name", "")
    if venue_name:
        field = "booktitle" if etype == "inproceedings" else "journal"
        lines.append(f"  {field} = {{{escape_bibtex(venue_name)}}},")

    if journal_info.get("volume"):
        lines.append(f"  volume = {{{journal_info['volume']}}},")
    if journal_info.get("pages"):
        lines.append(f"  pages = {{{journal_info['pages']}}},")

    ext_ids = paper.get("externalIds") or {}
    if ext_ids.get("DOI"):
        lines.append(f"  doi = {{{ext_ids['DOI']}}},")
    if paper.get("url"):
        lines.append(f"  url = {{{paper['url']}}},")

    oa_pdf = paper.get("openAccessPdf") or {}
    if oa_pdf.get("url"):
        lines.append(f"  pdf = {{{oa_pdf['url']}}},")
    if paper.get("abstract"):
        lines.append(f"  abstract = {{{escape_bibtex(paper['abstract'][:2000])}}},")
    if paper.get("citationCount"):
        lines.append(f"  note = {{Cited by {paper['citationCount']}}},")

    lines.append(f"  selected = {{false}},")
    lines.append("}")
    return "\n".join(lines)


def deduplicate_keys(items):
    seen = {}
    result = []
    for paper, key in items:
        if key in seen:
            seen[key] += 1
            key = f"{key}{chr(ord('a') + seen[key] - 1)}"
        else:
            seen[key] = 1
        result.append((paper, key))
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Semantic Scholar publications -> BibTeX for al-folio"
    )
    parser.add_argument("--author-id", action="append", default=None,
        help="Semantic Scholar author ID(s). Repeatable. Default: 2245053")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--json-dump", default=None)
    args = parser.parse_args()

    author_ids = args.author_id or DEFAULT_AUTHOR_IDS
    all_papers = []
    all_author_info = []

    for aid in author_ids:
        print(f"\nFetching author {aid}...")
        info = fetch_author_info(aid, args.api_key)
        all_author_info.append(info)
        print(f"  {info.get('name')} | {info.get('paperCount','?')} papers | h={info.get('hIndex','?')}")
        papers = fetch_all_papers(aid, args.api_key)
        all_papers.extend(papers)

    # Deduplicate by paperId
    seen_ids = set()
    unique = []
    for p in all_papers:
        pid = p.get("paperId")
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            unique.append(p)

    unique.sort(key=lambda p: p.get("year") or 0, reverse=True)
    keyed = deduplicate_keys([(p, make_citation_key(p)) for p in unique])

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    header = (
        f"% Multimodal Spatial Imaging Lab — Publication List\n"
        f"% Auto-generated from Semantic Scholar API\n"
        f"% Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"% Authors: {', '.join(i.get('name','?') for i in all_author_info)}\n"
        f"% Total papers: {len(keyed)}\n\n"
    )

    with open(output, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n\n".join(paper_to_bibtex(p, k) for p, k in keyed))
        f.write("\n")

    print(f"\nWrote {len(keyed)} entries to {output}")

    if args.json_dump:
        dump = Path(args.json_dump)
        dump.parent.mkdir(parents=True, exist_ok=True)
        with open(dump, "w") as f:
            json.dump({"authors": all_author_info, "papers": unique}, f, indent=2)
        print(f"JSON saved to {dump}")

    top = sorted(unique, key=lambda p: p.get("citationCount", 0), reverse=True)[:5]
    print(f"\nTop 5 cited:")
    for i, p in enumerate(top, 1):
        print(f"  {i}. [{p.get('citationCount',0)}] {(p.get('title') or '?')[:70]}")


if __name__ == "__main__":
    main()
