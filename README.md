# Claude Ecosystem, Andrei Nicolae Popa

Ecosistem complet Claude Desktop plus Cowork plus Code pentru juristi, doctoranzi,
consilieri juridici romanesti. Sistem integrat anti-AI tone, anti-halucinare,
fact-check, plus MCP-uri specializate pentru research juridic.

Construit pe baza analizei halucinatiilor reale documentate in rapoarte
profesionale generate prin LLM, calibrat pentru limba romana academica
(DOOM 3, format citare Scoala Doctorala UB Drept).

Versiune 1.4.0, iunie 2026. Open-source MIT.

## Continut monorepo

### MCP servers, 13 active

Anti-AI tone si anti-halucinare:

- **anti-ai-tone**, 7 tools (check_ai_tone, fact_check_document, compare_versions,
  quick_score, suggest_fixes, check_file, get_skill_rules)
- **cognee-legal**, 4 tools pentru memorie cross-session (cognify, search, prune,
  get_datasets)

Research juridic (in mcp-servers/legal-research):

- **legal-verificator-ro**, decizii CCR plus legislatie RO plus lege5.ro (9 tools)
- **eurlex**, legislatie UE plus CJUE via SPARQL (4 tools)
- **hudoc**, jurisprudenta CEDO (4 tools)
- **zotero**, gestiune bibliografica (6 tools)
- **doctrine-verifier**, verificare doctrina

Research academic:

- **semantic-scholar**, cautare articole academice plus citari (6 tools)
- **academic-search**, baza date academica plus full-text

Persona diplomatica:

- **irina-mihu-persona**, persona diplomat MAE (Secretar III, DAGFIJ, Departamentul
  UE, mandat Ambasada Romaniei in Israel), 7 tools plus 5 prompts plus 5 resources

### Skills, 27 active

Anti-AI tone:

- anti-ai-tone v2.1 (skill principal cu 25 reguli plus lista neagra 200 plus
  termeni RO/EN, sintetizat din 15 surse 2024-2026)

Anti-halucinare:

- anti-hallucination-document, protocol universal
- anti-hallucination-energetic, sectorial energie cu cifre baseline
- zero-hallucination-citations
- zero-legal-hallucination

Juridice specializate romanesti:

- constitutional-law-ro, drept constitutional roman, test art. 53
- cyber-law-ro, drept securitate cibernetica, Legea 58/2023, OUG 155/2024, NIS2
- ub-drept-citation, format citare Scoala Doctorala UB Drept
- analiza-juridica-critica, metodologie doctorala
- verificare-legislatie, validare acte normative
- format-bibliografie-doctorat-ub
- brief-legal, legal-response, legal-risk-assessment
- compliance-check, review-contract

Infrastructura:

- mcp-fallback-strategy
- research-context-persist
- ccr-url-patterns
- web-fetch-deadlock-prevention
- quality-gate-orchestrator

### Subagents, 4 specializati

- anti-ai-tone-reviewer, audit stilistic read-only
- juridic-style-reviewer, audit terminologie plus format UB Drept
- fact-checker-document, fact-check universal cu raport structurat
- fact-checker-energetic, fact-check sectorial energie cu cifre baseline

### Scripts, 8 utile

- detect_ai_tone.py, detector 25 plus pattern-uri AI tone
- ai_tone_hook.py, PostToolUse anti-AI tone
- fact_check_hook.py, PostToolUse fact-check
- prompt_injection_hook.py, UserPromptSubmit reminder
- session_end_hook.py, Stop audit final sesiune
- api_helpers.py, helper Anthropic API (caching, Files, Citations)
- cost_optimization_setup.py, estimare economii prompt caching
- status_line.py, status line custom cu scor anti-AI

### Cowork templates, 5 (Project Instructions)

