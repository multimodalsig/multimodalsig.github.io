"""Build _data/publications_generated.yml from ORCID + Crossref.

Why this exists
---------------
The Publications page used to assemble itself in the browser: it fetched the
PI's ORCID record, enriched it from Crossref, and rendered the list with
JavaScript. Search engines therefore received a page whose only text was
"Fetching the latest publications...", which for a research group hides the
single most valuable content on the site.

This script does that same work ahead of time, so the page ships as static HTML.
It is the ONLY place the citation formatting lives -- the logic here is a
port of the browser code it replaced (assets/js/site.js, initPublications).

Inputs
------
  _data/publications.yml         hand-maintained papers missing from ORCID
  _data/publications_hidden.yml  ORCID works to leave off the page
  _data/contact.yml              email, used for Crossref's "polite pool"

Output
------
  _data/publications_generated.yml   grouped by year, newest first, with every
                                     display string pre-formatted. Never edit
                                     it by hand; edit the inputs and re-run.

Usage
-----
  python tools/sync_publications.py            # write the file
  python tools/sync_publications.py --check    # print the fingerprint, write nothing

Refusing to write
-----------------
An empty or badly shrunken result is treated as an upstream failure, not as
news: if ORCID returns nothing, or the list would lose more than SHRINK_LIMIT
of its entries, the script exits non-zero and leaves the committed file alone.
Without that guard one bad API response would silently wipe the page.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

import yaml

ORCID = "0000-0001-7038-073X"
ORCID_API = "https://pub.orcid.org/v3.0/{}/works"
CROSSREF_API = "https://api.crossref.org/works"
CHUNK = 40           # DOIs per Crossref request
SHRINK_LIMIT = 0.20  # refuse a sync that drops >20% of the entries

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_data")
OUT = os.path.join(DATA, "publications_generated.yml")


# ---- helpers ---------------------------------------------------------------

def fetch_json(url, headers=None, retries=2):
    req = urllib.request.Request(url, headers=headers or {})
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception:
            if attempt == retries:
                raise
            time.sleep(1.5 * (attempt + 1))


def load_yaml(name, default=None):
    path = os.path.join(DATA, name)
    if not os.path.exists(path):
        return default if default is not None else []
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or (default if default is not None else [])


def title_key(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


# ---- formatting (ported from initPublications) ------------------------------

def initials(given):
    """"Derek D." -> "D. D."; "Faith" -> "F."."""
    if not given:
        return ""
    parts = [p for p in re.split(r"[\s.\-]+", given) if p]
    return " ".join(p[0].upper() + "." for p in parts)


def format_authors(items):
    """"Nayko, F., & Lichti, D. D."."""
    if not items:
        return ""
    names = []
    for a in items:
        if a.get("name"):                  # corporate authors have no given/family
            names.append(a["name"])
            continue
        ini = initials(a.get("given"))
        family = a.get("family")
        if family:
            names.append(f"{family}, {ini}" if ini else family)
        elif ini:
            names.append(ini)
    names = [n for n in names if n]
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", & " + names[-1]


def authors_of(w):
    """Curated entries carry a ready-made author string; ORCID ones get theirs
    from the Crossref lookup."""
    return w.get("authors") or format_authors((w.get("meta") or {}).get("author"))


def type_label(t):
    t = (t or "").lower()
    if "conference" in t:
        return "Conference", "badge--blue"
    if "book" in t:
        return "Book", "badge--purple"
    if "journal" in t:
        return "Journal", "badge--green"
    if not t:
        return "Other", "badge--grey"
    return t.replace("-", " ").title(), "badge--grey"


def pick_container(items):
    """Crossref gives proceedings both a series and a volume title, and some
    journals both a full and an abbreviated name. The longest entry is reliably
    the specific, spelled-out one."""
    if not items:
        return ""
    return sorted(items, key=lambda s: len(s or ""), reverse=True)[0]


def source_line(w):
    """"Sensors, 26(1), 319" -- whichever parts we actually have."""
    m = w.get("meta") or {}
    out = pick_container(m.get("container-title")) or w.get("journal") or ""
    # Crossref returns container titles HTML-escaped ("Engineering &amp; ..."),
    # and the browser version printed them raw. Undo it here.
    out = html.unescape(out)
    if m.get("volume"):
        out += (", " if out else "") + str(m["volume"])
        if m.get("issue"):
            out += f"({m['issue']})"
    if m.get("page"):
        out += (", " if out else "") + str(m["page"])
    return out


def citation(w):
    authors = authors_of(w)
    title = re.sub(r"\s*\.\s*$", "", w["title"])
    src = source_line(w)
    year = w.get("year") or ""
    if authors:
        out = authors + (f" ({year})" if year else "") + ". " + title + "."
        if src:
            out += " " + src + "."
    else:
        # Works ORCID lists without a DOI have no author data, so lead with the
        # title rather than a bare "(2016)." and put the year at the end.
        out = title + "."
        if src:
            out += " " + src
        if year:
            out += (", " if src else " ") + year
        out += "."
    if w.get("url"):
        out += " " + w["url"]
    return out


# ---- assembly ---------------------------------------------------------------

def curated_works():
    """Papers missing from ORCID, hand-maintained in _data/publications.yml.
    They are never sent to Crossref -- the YAML is the record."""
    out = []
    for p in load_yaml("publications.yml"):
        doi = p.get("doi") or ""
        out.append({
            "title": p.get("title") or "Untitled",
            "journal": p.get("journal") or "",
            "year": str(p["year"]) if p.get("year") else "",
            "month": int(p["month"]) if p.get("month") else 0,
            "type": p.get("type") or "journal-article",
            "url": f"https://doi.org/{doi}" if doi else (p.get("url") or ""),
            "doi": doi,
            "curated": True,
            "authors": p.get("authors") or "",
            "meta": {"volume": p.get("volume") or "", "issue": p.get("issue") or "",
                     "page": p.get("pages") or ""},
        })
    return out


def drop_hidden(works):
    """ORCID lists editorials and errata alongside research papers; the ones we
    don't want are named in _data/publications_hidden.yml."""
    hidden = load_yaml("publications_hidden.yml")
    if not hidden:
        return works
    dois = {h["doi"].lower() for h in hidden if h.get("doi")}
    titles = {title_key(h["title"]) for h in hidden if h.get("title")}
    return [w for w in works
            if not (w.get("doi") and w["doi"].lower() in dois)
            and title_key(w["title"]) not in titles]


