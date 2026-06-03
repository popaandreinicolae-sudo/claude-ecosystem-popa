"""Client for lege5.ro — authenticated access to legislation, jurisprudence, doctrine."""

import asyncio
import logging
import re
from typing import Optional, List

from bs4 import BeautifulSoup

from auth import Lege5Session, LEGE5_BASE

logger = logging.getLogger("legal-verificator.lege5")

_semaphore = asyncio.Semaphore(3)  # max 3 req/s


async def _rate_limited(session: Lege5Session, method: str, url: str, **kwargs):
    async with _semaphore:
        await asyncio.sleep(0.33)  # ~3 req/s
        if method == "get":
            return await session.get(url, **kwargs)
        return await session.post(url, **kwargs)


async def search(session: Lege5Session, query: str,
                 category: Optional[str] = None, max_results: int = 10) -> dict:
    """Full-text search on lege5.ro.

    Uses an unauthenticated request for search (simpler HTML with inline results),
    then the authenticated session for document fetching.
    """
    # Map category to section type ID
    section_map = {
        "legislatie": "1",
        "jurisprudenta": "2",
        "doctrina": "6",
        "ccr": "98",
    }

    params = {"Search_Term": query, "Rec": str(max_results)}
    if category and category in section_map:
        params["Search_SectionTypeId"] = section_map[category]

    # Use a fresh unauthenticated client for search — the free/unauth page
    # returns server-rendered HTML results, while the authenticated /App/Search
    # page loads results via JavaScript which httpx cannot execute.
    import httpx
    async with httpx.AsyncClient(follow_redirects=False, timeout=30.0) as anon_client:
        url = f"{LEGE5_BASE}/Search"
        resp = await anon_client.get(url, params=params, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # Parse search results from any result container
    for item in soup.find_all("div", class_=re.compile(r"search-result|result-item|rezResult")):
        title_el = item.find("a", class_=re.compile(r"result-title|titlu"))
        if not title_el:
            title_el = item.find("a")
        if not title_el:
            continue

        title = title_el.get_text(strip=True)
        href = title_el.get("href", "")
        if href and not href.startswith("http"):
            href = f"{LEGE5_BASE}{href}"

        snippet_el = item.find("div", class_=re.compile(r"snippet|preview|continut"))
        snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""

        results.append({
            "title": title,
            "snippet": snippet,
            "url": href,
            "category": category or "all",
        })

        if len(results) >= max_results:
            break

    # Fallback: look for any links with legal content
    if not results:
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text(strip=True)
            if text and len(text) > 15 and ("/Gratuit/" in href or "/App/" in href):
                if href and not href.startswith("http"):
                    href = f"{LEGE5_BASE}{href}"
                results.append({
                    "title": text,
                    "snippet": "",
                    "url": href,
                    "category": category or "all",
                })
                if len(results) >= max_results:
                    break

    return {"results": results, "total": len(results)}


async def fetch_document(session: Lege5Session, url: str) -> dict:
    """Fetch full text of a document from lege5.ro."""
    await session.ensure_authenticated()

    resp = await _rate_limited(session, "get", url)
    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract title
    title = ""
    title_el = soup.find("h1") or soup.find("title")
    if title_el:
        title = title_el.get_text(strip=True)

    # Extract main content
    content = (
        soup.find("div", class_=re.compile(r"document-content|act-content|content-body")) or
        soup.find("div", id=re.compile(r"content|document|act")) or
        soup.find("article") or
        soup.find("main")
    )

    if content:
        for tag in content.find_all(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        text = content.get_text(separator="\n", strip=True)
    else:
        # Fallback: get all text from body
        body = soup.find("body")
        if body:
            for tag in body.find_all(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            text = body.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

    # Extract metadata
    metadata = {}
    for meta in soup.find_all("meta"):
        name = meta.get("name", "") or meta.get("property", "")
        if name and meta.get("content"):
            metadata[name] = meta["content"]

    return {
        "text": text,
        "title": title,
        "metadata": metadata,
    }


async def search_ccr_decision(session: Lege5Session, number: int, year: int) -> dict:
    """Search for a CCR decision on lege5.ro."""
    query = f"Decizia {number}/{year} Curtea Constitutionala"
    result = await search(session, query, category="ccr", max_results=5)

    for r in result.get("results", []):
        if str(number) in r["title"] and str(year) in r["title"]:
            return {
                "found": True,
                "title": r["title"],
                "url": r["url"],
                "source": "lege5.ro",
            }

    # Try broader search
    result = await search(session, f"Decizia {number} {year} CCR", max_results=5)
    for r in result.get("results", []):
        if str(number) in r["title"]:
            return {
                "found": True,
                "title": r["title"],
                "url": r["url"],
                "source": "lege5.ro",
            }

    return {"found": False}


async def fetch_ccr_text(session: Lege5Session, number: int, year: int) -> dict:
    """Fetch full text of CCR decision from lege5.ro."""
    result = await search_ccr_decision(session, number, year)
    if not result.get("found"):
        return {
            "text": "",
            "source": "lege5.ro",
            "total_chars": 0,
            "truncated": False,
            "error": f"Decizia CCR nr. {number}/{year} nu a fost găsită pe lege5.ro.",
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
        "source": "lege5.ro",
        "total_chars": total_chars,
        "truncated": truncated,
    }
