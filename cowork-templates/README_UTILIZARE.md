# Sistem Integrat Anti-Halucinare, Ghid Utilizare

Acest sistem leaga 8 componente care lucreaza impreuna pentru a preveni halucinatiile in documente profesionale generate prin Claude (Cowork, Chat, Code).

Generat dupa analiza halucinatiilor reale din raportul DIAGNOZA+Proiecte_ENERGIE_BUCURESTI_ILFOV_BM_FINAL_FIX_v11.docx comparat cu versiunea corectata 31.05.

## Cele 8 componente create

### 1. Skill `anti-hallucination-document`

Locatie: `~/.claude/skills/anti-hallucination-document/`
Continut: SKILL.md (12 reguli pozitive) + references/ (checklist, marcaje, prioritate surse) + scripts/ (compare_docx_versions.py)
Activare: automat in Claude Code la documente peste 500 cuvinte cu cifre, sume, denumiri institutionale

### 2. Skill `anti-hallucination-energetic`

Locatie: `~/.claude/skills/anti-hallucination-energetic/SKILL.md`
Continut: 10 reguli sectoriale (denumiri institutionale 2024-2026, cifre baseline SACET, coduri SIDU verificate, pattern-uri halucinare clasice)
Activare: automat la documente despre sectorul energetic romanesc

### 3. Subagent `fact-checker-document`

Locatie: `~/.claude/agents/fact-checker-document.md`
Invocare: „fact-check document", „verifica halucinari", „audit raport"
Output: raport structurat cu probleme CRITICE, MAJORE, MINORE plus plan corectii

### 4. Subagent `fact-checker-energetic`

Locatie: `~/.claude/agents/fact-checker-energetic.md`
Invocare: „fact-check energetic", „audit raport energie", „verifica cifre SACET"
Output: raport sectorial cu denumiri, cifre, coduri SIDU, volume programe

### 5. Script `compare_docx_versions.py`

Locatie: `~/.claude/skills/anti-hallucination-document/scripts/compare_docx_versions.py`
Invocare:
```bash
python "C:/Users/Adrian Vasilescu/.claude/skills/anti-hallucination-document/scripts/compare_docx_versions.py" version_a.docx version_b.docx --output raport.md
```
Output: raport markdown cu diferente (cifre, capitole, citari, paragrafe unice)

### 6. MCP `anti-ai-tone` extins

Locatie: `~/anti-ai-tone-mcp/server.py`
Tool-uri noi:
- `fact_check_document(text, sector)`, detecteaza halucinari fara compare cu sursa primara
- `compare_versions(version_a_path, version_b_path)`, comparativa doua docx
Invocare directa in Claude Cowork prin Tool use.

### 7. Hook PostToolUse `fact_check_hook.py`

Locatie: `~/.claude/scripts/fact_check_hook.py`
Inregistrat in: `~/.claude/settings.json`, sectiunea hooks.PostToolUse
Activare: automat la Write/Edit/MultiEdit pe .md/.txt/.docx peste 500 cuvinte
Output: warning in stderr cu probleme critice plus majore detectate

### 8. Project Instructions templates Cowork

Locatie: `~/.claude/cowork-templates/`
- `PROJECT_INSTRUCTIONS_UNIVERSAL.md`, pentru orice document factual
- `PROJECT_INSTRUCTIONS_ENERGETIC.md`, pentru rapoarte energetice
- `PROJECT_INSTRUCTIONS_JURIDIC_DOCTORAT.md`, pentru cercetare doctorala

Aplicare: copiezi continutul in Claude.ai Cowork, Projects, Settings, Custom Instructions per project.

## Cum utilizezi sistemul, scenarii concrete

### Scenariu A, raport nou energetic in Cowork

1. Deschizi Claude Cowork si creezi Project nou „Energie regiune X"
2. Upload PDF-uri primare in Project Knowledge (Strategia Energetica, PNIESC, SIDU, planuri operatori)
3. Copy-paste continutul `PROJECT_INSTRUCTIONS_ENERGETIC.md` in Project Settings, Custom Instructions
4. Activezi Citations API in Beta features
5. Generezi raportul, primesti citatii inline la fiecare afirmatie factuala
6. Exportezi DOCX final
7. In Claude Code, rulezi compare_docx_versions cu versiuni anterioare daca exista
8. Invoci subagent fact-checker-energetic pentru audit independent

### Scenariu B, articol juridic pentru juridice.ro sau revista doctorala

1. Deschizi Claude Cowork si creezi Project „Articol decizia CCR 70/2023"
2. Upload PDF Decizia CCR 70/2023, tratate doctrinare relevante, hotarari CEDO citate
3. Copy-paste `PROJECT_INSTRUCTIONS_JURIDIC_DOCTORAT.md` in Custom Instructions
4. Activezi Citations API
5. Generezi articolul, modelul foloseste DOAR sursele uploadate
6. Verificare prin MCP juridice (legal-verificator-ro, eurlex, hudoc)
7. Audit prin subagent fact-checker-document plus juridic-style-reviewer
8. Livrare DOCX final

### Scenariu C, fact-check pe document existent primit de la colaboratori

