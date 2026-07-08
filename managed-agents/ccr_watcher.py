#!/usr/bin/env python3
"""
Managed Agent CCR-watcher.

Monitorizeaza ccr.ro zilnic pentru decizii noi pe domeniile de interes ale
utilizatorului (securitate cibernetica, drepturi fundamentale, art. 53,
art. 26, art. 28, art. 30, restrangerea exercitiului drepturilor).

Ruleaza ca Anthropic Managed Agent, deci nu necesita laptop deschis.
Costul: aproximativ 0.08 USD per ora sesiune plus tokens consumati.

Pentru a-l porni manual:
  python ccr_watcher.py

Pentru schedule recurent (Anthropic Managed Agents API):
  Pasul 1, salveaza scriptul pe Anthropic Files API
  Pasul 2, creeaza Managed Agent care invoca acest scenario
  Pasul 3, configureaza cron extern (GitHub Actions, Cloudflare Cron)
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG = {
    "watched_keywords": [
        "securitate cibernetica",
        "art. 53",
        "art. 26",
        "art. 28",
        "art. 30",
        "restrangerea exercitiului",
        "drepturi fundamentale",
        "calitatea legii",
        "previzibilitate",
        "viata privata",
        "secretul corespondentei",
        "libertatea de exprimare",
        "stari exceptionale",
        "stare de urgenta",
        "interceptari",
        "DNSC",
        "Legea 58/2023",
        "OUG 155/2024",
    ],
    "ccr_url_patterns": [
        "https://www.ccr.ro/decizii-recente/",
        "https://www.ccr.ro/decizia-{N}/",
        "https://www.ccr.ro/wp-content/uploads/{YYYY}/{MM}/",
    ],
    "output_path": "output/ccr-watch",
    "user_email": "popa.andrei.nicolae@gmail.com",
}


def daily_scan_prompt() -> str:
    """Genereaza promptul pe care Managed Agent il primeste zilnic."""
    keywords_str = "\n- ".join(CONFIG["watched_keywords"])
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    return f"""Sarcina, monitorizare zilnica CCR pentru Andrei Nicolae Popa.

Astazi este {today}. Verifica deciziile CCR publicate intre {yesterday} si {today}.

Pasi obligatorii:

1. Acceseaza https://www.ccr.ro/decizii-recente/ prin tool-ul web_fetch.
2. Identifica deciziile publicate sau anuntate intre {yesterday} si {today}.
3. Pentru fiecare decizie noua, fetch URL-ul detaliilor.
4. Verifica daca decizia atinge unul din topicurile de interes:
- {keywords_str}

5. Pentru fiecare decizie relevanta, extrage:
- Numar decizie plus an
- Subiect (din titlu plus rezumat)
- Sesizant (cine a sesizat CCR)
- Dispozitiv (admis, respins, respins ca devenit fara obiect)
- Data publicare in Monitorul Oficial daca este mentionata
- Articolul constitutional principal in discutie
- Doctrinari sau jurisprudenta CEDO/CJUE invocate

6. Salveaza raport zilnic in:
   {CONFIG["output_path"]}/{today}.md

7. Trimite sumar email la {CONFIG["user_email"]} daca exista cel putin
   1 decizie relevanta.

Daca nu exista decizii relevante in interval, marcheaza fisierul cu
"Niciuna relevanta" si nu trimite email.

Foloseste tool-urile MCP disponibile pentru verificare (legal-verificator-ro
pentru cross-check, eurlex daca apar referinte UE).

Aplica anti-hallucination strict, marcheaza [NEVERIFICAT] daca o informatie
pare plauzibila dar nu apare pe ccr.ro.
"""


def main() -> int:
    output_dir = Path(CONFIG["output_path"])
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    prompt_file = output_dir / f"prompt-{today}.txt"
    prompt_file.write_text(daily_scan_prompt(), encoding="utf-8")

    print(f"Prompt generat: {prompt_file}")
    print("Pentru a invoca Managed Agent cu acest prompt, foloseste Anthropic API:")
    print("  POST /v1/managed-agents/runs")
    print(f"  body: {{\"prompt\": <continut din {prompt_file}>, \"model\": \"claude-opus-4-8\"}}")
    print("")
    print("Sau ruleaza local pentru test:")
    print(f"  claude --prompt-file {prompt_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
