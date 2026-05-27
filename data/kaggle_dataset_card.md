# Normative GSE — Conto Termico Dataset

## Panoramica

Dataset strutturato delle normative italiane del **Conto Termico GSE** (Gestore dei Servizi Energetici),
estratto da PDF ufficiali con Gemini API e organizzato in formato JSON per applicazioni AI/NLP.

Copre **CT 2.0** (DM 16/02/2016) e **CT 3.0** (2026), il meccanismo di incentivazione
per l'efficienza energetica e la produzione di energia termica da fonti rinnovabili in Italia.

---

## Statistiche

| Metrica | Valore |
|---|---|
| Documenti totali | 7 |
| Sezioni estratte | 72 |
| Interventi ammissibili | 58 |
| Requisiti tecnici | 20 |
| Riferimenti normativi | 29 |
| Versioni CT coperte | CT 2.0, CT 3.0 |
| Lingua | Italiano |
| Formato | JSON |
| Licenza | MIT |

---

## Struttura del dataset

```
data/
├── dataset_completo.json          ← dataset principale (tutti i documenti)
├── decreto_dm_16_02_2016.json     ← DM 16/02/2016 singolo
├── allegato_criteri_ammissibilita.json
├── regole_applicative_ct.json     ← Regole Applicative CT 2.0
├── ct3_webinar_2026.json          ← Presentazione CT 3.0
├── guida_ct_pubblica_amministrazione.json
├── mappa_ct_imprese_privati.json
└── pompe_di_calore_regole_applicative.json
```

### Schema `dataset_completo.json`

```json
{
  "documenti": [
    {
      "source": "nome_file.pdf",
      "tipo": "decreto | allegato | regole_applicative | guida",
      "data_documento": "YYYY-MM-DD",
      "versione": "CT 2.0 | CT 3.0",
      "sezioni": [
        {
          "titolo": "Titolo sezione",
          "contenuto": "Testo estratto...",
          "pagina": 3,
          "tags": ["keyword1", "keyword2"]
        }
      ],
      "interventi": [
        {
          "codice": "1.A",
          "descrizione": "Isolamento termico superfici opache...",
          "requisiti": ["Trasmittanza termica massima..."],
          "incentivo": {},
          "zone_climatiche": ["A", "B", "C", "D", "E", "F"]
        }
      ],
      "tariffe": [],
      "requisiti_tecnici": ["COP minimo...", "..."],
      "citations": ["DM 16/02/2016", "UNI EN 14511", "..."]
    }
  ]
}
```

---

## Documenti inclusi

| Documento | Tipo | Versione CT | Sezioni | Interventi |
|---|---|---|---|---|
| DM 16/02/2016 | Decreto ministeriale | CT 2.0 | 7 | 12 |
| Allegato criteri ammissibilità | Allegato tecnico | CT 2.0 | 2 | 6 |
| Regole Applicative CT | Regole operative | CT 2.0 | 18 | 12 |
| Webinar CT 3.0 (2026) | Presentazione ufficiale | CT 3.0 | 18 | 9 |
| Guida PA | Guida operativa | CT 2.0 | 12 | 13 |
| Mappa interventi privati | Guida operativa | CT 2.0 | 9 | 5 |
| Regole pompe di calore | Regole tecniche | CT 2.0 | 6 | 1 |

---

## Interventi ammissibili (CT 2.0 — Regole Applicative)

### Titolo II — Riqualificazione energetica (PA e privati)

| Codice | Descrizione |
|---|---|
| 1.A | Isolamento termico di superfici opache (coperture, pavimenti, pareti) |
| 1.B | Sostituzione di chiusure trasparenti comprensive di infissi |
| 1.C | Sostituzione con generatori di calore a condensazione |
| 1.D | Installazione di sistemi di schermatura e ombreggiamento |
| 1.E | Trasformazione in edifici a energia quasi zero (NZEB) |
| 1.F | Sostituzione con sistemi di illuminazione efficienti |
| 1.G | Building automation — termoregolazione e contabilizzazione calore |

