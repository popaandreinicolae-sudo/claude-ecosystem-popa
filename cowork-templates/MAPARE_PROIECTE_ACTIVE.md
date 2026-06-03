# Mapare Proiecte Cowork Active, Template Recomandat per Proiect

Pe baza folder-elor trusted din `claude_desktop_config.json`, am identificat 5 categorii principale de proiecte active. Pentru fiecare, aplica template-ul Project Instructions specific.

## Categoria 1, Energie

Proiecte identificate, prioritate inalta pentru aplicare:

1. BM_Strategie_ADI_Bucuresti_Ilfov, raportul Banca Mondiala
2. Transgaz SA, consilieria juridica
3. Transgaz Bilant, materiale bilant
4. Legea Hidro SN, analize legislative
5. Cyber Article, articole pe securitate cibernetica plus energie

Template recomandat: `PROJECT_INSTRUCTIONS_ENERGETIC.md`

Surse primare obligatorii in Project Knowledge:
- Strategia Energetica Romaniei 2025-2035
- PNIESC 2021-2030
- SIDU Bucuresti componentele 01_2 pana la 01_6
- Plan dezvoltare Retele Electrice Romania 2026-2035
- Plan dezvoltare Transelectrica 2024-2033
- Raport audit SACET 2022 CMTEB

Pasi aplicare:
1. Deschide Claude.ai Cowork
2. Mergi la Projects, alege „BM_Strategie_ADI_Bucuresti_Ilfov" sau creaza Project nou
3. Settings, Custom Instructions
4. Copy-paste continutul `PROJECT_INSTRUCTIONS_ENERGETIC.md`
5. Project Knowledge, Upload Files, adauga PDF-urile primare
6. Settings, Beta features, Enable Citations API

## Categoria 2, Doctorat

Proiecte identificate:

1. Raport doctorat, materiale cercetare doctorala
2. Cyber Article, articole publicabile
3. CCR, materiale despre decizii Curtea Constitutionala

Template recomandat: `PROJECT_INSTRUCTIONS_JURIDIC_DOCTORAT.md`

Surse primare obligatorii:
- Constitutia Romaniei (text actualizat)
- Decizii CCR cheie: 70/2023, 672/2021, 875/2020, 152/2020, 157/2020, 341/2022, 342/2022, 455/2018, 640/2024, 322/2024
- Tratate doctrinare: Muraru-Tanasescu (CH Beck), Safta (Hamangiu)
- Hotarari CEDO: Zakharov, Big Brother Watch, S. si Marper
- Cauze CJUE: La Quadrature du Net, Digital Rights Ireland
- Legea 51/1991, Legea 58/2023, OUG 155/2024

Pasi aplicare: identici cu Categoria 1, dar template-ul juridic doctorat.

## Categoria 3, Juridic Practic (Burduja, CNCD, DNA, Bazavan)

Proiecte identificate:

1. Burduja (multiple), materiale parlamentare plus drept la replica
2. CNCD Burduja-Sindicat, conflict CNCD
3. Maties DNA, dosar DNA Maties
4. Bazavan, dosar Bazavan
5. CCR, sesizari plus opinii constitutionale

Template recomandat: `PROJECT_INSTRUCTIONS_JURIDIC_DOCTORAT.md` adaptat pentru memorii plus opinii (sterge sectiunea metodologie doctorala, pastreaza format citare plus anti-halucinare).

Surse primare obligatorii (per proiect):
- Acte normative aplicabile cazului
- Jurisprudenta CCR plus CEDO plus CJUE relevanta
- Doctrina specifica (drept administrativ, contencios, penal)

## Categoria 4, Burduja Comunicare

Proiecte identificate:

1. Interviu Burduja
2. Brief Burduja
3. Materiale parlamentare Burduja
4. Burduja drept la replica

Template recomandat: `PROJECT_INSTRUCTIONS_UNIVERSAL.md` plus invocare MCP `burduja-persona`.

Beneficiu: persona MCP injecteaza vocea autentica Sebastian Burduja, anti-AI tone elimina pattern-urile artificiale, anti-hallucination valideaza cifrele specifice mandatului de ministru.

## Categoria 5, Corporate (Hexagon, Realitate, Sapa Sigur, ONJN)

Proiecte identificate:

1. Hexagon, Adrese Hexagon
2. Realitate, materiale conflict
3. Aplicatie Sapa Sigur
4. ONJN, materiale jocuri noroc

Template recomandat: `PROJECT_INSTRUCTIONS_UNIVERSAL.md`

Anti-halucinare strict pe cifre financiare, contracte, sume in dispute. Pentru ONJN, atentie la terminologia tehnica jocuri de noroc plus jurisprudenta CJUE pe libertatea de stabilire.

## Categoria 6, Personal plus Alte

Proiecte identificate, fara template specific:

1. Belegal, materiale personale
2. Almasu, dosare
3. Saragea
4. Alina Omnivar
5. Sandbox AI, experimente AI
6. Spatiu, materiale spatiale (Agentia Spatiala Romana)
7. Proeict Paul
8. CFR

Recomandare: aplica `PROJECT_INSTRUCTIONS_UNIVERSAL.md` pentru oricare proiect cu mize profesionale.

## Plan secvential aplicare

Saptamana 1 (acum):
- Proiectul BM_Strategie_ADI_Bucuresti_Ilfov, template ENERGETIC plus Citations API
- Proiectul Raport doctorat, template JURIDIC_DOCTORAT plus PDF-uri primare
- Proiectul Burduja, template UNIVERSAL plus invocare persona MCP

Saptamana 2:
- Transgaz SA plus Transgaz Bilant, template ENERGETIC
- CCR, template JURIDIC_DOCTORAT
- Cyber Article, template ENERGETIC plus skill cyber-law-ro

Saptamana 3:
- Proiectele corporate (Hexagon, Realitate, ONJN), template UNIVERSAL
- Proiectele Burduja secundare, template UNIVERSAL plus persona

## Verificare ca template-ul s-a aplicat

In fiecare Project Cowork, dupa setare Custom Instructions, scrii intr-un chat nou:

```
Listeaza regulile anti-halucinare pe care le aplici in acest proiect.
```

Claude trebuie sa raspunda cu cele 12 reguli pozitive plus regulile sectoriale specifice. Daca nu, verifica daca template-ul s-a salvat corect.
