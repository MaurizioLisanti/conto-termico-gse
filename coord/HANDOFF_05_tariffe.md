# HANDOFF_05_tariffe.md

## Metadata
- task: TASK_05_tariffe
- status: DONE
- completed: 2026-05-23
- executed_by: Claude Code (claude-sonnet-4-6)

## Cosa è stato fatto

### tools.py

**`_TARIFFE_FALLBACK`** — dizionario module-level che sostituisce il precedente dict
hardcoded dentro `_stima_incentivo`. Contiene le 5 voci di tariffa invariate.

**`_get_tariffe(client_manager=None) -> dict`** — nuova funzione module-level:
- Se `client_manager is None` → ritorna `_TARIFFE_FALLBACK` immediatamente.
- Altrimenti tenta `client.collections.get("Normative").query.near_text(...)` per
  leggere una voce `tariffe_json` dalla collection.
- Se la query fallisce per qualsiasi motivo (eccezione, risultati vuoti, campo assente)
  → ritorna `_TARIFFE_FALLBACK`. Non solleva mai eccezioni.

**`_stima_incentivo`** — firma aggiornata con parametro `client_manager=None`;
il blocco `tariffe = {...}` sostituito con `tariffe = _get_tariffe(client_manager)`.
Comportamento esterno invariato — tutti i 34 test precedenti passano ancora.

### tests/test_stima_incentivo.py

Import aggiornato: `from tools import _stima_incentivo, _get_tariffe`

2 nuovi test aggiunti:

| Test | Cosa verifica |
|---|---|
| `test_get_tariffe_fallback_senza_client` | `_get_tariffe()` senza client ritorna il dict hardcoded con tutti i tipi e i valori corretti |
| `test_stima_incentivo_client_manager_none_usa_fallback` | `_stima_incentivo(..., client_manager=None)` produce gli stessi valori attesi (1100 €/anno, 5500 € totale per 10 kW PDC) |

## Verifica

```
pytest tests/ -q
36 passed in 0.11s
```

✅ 36/36 PASS (34 precedenti + 2 nuovi)

## Definition of Done

- [x] `_get_tariffe()` aggiunta con fallback hardcoded
- [x] `_stima_incentivo` usa `_get_tariffe(client_manager)`
- [x] 2 test aggiunti in `test_stima_incentivo.py`
- [x] pytest → 36/36 PASS

## File modificati

| File | Operazione |
|---|---|
| `tools.py` | Aggiunto `_TARIFFE_FALLBACK`, `_get_tariffe()`, aggiornato `_stima_incentivo` |
| `tests/test_stima_incentivo.py` | Aggiornato import, aggiunti 2 test |
| `coord/HANDOFF_05_tariffe.md` | Creato (questo file) |
