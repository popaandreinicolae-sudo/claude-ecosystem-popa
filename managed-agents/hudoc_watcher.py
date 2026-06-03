#!/usr/bin/env python3
"""
Managed Agent HUDOC-watcher.

Monitorizeaza hudoc.echr.coe.int pentru hotarari CEDO noi pe art. 8
(viata privata), art. 10 (libertatea de exprimare), art. 6 (drept la un
proces echitabil), relevante pentru teza de doctorat plus practica
profesionala.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

CONFIG = {
    "watched_articles": ["art. 8", "art. 10", "art. 6", "art. 14", "Protocol 12"],
    "watched_topics": [
        "mass surveillance",
        "metadata retention",
        "cybersecurity",
        "national security exception",
        "interception of communications",
        "data protection",
        "AI surveillance",
        "facial recognition",
        "encryption",
        "law quality test",
    ],
    "priority_states": ["Romania", "United Kingdom", "Germany", "France", "Czechia"],
    "output_path": "C:/Users/Adrian Vasilescu/managed-agents/output/hudoc-watch",
    "user_email": "popa.andrei.nicolae@gmail.com",
}


def weekly_scan_prompt() -> str:
    topics_str = "\n- ".join(CONFIG["watched_topics"])
    articles_str = ", ".join(CONFIG["watched_articles"])
    states_str = ", ".join(CONFIG["priority_states"])
    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    return f"""Sarcina, monitorizare saptamanala HUDOC pentru Andrei Nicolae Popa.

Astazi este {today}. Verifica hotararile CEDO publicate intre {week_ago}
si {today} pe hudoc.echr.coe.int.

Articolele monitorizate prioritar: {articles_str}.
State prioritare: {states_str}.

Topicuri prioritare:
- {topics_str}

Pasi obligatorii:

1. Foloseste tool-ul MCP mcp__hudoc__hudoc_search_cases cu:
- date_from {week_ago}
- date_to {today}
- importance level 1 (Key cases)

2. Pentru fiecare hotarare relevanta, extrage:
- Cauza (X c. Y)
- Cererea nr. NNNNN/AA
- Data hotararii
- Articolul CEDO principal in discutie
- Subiect plus contextul faptic (3 propozitii)
- Ratiunea principala a deciziei
- Standardul aplicat (de exemplu testul de calitate al legii, testul de
  proporționalitate)
- Relevanta pentru tema doctorala securitate cibernetica plus drepturi
  fundamentale

3. Pentru hotararile cu impact constitutional pe drept roman, semnaleaza
explicit, plus invoca posibile sesizari ulterioare CCR.

4. Salveaza raport saptamanal in:
   {CONFIG["output_path"]}/{today}.md

5. Trimite email la {CONFIG["user_email"]} daca exista cel putin 1
hotarare cu impact direct pe teza doctorala.

Aplica anti-hallucination strict, valideaza fiecare cerere nr prin
MCP hudoc inainte de citare.

Format output MCMC pentru fiecare hotarare:

```
Cauza: X c. Y
Cererea nr.: NNNNN/AA
Data hotarare: YYYY-MM-DD
Articol CEDO: art. 8 (sau alte)
Subiect: ...
Ratiune: ...
Standard aplicat: ...
Relevanta teza Popa: ...
URL HUDOC: https://hudoc.echr.coe.int/eng?i=001-XXXXXX
```
"""


def main() -> int:
    output_dir = Path(CONFIG["output_path"])
    output_dir.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    prompt_file = output_dir / f"prompt-{today}.txt"
    prompt_file.write_text(weekly_scan_prompt(), encoding="utf-8")

    print(f"Prompt generat: {prompt_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
