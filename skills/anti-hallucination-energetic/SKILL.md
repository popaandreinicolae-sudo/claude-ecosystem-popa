---
name: anti-hallucination-energetic
description: |
  Protocol specializat anti-halucinare pentru documente despre sectorul energetic romanesc. APLICA AUTOMAT la documente, rapoarte, strategii, opinii juridice, fundamentari care abordeaza: sistemul energetic national, sectorul gazier (Transgaz, Romgaz, Distrigaz), sectorul electric (Transelectrica, Retele Electrice Romania, Hidroelectrica), termoficare (CMTEB, ELCEN, RADET, SACET), regenerabile (fotovoltaic, eolian, geotermal, biomasa), eficienta energetica cladiri, mobilitate electrica, securitate energetica, infrastructura critica, ANRE, ANRSC, Ministerul Energiei. Triggere: "energie", "electricitate", "gaze naturale", "termoficare", "SACET", "CET", "ELCEN", "CMTEB", "Transgaz", "Transelectrica", "Hidroelectrica", "Romgaz", "Distrigaz", "ANRE", "regenerabile", "PNRR energie", "PNIESC", "Strategia Energetica", "Fondul Modernizare", "ETS", "MWh", "GWh", "kV", "Gcal", "kWh termic", "regiune Bucuresti-Ilfov sectorul energetic", "infrastructura energetica", "tarif energie", "subventie energie". Construit pe baza halucinatiilor reale documentate in versiunea v11 a raportului energetic Bucuresti-Ilfov (44 angajati PIU fabricati, 3 milioane EUR Trust Fund inventat, scenarii BAU/Strategy/Ambitious cu cifre fictive, 200 si 800 milioane EUR programe europene atribuite fara sursa, BCR 3,5 fabricat, anexa E sensibilitate complet inventata).
version: 1.0
last_updated: 2026-06-01
parent_skill: anti-hallucination-document
---

# Anti-Hallucination Energetic, Sector Specific

Acest skill extinde `anti-hallucination-document` cu reguli si referinte specifice sectorului energetic romanesc. Citeste mai intai SKILL.md al parintelui pentru regulile universale, apoi aplica regulile sectoriale de mai jos.

## Surse obligatorii incarcate in Project Knowledge

Pentru orice document despre sectorul energetic al Bucurestiului sau al Romaniei, incarca obligatoriu in Cowork Project Knowledge:

1. Strategia Energetica a Romaniei 2025-2035 cu perspectiva 2050, adoptata prin HG 23 octombrie 2024
2. Planul National Integrat in domeniul Energiei si Schimbarilor Climatice 2021-2030, versiunea actualizata transmisa CE iulie 2024
3. Strategia Integrata de Dezvoltare Urbana a Municipiului Bucuresti 2021-2030, componentele 01_2 pana la 01_6
4. Plan dezvoltare Retele Electrice Romania S.A. 2026-2035
5. Plan dezvoltare CNTEE Transelectrica S.A. 2024-2033
6. Raport audit energetic SACET CMTEB pentru exercitiul 2022, publicat 2023
7. Acte normative cheie: OUG 27/2022, OUG 64/2022, Legea 372/2005, Metodologia Mc001/2022, Legea 121/2014 eficienta energetica
8. Memorandumuri ELCEN cu Departamentul Energiei SUA (februarie 2024) plus SAGE Geosystems (iulie 2024)
9. Cele 4 directive UE relevante: 2018/2001 modificata 2023/2413 (RED III), 2023/1791 EED reformare, 2024/1275 EPBD, Regulamentul 2019/943
10. Documente ANRE: rapoarte ANRE 2024-2025, decizii reglementare tarif distributie

## Reguli sectoriale specifice

### Regula E1, validare cifre cu unitati corecte

Confuzia intre unitati este halucinatie clasica. Verifica:
- MW este capacitate instalata, MWh este energie produsa pe an
- Gcal/h este capacitate termica, Gcal este energie termica
- kV este nivel tensiune, kW este putere consumator
- m³ este volum gaz natural absolut, m³ normal (Nm³) este la conditii standard
- MJ, GJ, TJ sunt unitati de energie, nu de putere

