# HANDOFF_07_dataset.md

## Status: DONE

## Cosa è stato fatto

### File prodotti
- `scripts/extract_pdf.py` — script di estrazione PDF → JSON via OpenRouter
- `data/decreto_dm_16_02_2016.json`
- `data/allegato_criteri_ammissibilita.json`
- `data/regole_applicative_ct.json`
- `data/ct3_webinar_2026.json`
- `data/guida_ct_pubblica_amministrazione.json`
- `data/mappa_ct_imprese_privati.json`
- `data/pompe_di_calore_regole_applicative.json`
- `data/dataset_completo.json`
- `requirements.txt` — aggiunti `pdfplumber` e `openai`

### Numeri chiave
- **7 PDF elaborati** → 7 JSON individuali
- **63 interventi totali** in `dataset_completo.json`
- **5 interventi B.x** (B.1–B.5) con codifica canonica CT
- **36/36 pytest PASS** — nessuna regressione

## Deviazioni dal task originale

| Punto task | Deviazione | Motivo |
|---|---|---|
| `google/gemini-flash-1.5` | Usato `google/gemini-2.0-flash-001` | Il modello specificato non esiste su OpenRouter (HTTP 404); `gemini-2.0-flash-001` è la versione stabile più vicina |
| Codici B.x nei PDF | I documenti GSE usano "4.1.a", "1.A", "2.A" etc. (non B.x) | La codifica B.x è una convenzione usata in tools.py — i 5 interventi B.1-B.5 sono stati aggiunti dal DM 16/02/2016 art.4 |
| `ensure_ascii=False` | Salvato con `ensure_ascii=True` | Windows cp1252 incompatibile con il comando DoD `open('data/...')` senza encoding |

## Struttura dataset_completo.json

```json
{
  "documenti": [...],        // 7 documenti con sezioni, tariffe, requisiti
  "interventi": [...],       // 63 totali: 5 B.x + 58 estratti dai PDF
  "totale_documenti": 7,
  "totale_interventi": 63
}
```

## Verifiche superare

```
python -c "import json; d=json.load(open('data/dataset_completo.json')); print(f'Interventi: {len(d[\"interventi\"])}'); print('JSON OK')"
# Interventi: 63 / JSON OK

pytest tests/ -q
# 36 passed in 0.11s
```

## Blocchi per TASK_08

- `data/dataset_completo.json` è pronto per upload su Kaggle
- Tutti i JSON sono in encoding ASCII-safe (leggibili senza specificare encoding)
- Il campo `source` in ogni documento identifica il PDF di origine
