# TASK_03_refactor.md

## Metadata
- task: TASK_03_refactor
- status: TODO
- priority: HIGH
- risk: MED
- blocked_by: —
- blocks: TASK_06_screenshot

## Obiettivo
Eliminare il subprocess anti-pattern in main.py.
import_data.py diventa un modulo importabile con funzione
run_import() chiamata direttamente da main.py.

## Allowed Paths
- main.py
- import_data.py

## Cosa fare

### 1. import_data.py
Racchiudi tutto il blocco if __name__ == "__main__" in una
funzione run_import() che esegue get_client(), create_collections(),
import_all_data(), verify_import() e chiude il client.
Il blocco if __name__ == "__main__" rimane e chiama run_import()
così il file è ancora eseguibile standalone.

### 2. main.py
Rimuovi subprocess.run(["python", "import_data.py"]).
Aggiungi import run_import from import_data.
Chiama run_import() direttamente dentro setup_elysia().

## Definition of Done
- [ ] Nessun subprocess.run in main.py
- [ ] import_data.py ha funzione run_import() pubblica
- [ ] python -c "from import_data import run_import; print('import OK')" → PASS
- [ ] pytest tests/ -q → ancora 34/34 PASS

## Comandi verifica
python -c "from import_data import run_import; print('import OK')"
pytest tests/ -q