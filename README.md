# 🔥 Conto Termico GSE — Assistente AI con Elysia

Applicazione dimostrativa per la **gestione documentale del Conto Termico GSE**,
costruita su [Elysia](https://github.com/weaviate/elysia) (framework RAG agentico di Weaviate).

---

## 📋 Cosa fa questa applicazione

L'assistente AI può rispondere a domande come:

- *"Questa pompa di calore da 12 kW con COP 3.4 in zona E è ammissibile al Conto Termico?"*
- *"Quali documenti devo presentare per un solare termico?"*
- *"Stima l'incentivo per 24 m² di solare termico, cliente privato"*
- *"Qual è lo stato della pratica CT-2024-001234?"*
- *"Cosa dice il decreto sulla cumulabilità con l'Ecobonus?"*

---

## 🏗️ Architettura

```
conto_termico_gse/
├── .env.example        ← Template configurazione API keys
├── import_data.py      ← Popola Weaviate con dati di esempio
├── tools.py            ← Tool personalizzati Elysia per il CT GSE
├── main.py             ← Entry point (web app o console)
└── README.md           ← Questa guida
```

**Stack tecnologico:**
| Componente | Tecnologia |
|---|---|
| Framework AI agentico | Elysia (Weaviate) |
| Vector Database | Weaviate Cloud |
| LLM decision agent | GPT-4.1-mini / Gemini Flash |
| LLM query complesse | GPT-4.1 / Gemini Pro |
| Backend | FastAPI (incluso in Elysia) |
| Frontend | Elysia Web UI |

---

## ✅ Prerequisiti

Prima di iniziare, ti servono:

### 1. Python 3.12
```bash
python --version  # Deve essere 3.12.x
```
Se non ce l'hai: https://www.python.org/downloads/

### 2. Account Weaviate Cloud (GRATIS per 14 giorni)
1. Vai su https://console.weaviate.cloud/
2. Crea un account gratuito
3. Crea un nuovo cluster (scegli "Sandbox" - gratuito)
4. Copia l'**URL del cluster** e l'**API Key** (le trovi nel pannello del cluster)

### 3. API Key LLM (scegli uno)
**Opzione A - OpenAI (consigliato):**
- Vai su https://platform.openai.com/api-keys
- Crea una nuova API Key
- Carica qualche credito (costo stimato per questa demo: < $1)

**Opzione B - Google Gemini (gratuito con limiti generosi):**
- Vai su https://aistudio.google.com/app/apikey
- Ottieni la chiave gratuita

---

## 🚀 Installazione passo-passo

### Passo 1: Clona o scarica il progetto
```bash
# Se hai git:
git clone <url-repo>
cd conto_termico_gse

# Oppure scarica e decomprimi il file ZIP
cd conto_termico_gse
```

### Passo 2: Crea l'ambiente virtuale Python
```bash
python3.12 -m venv .venv

# Attiva su macOS/Linux:
source .venv/bin/activate

# Attiva su Windows:
.venv\Scripts\activate
```
Vedrai `(.venv)` nel prompt del terminale.

### Passo 3: Installa le dipendenze
```bash
pip install elysia-ai weaviate-client python-dotenv
```
> ⏳ Ci vogliono 2-5 minuti, Elysia ha molte dipendenze.

### Passo 4: Configura le API keys
```bash
# Copia il template
cp .env.example .env

# Apri .env con un editor (es. VS Code, Notepad, nano)
# e compila i tuoi valori reali:
```

Modifica il file `.env`:
```env
WCD_URL=https://il-tuo-cluster.weaviate.network
WCD_API_KEY=la-tua-api-key-weaviate
OPENAI_API_KEY=sk-...
```

### Passo 5: Importa i dati di esempio in Weaviate
```bash
python import_data.py
```

Dovresti vedere:
```
🚀 Avvio importazione dati Conto Termico GSE...
✅ Connesso a Weaviate: True
✅ Collection 'Normative' creata
✅ Collection 'Pratiche' creata
✅ Collection 'Impianti' creata
✅ Importate 3 normative
✅ Importate 4 pratiche
✅ Importati 4 impianti
🎉 Importazione completata!
```

### Passo 6: Avvia l'applicazione

**Modalità Web App (consigliata per demo):**
```bash
python main.py
```
Poi apri il browser su: http://localhost:8000

**Modalità Console (per sviluppatori):**
```bash
python main.py --console
```

---

## 🎯 Come usare la Web App

1. **Apri** http://localhost:8000 nel browser
2. Vai in **Settings** (ingranaggio) → aggiungi le tue credenziali se non le hai già nel .env
3. Vai in **Data** → clicca "Analyze" su ogni collection (Normative, Pratiche, Impianti)
4. Vai in **Chat** → inizia a fare domande!

### Domande di esempio da provare:
```
Pompa di calore Daikin 12 kW, COP 3.4, zona E - è ammissibile?
Stima incentivo solare termico 24 m², privato, zona E
Quali documenti servono per una caldaia a biomassa?
Stato pratica CT-2024-001234
Cosa dice il DM 16/02/2016 sulla cumulabilità con Ecobonus?
Elenca tutte le pratiche approvate
Qual è l'incentivo massimo per le pompe di calore?
```

---

## 🔧 Personalizzazione

### Aggiungere nuovi documenti/normative
Aggiungi oggetti alla lista `NORMATIVE` in `import_data.py` e riesegui lo script.

### Aggiungere nuovi tool
In `tools.py`, aggiungi una nuova funzione con il decoratore `@tool`:

```python
@tool(tree=tree, status="⚡ Eseguendo tool personalizzato...")
async def mio_tool_custom(parametro: str):
    """
    Descrizione dettagliata per l'LLM di quando usare questo tool.
    """
    # la tua logica
    yield {"risultato": "..."}
    yield "Messaggio testuale all'utente"
```

### Cambiare modello LLM
Modifica in `main.py`:
```python
configure(
    base_model="gpt-4.1-nano",      # Più economico
    complex_model="gpt-4.1",         # Più potente per le query
    ...
)
```

---

## 📊 Struttura dei dati

### Collection `Normative`
| Campo | Tipo | Descrizione |
|---|---|---|
| codice | text | Codice normativa (es. DM-16-02-2016) |
| titolo | text | Titolo del documento |
| testo | text | Testo completo (vettorizzato) |
| tipo | text | Decreto, Circolare, Nota Tecnica |
| ente | text | MISE, GSE, ARERA... |
| tags | text[] | Parole chiave |

### Collection `Pratiche`
| Campo | Tipo | Descrizione |
|---|---|---|
| codice_pratica | text | Codice univoco (CT-YYYY-XXXXXX) |
| stato | text | In istruttoria, Approvata, Rigettata, Bozza |
| tipo_intervento | text | B.2, B.4, ecc. con descrizione |
| documenti_mancanti | text[] | Lista doc mancanti |
| incentivo_totale_stimato | number | Euro |

### Collection `Impianti`
| Campo | Tipo | Descrizione |
|---|---|---|
| modello | text | Nome modello |
| tipo | text | Pompa di calore, Solare termico... |
| cop_a7w35 | number | COP a +7°C (standard) |
| ammissibile_ct | bool | True/False |
| motivazione_ammissibilita | text | Spiegazione |

---

## ❓ Problemi comuni

**Errore "Connection refused" Weaviate:**
→ Verifica che WCD_URL e WCD_API_KEY nel .env siano corretti

**Errore LLM "API key not found":**
→ Verifica che OPENAI_API_KEY sia impostata e valida

**Tool non trovato / l'agente non usa i tool:**
→ Assicurati che `python import_data.py` sia stato eseguito
→ Nella web app, clicca "Analyze" nel tab Data per ogni collection

**"Collection not found" durante il preprocessing:**
→ Esegui prima `python import_data.py`

---

## 📚 Risorse utili

- [Documentazione Elysia](https://weaviate.github.io/elysia/)
- [GitHub Elysia](https://github.com/weaviate/elysia)
- [Weaviate Cloud Console](https://console.weaviate.cloud/)
- [GSE Conto Termico](https://www.gse.it/servizi-per-te/efficienza-energetica/conto-termico)
- [DM 16/02/2016 testo ufficiale](https://www.gse.it/documenti_site/Documenti%20GSE/Conto%20Termico)

---

*Progetto dimostrativo — i dati GSE inclusi sono fittizi e a solo scopo illustrativo.*
