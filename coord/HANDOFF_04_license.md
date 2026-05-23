# HANDOFF_04_license.md

## Metadata
- task: TASK_04_license
- status: DONE
- completed: 2026-05-23
- executed_by: Claude Code (claude-sonnet-4-6)

## Cosa è stato fatto

### 1. LICENSE (nuovo)
- File `LICENSE` creato con testo MIT standard
- Anno: 2025
- Titolare: Maurizio Lisanti

### 2. CONTRIBUTING.md (nuovo)
- Contenuto bilingue (italiano + inglese)
- Menzione esplicita di PropLUG con link https://proplug.it
- Flusso contribuzione: fork → branch → PR
- Standard del codice: commenti in italiano, docstring obbligatorie con esempio
- Frase finale: "Progetto sviluppato nell'ambito di Linux PropLUG"

### 3. README.md (aggiornato)
- Badge `![License: MIT]` aggiunto sulla riga dopo il badge CI
- Sezione `## 🤝 Community — Linux PropLUG` aggiunta in fondo con link e riferimento a CONTRIBUTING.md

## Verifica

```
pytest tests/ -q
34 passed in 0.08s
```

✅ 34/34 PASS — nessuna regressione

## Definition of Done

- [x] LICENSE presente con testo MIT valido
- [x] CONTRIBUTING.md presente con menzione PropLUG
- [x] README.md aggiornato con badge license e sezione PropLUG
- [x] pytest tests/ -q → 34/34 PASS

## File modificati

| File | Operazione |
|---|---|
| `LICENSE` | Creato |
| `CONTRIBUTING.md` | Creato |
| `README.md` | Aggiornato (badge + sezione PropLUG) |
| `coord/HANDOFF_04_license.md` | Creato (questo file) |