def merge(orcid_works, curated):
    """Curated entries win: if one also shows up in ORCID later, the ORCID copy
    is dropped rather than listed twice."""
    if not curated:
        return orcid_works
    dois = {w["doi"].lower() for w in curated if w.get("doi")}
    titles = {title_key(w["title"]) for w in curated}
    kept = [w for w in orcid_works
            if not (w.get("doi") and w["doi"].lower() in dois)
            and title_key(w["title"]) not in titles]
    return kept + curated


def fetch_orcid():
    data = fetch_json(ORCID_API.format(ORCID), headers={"Accept": "application/json"})
    works = []
    for g in data.get("group") or []:
        summaries = g.get("work-summary") or []
        if not summaries:
            continue
        s = summaries[0]
        pd = s.get("publication-date") or {}
        ids = ((s.get("external-ids") or {}).get("external-id")) or []
        doi, doi_url = "", ""
        for x in ids:
            if x.get("external-id-type") == "doi":
                doi = x.get("external-id-value") or ""
                doi_url = ((x.get("external-id-url") or {}).get("value")
                           or (f"https://doi.org/{doi}" if doi else ""))
        if not doi_url and ids and ids[0].get("external-id-url"):
            doi_url = ids[0]["external-id-url"].get("value") or ""
        title = (((s.get("title") or {}).get("title") or {}).get("value")) or "Untitled"
        works.append({
            "title": title,
            "journal": ((s.get("journal-title") or {}).get("value")) or "",
            "year": ((pd.get("year") or {}).get("value")) or "",
            "month": int((pd.get("month") or {}).get("value") or 0),
            "type": s.get("type") or "",
            "url": doi_url,
            "doi": doi,
        })
    return works


