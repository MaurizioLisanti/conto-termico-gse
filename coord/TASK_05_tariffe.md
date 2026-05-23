# TASK_05_tariffe.md

## Metadata
- task: TASK_05_tariffe
- status: TODO
- priority: MED
- risk: MED
- blocked_by: TASK_01_tests
- blocks: TASK_06_screenshot

## Obiettivo
Eliminare il hardcoding delle tariffe incentivo in tools.py.
Le tariffe vengono lette dalla collection Normative di Weaviate
tramite query semantica, con fallback ai valori hardcoded
se Weaviate non è raggiungibile.

## Allowed Paths
- tools.py
- tests/test_stima_incentivo.py

## Cosa fare

### 1. tools.py — funzione _get_tariffe()
Aggiungi funzione module-level:

def _get_tariffe(client_manager=None) -> dict:
    Tenta di leggere le tariffe dalla collection Normative.
    Se client_manager è None o la query fallisce,
    ritorna il dizionario tariffe hardcoded esistente.
    Mai sollevare eccezioni — sempre ritornare un dict valido.

La funzione cerca nella collection Normative