Cand citezi capacitate, marcheaza explicit: "capacitate instalata X MW" sau "energie produsa Y MWh/an".

### Regula E2, denumiri institutionale oficiale 2024-2026

Folosesti denumirile oficiale curente. Halucinari frecvente:
- CORECT: Retele Electrice Romania S.A. (fuziune Muntenia, Banat, Dobrogea, in vigoare 30 noiembrie 2024)
- GRESIT: E-Distributie Muntenia (denumire pre-fuziune, depasita)
- CORECT: Compania Municipala Termoenergetica Bucuresti S.A. (CMTEB), din 1 decembrie 2019
- GRESIT: RADET (regie auto-desfiintata, transferata la CMTEB)
- CORECT: Societatea Electrocentrale Bucuresti S.A. (ELCEN)
- CORECT: CNTEE Transelectrica S.A. cu sediu Bucuresti
- CORECT: Transgaz S.A. cu sediu Medias (sediu social)
- CORECT: Distrigaz Sud Retele S.A. (parte din grupul ENGIE Romania)
- CORECT: Hidroelectrica S.A.
- CORECT: Romgaz S.A. cu sediu Medias

### Regula E3, cifrele de consum Bucuresti-Ilfov 2024 (verificate)

Aceste cifre au fost verificate in versiunea finala 31.05 a raportului. Foloseste-le ca baseline:
- Municipiul Bucuresti, consum total 2024: marcheaza [VERIFICARE] cu Retele Electrice Romania
- Judetul Ilfov, consum total 2024: 2.069.813 MWh (verificat in document final)
- Distributie consum Ilfov: 977.449 MWh MT plus 976.205 MWh JT
- Consum medie tensiune Bucuresti 2024: 2.024.888 MWh
- Prognoza Bucuresti 2026-2035: 1.210 MW (2026) la 1.509 MW (2035), crestere aproximativ 25%
- Prognoza Ilfov 2026-2035: 309 MW la 374 MW
- Productie locala SRE Bucuresti 2033: 26 MW (plafonata, dependenta de fluxuri RET)

### Regula E4, cifrele SACET (verificate)

- Lungime retea primara SACET: 884,07 km
- Lungime retea secundara SACET: 2.763 km
- Vechime peste 25 ani retea primara: 65,50%
- Vechime peste 25 ani retea secundara: 45,59%
- Pierderi reale caldura SACET 2022: 39,88%
- Avarii primar 2022: 2.241
- Avarii cumulat sistem 2022: 4.412
- Productie tert (ELCEN majoritar) in SACET 2022: 95,34%
- Capacitate termica 4 CET-uri ELCEN cumulat: maxim 1.800 Gcal/h
- Pierderi cumulate transformare-transport national: 9% (Strategia Energetica)

### Regula E5, indicatori care SUNT OBLIGATORIU marcați ca neverificați

Aceste cifre apar frecvent halucinate. Marcheaza [VERIFICARE NECESARA] daca nu ai sursa primara:
- Numarul exact de apartamente cu centrale termice individuale in Bucuresti
- Volumul exact al platilor cumulate ELCEN catre Distrigaz Sud Retele (estimare 3,2 mld lei dar necesita sursa)
- BCR (Benefit-Cost Ratio) pentru proiecte specifice
- Volume aplicabile pe programe europene specifice fara confirmare ministeriala
- Numar angajati PIU (Project Implementation Unit) ADIZMB
- Suma Trust Fund Banca Mondiala pentru institutional development
- Mid-Term Review threshold (NU folosi 30% disbursement fara sursa BM)
- NPV, EIRR per proiect individual
- Procent disbursement pentru milestones

### Regula E6, structura corecta capitole pentru raport energetic

