# irina-mihu-persona

Server MCP de persona pentru Claude Cowork / Claude Desktop. Face ca Claude să
gândească, să scrie și să documenteze ca Irina Mihu, diplomat MAE (Secretar III,
DAGFIJ, Departamentul UE, cu mandat la Ambasada României în Israel), expertă pe
afaceri europene, energie, diplomație economică, drept diplomatic și internațional,
diplomație cibernetică, protocol și negociere.

Construit pe standardele MCP și de persona engineering din 2026: transport stdio
local, trei primitive (prompts, resources, tools), persona versionabilă în markdown
cu frontmatter, ancorare în surse reale, fără date personale de contact.

## Structură

```
irina-mihu-persona/
  server.py                       server FastMCP (stdio)
  persona/irina-mihu.md           definiția personei (frontmatter + corp)
  knowledge/profil.md             profil profesional (fără date de contact)
  knowledge/canon-bibliografic.md canonul MAE
  knowledge/surse-primare.md      instrumente-cheie cu reper de citare
  knowledge/sabloane.md           șabloane de documente diplomatice
  requirements.txt
  claude_desktop_config.example.json
```

## Instalare

1. Instalează dependențele (Python 3.10+):

```powershell
cd "C:\Users\Adrian Vasilescu\Downloads\Irina Mihu\irina-mihu-persona"
pip install -r requirements.txt
```

2. Testează rapid că serverul pornește și își listează capabilitățile:

```powershell
python test_server.py
```

3. Conectează serverul la Claude Desktop / Cowork. Deschide fișierul de
configurare:

```
%APPDATA%\Claude\claude_desktop_config.json
```

Adaugă blocul din `claude_desktop_config.example.json` în secțiunea `mcpServers`
(ajustează calea către `server.py` dacă ai mutat folderul). Repornește aplicația
Claude.

## Folosire

- Activează persona prin prompt-ul `activate_irina` (apare în lista de prompts a
  serverului). Variante: `mode_centrala`, `mode_exterior_israel`,
  `mode_analiza_juridica`, `draft` (cu gen, subiect, limbă).
- Resursele (`persona://profil`, `persona://canon`, `persona://surse`,
  `persona://sabloane`, `persona://definitie`) pot fi atașate la conversație.
- Tool-urile pe care le poate apela Claude: `get_persona_profile`, `list_domenii`,
  `list_templates`, `get_template`, `get_source`, `search_knowledge`,
  `research_guidance`.

Căutarea pe web pe domeniile ei se face cu instrumentele proprii ale Claude
Cowork; `research_guidance` îi spune lui Claude cum să caute și ce surse canonice
să folosească drept punct de plecare.

## Standarde respectate

- Acuratețe: zero invenție de cifre, articole, decizii sau citate; marcaj
  `[NEVERIFICAT]` unde lipsește sursa.
- Confidențialitate: datele personale de contact din CV sunt excluse din persona.
- Multilingv: răspuns în limba interlocutorului, corect gramatical la nivel C2.
- Stil anti-AI tone: diateză activă, fraze de lungimi variate, fără clișee.

## Versionare

Persona este cod. Modifică `persona/irina-mihu.md` și fișierele din `knowledge/`,
incrementează `version` din frontmatter și repornește serverul.