def enrich(works, mailto):
    """Look the DOIs up at Crossref in batches and hang the result on each work.
    Any chunk that fails just leaves those entries with their ORCID detail."""
    by_doi = {w["doi"].lower(): w for w in works if w.get("doi") and not w.get("curated")}
    dois = list(by_doi)
    if not dois:
        return 0
    hit = 0
    for i in range(0, len(dois), CHUNK):
        chunk = dois[i:i + CHUNK]
        params = {
            "rows": "100",
            "select": "DOI,author,container-title,volume,issue,page",
            "filter": ",".join("doi:" + d for d in chunk),
        }
        if mailto:
            params["mailto"] = mailto
        url = CROSSREF_API + "?" + urllib.parse.urlencode(params)
        try:
            j = fetch_json(url, retries=1)
        except Exception as e:
            print(f"  ! Crossref chunk {i // CHUNK + 1} failed ({e}); "
                  f"those entries keep their ORCID detail", file=sys.stderr)
            continue
        for item in ((j.get("message") or {}).get("items") or []):
            w = by_doi.get((item.get("DOI") or "").lower())
            if w:
                w["meta"] = item
                hit += 1
    return hit


def build():
    curated = curated_works()
    orcid = fetch_orcid()
    if not orcid:
        raise SystemExit("ORCID returned no works — refusing to write. "
                         "Treat this as an upstream outage, not an empty record.")
    print(f"  ORCID: {len(orcid)} works, curated: {len(curated)}")

    works = merge(drop_hidden(orcid), curated)
    contact = load_yaml("contact.yml", default={}) or {}
    hit = enrich(works, contact.get("email", ""))
    print(f"  Crossref enriched: {hit}/{len(works)}")

    works.sort(key=lambda w: (int(w.get("year") or 0), w.get("month") or 0), reverse=True)

    groups, by_year = [], {}
    for w in works:
        yr = w.get("year") or "Undated"
        if yr not in by_year:
            by_year[yr] = {"year": yr, "count": 0, "entries": []}
            groups.append(by_year[yr])
        label, cls = type_label(w.get("type"))
        by_year[yr]["entries"].append({
            "title": w["title"],
            "authors": authors_of(w),
            "venue": source_line(w),
            "type_label": label,
            "type_class": cls,
            "url": w.get("url") or "",
            "citation": citation(w),
        })
        by_year[yr]["count"] += 1
    return works, groups


def fingerprint(works, groups):
    return {
        "total": len(works),
        "groups": [[g["year"], g["count"]] for g in groups],
        "order": [title_key(w["title"])[:44] for w in works],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="print the fingerprint and write nothing")
    ap.add_argument("--force", action="store_true",
                    help="write even if the list shrank past the safety limit")
    args = ap.parse_args()

    works, groups = build()

    previous = load_yaml("publications_generated.yml", default={}) or {}
    prev_total = previous.get("total") or 0
    if prev_total and len(works) < prev_total * (1 - SHRINK_LIMIT) and not args.force:
        raise SystemExit(
            f"Refusing to write: {len(works)} entries, down from {prev_total} "
            f"(>{int(SHRINK_LIMIT * 100)}% smaller). Re-run with --force if the "
            f"drop is real.")

    fp = fingerprint(works, groups)
    if args.check:
        print(json.dumps(fp))
        return

    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# GENERATED by tools/sync_publications.py -- do not edit by hand.\n"
                "# Edit _data/publications.yml (extra papers) or\n"
                "# _data/publications_hidden.yml (exclusions) and re-run the script.\n")
        yaml.safe_dump({"total": len(works), "years": groups}, f,
                       allow_unicode=True, sort_keys=False, width=100)
    print(f"  wrote {os.path.relpath(OUT, ROOT)}: "
          f"{len(works)} publications across {len(groups)} years")


if __name__ == "__main__":
    main()
