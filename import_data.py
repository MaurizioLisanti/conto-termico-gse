"""
import_data.py
=============
Importa dati di esempio (fittizi ma realistici) nelle collection Weaviate
per la demo del Conto Termico GSE.

Esegui UNA VOLTA prima di avviare l'applicazione:
    python import_data.py
"""

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

WCD_URL = os.environ["WCD_URL"]
WCD_API_KEY = os.environ["WCD_API_KEY"]
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# ─────────────────────────────────────────
# DATI FITTIZI — NORMATIVE GSE
# ─────────────────────────────────────────
NORMATIVE = [
    {
        "codice": "DM-16-02-2016",
        "titolo": "Decreto Ministeriale 16 febbraio 2016 - Conto Termico 2.0",
        "tipo": "Decreto",
        "ente": "MISE",
        "data_pubblicazione": "2016-02-16",
        "testo": """
Il Decreto Ministeriale 16 febbraio 2016 aggiorna il meccanismo di incentivazione 
per interventi di piccole dimensioni per l'incremento dell'efficienza energetica 
e per la produzione di energia termica da fonti rinnovabili (Conto Termico 2.0).

SOGGETTI AMMESSI:
- Pubblica Amministrazione (PA): edifici, impianti e infrastrutture esistenti
- Soggetti privati: imprese e privati cittadini

INTERVENTI INCENTIVABILI (Tipologia A - Solo PA):
A.1 - Isolamento termico di superfici opache delimitanti il volume climatizzato
A.2 - Sostituzione di chiusure trasparenti comprese gli infissi
A.3 - Sostituzione di impianti di climatizzazione invernale con impianti a pompa di calore

INTERVENTI INCENTIVABILI (Tipologia B - PA e Privati):
B.1 - Sostituzione di impianti di climatizzazione invernale con caldaie a condensazione
B.2 - Sostituzione di impianti di climatizzazione invernale con pompe di calore
B.3 - Sostituzione di scaldacqua elettrici con scaldacqua a pompa di calore
B.4 - Installazione di collettori solari termici (incluso il solare a concentrazione)
B.5 - Sostituzione di impianti di climatizzazione invernale con generatori di calore a biomassa
B.6 - Sistemi ibridi a pompa di calore
B.7 - Connessione di edifici a sistemi di teleriscaldamento

INCENTIVI:
L'incentivo è una somma annuale costante per un periodo di 2 o 5 anni a seconda dell'intervento.
Per pompe di calore e solare termico: 5 anni.
Per caldaie a condensazione: 2 anni.

POTENZA MASSIMA:
- Solare termico: nessun limite di taglia
- Pompe di calore: fino a 2000 kW termici
- Caldaie a biomassa: fino a 2000 kW termici

VINCOLI TEMPORALI:
La domanda di incentivazione deve essere inviata al GSE entro 60 giorni 
dalla data di conclusione dei lavori.
""",
        "url_fonte": "https://www.gse.it/servizi-per-te/efficienza-energetica/conto-termico",
        "tags": ["pompa di calore", "solare termico", "biomassa", "caldaia condensazione", "incentivi", "PA", "privati"]
    },
    {
        "codice": "CIRC-GSE-2023-CT",
        "titolo": "Circolare GSE 2023 - Chiarimenti procedure Conto Termico",
        "tipo": "Circolare",
        "ente": "GSE",
        "data_pubblicazione": "2023-03-15",
        "testo": """
CHIARIMENTI PROCEDURALI CONTO TERMICO - ANNO 2023

1. DOCUMENTAZIONE TECNICA RICHIESTA
La documentazione tecnica per accedere al Conto Termico deve includere:
- Relazione tecnica descrittiva dell'intervento firmata da tecnico abilitato
- Documentazione fotografica ante-operam e post-operam
- Schede tecniche dei componenti installati (con marcatura CE)
- Certificato di conformità dell'impianto (modello CPI o dichiarazione di conformità)
- APE (Attestato di Prestazione Energetica) pre e post intervento (solo per PA)
- Fatture o ricevute dei pagamenti (tracciabili, no contanti)

2. PROCEDURA DI ACCESSO DIRETTO (interventi < 5.000 € di incentivo annuo)
Gli interventi con incentivo annuo inferiore a 5.000 € accedono tramite 
"Accesso Diretto": la domanda si invia entro 60 giorni dai lavori sul portale GSE.
Il GSE deve rispondere entro 60 giorni dalla ricezione della domanda completa.

3. PROCEDURA A PRENOTAZIONE (interventi ≥ 5.000 € di incentivo annuo)
Per incentivi annui pari o superiori a 5.000 €, è prevista la "Prenotazione":
- Il soggetto responsabile prenota l'incentivo prima dell'avvio dei lavori
- Ha 12 mesi per completare i lavori e inviare la documentazione finale
- Il GSE rilascia una prenotazione vincolante per 12 mesi

4. CUMULABILITÀ
Il Conto Termico NON è cumulabile con altri incentivi statali sullo stesso intervento.
È invece cumulabile con incentivi regionali/locali, salvo diversa disposizione regionale.
NON cumulabile con Ecobonus, Superbonus 110%, Bonus Ristrutturazioni per lo stesso intervento.

5. REQUISITI TECNICI POMPE DI CALORE
Per le pompe di calore (B.2):
- COP minimo: 2,6 (per clima freddo) o 3,0 (per clima medio)
- EER minimo per pompe di calore reversibili: 2,4
- Certificazione EHPA o equivalente
- Potenza nominale: da 5 kW a 2.000 kW termici

6. REQUISITI TECNICI SOLARE TERMICO
Per i collettori solari termici (B.4):
- Efficienza a η0 ≥ 0,7 (piani) o η0 ≥ 0,65 (tubi evacuati)
- Certificazione Solar Keymark o equivalente europea
- Area totale (lorda) minima: 1,5 m²
""",
        "url_fonte": "https://www.gse.it/documenti_site/Documenti%20GSE/Conto%20Termico",
        "tags": ["documentazione", "procedura", "accesso diretto", "prenotazione", "cumulabilità", "requisiti tecnici"]
    },
    {
        "codice": "NOTA-GSE-2024-POMPE",
        "titolo": "Nota Tecnica GSE 2024 - Requisiti minimi pompe di calore",
        "tipo": "Nota Tecnica",
        "ente": "GSE",
        "data_pubblicazione": "2024-01-10",
        "testo": """
NOTA TECNICA: REQUISITI MINIMI POMPE DI CALORE - CONTO TERMICO 2024

CLASSIFICAZIONE PER ZONA CLIMATICA:
Zone A e B (clima mite):    COP ≥ 2.6, SCOP ≥ 3.2
Zone C e D (clima medio):   COP ≥ 2.8, SCOP ≥ 3.5  
Zone E e F (clima freddo):  COP ≥ 3.0, SCOP ≥ 3.8

TEMPERATURE DI PROVA (EN 14511):
- Aria-Acqua: A7/W35 (COP a +7°C aria esterna, +35°C mandata)
- Aria-Aria: A7/W20 (riscaldamento a +7°C)
- Geotermiche: W10/W35

DOCUMENTI OBBLIGATORI:
1. Scheda tecnica del costruttore con i valori COP/SCOP certificati
2. Certificato di test da laboratorio accreditato EN 14511
3. Certificazione EHPA Gold o Solar Keymark (sistemi ibridi)
4. Dichiarazione CE del costruttore

POTENZA INCENTIVABILE:
La potenza termina utile (kW) deve essere verificata al punto di funzionamento 
nominale dichiarato dal costruttore. Non si accettano potenze stimate o calcolate 
dall'installatore.

INTERVENTI IN SOSTITUZIONE:
Devono dimostrare la dismissione del vecchio generatore (fotografie + dichiarazione 
del tecnico). Il vecchio generatore deve essere smaltito in conformità al D.Lgs 49/2014.
""",
        "url_fonte": "https://www.gse.it",
        "tags": ["pompa di calore", "COP", "SCOP", "requisiti tecnici", "zona climatica", "EN 14511"]
    }
]