- PROJECT_INSTRUCTIONS_UNIVERSAL.md, orice document factual
- PROJECT_INSTRUCTIONS_ENERGETIC.md, sector energetic cu cifre baseline
- PROJECT_INSTRUCTIONS_JURIDIC_DOCTORAT.md, cercetare doctorala UB Drept
- MAPARE_PROIECTE_ACTIVE.md, lista proiecte cu template recomandat
- README_UTILIZARE.md, ghid scenarii concrete

### Output styles, 2

- juridic-doctoral.md, stil text juridic academic doctoral
- policy-paper-romanesc.md, stil consultanta strategica romaneasca

### Managed agents, 3

- ccr_watcher.py, monitorizare zilnica ccr.ro
- mof_watcher.py, monitorizare zilnica Monitorul Oficial
- hudoc_watcher.py, monitorizare saptamanala hudoc.echr.coe.int

Plus 3 GitHub Actions workflows in .github/workflows/ pentru rulare cron automata.

## Cerinte sistem

- Windows 10/11, macOS 12 plus, sau Linux modern
- Python 3.10 plus
- Node 18 plus (pentru MCP-urile TypeScript: eurlex, hudoc, zotero)
- Claude Desktop instalat
- Claude Code optional
- Abonament Claude Pro, Max, Team sau Enterprise
- Microsoft Word optional (pentru integrare Claude for Word add-in)

## Instalare rapida

```bash
git clone https://github.com/popaandreinicolae-sudo/claude-ecosystem-popa
cd claude-ecosystem-popa
```

### MCP-uri Python

```bash
pip install -r requirements.txt
```

### MCP-uri TypeScript

```bash
cd mcp-servers/legal-research/eurlex && npm install && npm run build
cd ../hudoc && npm install && npm run build
cd ../zotero && npm install && npm run build
```

### Configurare credentiale

```bash
cd mcp-servers/legal-research
cp .env.example .env
# Editeaza .env cu propriile tale credentiale lege5, zotero
```

### Inregistrare MCP-uri in Claude Desktop

Editeaza `%APPDATA%\Claude\claude_desktop_config.json` plus adauga MCP-urile dorite.
Vezi `cowork-templates/README_UTILIZARE.md` pentru exemple complete.

## Componente single-click

Pentru utilizare rapida fara configurare manuala, foloseste pachetul MCPB:

- `mcp-servers/anti-ai-tone/anti-ai-tone-v1.1.0.mcpb`, dublu-click in Windows
  pentru instalare single-click in Claude Desktop

## Verificare functionare

Dupa instalare, in Claude Desktop chat:

```
Foloseste tool-ul anti-ai-tone fact_check_document pe acest text:
"RADET continua sa opereze in Bucuresti. PIU are 44 angajati cu Trust Fund 3 milioane EUR."
```

Claude raspunde cu detectie RADET depasit (CMTEB din 1 dec 2019), Trust Fund inventat.

## Distribuie colegilor

Pentru colegi doctoranzi sau profesionisti, trimite link-ul acestui repo:

https://github.com/popaandreinicolae-sudo/claude-ecosystem-popa

Sau direct fisierul anti-ai-tone-v1.1.0.mcpb pentru instalare single-click.

## Suport

Pentru bug-uri, intrebari, sugestii noi:

- GitHub Issues: https://github.com/popaandreinicolae-sudo/claude-ecosystem-popa/issues
- Email: popa.andrei.nicolae@gmail.com

## Surse informationale

Sistemul este construit pe sinteza a 15 surse internationale 2024-2026 privind
detectia textului AI plus halucinatii LLM, plus normele lingvistice oficiale
ale limbii romane (DOOM 3, Gramatica Academiei Romane), plus standardele Scolii
Doctorale Facultatea de Drept Universitatea din Bucuresti pentru format citare
juridica.

Lista completa surse in: skills/anti-ai-tone.md (sectiunea SURSE SINTETIZATE).

## Licenta

MIT, copiere libera cu pastrare atribuire.