1. Salvezi documentul DOCX in `C:/Users/Adrian Vasilescu/Downloads/TEST/` sau similar
2. In Claude Code, rulezi:
```bash
python "C:/Users/Adrian Vasilescu/.claude/skills/anti-hallucination-document/scripts/compare_docx_versions.py" \
  "document_primit.docx" \
  "document_referinta.docx" \
  --output "raport_comparativ.md"
```
3. Invoci subagent fact-checker-energetic sau fact-checker-document
4. Primesti raport structurat cu probleme detectate

### Scenariu D, livrare iterativa rapoarte cu fact-check continuu

1. Versionezi documentul: v1, v2, v3, ... vN
2. Dupa fiecare iteratie, rulezi compare_docx_versions.py pentru a vedea diferentele
3. Hook-ul fact_check_hook.py ruleaza automat la fiecare Edit/Write
4. La final, audit complet prin subagent inainte de livrare

## Integrare cu masurile anterioare

Sistemul nou se leaga cu cele 6 straturi anti-AI tone construite anterior:

| Strat existent | Strat fact-check nou | Cum se completeaza |
|---|---|---|
| anti-ai-tone v2.1 skill | anti-hallucination-document skill | Stilul vs continutul, ambele aplicate paralel |
| PostToolUse hook ai_tone | PostToolUse hook fact_check | Ruleaza secvential la fiecare Write |
| UserPromptSubmit hook | reminder permanent | Aceeasi inj de context |
| Stop hook audit sesiune | Stop hook | Audit final post-sesiune |
| MCP anti-ai-tone (5 tools) | MCP extins (7 tools, +2) | Aceeasi infrastructura MCP |
| Subagent anti-ai-tone-reviewer | Subagent fact-checker-document | Lucreaza in pipeline |
| Subagent juridic-style-reviewer | Subagent fact-checker-energetic | Lucreaza in pipeline |

## Pasi efectivi pentru tine, in ordine

### Astazi, 5 minute

1. Verifici ca toate componentele sunt active prin restart Claude Code (necesar pentru a incarca skill-urile noi plus subagentii noi)
2. Restart Claude Desktop daca esti in mijlocul unei conversatii Cowork

### Maine, 20 minute

1. Deschizi Claude.ai Cowork
2. Pentru un proiect existent unde generezi rapoarte energetice, mergi la Settings, Custom Instructions
3. Copy-paste continutul din `~/.claude/cowork-templates/PROJECT_INSTRUCTIONS_ENERGETIC.md`
4. Activezi Citations API in Beta features
5. Upload-uri sursele primare daca lipsesc

### Saptamana asta, ad-hoc

1. Cand primesti versiuni noi de documente, ruleaza compare_docx_versions.py
2. Cand finalizezi un draft, invoca subagent fact-checker-document
3. Cand vezi un pattern de halucinare nou, adauga-l in regulile skill-ului

## Verificare ca totul functioneaza

Pentru a verifica sistemul end-to-end, ruleaza din Claude Code:

```bash
echo '{"tool_input":{"file_path":"C:/Users/Adrian Vasilescu/Downloads/TEST/DIAGNOZA+Proiecte_ENERGIE_BUCURESTI_ILFOV_BM_FINAL_FIX_v11.docx"}}' | python "C:/Users/Adrian Vasilescu/.claude/scripts/fact_check_hook.py"
```

Daca primesti raport cu CRITICAL plus MAJOR detections (Trust Fund, scenarii fara disclaimer, cifre rotunde fara sursa), sistemul functioneaza corect.

## Limite oneste ale sistemului

1. Pe Claude Code (local), toate componentele functioneaza imediat dupa restart.
2. Pe Claude Cowork (web/Desktop), trebuie sa aplici manual Project Instructions plus Citations API.
3. Hook-urile PostToolUse functioneaza DOAR in Claude Code, nu in Cowork.
4. Skill-urile auto-aplicate din ~/.claude/skills/ sunt citite DOAR de Claude Code.
5. MCP `anti-ai-tone` extins functioneaza in AMBELE medii (Cowork plus Code) prin tool invocation explicita.

Pentru Cowork chat specific, garantia anti-halucinare vine prin:
- Project Instructions cu protocolul activ
- Citations API care leaga afirmatiile la PDF-urile uploadate
- Invocare explicita a tool-urilor MCP `fact_check_document` plus `compare_versions`
- Audit post-generare prin export DOCX si verificare in Claude Code

## Costuri estimate

- Sistemul anti-halucinare ruleaza local, fara cost API suplimentar
- MCP extins consuma tokens doar la invocare explicita (~$0.01 per fact_check_document call)
- Citations API este zero cost suplimentar pe output tokens
- Project Knowledge cu PDF-uri uploadate, prima incarcare consuma tokens (intermitent)
- Cu prompt caching activ, costul scade cu 80-95% pentru sesiuni cu PDF-uri repetate

Costul total al sistemului anti-halucinare integrat: aproximativ $5-15/luna pentru utilizare profesionala intensiva, mult sub costul unei singure halucinari neidentificate intr-un raport livrat.