# ─────────────────────────────────────────
# DATI FITTIZI — PRATICHE
# ─────────────────────────────────────────
PRATICHE = [
    {
        "codice_pratica": "CT-2024-001234",
        "tipo_soggetto": "Privato",
        "nome_richiedente": "Mario Rossi",
        "tipo_intervento": "B.2 - Pompa di calore aria-acqua",
        "indirizzo_impianto": "Via Roma 15, Milano (MI) - Zona E",
        "data_lavori_fine": "2024-03-20",
        "data_invio_domanda": "2024-05-10",
        "stato": "In istruttoria",
        "potenza_kw": 12.0,
        "incentivo_annuo_stimato": 1850.0,
        "durata_anni": 5,
        "incentivo_totale_stimato": 9250.0,
        "documenti_presenti": ["Relazione tecnica", "Foto ante-operam", "Foto post-operam", "Fatture", "Scheda tecnica"],
        "documenti_mancanti": ["Dichiarazione di conformità impianto", "APE post-intervento"],
        "note": "Domanda ricevuta in data 10/05/2024. Richiesta integrazione documenti inviata il 25/05/2024.",
        "tecnico_responsabile": "Ing. Luigi Bianchi",
        "marca_modello": "Daikin Altherma 3 R ECH+O - 12 kW",
        "cop_certificato": 3.4
    },
    {
        "codice_pratica": "CT-2024-005678",
        "tipo_soggetto": "Pubblica Amministrazione",
        "nome_richiedente": "Comune di Bergamo",
        "tipo_intervento": "B.4 - Solare termico",
        "indirizzo_impianto": "Piazza Vecchia 1, Bergamo (BG) - Zona E",
        "data_lavori_fine": "2024-01-15",
        "data_invio_domanda": "2024-03-01",
        "stato": "Approvata",
        "potenza_kw": None,
        "superficie_mq": 24.5,
        "incentivo_annuo_stimato": 3200.0,
        "durata_anni": 5,
        "incentivo_totale_stimato": 16000.0,
        "documenti_presenti": ["Relazione tecnica", "Foto ante-operam", "Foto post-operam", "Fatture", "Scheda tecnica", "Dichiarazione di conformità impianto", "APE pre e post", "Solar Keymark"],
        "documenti_mancanti": [],
        "note": "Pratica approvata il 15/06/2024. Incentivo erogato dalla data di approvazione.",
        "tecnico_responsabile": "Arch. Francesca Conti",
        "marca_modello": "Viessmann Vitosol 300-F - 24,5 m²",
        "cop_certificato": None,
        "efficienza_eta0": 0.81
    },
    {
        "codice_pratica": "CT-2023-009900",
        "tipo_soggetto": "Privato",
        "nome_richiedente": "Azienda Agricola Martinelli Srl",
        "tipo_intervento": "B.5 - Caldaia a biomassa (pellet)",
        "indirizzo_impianto": "Via Campagna 8, Brescia (BS) - Zona E",
        "data_lavori_fine": "2023-10-05",
        "data_invio_domanda": "2023-11-28",
        "stato": "Rigettata",
        "potenza_kw": 85.0,
        "incentivo_annuo_stimato": 4200.0,
        "durata_anni": 5,
        "incentivo_totale_stimato": 21000.0,
        "documenti_presenti": ["Relazione tecnica", "Fatture", "Scheda tecnica"],
        "documenti_mancanti": ["Foto ante-operam", "Certificato emissioni (EN 303-5)", "Dichiarazione di conformità impianto"],
        "note": "Pratica rigettata per mancanza della certificazione emissioni EN 303-5 e assenza foto ante-operam. Possibile ri-presentazione con documentazione completa.",
        "tecnico_responsabile": "Per. Ind. Roberto Ferrara",
        "marca_modello": "Herz BioMatic 80 kW",
        "cop_certificato": None
    },
    {
        "codice_pratica": "CT-2024-012345",
        "tipo_soggetto": "Privato",
        "nome_richiedente": "Giulia Verdi",
        "tipo_intervento": "B.3 - Scaldacqua a pompa di calore",
        "indirizzo_impianto": "Via Garibaldi 22, Roma (RM) - Zona C",
        "data_lavori_fine": "2024-06-01",
        "data_invio_domanda": None,
        "stato": "Bozza - non ancora inviata",
        "potenza_kw": 3.0,
        "incentivo_annuo_stimato": 320.0,
        "durata_anni": 2,
        "incentivo_totale_stimato": 640.0,
        "documenti_presenti": ["Fatture", "Scheda tecnica"],
        "documenti_mancanti": ["Relazione tecnica", "Foto ante-operam", "Foto post-operam", "Dichiarazione di conformità impianto"],
        "note": "ATTENZIONE: scadenza invio domanda entro il 30/07/2024 (60 giorni dalla fine lavori il 01/06/2024). Urgente completare la documentazione.",
        "tecnico_responsabile": "Non assegnato",
        "marca_modello": "Ariston Nuos Primo 80",
        "cop_certificato": 3.1
    }
]

