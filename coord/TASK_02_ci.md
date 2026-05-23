# TASK_02_ci.md

## Metadata
- task: TASK_02_ci
- status: TODO
- priority: HIGH
- risk: LOW
- blocked_by: TASK_01_tests
- blocks: TASK_06_screenshot

## Obiettivo
Aggiungere GitHub Actions CI che esegue pytest ad ogni push/PR
e aggiungere il badge verde nel README.md.

## Allowed Paths
- .github/workflows/ci.yml     (nuovo)
- README.md                    (aggiunta badge in cima)

## Cosa fare

### 1. Crea .github/workflows/ci.yml
Workflow con queste caratteristiche:
- trigger: push e pull_request su branch main
- os: ubuntu-latest
- python: 3.12
- steps:
  1. checkout repo
  2. setup python 3.12
  3. pip install -r requirements.txt
  4. pytest tests/ -q

### 2. Aggiorna README.md
Aggiungi in cima al README, subito dopo il titolo H1, il badge CI:
![CI](https://github.com/MaurizioLisanti/conto-termico-gse/actions/workflows/ci.yml/badge.svg)

## Definition of Done
- [ ] .github/workflows/ci.yml presente e sintassi YAML valida
- [ ] Badge aggiunto nel README.md
- [ ] python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))" → nessun errore

## Comandi verifica
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('YAML OK')"