#!/usr/bin/env python3
"""
MCP Server - Cautare academica in bazele de date universitare.

Permite Claude Code si Claude Desktop sa caute si sa descarce articole
din bazele de date accesibile prin contul institutional UB:
- Wiley Online Library
- ScienceDirect (Elsevier)
- SpringerLink
- EUR-Lex
- ProQuest

Autentificarea se face prin e-nformation.ro si romdidac.ro.
"""
import sys
import json
import asyncio
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from mcp.server.fastmcp import FastMCP

# Import modulele locale
from auth import AcademicSession, load_config
from search import search_all, download_pdf, DATABASE_MAP

# ============================================================
# MCP SERVER
# ============================================================

mcp = FastMCP("academic-search")

# Sesiune globala
_session: AcademicSession | None = None


def get_session() -> AcademicSession:
    global _session
    if _session is None:
        _session = AcademicSession()
        _session.start()
    return _session


# ============================================================
# TOOLS
# ============================================================

@mcp.tool()
def search_articles(
    query: str,
    databases: str = "wiley,sciencedirect,springer",
    max_results: int = 5,
) -> str:
    """
    Cauta articole academice in bazele de date universitare.

    Args:
        query: Termenul de cautare (ex: "cybersecurity fundamental rights EU")
        databases: Bazele de date, separate prin virgula. Disponibile: wiley, sciencedirect, springer, eurlex
        max_results: Numar maxim de rezultate per baza de date (default: 5)

    Returns:
        Lista de articole gasite cu titlu, autori, URL si sursa.
    """
    session = get_session()

    # Autentificare pe e-nformation daca e necesar
    db_list = [d.strip() for d in databases.split(",")]
    needs_auth = any(d in ("wiley", "sciencedirect", "springer") for d in db_list)

    if needs_auth:
        auth_ok = session.ensure_enformation()
        if not auth_ok:
            return json.dumps({
                "error": "Autentificare esuata pe e-nformation.ro. Verifica parola in config.json.",
                "action": "Seteaza parola corecta in academic_db_mcp/config.json"
            }, ensure_ascii=False, indent=2)

    page = session.new_page()
    try:
        results = search_all(page, query, db_list, max_results)

        # Formateaza rezultatele
        output = {"query": query, "databases": db_list, "results": {}}
        total = 0
        for db_name, items in results.items():
            output["results"][db_name] = items
            total += len([i for i in items if "error" not in i])
        output["total_results"] = total

        return json.dumps(output, ensure_ascii=False, indent=2)
    finally:
        page.close()


@mcp.tool()
def download_article(
    url: str,
    filename: str = "",
) -> str:
    """
    Descarca un articol PDF din baza de date academica.
    Foloseste sesiunea autentificata pentru a accesa articole paywalled.

    Args:
        url: URL-ul articolului (ex: https://onlinelibrary.wiley.com/doi/10.1111/jcms.13654)
        filename: Numele fisierului de salvare (ex: "Carrapico_2024.pdf"). Daca gol, se genereaza automat.

    Returns:
        Status download cu calea fisierului salvat.
    """
    session = get_session()
    config = load_config()

    # Autentificare
    if "wiley" in url or "sciencedirect" in url or "springer" in url:
        session.ensure_enformation()
    elif "cambridge" in url or "oxford" in url:
        session.ensure_romdidac()

    # Determina calea de salvare
    download_dir = Path(__file__).parent / config.get("download_dir", "../surse/doctrina_straina")
    download_dir = download_dir.resolve()

    if not filename:
        # Genereaza nume din URL
        parts = url.rstrip("/").split("/")
        doi_part = parts[-1] if parts else "article"
        filename = doi_part.replace("/", "_").replace(".", "_") + ".pdf"

    dest = download_dir / filename

    page = session.new_page()
    try:
        result = download_pdf(page, url, dest)
        return json.dumps(result, ensure_ascii=False, indent=2)
    finally:
        page.close()