# ─────────────────────────────────────────
# DATI FITTIZI — IMPIANTI
# ─────────────────────────────────────────
IMPIANTI = [
    {
        "modello": "Daikin Altherma 3 R ECH+O",
        "tipo": "Pompa di calore aria-acqua",
        "marca": "Daikin",
        "potenza_kw": 12.0,
        "cop_a7w35": 3.4,
        "cop_a2w35": 2.8,
        "scop_zona_e": 3.6,
        "classe_energetica": "A+++",
        "certificazioni": ["EHPA Gold", "EN 14511", "CE"],
        "prezzo_indicativo_eur": 8500.0,
        "adatto_per": "Abitazioni residenziali con radiatori a bassa temperatura o pavimento radiante",
        "note_tecniche": "Compatibile con sistemi idroni esistenti. Funziona fino a -25°C. Incluso bollitore 180L.",
        "ammissibile_ct": True,
        "motivazione_ammissibilita": "COP 3.4 > soglia minima 2.8 per zona E. Certificazione EHPA Gold presente."
    },
    {
        "modello": "Viessmann Vitosol 300-F",
        "tipo": "Collettore solare termico piano",
        "marca": "Viessmann",
        "potenza_kw": None,
        "superficie_unitaria_mq": 2.51,
        "efficienza_eta0": 0.81,
        "coefficiente_a1": 3.325,
        "classe_energetica": "A+",
        "certificazioni": ["Solar Keymark", "EN 12975", "CE"],
        "prezzo_indicativo_eur_mq": 450.0,
        "adatto_per": "Produzione ACS e riscaldamento per edifici residenziali e commerciali",
        "note_tecniche": "Rivestimento selettivo TiNOX. Ottimo anche in condizioni di nuvolosità.",
        "ammissibile_ct": True,
        "motivazione_ammissibilita": "Efficienza η0 = 0.81 > soglia minima 0.70. Certificazione Solar Keymark presente."
    },
    {
        "modello": "Ariston Nuos Primo 80",
        "tipo": "Scaldacqua a pompa di calore",
        "marca": "Ariston",
        "potenza_kw": 1.2,
        "cop_nominale": 3.1,
        "volume_litri": 80,
        "classe_energetica": "A+",
        "certificazioni": ["EN 16147", "CE"],
        "prezzo_indicativo_eur": 950.0,
        "adatto_per": "Sostituzione scaldacqua elettrico in abitazioni monofamiliari o appartamenti",
        "note_tecniche": "Consumo annuo stimato 230 kWh vs 900 kWh dello scaldacqua elettrico tradizionale.",
        "ammissibile_ct": True,
        "motivazione_ammissibilita": "COP 3.1 > soglia minima. Rientra nella tipologia B.3 del CT 2.0."
    },
    {
        "modello": "Generatore caldaia standard non condensazione",
        "tipo": "Caldaia a gas non condensante",
        "marca": "Generico",
        "potenza_kw": 24.0,
        "rendimento_pci": 0.87,
        "classe_energetica": "D",
        "certificazioni": ["CE"],
        "prezzo_indicativo_eur": 600.0,
        "adatto_per": "Non consigliato per nuove installazioni",
        "note_tecniche": "Prodotto legacy, non più vendibile in UE per riscaldamento ambienti dal 2015.",
        "ammissibile_ct": False,
        "motivazione_ammissibilita": "NON AMMISSIBILE: le caldaie non a condensazione non rientrano negli interventi incentivabili del Conto Termico 2.0."
    }
]

