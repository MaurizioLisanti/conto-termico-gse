# TASK_07_dataset.md

## Metadata
- task: TASK_07_dataset
- status: TODO
- priority: HIGH
- risk: MED
- blocked_by: —
- blocks: TASK_08_kaggle

## Obiettivo
Estrarre il contenuto strutturato dai 7 PDF ufficiali GSE
usando Claude API con Citations API.
Produrre file JSON normalizzati nella cartella data/.

## Allowed Paths
- data/                          (nuova cartella)
- data/decreto_dm_16_02_2016.json
- data/allegato_criteri_ammissibilita.json
- data/regole_applicative_ct.json
- data/ct3_webinar_2026.json
- data/guida_ct_pubblica_amministrazione.json
- data/mappa_ct_imprese_privati.json
- data/pompe_di_calore_regole_applicative.json
- data/dataset_completo.json
- scripts/extract_pdf.py         (nuovo script)
- requirements.txt               (aggiunta anthropic)

## Struttura JSON per ogni documento

```json
{
  "source": "nome_file.pdf",
  "tipo": "decreto | regole_applicative | allegato | guida",
  "data_documento": "2016-02-16",
  "versione": "CT 2.0 | CT 3.0",
  "sezioni": [
    {
      "titolo": "Articolo 1 — Definizioni",
      "contenuto": "testo estratto...",
      "pagina": 1,
      "tags": ["definizioni", "soggetti_ammessi"]
    }
  ],
  "interventi": [
    {
      "codice": "B.1",
      "descrizione": "Caldaie a condensazione",
      "requisiti": [],
      "incentivo": {},
      "zone_climatiche": []
    }
  ],
  "tariffe": [],
  "requisiti_tecnici": [],
  "citations": []
}
```

## Script da creare: scripts/extract_pdf.py

Lo script deve:
1. Leggere ogni PDF da raw/ in base64
2. Inviarlo a Claude API (claude-sonnet-4-20250514)
   con prompt di estrazione strutturata
3. Richiedere risposta SOLO in JSON valido
4. Salvare il JSON in data/
5. Alla fine unire tutti i JSON in data/dataset_completo.json

Prompt di estrazione da usare nella API call:
"Sei un esperto di normativa energetica italiana.
Analizza questo documento ufficiale GSE sul Conto Termico.
Estrai e struttura in JSON:
- Tipo documento e data
- Tutte le sezioni con titolo e contenuto
- Interventi ammissibili con codice (B.1, B.2 ecc)
- Requisiti tecnici (COP, certificazioni, soglie)
- Tariffe incentivo per tipo intervento
- Zone climatiche e relativi requisiti
Rispondi SOLO con JSON valido, nessun testo aggiuntivo."

## Definition of Done
- [ ] cartella data/ con 7 JSON + dataset_completo.json
- [ ] scripts/extract_pdf.py funzionante
- [ ] python scripts/extract_pdf.py → PASS senza errori
- [ ] pytest tests/ -q → ancora 36/36 PASS
- [ ] dataset_completo.json ha almeno 3 interventi
      con codice B.x documentati

## Comandi verifica
python scripts/extract_pdf.py
python -c "import json; d=json.load(open('data/dataset_completo.json')); print(f'Interventi: {len(d[\"interventi\"])}'); print('JSON OK')"
pytest tests/ -q