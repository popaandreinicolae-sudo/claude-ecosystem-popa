"""Client for lege6.ro - authenticated access to legislation, jurisprudence, doctrine.

Lege6.ro is the modern Indaco Systems platform that replaces lege5.ro.
Contains the most up-to-date Romanian legislation, jurisprudence (including CCR decisions),
and legal doctrine.
"""

import asyncio
import logging
import re
from typing import Optional

from bs4 import BeautifulSoup

from auth import Lege6Session, LEGE6_BASE

logger = logging.getLogger("legal-verificator.lege6")

_semaphore = asyncio.Semaphore(3)


async def _rate_limited(session: Lege6Session, method: str, url: str, **kwargs):
    async with _semaphore:
        await asyncio.sleep(0.33)
        if method == "get":
            return await session.get(url, **kwargs)
        return await session.post(url, **kwargs)


# Section type IDs may differ from lege5 — try multiple known patterns
SECTION_MAP = {
    "legislatie": ["1", "Legislatie"],
    "jurisprudenta": ["2", "Jurisprudenta"],
    "doctrina": ["6", "Doctrina"],
    "ccr": ["98", "CCR", "DecizieCCR"],
}


async def search(session: Lege6Session, query: str,
                 category: Optional[str] = None, max_results: int = 10) -> dict:
    """Full-text search on lege6.ro.

    Tries authenticated search first; falls back to public search endpoint.
    """
    await session.ensure_authenticated()

    params = {
        "term": query,
        "Search_Term": query,
        "Rec": str(max_results),
        "limit": str(max_results),
    }
    if category and category in SECTION_MAP:
        params["Search_SectionTypeId"] = SECTION_MAP[category][0]
        params["sectionType"] = SECTION_MAP[category][1]

    candidate_endpoints = [
        f"{LEGE6_BASE}/app/search",
        f"{LEGE6_BASE}/Search",
        f"{LEGE6_BASE}/app/api/search",
    ]

    soup = None
    for url in candidate_endpoints:
        try:
            resp = await _rate_limited(session, "get", url, params=params)
            if resp.status_code == 200 and len(resp.text) > 500:
                soup = BeautifulSoup(resp.text, "html.parser")
                break
        except Exception as e:
            logger.debug("lege6 search endpoint %s failed: %s", url, e)
            continue

    if soup is None:
        return {"results": [], "total": 0, "error": "Niciun endpoint de cautare lege6 nu a raspuns."}

    results = []

    for item in soup.find_all(["div", "article"], class_=re.compile(r"search-result|result-item|rezResult|rezultat", re.IGNORECASE)):
        title_el = item.find("a", class_=re.compile(r"result-title|titlu|title", re.IGNORECASE))
        if not title_el:
            title_el = item.find("a")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        if href and not href.startswith("http"):
            href = f"{LEGE6_BASE}{href}"

        snippet_el = item.find(["div", "p"], class_=re.compile(r"snippet|preview|continut|extract", re.IGNORECASE))
        snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""

        results.append({
            "title": title,
            "snippet": snippet,
            "url": href,
            "category": category or "all",
            "source": "lege6.ro",
        })
        if len(results) >= max_results:
            break

    if not results:
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)
            if text and len(text) > 15 and any(p in href for p in ("/Gratuit/", "/App/", "/app/", "/document/", "/decizie/", "/lege/")):
                full_href = f"{LEGE6_BASE}{href}" if not href.startswith("http") else href
                results.append({
                    "title": text,
                    "snippet": "",
                    "url": full_href,
                    "category": category or "all",
                    "source": "lege6.ro",
                })
                if len(results) >= max_results:
                    break

    return {"results": results, "total": len(results), "source": "lege6.ro"}