# ─────────────────────────────────────────
# FUNZIONI DI IMPORTAZIONE
# ─────────────────────────────────────────

def get_client():
    """Connette a Weaviate Cloud."""
    headers = {}
    if OPENAI_API_KEY:
        headers["X-OpenAI-Api-Key"] = OPENAI_API_KEY

    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WCD_URL,
        auth_credentials=Auth.api_key(WCD_API_KEY),
        headers=headers if headers else None
    )
    print(f"✅ Connesso a Weaviate: {client.is_ready()}")
    return client


def create_collections(client):
    """Crea le collection se non esistono."""

    # --- Collection: Normative ---
    if not client.collections.exists("Normative"):
        client.collections.create(
            name="Normative",
            vector_config=[
                Configure.Vectors.text2vec_openai(
                    name="default",
                    source_properties=["titolo", "testo"],
                )
            ],
            properties=[
                Property(name="codice", data_type=DataType.TEXT),
                Property(name="titolo", data_type=DataType.TEXT),
                Property(name="tipo", data_type=DataType.TEXT),
                Property(name="ente", data_type=DataType.TEXT),
                Property(name="data_pubblicazione", data_type=DataType.TEXT),
                Property(name="testo", data_type=DataType.TEXT),
                Property(name="url_fonte", data_type=DataType.TEXT),
                Property(name="tags", data_type=DataType.TEXT_ARRAY),
            ]
        )
        print("✅ Collection 'Normative' creata")
    else:
        print("ℹ️  Collection 'Normative' già esiste")

    # --- Collection: Pratiche ---
    if not client.collections.exists("Pratiche"):
        client.collections.create(
            name="Pratiche",
            vector_config=[
                Configure.Vectors.text2vec_openai(
                    name="default",
                    source_properties=["tipo_intervento", "note", "tipo_soggetto"],
                )
            ],
            properties=[
                Property(name="codice_pratica", data_type=DataType.TEXT),
                Property(name="tipo_soggetto", data_type=DataType.TEXT),
                Property(name="nome_richiedente", data_type=DataType.TEXT),
                Property(name="tipo_intervento", data_type=DataType.TEXT),
                Property(name="indirizzo_impianto", data_type=DataType.TEXT),
                Property(name="data_lavori_fine", data_type=DataType.TEXT),
                Property(name="data_invio_domanda", data_type=DataType.TEXT),
                Property(name="stato", data_type=DataType.TEXT),
                Property(name="potenza_kw", data_type=DataType.NUMBER),
                Property(name="incentivo_annuo_stimato", data_type=DataType.NUMBER),
                Property(name="durata_anni", data_type=DataType.INT),
                Property(name="incentivo_totale_stimato", data_type=DataType.NUMBER),
                Property(name="documenti_presenti", data_type=DataType.TEXT_ARRAY),
                Property(name="documenti_mancanti", data_type=DataType.TEXT_ARRAY),
                Property(name="note", data_type=DataType.TEXT),
                Property(name="tecnico_responsabile", data_type=DataType.TEXT),
                Property(name="marca_modello", data_type=DataType.TEXT),
                Property(name="cop_certificato", data_type=DataType.NUMBER),
            ]
        )
        print("✅ Collection 'Pratiche' creata")
    else:
        print("ℹ️  Collection 'Pratiche' già esiste")

    # --- Collection: Impianti ---
    if not client.collections.exists("Impianti"):
        client.collections.create(
            name="Impianti",
            vector_config=[
                Configure.Vectors.text2vec_openai(
                    name="default",
                    source_properties=["modello", "tipo", "adatto_per", "note_tecniche"],
                )
            ],
            properties=[
                Property(name="modello", data_type=DataType.TEXT),
                Property(name="tipo", data_type=DataType.TEXT),
                Property(name="marca", data_type=DataType.TEXT),
                Property(name="potenza_kw", data_type=DataType.NUMBER),
                Property(name="cop_a7w35", data_type=DataType.NUMBER),
                Property(name="scop_zona_e", data_type=DataType.NUMBER),
                Property(name="classe_energetica", data_type=DataType.TEXT),
                Property(name="certificazioni", data_type=DataType.TEXT_ARRAY),
                Property(name="prezzo_indicativo_eur", data_type=DataType.NUMBER),
                Property(name="adatto_per", data_type=DataType.TEXT),
                Property(name="note_tecniche", data_type=DataType.TEXT),
                Property(name="ammissibile_ct", data_type=DataType.BOOL),
                Property(name="motivazione_ammissibilita", data_type=DataType.TEXT),
            ]
        )
        print("✅ Collection 'Impianti' creata")
    else:
        print("ℹ️  Collection 'Impianti' già esiste")


