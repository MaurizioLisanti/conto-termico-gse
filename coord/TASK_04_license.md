# TASK_04_license.md

## Metadata
- task: TASK_04_license
- status: TODO
- priority: MED
- risk: LOW
- blocked_by: —
- blocks: —

## Obiettivo
Aggiungere LICENSE MIT, CONTRIBUTING.md con menzione PropLUG
e aggiornare README con badge license e sezione community.

## Allowed Paths
- LICENSE                    (nuovo)
- CONTRIBUTING.md            (nuovo)
- README.md                  (aggiunta sezione PropLUG e badge license)

## Cosa fare

### 1. Crea LICENSE
File LICENSE MIT standard con:
- Anno: 2025
- Titolare: Maurizio Lisanti

### 2. Crea CONTRIBUTING.md
Contenuto in italiano e inglese con:
- Benvenuto al progetto PropLUG
- Link associazione: https://proplug.it
- Come contribuire (fork → branch → PR)
- Standard del codice (commenti in italiano, docstring obbligatorie)
- Menzione: "Progetto sviluppato nell'ambito di Linux PropLUG"

### 3. Aggiorna README.md
- Aggiungi badge license dopo badge CI:
  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
- Aggiungi in fondo sezione ## 🤝 Community — Linux PropLUG
  con link al sito e descrizione del progetto come iniziativa PropLUG

## Definition of Done
- [ ] LICENSE presente con testo MIT valido
- [ ] CONTRIBUTING.md presente con menzione PropLUG
- [ ] README.md aggiornato con badge license e sezione PropLUG
- [ ] pytest tests/ -q → ancora 34/34 PASS

## Comandi verifica
pytest tests/ -q