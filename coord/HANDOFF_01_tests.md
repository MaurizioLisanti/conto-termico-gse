# HANDOFF_01_tests — Unit test suite for pure business logic

**Task:** TASK_01_tests  
**Executor:** Claude Sonnet 4.6  
**Date:** 2026-05-22  
**Status:** ✅ COMPLETATO — 34/34 passed

---

## Cosa è stato fatto

### 1. Funzioni pure module-level aggiunte in `tools.py`

Due nuove funzioni con prefisso `_` sono state inserite **prima** di `register_tools`, estraendo tutta la logica di calcolo dalle inner closures Elysia:

| Funzione | Restituisce | Errore |
|---|---|---|
| `_verifica_ammissibilita(tipo_impianto, potenza_kw, cop_certificato, zona_climatica, superficie_mq, certificazioni)` | `dict` con campi `ammissibile`, `motivazione`, `requisiti_mancanti`, ecc. | — |
| `_stima_incentivo(tipo_intervento, potenza_kw, superficie_mq, zona_climatica, tipo_soggetto)` | `dict` con `incentivo_annuo_eur`, `incentivo_totale_eur`, ecc. | `ValueError` se tipo non riconosciuto |

### 2. Inner closures refactored

- `verifica_ammissibilita` ora chiama `_verifica_ammissibilita(...)` e fa `yield risultati` + yield summary.
- `stima_incentivo` ora chiama `_stima_incentivo(...)` in un try/except; in caso di `ValueError` fa `yield Error(...)`.
- Comportamento esterno **invariato**.

### 3. Test suite creata

```
tests/
  conftest.py             — stub elysia (non installabile via pip); sys.path setup
  test_ammissibilita.py   — 20 test cases
  test_stima_incentivo.py — 14 test cases
```

### 4. `requirements.txt` aggiornato

Aggiunto `pytest`.

---

## Risultato pytest

```
34 passed in 0.14s
```

---

## Note tecniche

### Stub elysia in conftest.py

`elysia-ai` non è disponibile su PyPI. Il pacchetto viene stubbiato in `conftest.py` tramite `sys.modules` prima dell'import di `tools.py`. Lo stub non viene usato nei test: le funzioni testate (`_verifica_ammissibilita`, `_stima_incentivo`) non dipendono da Elysia.

### Bug pre-esistente — tariff "scaldacqua pompa di calore" irraggiungibile

In `_stima_incentivo`, la chiave `"scaldacqua pompa di calore"` nel dict `tariffe` non viene mai raggiunta perché `"pompa di calore"` appare prima nel dict e la stringa `"scaldacqua pompa di calore"` contiene `"pompa di calore"` come sottostringa. I test sono stati scritti per riflettere il comportamento **effettivo** (non quello inteso). Bug non corretto (fuori scope TASK_01).

---

## File modificati / creati

| Percorso | Azione |
|---|---|
| `tools.py` | Aggiunta `_verifica_ammissibilita`, `_stima_incentivo`; refactored 2 closures |
| `tests/conftest.py` | Creato |
| `tests/test_ammissibilita.py` | Creato — 20 test |
| `tests/test_stima_incentivo.py` | Creato — 14 test |
| `requirements.txt` | Aggiunto `pytest` |
| `coord/HANDOFF_01_tests.md` | Creato (questo file) |

---

## Prossimi passi suggeriti

- Correggere il bug della chiave `"scaldacqua pompa di calore"` in `_stima_incentivo` (spostare la chiave prima di `"pompa di calore"` nel dict `tariffe`).
- Aggiungere test di integrazione per le inner closures Elysia quando l'ambiente di runtime sarà disponibile.
