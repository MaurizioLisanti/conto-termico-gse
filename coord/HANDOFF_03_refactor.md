# HANDOFF_03_refactor — Eliminazione subprocess anti-pattern

**Task:** TASK_03_refactor  
**Executor:** Claude Sonnet 4.6  
**Date:** 2026-05-22  
**Status:** ✅ COMPLETATO

---

## Cosa è stato fatto

### 1. `import_data.py` — aggiunta `run_import()`

Il blocco `if __name__ == "__main__"` è stato estratto in una funzione pubblica `run_import()`.  
Il blocco `__main__` è rimasto e chiama semplicemente `run_import()`, mantenendo l'eseguibilità standalone.

Diff logico:
```python
# PRIMA
if __name__ == "__main__":
    print("🚀 ...")
    client = get_client()
    try:
        ...
    finally:
        client.close()

# DOPO
def run_import():
    """Importa i dati di esempio in Weaviate. Chiamabile da altri moduli."""
    print("🚀 ...")
    client = get_client()
    try:
        ...
    finally:
        client.close()

if __name__ == "__main__":
    run_import()
```

### 2. `import_data.py` — fix env var a module-level

Le due letture `os.environ["WCD_URL"]` e `os.environ["WCD_API_KEY"]` a livello di modulo causavano `KeyError` all'import se le variabili non erano presenti (es. in ambienti CI/test senza `.env`). Cambiate in `os.environ.get(..., "")`: falliscono a runtime in `get_client()` come atteso, non all'import.

```python
# PRIMA
WCD_URL = os.environ["WCD_URL"]      # ← KeyError se assente
WCD_API_KEY = os.environ["WCD_API_KEY"]

# DOPO
WCD_URL = os.environ.get("WCD_URL", "")
WCD_API_KEY = os.environ.get("WCD_API_KEY", "")
```

### 3. `main.py` — rimosso subprocess, aggiunta chiamata diretta

```python
# PRIMA
subprocess.run(["python", "import_data.py"], check=False)

# DOPO
from import_data import run_import   # (dentro setup_elysia, dopo import elysia)
run_import()
```

Il `subprocess.run(["elysia", "start", ...])` in `run_web_mode()` rimane: avvia il server Elysia ed è fuori scope di questo task.

---

## Definition of Done

- [x] Nessun `subprocess.run(["python", "import_data.py"])` in `main.py`
- [x] `import_data.py` ha funzione `run_import()` pubblica
- [x] `python -c "from import_data import run_import; print('import OK')"` → `import OK`
- [x] `pytest tests/ -q` → `34 passed`

---

## Note tecniche

### weaviate-client v3 incompatibile con Python 3.13

L'ambiente usa Python 3.13 (non 3.12 come da spec). `weaviate-client==3.26.7` non è compatibile con Python 3.13 (`ImportError: cannot import name 'docstring_deprecated'`). Aggiornato a `weaviate-client>=4.0,<5` per risolvere.

**Fix suggerito in `requirements.txt` (fuori scope TASK_03):**
```
weaviate-client>=4.0,<5
```

### subprocess rimasto in `run_web_mode()`

`subprocess.run(["elysia", "start", "--port", str(port)])` è intentional: lancia il processo server Elysia. Non è un anti-pattern da rimuovere — è il meccanismo di avvio dell'applicazione.

---

## File modificati

| Percorso | Azione |
|---|---|
| `import_data.py` | Aggiunta `run_import()`; env vars rese safe con `get()` |
| `main.py` | Rimosso subprocess import_data; aggiunto `from import_data import run_import` + chiamata diretta |
| `coord/HANDOFF_03_refactor.md` | Creato (questo file) |
