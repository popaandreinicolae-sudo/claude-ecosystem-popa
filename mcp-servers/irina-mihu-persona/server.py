"""
irina-mihu-persona, server MCP (FastMCP) pentru Claude Cowork / Claude Desktop.

Persona diplomat MAE Irina Mihu. Expune trei straturi:
- prompts: activarea personei si modurile de lucru (controlate de utilizator);
- resources: profilul, canonul bibliografic, sursele primare, sabloanele;
- tools: regasire in cunoasterea proprie, surse, sabloane, ghidare de research.

Transport: stdio (subproces local). Fara chei API, fara retea proprie.
Cautarea pe web foloseste instrumentele mediului Claude Cowork.
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from mcp.server.fastmcp import FastMCP

BASE = Path(__file__).resolve().parent
PERSONA_DIR = BASE / "persona"
KNOW_DIR = BASE / "knowledge"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[lipsa fisier: {path.name}]"


def _split_frontmatter(text: str) -> tuple[str, str]:
    """Returneaza (frontmatter, corp) pentru un fisier markdown cu frontmatter YAML."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[1].strip(), parts[2].strip()
    return "", text


def _fold(s: str) -> str:
    """Normalizeaza pentru cautare: minuscule, fara diacritice."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


# Continut incarcat la pornire
PERSONA_RAW = _read(PERSONA_DIR / "irina-mihu.md")
FRONTMATTER, PERSONA_BODY = _split_frontmatter(PERSONA_RAW)
PROFIL = _read(KNOW_DIR / "profil.md")
CANON = _read(KNOW_DIR / "canon-bibliografic.md")
SURSE = _read(KNOW_DIR / "surse-primare.md")
SABLOANE = _read(KNOW_DIR / "sabloane.md")

KNOWLEDGE = {
    "profil": PROFIL,
    "canon-bibliografic": CANON,
    "surse-primare": SURSE,
    "sabloane": SABLOANE,
}

DOMENII = [
    "afaceri-ue", "energie-tranzitie", "diplomatie-economica-investitii",
    "drept-diplomatic-consular", "drept-international-public",
    "diplomatie-cibernetica", "observare-electorala-osce-odihr",
    "protocol-negociere-psihologie",
]

mcp = FastMCP("irina-mihu-persona")


# --------------------------------------------------------------------------
# PROMPTS (controlate de utilizator): activare si moduri de lucru
# --------------------------------------------------------------------------

@mcp.prompt(title="Activeaza persona Irina Mihu")
def activate_irina() -> str:
    """Activeaza persona completa Irina Mihu (diplomat MAE). Claude va prelua
    rolul, expertiza, registrul si standardele de acuratete si confidentialitate."""
    return (
        "Adopta integral si pana la noi instructiuni urmatoarea persona. "
        "Raspunde de acum ca Irina Mihu.\n\n" + PERSONA_BODY
    )


@mcp.prompt(title="Mod Centrala MAE")
def mode_centrala() -> str:
    """Comuta persona in modul de lucru Centrala MAE (material care urca pe
    verticala ierarhica, gata de avizat)."""
    return (
        PERSONA_BODY
        + "\n\nMOD ACTIV: Centrala MAE. Produci material gata de avizat, corect "
        "ca fond si impecabil ca forma, in stilul de casa al ministerului."
    )


@mcp.prompt(title="Mod serviciu exterior (Israel)")
def mode_exterior_israel() -> str:
    """Comuta persona in modul serviciu exterior, mandatul de la Ambasada Romaniei
    in Israel: informarea Centralei si propuneri de promovare si investitii."""
    return (
        PERSONA_BODY
        + "\n\nMOD ACTIV: serviciu exterior, Ambasada Romaniei in Statul Israel. "
        "Fiecare material informeaza Centrala si propune pasi operationali: "
        "promovarea intereselor Romaniei, atragerea de investitii catre Romania si "
        "sustinerea investitiilor romanesti in exterior. Valorifici suprapunerea cu "
        "tehnologia si securitatea cibernetica, energia si diplomatia economica."
    )


@mcp.prompt(title="Mod analiza juridica")
def mode_analiza_juridica() -> str:
    """Comuta persona pe analiza de drept (UE, international public, diplomatic),
    cu separarea stricta intre fapt stabilit si evaluare proprie."""
    return (
        PERSONA_BODY
        + "\n\nMOD ACTIV: analiza juridica. Ancorezi fiecare afirmatie in sursa "
        "(tratat, act UE, jurisprudenta). Separi explicit faptul stabilit de "
        "evaluare si de ipoteza. Marchezi [NEVERIFICAT] orice nu poti confirma."
    )


@mcp.prompt(title="Redacteaza un document diplomatic")
def draft(genre: str, subiect: str, limba: str = "ro") -> str:
    """Pregateste o sarcina de redactare in persona Irina Mihu, pe un gen anume.

    Args:
        genre: genul de document (ex.: nota-verbala, telegrama, fisa-dosar,
            elemente-de-limbaj, non-paper, raport-misiune, fisa-tara).
        subiect: subiectul concret al documentului.
        limba: limba de redactare (ro, en, it, fr).
    """
    sablon = _extract_template(genre) or "[gen necunoscut; foloseste structura standard]"
    return (
        PERSONA_BODY
        + f"\n\nSARCINA: redacteaza un document de tip '{genre}' despre: {subiect}. "
        f"Limba: {limba}. Foloseste structura de mai jos si livreaza text finit.\n\n"
        + sablon
    )


# --------------------------------------------------------------------------
# RESOURCES (controlate de aplicatie): cunoasterea
# --------------------------------------------------------------------------

@mcp.resource("persona://definitie", title="Definitia personei", mime_type="text/markdown")
def res_definitie() -> str:
    """Definitia completa a personei Irina Mihu (markdown cu frontmatter)."""
    return PERSONA_RAW


@mcp.resource("persona://profil", title="Profil profesional", mime_type="text/markdown")
def res_profil() -> str:
    """Profilul profesional: pozitie, portofoliu, formare, specializari, limbi."""
    return PROFIL


@mcp.resource("persona://canon", title="Canon bibliografic MAE", mime_type="text/markdown")
def res_canon() -> str:
    """Canonul bibliografic MAE pentru posturi diplomatice si consulare."""
    return CANON


@mcp.resource("persona://surse", title="Surse primare", mime_type="text/markdown")
def res_surse() -> str:
    """Instrumente-cheie cu reper de citare (Viena, TUE, TFUE, CEDO, NATO etc.)."""
    return SURSE


@mcp.resource("persona://sabloane", title="Sabloane documente", mime_type="text/markdown")
def res_sabloane() -> str:
    """Sabloane pentru genurile de documente diplomatice."""
    return SABLOANE


# --------------------------------------------------------------------------
# TOOLS (controlate de model): regasire si ghidare
# --------------------------------------------------------------------------

def _extract_template(genre: str) -> str | None:
    """Extrage blocul de sablon marcat cu [genre] din sabloane.md."""
    tag = genre.strip().lower()
    pattern = re.compile(
        r"^##\s*\[" + re.escape(tag) + r"\].*?(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pattern.search(SABLOANE)
    return m.group(0).strip() if m else None


@mcp.tool(title="Profilul personei")
def get_persona_profile() -> str:
    """Returneaza profilul profesional al Irinei Mihu (fara date personale de contact)."""
    return PROFIL


@mcp.tool(title="Listeaza domeniile de expertiza")
def list_domenii() -> list[str]:
    """Listeaza domeniile de expertiza ale personei."""
    return DOMENII


@mcp.tool(title="Listeaza sabloanele")
def list_templates() -> list[str]:
    """Listeaza genurile de documente pentru care exista sablon."""
    return re.findall(r"^##\s*\[([a-z\-]+)\]", SABLOANE, re.MULTILINE)


@mcp.tool(title="Obtine un sablon de document")
def get_template(genre: str) -> str:
    """Returneaza sablonul pentru un gen de document diplomatic.

    Args:
        genre: eticheta genului (ex.: nota-verbala, telegrama, fisa-dosar,
            elemente-de-limbaj, non-paper, raport-misiune, fisa-tara).
    """
    t = _extract_template(genre)
    if t:
        return t
    disponibile = ", ".join(re.findall(r"^##\s*\[([a-z\-]+)\]", SABLOANE, re.MULTILINE))
    return f"[gen necunoscut: '{genre}'] Genuri disponibile: {disponibile}"


@mcp.tool(title="Obtine o sursa canonica")
def get_source(name: str) -> str:
    """Cauta in sursele primare si in canon o sursa (tratat, lege, autor) si
    returneaza paragrafele relevante, cu reper de citare.

    Args:
        name: numele sau cuvantul-cheie al sursei (ex.: 'Viena 1961', 'TFUE',
            'Miga-Besteliu', 'NATO', 'Legea 269').
    """
    q = _fold(name)
    hits: list[str] = []
    for doc in (SURSE, CANON):
        for para in re.split(r"\n\s*\n", doc):
            if q in _fold(para):
                hits.append(para.strip())
    if not hits:
        return f"[fara potrivire pentru '{name}' in surse/canon]"
    return "\n\n---\n\n".join(dict.fromkeys(hits))


@mcp.tool(title="Cauta in cunoasterea personei")
def search_knowledge(query: str, max_results: int = 5) -> str:
    """Cauta in toata baza de cunoastere a personei (profil, canon, surse,
    sabloane) si returneaza paragrafele cele mai relevante, cu sursa.

    Args:
        query: termenii de cautare (insensibil la diacritice si la majuscule).
        max_results: numarul maxim de paragrafe returnate.
    """
    terms = [t for t in _fold(query).split() if t]
    if not terms:
        return "[interogare goala]"
    scored: list[tuple[int, str, str]] = []
    for label, doc in KNOWLEDGE.items():
        for para in re.split(r"\n\s*\n", doc):
            folded = _fold(para)
            score = sum(folded.count(t) for t in terms)
            if score:
                scored.append((score, label, para.strip()))
    if not scored:
        return f"[fara rezultate pentru '{query}']"
    scored.sort(key=lambda x: x[0], reverse=True)
    out = [f"[{label}] {para}" for _, label, para in scored[:max_results]]
    return "\n\n---\n\n".join(out)


@mcp.tool(title="Ghidare de research pe domeniile personei")
def research_guidance(topic: str) -> str:
    """Returneaza cum ar aborda Irina Mihu cercetarea unui subiect: domeniile
    relevante, sursele canonice de pornire si interogari de cautare sugerate
    (de rulat cu instrumentele de web ale mediului Claude Cowork).

    Args:
        topic: subiectul de cercetat.
    """
    folded = _fold(topic)
    mapa = {
        "afaceri-ue": ["ue", "coreper", "ecofin", "cfm", "coeziune", "piata interna",
                       "dsa", "dma", "ai act", "consiliu", "buget"],
        "energie-tranzitie": ["energie", "gaz", "brua", "neptun", "climatic",
                              "regenerabil", "marea neagra"],
        "diplomatie-economica-investitii": ["investit", "economic", "comert",
                                            "intelligence economic", "fdi"],
        "drept-diplomatic-consular": ["viena", "consular", "diplomatic", "imunitat",
                                     "misiune speciala"],
        "drept-international-public": ["international", "tratat", "cedo", "drepturile omului"],
        "diplomatie-cibernetica": ["cibernetic", "cyber", "tic", "unoda"],
        "observare-electorala-osce-odihr": ["osce", "odihr", "alegeri", "electoral"],
        "protocol-negociere-psihologie": ["protocol", "ceremonial", "negociere",
                                         "psiholog"],
    }
    relevante = [d for d, kws in mapa.items() if any(k in folded for k in kws)]
    if not relevante:
        relevante = ["(subiect general; raporteaza-l la cel mai apropiat domeniu)"]
    surse = get_source(topic)
    surse_txt = "" if surse.startswith("[fara") else f"\n\nSURSE DE PORNIRE:\n{surse}"
    interogari = [
        f"{topic} site:europa.eu",
        f"{topic} Romania pozitie oficiala",
        f"{topic} 2026 analiza",
    ]
    return (
        f"SUBIECT: {topic}\n"
        f"DOMENII RELEVANTE: {', '.join(relevante)}\n"
        "ABORDARE: identifica miza si interesul national, cadrul juridic aplicabil, "
        "pozitiile actorilor (state membre, institutii UE, parteneri bilaterali), "
        "apoi formuleaza concluzii si propuneri.\n"
        f"INTEROGARI SUGERATE:\n- " + "\n- ".join(interogari)
        + surse_txt
    )


if __name__ == "__main__":
    mcp.run()
