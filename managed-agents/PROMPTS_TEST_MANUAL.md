# Prompts Test Managed Agents pentru Rulare Manuala in Claude Desktop Chat

Pana cand activezi Managed Agents prin API (necesita acces beta), poti rula manual prompt-urile in Claude Desktop chat plus salvezi rezultatele.

## Prompt 1, CCR Watcher manual

Copy-paste in Claude Desktop chat, ideal proiect „Cercetare doctorat":

```
Sarcina, monitorizare manuala CCR pentru deciziile recente.

Astazi este [SCRIE DATA].

Acceseaza https://www.ccr.ro/decizii-recente/ prin tool-ul de fetching disponibil.

Identifica deciziile publicate sau anuntate in ultimele 7 zile.

Pentru fiecare decizie, evalueaza relevanta contra topicurilor:
- securitate cibernetica, art. 53, art. 26, art. 28, art. 30
- restrangerea exercitiului drepturilor
- calitatea legii, previzibilitate
- stari exceptionale, stare de urgenta
- interceptari, DNSC
- Legea 58/2023, OUG 155/2024

Pentru fiecare decizie relevanta, extrage:
- Numar plus an
- Subiect
- Sesizant
- Dispozitiv (admis, respins)
- M.Of. plus data
- Articol constitutional principal
- Doctrinari sau jurisprudenta CEDO si CJUE invocate

Genereaza tabel rezumativ plus comentariu doctoral scurt pentru fiecare.

Foloseste MCP-ul legal-verificator-ro pentru cross-check daca este nevoie.
Marcheaza [VERIFICARE NECESARA] daca o informatie pare plauzibila dar nu apare confirmata.
```

## Prompt 2, M.Of. Watcher manual

```
Sarcina, monitorizare manuala Monitorul Oficial pentru acte normative noi.

Astazi este [DATA].

Acceseaza monitoruloficial.ro sau legislatie.just.ro prin tool-ul de fetching.

Identifica actele publicate in ultimele 7 zile in domeniile:
- Energie (ANRE, Transgaz, Transelectrica, ELCEN, regenerabile, PNRR energie)
- Securitate cibernetica (DNSC, NIS2, GDPR, infrastructura critica)
- Constitutional (CCR, drepturi fundamentale, art. 53)
- Administrativ (Codul administrativ, achizitii publice)

Pentru fiecare act relevant, extrage:
- Tip (Lege, OUG, HG, Ordin)
- Numar plus an
- Titlu complet
- M.Of. nr plus data
- Initiator
- Sector atins
- Articolele cheie
- Acte abrogate sau modificate
- Probabilitate sesizare CCR

Genereaza raport rezumativ cu tabel plus comentariu juridic per act.

Foloseste MCP-urile legal-verificator-ro plus eurlex pentru cross-check.
```

## Prompt 3, HUDOC Watcher manual

```
Sarcina, monitorizare manuala HUDOC pentru hotarari CEDO recente.

Astazi este [DATA].

Acceseaza hudoc.echr.coe.int prin MCP mcp__hudoc__hudoc_search_cases cu:
- date_from = [DATA - 14 zile]
- date_to = [DATA]
- importance = 1 (Key cases)

Filtreaza dupa articolele:
- art. 8 (viata privata)
- art. 10 (libertatea de exprimare)
- art. 6 (drept la un proces echitabil)
- art. 14 (interdictia discriminarii)
- Protocol 12

State prioritare: Romania, UK, Germania, Franta, Cehia.

Topicuri prioritare:
- mass surveillance, metadata retention
- cybersecurity, AI surveillance
- national security exception
- interception of communications
- data protection, GDPR
- law quality test, foreseeability

Pentru fiecare hotarare relevanta, extrage:
- Cauza X c. Y
- Cererea nr. NNNNN/AA
- Data hotararii
- Articol principal in discutie
- Subiect plus context faptic (3 propozitii)
- Ratiunea principala
- Standardul aplicat
- Relevanta pentru teza Popa (restrangerea exercitiului drepturilor fundamentale pentru ratiuni de securitate cibernetica)
- URL HUDOC

Genereaza raport saptamanal cu tabel plus comentariu doctoral.
Aplica anti-hallucination strict, verifica fiecare cerere nr prin MCP.
```

## Cum salvezi rezultatele

Dupa fiecare rulare in Claude Desktop chat, copy-paste rezultatul in:

```
C:/Users/Adrian Vasilescu/managed-agents/output/[ccr|mof|hudoc]-watch/YYYY-MM-DD.md
```

Cu timpul, vei avea o arhiva valoroasa de jurisprudenta plus legislatie de referinta pentru cercetare doctorala plus consultanta profesionala.

## Cum integrezi cu Cowork Project Knowledge

Dupa 7-14 zile de rulari manuale, ai 20 plus rapoarte salvate. Mutele in folderul Cowork sincronizat:

```
C:/Users/Adrian Vasilescu/OneDrive/Documents/Claude/Projects/Cercetare-doctorat/jurisprudenta-recenta/
```

Cowork le indexeaza automat plus orice conversatie din Project Cercetare doctorat are acces la jurisprudenta zilnica plus saptamanala actualizata.

## Frecventa recomandata pentru rulare manuala

- CCR Watcher, dupa fiecare sedinta CCR publicata (saptamanal, marti)
- M.Of. Watcher, dupa fiecare publicatie M.Of. relevanta (daily check, scan rapid 5 minute)
- HUDOC Watcher, saptamanal, lunea dimineata

Total efort estimat: 30-45 minute saptamanal pentru toate 3.

Cand obtii acces oficial Managed Agents, transferi prompt-urile in workflows GitHub Actions plus automatizezi complet.