def import_all_data(client):
    """Importa tutti i dati nelle collection."""

    # --- Normative ---
    normative_coll = client.collections.get("Normative")
    with normative_coll.batch.fixed_size(batch_size=10) as batch:
        for item in NORMATIVE:
            batch.add_object(item)
    print(f"✅ Importate {len(NORMATIVE)} normative")

    # --- Pratiche ---
    pratiche_coll = client.collections.get("Pratiche")
    with pratiche_coll.batch.fixed_size(batch_size=10) as batch:
        for item in PRATICHE:
            # Rimuovi None per evitare errori Weaviate
            clean_item = {k: v for k, v in item.items() if v is not None}
            batch.add_object(clean_item)
    print(f"✅ Importate {len(PRATICHE)} pratiche")

    # --- Impianti ---
    impianti_coll = client.collections.get("Impianti")
    with impianti_coll.batch.fixed_size(batch_size=10) as batch:
        for item in IMPIANTI:
            clean_item = {k: v for k, v in item.items() if v is not None}
            batch.add_object(clean_item)
    print(f"✅ Importati {len(IMPIANTI)} impianti")


def verify_import(client):
    """Verifica quanti oggetti sono stati importati."""
    for name in ["Normative", "Pratiche", "Impianti"]:
        coll = client.collections.get(name)
        count = coll.aggregate.over_all(total_count=True).total_count
        print(f"  📦 {name}: {count} oggetti")


if __name__ == "__main__":
    print("\n🚀 Avvio importazione dati Conto Termico GSE...\n")
    client = get_client()
    try:
        print("\n📂 Creazione collection...")
        create_collections(client)
        print("\n📥 Importazione dati...")
        import_all_data(client)
        print("\n✅ Verifica importazione:")
        verify_import(client)
        print("\n🎉 Importazione completata! Ora puoi avviare Elysia con:")
        print("   python main.py\n")
    finally:
        client.close()