async def fetch_document(session: Lege6Session, url: str) -> dict:
    """Fetch full text of a document from lege6.ro."""
    await session.ensure_authenticated()

    resp = await _rate_limited(session, "get", url)
    soup = BeautifulSoup(resp.text, "html.parser")

    title = ""
    title_el = soup.find("h1") or soup.find("title")
    if title_el:
        title = title_el.get_text(strip=True)

    content = (
        soup.find("div", class_=re.compile(r"document-content|act-content|content-body|document-body|continut-act", re.IGNORECASE)) or
        soup.find("div", id=re.compile(r"content|document|act|continutAct", re.IGNORECASE)) or
        soup.find("article") or
        soup.find("main")
    )

    if content:
        for tag in content.find_all(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = content.get_text(separator="\n", strip=True)
    else:
        body = soup.find("body")
        if body:
            for tag in body.find_all(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            text = body.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

    metadata = {}
    for meta in soup.find_all("meta"):
        name = meta.get("name", "") or meta.get("property", "")
        if name and meta.get("content"):
            metadata[name] = meta["content"]

    return {
        "text": text,
        "title": title,
        "metadata": metadata,
        "source": "lege6.ro",
    }


async def search_ccr_decision(session: Lege6Session, number: int, year: int) -> dict:
    """Search for a CCR decision on lege6.ro."""
    queries = [
        (f"Decizia {number}/{year} Curtea Constitutionala", "ccr"),
        (f"Decizia {number} {year} CCR", "ccr"),
        (f"Decizia nr. {number} din {year}", None),
        (f"DCC {number}/{year}", "jurisprudenta"),
    ]

    for query, category in queries:
        result = await search(session, query, category=category, max_results=5)
        for r in result.get("results", []):
            if str(number) in r["title"] and str(year) in r["title"]:
                return {
                    "found": True,
                    "title": r["title"],
                    "url": r["url"],
                    "source": "lege6.ro",
                }

    return {"found": False, "source": "lege6.ro"}


async def fetch_ccr_text(session: Lege6Session, number: int, year: int) -> dict:
    """Fetch full text of CCR decision from lege6.ro."""
    result = await search_ccr_decision(session, number, year)
    if not result.get("found"):
        return {
            "text": "",
            "source": "lege6.ro",
            "total_chars": 0,
            "truncated": False,
            "error": f"Decizia CCR nr. {number}/{year} nu a fost gasita pe lege6.ro.",
        }

    doc = await fetch_document(session, result["url"])
    text = doc.get("text", "")
    total_chars = len(text)
    truncated = False

    if total_chars > 30000:
        text = text[:15000] + "\n\n[...TRUNCAT...]\n\n" + text[-5000:]
        truncated = True

    return {
        "text": text,
        "source": "lege6.ro",
        "total_chars": total_chars,
        "truncated": truncated,
        "url": result["url"],
        "title": result.get("title", ""),
    }


async def search_legislation(session: Lege6Session, act_type: str, number: int, year: int) -> dict:
    """Search for a legislative act on lege6.ro by type, number, year."""
    type_map = {
        "lege": "Legea",
        "oug": "Ordonanta de urgenta",
        "og": "Ordonanta",
        "hg": "Hotararea Guvernului",
        "ordin": "Ordin",
        "cod": "Codul",
        "constitutie": "Constitutia",
        "constituție": "Constitutia",
    }
    act_name = type_map.get(act_type.lower(), act_type)
    query = f"{act_name} {number}/{year}"

    result = await search(session, query, category="legislatie", max_results=5)
    for r in result.get("results", []):
        if str(number) in r["title"] and str(year) in r["title"]:
            title_lower = r["title"].lower()
            status = "in_vigoare"
            if "abrogat" in title_lower:
                status = "abrogat"
            elif "modificat" in title_lower or "republicat" in title_lower:
                status = "modificat"
            return {
                "found": True,
                "title": r["title"],
                "url": r["url"],
                "status": status,
                "source": "lege6.ro",
            }

    return {"found": False, "source": "lege6.ro"}
