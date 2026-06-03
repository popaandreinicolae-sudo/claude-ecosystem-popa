#!/usr/bin/env python3
"""
Managed Agent M.Of.-watcher.

Monitorizeaza Monitorul Oficial al Romaniei pentru acte normative noi
relevante pentru profilul utilizatorului (energie, securitate cibernetica,
drepturi fundamentale, administratie publica, achizitii publice).
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG = {
    "watched_sectors": {
        "energie": [
            "energie", "electricitate", "gaze naturale", "termoficare",
            "ANRE", "Transgaz", "Transelectrica", "ELCEN", "CMTEB",
            "regenerabile", "fotovoltaic", "eolian", "geotermal",
            "PNRR energie", "Fondul Modernizare", "ETS",
        ],
        "securitate_cibernetica": [
            "securitate cibernetica", "DNSC", "NIS2", "infrastructura critica",
            "atac cibernetic", "incident cibernetic", "cloud guvernamental",
            "date cu caracter personal", "GDPR",
        ],
        "constitutional": [
            "Curtea Constitutionala", "obiectie neconstitutionalitate",
            "exceptie neconstitutionalitate", "conflict juridic natura constitutionala",
            "art. 53", "restrangerea exercitiului", "drepturi fundamentale",
        ],
        "administrativ": [
            "Codul administrativ", "OUG 57/2019", "achizitii publice",
            "Legea 98/2016", "Legea 99/2016", "concesiuni",
        ],
    },
    "ignored_categories": [
        "ordine ministru aparare specifica",
        "decizii director general agentii regionale fara impact larg",
    ],
    "output_path": "C:/Users/Adrian Vasilescu/managed-agents/output/mof-watch",
    "user_email": "popa.andrei.nicolae@gmail.com",
}


def daily_scan_prompt() -> str:
    sectors_str = json.dumps(CONFIG["watched_sectors"], ensure_ascii=False, indent=2)
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    return f"""Sarcina, monitorizare zilnica Monitorul Oficial pentru Andrei Nicolae Popa.

Astazi este {today}. Verifica actele normative publicate intre {yesterday}
si {today} pe portalul Monitorului Oficial (legislatie.just.ro).

Pasi obligatori:

1. Acceseaza www.monitoruloficial.ro plus legislatie.just.ro via web_fetch.
2. Listeaza acte publicate in intervalul {yesterday} pana {today}.
3. Pentru fiecare act (lege, OUG, HG, ordin), evalueaza relevanta contra
sectoarelor monitorizate:
{sectors_str}

4. Pentru fiecare act relevant, extrage:
- Tip act (Lege, OUG, HG, Ordin)
- Numar si an
- Titlu complet
- Numar M.Of. de publicare plus data
- Initiator (Guvern, Parlament, minister)
- Sector monitorizat care a fost atins (energie, cibernetic, constitutional,
  administrativ)
- Articolele cele mai relevante pentru topicurile lui
- Acte normative abrogate sau modificate (incompatibilitati)

5. Pentru OUG-uri pe energie sau securitate cibernetica, verifica daca
exista probabilitate de sesizare CCR (criterii: ingerinta in drepturi
fundamentale, calitatea legii, depasire competenta).

6. Salveaza raport zilnic in:
   {CONFIG["output_path"]}/{today}.md

7. Trimite sumar email la {CONFIG["user_email"]} daca exista cel putin
1 act normativ critic pentru profilul utilizatorului.

Folosseste MCP-urile:
- legal-verificator-ro pentru cross-check
- eurlex pentru directive UE transpuse

Aplica anti-hallucination, marcheaza [NEVERIFICAT] daca informatia nu apare
pe surse oficiale.

NU semnala acte din categoria "ignored_categories" exceptand cazul cand au
impact secundar masiv.
"""


def main() -> int:
    output_dir = Path(CONFIG["output_path"])
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    prompt_file = output_dir / f"prompt-{today}.txt"
    prompt_file.write_text(daily_scan_prompt(), encoding="utf-8")

    print(f"Prompt generat: {prompt_file}")
    print("Pentru Managed Agent, foloseste:")
    print(f"  curl POST /v1/managed-agents/runs -d @{prompt_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
