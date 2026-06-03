# Taxonomia Marcajelor de Incertitudine

Vocabular consistent pentru marcarea diferitelor categorii de informatie in documente profesionale.

## Marcaje principale

### [DATA]

Informatie confirmata din sursa primara verificata. Se foloseste pentru:
- Cifre din rapoarte oficiale uploadate in Project Knowledge
- Procente din statistici publicate (INS, Eurostat, ANRE)
- Articole de lege verificate prin MCP `legal-verificator-ro`
- Decizii CCR verificate prin MCP plus citate verbatim

Exemplu: `Pierderile reale de caldura pentru sistemul SACET au fost de 39,88% in 2022 [DATA, sursa: Raport audit energetic CMTEB 2023, p. 47].`

### [ESTIMARE]

Calcul propriu construit prin extrapolare, agregare sau extrapolare. Marcat obligatoriu cu metoda. Se foloseste pentru:
- Volume cumulate calculate prin agregare istorica
- Proiectii bazate pe trend istoric
- Indicatori derivati din date primare

Exemplu: `Volumul cumulat al platilor ELCEN catre Distrigaz Sud Retele din 2007 [ESTIMARE PROPRIE, metoda: extrapolare consum gaz CET-uri ELCEN inmultit cu tarif distributie ANRE acumulat 2007-2024, sursa primara consum: rapoartele anuale ELCEN].`

### [NEVERIFICAT]

Informatie plauzibila dar fara sursa confirmata in momentul redactarii. Marcaj obligatoriu cu indicare sursa potentiala. Se foloseste pentru:
- Cifre din memorie a modelului fara sursa primara accesibila
- Atribuiri partiale (institutie cunoscuta, dar context specific neconfirmat)
- Detalii contextuale plauzibile dar nedocumentate

Exemplu: `Numarul total de apartamente cu centrale termice individuale in Bucuresti este de aproximativ 600.000 [NEVERIFICAT, sursa necesara: raport ANRE statistici distribuitori gaz natural 2024 sau date Distrigaz Sud Retele].`

## Marcaje secundare

### [SCENARIU, ipoteza X]

Pentru constructii analitice care nu reflecta date observate, ci modelari ipotetice.

Exemplu: `Scenariul Ambitious presupune 20.000 - 40.000 apartamente cuplate la sursa geotermala pana in 2035 [SCENARIU, ipoteze: faza Go la Otopeni declanseaza in 2027 plus infrastructura SACET adaptata in 5 ani].`

### [VERIFICARE NECESARA]

Pentru cifre, decizii, cauze care exista probabil dar trebuie validate prin MCP specific.

Exemplu: `Decizia CCR nr. 552/2024 [VERIFICARE NECESARA prin mcp__legal-verificator-ro__verify_ccr_citation, subiect declarat: securitate cibernetica].`

### [PRECIZIE LIMITATA]

Pentru date publicate cu interval, nu valoare punctuala.

Exemplu: `Pierderile retelei de termoficare la nivel european variaza intre 8% si 20% [PRECIZIE LIMITATA, sursa: Heat Roadmap Europe 2050, p. 134, interval pentru orase comparabile].`

### [CONFIDENTIAL]

Pentru informatii cu acces restrictionat care nu pot fi citate public.

Exemplu: `Volumul de gaz contractat pentru iarna 2025-2026 [CONFIDENTIAL, sursa: contract ELCEN catre Romgaz, accesibil prin clearance industrial].`

### [DEPASIT]

Pentru informatii anterior valide dar nu mai actuale.

Exemplu: `Pana in 2019, distribuitorul de termoficare al Bucurestiului era RADET [DEPASIT, RADET a fost reorganizata in CMTEB la 1 decembrie 2019].`

## Reguli de utilizare

1. Niciodata nu lasa o cifra factuala fara marcaj cand sursa nu este evident citata in propozitia anterioara.
2. La sfarsitul documentului, lista [NEVERIFICAT] devine TODO de verificare pentru livrarea finala.
3. La sfarsitul documentului, lista [SCENARIU] permite cititorului sa intelega ce este factual versus modelat.
4. Marcajul [DATA] poate fi omis cand intregul capitol foloseste o singura sursa citata in titlu.
5. Marcajul [ESTIMARE] este obligatoriu chiar cand calculul pare evident, pentru transparenta metodei.
