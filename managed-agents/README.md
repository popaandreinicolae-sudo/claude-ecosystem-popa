# Managed Agents pentru Andrei Nicolae Popa

3 agenți autonomi care monitorizează surse juridice oficiale și alertează
asupra deciziilor, actelor normative, hotărârilor noi de interes.

## Cele 3 agente

### ccr_watcher.py, zilnic

Monitorizează ccr.ro pentru decizii CCR noi pe securitate cibernetică,
drepturi fundamentale, art. 53, art. 26, 28, 30. Salvează raport zilnic
plus email alertă dacă există decizie critică.

### mof_watcher.py, zilnic

Monitorizează Monitorul Oficial pentru OUG, legi, HG-uri noi pe energie,
securitate cibernetică, constitutional, administrativ. Cross-check cu
legal-verificator-ro MCP.

### hudoc_watcher.py, săptămânal

Monitorizează hudoc.echr.coe.int pentru hotărâri CEDO noi pe art. 8, 10,
6 cu topicuri prioritare (mass surveillance, metadata retention,
cybersecurity, AI surveillance).

## Cum se rulează

### Variantă 1, generare prompt local

```bash
cd "C:/Users/Adrian Vasilescu/managed-agents"
python ccr_watcher.py       # genereaza prompt-CCR-YYYY-MM-DD.txt
python mof_watcher.py       # genereaza prompt-MOF-YYYY-MM-DD.txt
python hudoc_watcher.py     # genereaza prompt-HUDOC-YYYY-MM-DD.txt
```

Apoi rulezi prompt-ul prin Claude API sau direct in Claude Desktop chat.

### Variantă 2, integrare cu Anthropic Managed Agents API

Setup necesar:
1. Cont Anthropic cu acces Managed Agents (in beta, cere acces)
2. API key Anthropic stocat in env var ANTHROPIC_API_KEY
3. Schedule extern (GitHub Actions, Cloudflare Cron Triggers, Azure
   Functions)

Exemplu invocare prin API:

```python
import anthropic
client = anthropic.Anthropic()

agent_run = client.managed_agents.runs.create(
    model="claude-opus-4-8",
    prompt=Path("prompt-CCR-2026-06-01.txt").read_text(),
    tools=[
        {"name": "web_fetch"},
        {"mcp": "legal-verificator-ro"},
        {"mcp": "hudoc"},
        {"mcp": "eurlex"},
    ],
    effort="high",
    timeout_seconds=3600,
)
```

### Variantă 3, schedule prin GitHub Actions

Salvează in `.github/workflows/ccr-watcher.yml`:

```yaml
name: CCR Watcher Daily
on:
  schedule:
    - cron: '0 8 * * *'   # 8 AM UTC zilnic
jobs:
  ccr-watch:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Invoke Claude Managed Agent
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python ccr_watcher.py && python invoke_agent.py
```

## Costuri estimate

Pentru fiecare agent rulat zilnic la 1 oră durată sesiune:

- 0.08 USD per oră sesiune Managed Agents (overhead)
- aproximativ 0.50 USD per zi pentru tokens consumați (Opus 4.8 cu effort
  high, citire ccr.ro plus parsare plus generare raport)
- Total: aproximativ 17 USD lunar per agent zilnic

Pentru cei 3 agenți activi:
- CCR-watcher zilnic, 17 USD lunar
- M.Of.-watcher zilnic, 17 USD lunar
- HUDOC-watcher săptămânal, 5 USD lunar

Total estimat: aproximativ 40 USD lunar pentru monitorizare juridică
autonomă completă. Comparativ cu un asistent uman care ar costa 1500 plus
USD lunar pentru aceeași sarcină.

## Setup output folder

Output-ul agenților se salvează automat in:

```
C:/Users/Adrian Vasilescu/managed-agents/output/
├── ccr-watch/
│   ├── 2026-06-01.md
│   └── prompt-2026-06-01.txt
├── mof-watch/
│   └── ...
└── hudoc-watch/
    └── ...
```

Util pentru consultare istorică plus material pentru teza doctorală.

## Plus integrare Cowork

Pentru integrare cu Claude Cowork, output-ul agenților se incarcă
automat in Project Knowledge al proiectului „Cercetare doctorat
constitutional". Astfel, conversațiile din Cowork au acces la jurisprudența
zilnică actualizată.

Configurare manuală: după primele 7 zile de rulare, mutați fișierele
.md generate in OneDrive/Documents/Claude/Projects/Cercetare-doctorat/.
Cowork le va indexa automat.