Format validat dupa documentul corectat:
- Cap. I, Diagnoza energetica a regiunii (NU "Contextul energetic" generic)
- Cap. II, SACET
- Cap. III, Electricitate generare si cogenerare
- Cap. IV, Electricitate distributie si transport
- Cap. V, Gaze naturale
- Cap. VI, Eficienta energetica cladiri
- Cap. VII, Iluminat public
- Cap. VIII, Mobilitate electrica
- Cap. IX, Securitate energetica metropolitana
- Cap. X, Roadmap implementare
- Cap. XI, Surse de finantare (NU "Cadru juridic" daca nu ai continut)

NU genera capitole goale ca slot fillers. Daca utilizatorul nu cere explicit capitol cadru juridic plus nu are continut, omite-l.

### Regula E7, scenarii cu disclaimers obligatorii

Cand prezinti scenarii BAU/Strategy/Ambitious:
- Marcheaza fiecare cifra ca [SCENARIU, ipoteza X]
- Mentioneaza ca scenariile sunt constructii analitice, nu prognoze oficiale
- Nu invoca surse oficiale (Banca Mondiala, ANRE) pentru cifrele scenariilor decat daca au validare publica
- Indica explicit ce variabile fac diferenta intre scenarii

### Regula E8, surse finantare cu volume

Cand mentionezi programe europene de finantare:
- Nume program complet plus perioada 2021-2027 sau 2028-2034
- Volum total aplicabil DOAR daca exista in document oficial alocat sectorului
- Nu inventa volume tip "peste 200 milioane EUR", "peste 800 milioane EUR"
- Pentru PNRR, citeaza componenta specifica plus alocarea oficiala publicata
- Pentru Fondul de Modernizare, citeaza data adoptata plus tara beneficiar plus suma

### Regula E9, valori geotermale Otopeni

Verificat:
- Suprafata rezervor: aproximativ 300 km²
- Temperatura cap sonda: 58-84 grade Celsius
- Debite individuale: 22-35 litri pe secunda
- Acvifer carbonatic: calcare si dolomite jurassic-cretacice
- O singura licenta concesiune activa: CN Aeroporturi Bucuresti, iunie 2020, pentru Aeroportul Henri Coanda
- Valoare estimata proiect LL-71: 100 milioane EUR

Restul cifrelor geotermale (numar puturi, productie estimata, beneficiari finali) trebuie marcate [SCENARIU] sau [VERIFICARE NECESARA].

### Regula E10, coduri proiecte SIDU

Proiectele SIDU au coduri oficiale:
- LS-X pentru lista scurta (X numar)
- LL-X pentru lista lunga (X numar)

Verificate in documentul corectat:
- LS-7: consolidare seismica plus eficienta cladiri sanitare, 31,5 milioane EUR
- LS-12: consolidare plus renovare Calea Victoriei 22-24, 8,29 milioane EUR
- LS-13: eficienta unitati invatamant, 30 milioane EUR
- LS-21: eficienta scoli sectorul 2, 40 milioane EUR
- LS-22: eficienta scoli si colegii, 285,11 milioane EUR
- LS-23: iluminat public LED, 125 milioane EUR
- LS-28: modernizare cladiri apartamente pre-1990, 732,81 milioane EUR
- LL-32: retea statii reincarcare electrica, 7,5 milioane EUR
- LL-41: modernizare linii electrice subterane JT, MT, 7,20 milioane EUR
- LL-42: cresterea capacitatii furnizare, valoare verificare in document
- LL-67: cogenerare 110 MW Aviatiei, Lacul Tei
- LL-68: capacitati fotovoltaice sectoarele 1-6, faza initiala
- LL-71: Geotermal Bucuresti-Ilfov, 100 milioane EUR
- LL-72: modernizare termoelectrice CMTB
- LL-73: smart metering SACET

Nu inventa coduri LS-NEW1 sau LL-X cu numere care nu sunt confirmate in SIDU oficial.

## Integrare cu MCP-uri si skill-uri

Acest skill ruleaza in pipeline cu:
- `anti-hallucination-document` (parinte, reguli universale)
- `zero-hallucination-citations` (citarea bibliografica)
- `verificare-legislatie` (validare OUG-uri, HG-uri, legi energie)
- `legal-verificator-ro` MCP (verificare acte normative romanesti)
- `eurlex` MCP (verificare directive UE energie)