@mcp.tool()
def list_databases() -> str:
    """
    Listeaza bazele de date academice disponibile si statusul autentificarii.

    Returns:
        Lista bazelor de date cu informatii despre acces.
    """
    session = get_session()

    databases = {
        "enformation": {
            "platform": "e-nformation.ro",
            "databases": [
                "Wiley Journals (wiley)",
                "ScienceDirect / Elsevier (sciencedirect)",
                "SpringerLink Journals (springer)",
                "ProQuest Central",
                "Web of Science",
                "Scopus",
                "Emerald Management",
                "Nature Journals",
            ],
            "authenticated": session._authenticated_enformation,
            "login_url": "https://www.e-nformation.ro/login",
        },
        "romdidac": {
            "platform": "accesmobil.romdidac.ro",
            "databases": [
                "EBSCO",
                "Cambridge University Press",
                "Oxford University Press",
            ],
            "authenticated": session._authenticated_romdidac,
            "login_url": "https://accesmobil.romdidac.ro/login",
        },
        "open_access": {
            "platform": "Acces liber (fara autentificare)",
            "databases": [
                "EUR-Lex (eurlex)",
                "HUDOC (CEDO)",
                "CURIA (CJUE)",
                "SSRN",
                "PMC / PubMed Central",
                "OAPEN (carti Open Access)",
            ],
            "authenticated": True,
        },
    }

    return json.dumps(databases, ensure_ascii=False, indent=2)


@mcp.tool()
def authenticate(platform: str = "enformation") -> str:
    """
    Autentificare manuala pe o platforma academica.

    Args:
        platform: "enformation" sau "romdidac"

    Returns:
        Status autentificare.
    """
    session = get_session()

    if platform == "enformation":
        ok = session.ensure_enformation()
        return json.dumps({
            "platform": "e-nformation.ro",
            "authenticated": ok,
            "message": "Autentificat cu succes!" if ok else "Autentificare esuata. Verifica config.json.",
        }, ensure_ascii=False)

    elif platform == "romdidac":
        ok = session.ensure_romdidac()
        return json.dumps({
            "platform": "romdidac.ro",
            "authenticated": ok,
            "message": "Autentificat cu succes!" if ok else "Autentificare esuata. Verifica config.json.",
        }, ensure_ascii=False)

    return json.dumps({"error": f"Platforma necunoscuta: {platform}"})


@mcp.tool()
def search_and_download(
    query: str,
    database: str = "wiley",
    download_first: bool = False,
) -> str:
    """
    Cauta un articol si optional il descarca.
    Util pentru a gasi si descarca rapid un articol specific.

    Args:
        query: Cautare (ex: "Carrapico Farrand cybersecurity regulatory mercantilism 2024")
        database: Baza de date: wiley, sciencedirect, springer
        download_first: Daca True, descarca automat primul rezultat

    Returns:
        Rezultatele cautarii si, daca download_first=True, statusul descarcarii.
    """
    session = get_session()

    if database in ("wiley", "sciencedirect", "springer"):
        session.ensure_enformation()

    page = session.new_page()
    try:
        search_fn = DATABASE_MAP.get(database)
        if not search_fn:
            return json.dumps({"error": f"Baza de date necunoscuta: {database}"})

        results = search_fn(page, query, max_results=5)

        output = {
            "query": query,
            "database": database,
            "results": results,
        }

        if download_first and results and "error" not in results[0]:
            first_url = results[0].get("url", "")
            if first_url:
                config = load_config()
                download_dir = Path(__file__).parent / config.get("download_dir", "../surse/doctrina_straina")
                download_dir = download_dir.resolve()

                # Genereaza nume fisier din titlu
                title = results[0].get("title", "article")
                safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:60]
                filename = f"{safe_title}.pdf"

                dl_result = download_pdf(page, first_url, download_dir / filename)
                output["download"] = dl_result

        return json.dumps(output, ensure_ascii=False, indent=2)
    finally:
        page.close()


# ============================================================
# CLEANUP la inchidere
# ============================================================

import atexit

def cleanup():
    global _session
    if _session:
        _session.stop()
        _session = None

atexit.register(cleanup)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
