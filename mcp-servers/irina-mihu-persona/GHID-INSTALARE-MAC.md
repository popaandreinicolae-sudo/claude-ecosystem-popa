# Ghid de instalare pe Mac, persona Irina Mihu pentru Claude

Acest pachet adaugă în Claude (Desktop / Cowork) o persona care face ca asistentul
să gândească, să scrie și să documenteze ca un diplomat MAE. Durează în jur de zece
minute. Urmează pașii în ordine.

## Ce îți trebuie întâi

- Aplicația Claude pentru Mac, instalată și conectată (abonament Pro, Max, Team sau
  Enterprise pentru Cowork).
- Python 3 pe Mac. Verifici dacă există: deschizi aplicația **Terminal** (din
  Launchpad, scrii „Terminal") și scrii comanda de mai jos, apoi Enter:

  ```
  python3 --version
  ```

  Dacă apare un număr (de exemplu „Python 3.12.4"), ai Python. Dacă apare o eroare,
  instalează-l de la https://www.python.org/downloads/macos/ (descarci, deschizi
  fișierul .pkg și dai Next până la final).

## Pasul 1, pune folderul la locul lui

Dezarhivează `irina-mihu-persona.zip`. Mută folderul rezultat în **Documents**.
Calea finală trebuie să arate așa:

```
/Users/NUMELE_TAU/Documents/irina-mihu-persona
```

Înlocuiește `NUMELE_TAU` cu numele contului tău de Mac. Ca să afli calea exactă:
click dreapta pe folder, apoi ține apăsat tasta **Option** și alege „Copy ... as
Pathname".

## Pasul 2, instalează componenta de care depinde

În Terminal, scrie (înlocuind calea dacă ai pus folderul altundeva):

```
pip3 install -r /Users/NUMELE_TAU/Documents/irina-mihu-persona/requirements.txt
```

Aștepți să se termine. Dacă `pip3` dă eroare, încearcă:

```
python3 -m pip install -r /Users/NUMELE_TAU/Documents/irina-mihu-persona/requirements.txt
```

## Pasul 3, verifică (opțional, dar recomandat)

```
python3 /Users/NUMELE_TAU/Documents/irina-mihu-persona/test_server.py
```

Dacă vezi la final „TOATE TESTELE AU TRECUT", totul e în regulă.

## Pasul 4, conectează persona la Claude

1. Deschizi aplicația Claude. Mergi la **Settings** (Setări), apoi la secțiunea de
   **Developer / MCP / Connectors** și deschizi fișierul de configurare. Dacă nu
   găsești butonul, fișierul stă aici:

   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

   Ca să-l deschizi rapid: în Finder, meniul **Go**, apoi **Go to Folder**, lipești
   calea de mai sus.

2. În acel fișier, adaugi blocul din `claude_desktop_config.mac.example.json` (din
   pachet), în secțiunea `mcpServers`. Înlocuiești calea cu cea reală către
   `server.py`. Dacă fișierul e gol, pui tot conținutul exemplului.

3. Salvezi fișierul și **repornești complet** aplicația Claude (ieși de tot, apoi o
   deschizi din nou).

## Pasul 5, folosește persona

În Claude, persona apare ca server „irina-mihu-persona". O activezi rulând prompt-ul
**activate_irina**. Ai și moduri separate: `mode_centrala`, `mode_exterior_israel`,
`mode_analiza_juridica`, plus `draft` pentru redactarea unui document pe gen, subiect
și limbă.

## Dacă ceva nu merge

- Claude nu vede serverul: verifică în config că ai calea corectă către `server.py`
  și că ai repornit complet aplicația.
- Eroare de Python: rulează din nou comanda de la Pasul 2; e nevoie de Python 3.10
  sau mai nou.
- Vrei ajutor: trimite o captură de ecran cu eroarea.

## Variantă fără instalare (de rezervă)

Dacă instalarea pare prea complicată, poți folosi conținutul personei direct: creezi
un Project în Claude, pui textul din `persona/irina-mihu.md` în câmpul de instrucțiuni
și încarci fișierele din folderul `knowledge/` ca documente ale proiectului. Nu e
server MCP, dar obții aproape același rezultat fără cod.