### Titolo III — Fonti rinnovabili e alta efficienza (PA e privati)

| Codice | Descrizione |
|---|---|
| 2.A | Pompe di calore elettriche o a gas (fino a 2000 kW) |
| 2.B | Generatori di calore a biomassa (fino a 2000 kW) |
| 2.C | Collettori solari termici (fino a 2500 m²) |
| 2.D | Sostituzione scaldacqua elettrici con scaldacqua a pompa di calore |
| 2.E | Sistemi ibridi a pompa di calore |

---

## Casi d'uso

### RAG su normativa italiana
Il dataset è ottimale per sistemi di Retrieval-Augmented Generation su normativa specialistica.
Ogni sezione estratta include metadati (fonte, pagina, tipo, versione CT) per il retrieval contestuale.

```python
# Preparazione chunk per vector store
chunks = []
for doc in dataset['documenti']:
    for sezione in doc['sezioni']:
        if sezione.get('contenuto'):
            chunks.append({
                'text': sezione['contenuto'],
                'metadata': {
                    'fonte': doc['source'],
                    'versione': doc['versione'],
                    'titolo': sezione['titolo'],
                    'pagina': sezione['pagina'],
                }
            })
```

### Fine-tuning LLM
Gli interventi con requisiti tecnici forniscono coppie `(domanda, risposta)` naturali
per il fine-tuning di modelli specializzati su normativa energetica italiana.

### Analisi NLP
Testo normativo tecnico italiano per task di:
- Classificazione documenti
- Named Entity Recognition (codici normativi, tecnologie, zone climatiche)
- Estrazione relazioni (intervento → requisiti → incentivo)

---

## Pipeline di estrazione

```
PDF ufficiali GSE (pubblici)
         │
         ▼
    pdfplumber          ← estrazione testo grezzo
         │
         ▼
    Gemini 2.0 Flash    ← strutturazione JSON via prompt
         │
         ▼
    Validazione JSON    ← schema fisso per coerenza
         │
         ▼
    dataset_completo.json
```

**Il notebook `notebooks/estrazione_normative_gse.ipynb` documenta l'intero processo
ed è eseguibile senza API key**, usando i dati già estratti.

---

## Come usare su Kaggle

```python
import json
from pathlib import Path

# Percorso dataset su Kaggle
DATA_PATH = Path('/kaggle/input/conto-termico-gse-normative/dataset_completo.json')

with open(DATA_PATH, encoding='utf-8') as f:
    dataset = json.load(f)

documenti = dataset['documenti']
print(f'Documenti caricati: {len(documenti)}')
```

---

## Progetto correlato

Questo dataset alimenta **conto-termico-gse**, un assistente AI agentico che risponde
a domande di ammissibilità CT GSE usando RAG su Weaviate.

🔗 **Repository:** [github.com/MaurizioLisanti/conto-termico-gse](https://github.com/MaurizioLisanti/conto-termico-gse)

---

## Community — Linux PropLUG

Dataset creato da **Maurizio Lisanti** nell'ambito di **Linux PropLUG**,
l'associazione Linux di Baronissi (SA) che promuove il software libero e open source
nella comunità tecnica campana.

🌐 [https://proplug.it](https://proplug.it)

Contribuzioni benvenute — apri una Issue o PR sul repository GitHub.

---

## Fonti

I PDF sono documenti ufficiali disponibili pubblicamente su:
- [GSE — Conto Termico](https://www.gse.it/servizi-per-te/efficienza-energetica/conto-termico)
- [MiTE — Decreti efficienza energetica](https://www.mite.gov.it)

---

## Licenza

**MIT License** — vedi [LICENSE](../LICENSE).

I testi normativi estratti sono atti pubblici ai sensi della legge italiana.

---

*Versione dataset: 1.0.0 — Maggio 2026*
