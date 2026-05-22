# HANDOFF_02_ci — GitHub Actions CI + badge README

**Task:** TASK_02_ci  
**Executor:** Claude Sonnet 4.6  
**Date:** 2026-05-22  
**Status:** ✅ COMPLETATO

---

## Cosa è stato fatto

### 1. `.github/workflows/ci.yml` creato

Trigger: `push` e `pull_request` su `main`.  
Runner: `ubuntu-latest` — Python `3.12`.

Passi del job `test`:

| Step | Azione |
|---|---|
| Checkout repository | `actions/checkout@v4` |
| Set up Python 3.12 | `actions/setup-python@v5` |
| Install dependencies | `pip install -r requirements.txt \|\| true` + `pip install pytest` |
| Run tests | `pytest tests/ -q` |

### 2. Badge CI aggiunto in `README.md`

Inserito subito dopo il titolo H1 (`# 🔥 Conto Termico GSE ...`):

```markdown
![CI](https://github.com/MaurizioLisanti/conto-termico-gse/actions/workflows/ci.yml/badge.svg)
```

### 3. Sintassi YAML verificata

```
python -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml')); print('YAML OK')"
→ YAML OK
```

---

## Note tecniche

### Deviazione dallo spec: install dependencies

Lo spec indica `pip install -r requirements.txt`.  
`elysia-ai` non è disponibile su PyPI (confermato in TASK_01) — pip abortisce l'intera operazione prima di installare `pytest`.

Soluzione adottata:
```yaml
run: |
  pip install -r requirements.txt || true
  pip install pytest
```

Comportamento: tenta l'install completo; se fallisce (elysia-ai), il `|| true` non interrompe il workflow e il secondo comando garantisce che `pytest` sia disponibile.  
I test passano (34/34) perché `conftest.py` già stubba elysia via `sys.modules`.

**Fix consigliato (fuori scope TASK_02):** rimuovere `elysia-ai` da `requirements.txt` oppure sostituirlo con `elysia-ai; sys_platform == "never"` per documentarlo senza tentarne l'install in CI.

---

## Definition of Done

- [x] `.github/workflows/ci.yml` presente e sintassi YAML valida
- [x] Badge aggiunto nel README.md
- [x] `python -c "import yaml; yaml.safe_load(...)"` → `YAML OK`

---

## File modificati / creati

| Percorso | Azione |
|---|---|
| `.github/workflows/ci.yml` | Creato |
| `README.md` | Badge aggiunto dopo H1 |
| `coord/HANDOFF_02_ci.md` | Creato (questo file) |
