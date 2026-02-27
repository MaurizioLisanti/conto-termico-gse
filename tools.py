"""
tools.py
========
Tool personalizzati Elysia per la gestione del Conto Termico GSE.

Ogni tool è una funzione async decorata con @tool.
Il docstring descrive all'LLM quando e come usare il tool.
"""

from elysia import tool, Error, Tree


def register_tools(tree: Tree):
    """Registra tutti i tool custom nel tree Elysia."""

    # ─────────────────────────────────────────────────────────
    # TOOL 1: Verifica ammissibilità impianto
    # ─────────────────────────────────────────────────────────
    @tool(tree=tree, end=False, status="🔍 Verifico ammissibilità impianto...")
    async def verifica_ammissibilita(
        tipo_impianto: str,
        potenza_kw: float = None,
        cop_certificato: float = None,
        zona_climatica: str = None,
        superficie_mq: float = None,
        certificazioni: list[str] = None,
        client_manager=None
    ):
        """
        Verifica se un impianto o una tecnologia è ammissibile al Conto Termico GSE.
        
        Usa questo tool quando l'utente chiede:
        - "Questo impianto è ammissibile al Conto Termico?"
        - "Posso incentivare questa pompa di calore?"
        - "Il mio solare termico rientra nel CT?"
        - Qualsiasi domanda su ammissibilità, idoneità, requisiti di un impianto specifico.
        
        Parametri:
        - tipo_impianto: tipo di impianto (es. "pompa di calore aria-acqua", "solare termico", "caldaia biomassa")
        - potenza_kw: potenza nominale in kW (opzionale)
        - cop_certificato: COP certificato dell'impianto (opzionale, per pompe di calore)
        - zona_climatica: zona climatica dell'edificio A/B/C/D/E/F (opzionale)
        - superficie_mq: superficie collettori in m² (opzionale, per solare termico)
        - certificazioni: lista certificazioni presenti (opzionale)
        - client_manager: client Weaviate (iniettato automaticamente da Elysia)
        """

        # Soglie minime per zona climatica (pompe di calore)
        soglie_cop = {
            "A": 2.6, "B": 2.6,
            "C": 2.8, "D": 2.8,
            "E": 3.0, "F": 3.0
        }

        risultati = {
            "tipo_impianto": tipo_impianto,
            "ammissibile": None,
            "motivazione": "",
            "requisiti_mancanti": [],
            "raccomandazioni": []
        }

        tipo_lower = tipo_impianto.lower()

        # --- Pompa di calore ---
        if "pompa di calore" in tipo_lower or "heat pump" in tipo_lower:
            tipo_intervento = "B.2 - Pompe di calore per climatizzazione invernale"
            risultati["tipo_intervento_ct"] = tipo_intervento
            risultati["durata_incentivo"] = "5 anni"

            problemi = []

            if cop_certificato and zona_climatica:
                soglia = soglie_cop.get(zona_climatica.upper(), 2.8)
                if cop_certificato >= soglia:
                    risultati["ammissibile"] = True
                    risultati["motivazione"] = f"COP {cop_certificato} ≥ soglia minima {soglia} per zona {zona_climatica}. ✅"
                else:
                    problemi.append(f"COP {cop_certificato} < soglia minima {soglia} per zona {zona_climatica}")
            elif cop_certificato and not zona_climatica:
                risultati["raccomandazioni"].append("Specifica la zona climatica per una verifica precisa del COP minimo")

            if potenza_kw and potenza_kw > 2000:
                problemi.append(f"Potenza {potenza_kw} kW supera il limite massimo di 2.000 kW")

            if certificazioni:
                cert_lower = [c.lower() for c in certificazioni]
                if not any("ehpa" in c or "en 14511" in c for c in cert_lower):
                    risultati["requisiti_mancanti"].append("Certificazione EHPA o test EN 14511 richiesta")
            else:
                risultati["requisiti_mancanti"].append("Verificare presenza certificazione EHPA o EN 14511")

            if problemi:
                risultati["ammissibile"] = False
                risultati["motivazione"] = "Non ammissibile: " + "; ".join(problemi)

            if risultati["ammissibile"] is None:
                risultati["ammissibile"] = True
                risultati["motivazione"] = "Tipo impianto compatibile con CT 2.0. Verificare COP e certificazioni."

        # --- Solare termico ---
        elif "solare" in tipo_lower:
            tipo_intervento = "B.4 - Collettori solari termici"
            risultati["tipo_intervento_ct"] = tipo_intervento
            risultati["durata_incentivo"] = "5 anni"

            if superficie_mq and superficie_mq < 1.5:
                risultati["ammissibile"] = False
                risultati["motivazione"] = f"Superficie {superficie_mq} m² < minimo 1,5 m² richiesto"
            else:
                risultati["ammissibile"] = True
                risultati["motivazione"] = "Solare termico ammissibile. Verificare certificazione Solar Keymark."

            if certificazioni:
                if not any("solar keymark" in c.lower() for c in certificazioni):
                    risultati["requisiti_mancanti"].append("Certificazione Solar Keymark richiesta")
            else:
                risultati["requisiti_mancanti"].append("Verificare presenza certificazione Solar Keymark o equivalente europea")

        # --- Caldaia biomassa ---
        elif "biomassa" in tipo_lower or "pellet" in tipo_lower or "legna" in tipo_lower:
            tipo_intervento = "B.5 - Generatori di calore a biomassa"
            risultati["tipo_intervento_ct"] = tipo_intervento
            risultati["durata_incentivo"] = "5 anni"
            risultati["ammissibile"] = True
            risultati["motivazione"] = "Caldaia a biomassa ammissibile (tipologia B.5). Verificare certificazione emissioni EN 303-5."
            risultati["requisiti_mancanti"].append("Certificato emissioni EN 303-5 obbligatorio")

        # --- Caldaia a gas non condensante ---
        elif "gas" in tipo_lower and "condensaz" not in tipo_lower:
            risultati["ammissibile"] = False
            risultati["motivazione"] = "❌ Le caldaie a gas NON a condensazione non rientrano negli interventi del Conto Termico 2.0."

        # --- Caldaia a condensazione ---
        elif "condensaz" in tipo_lower:
            tipo_intervento = "B.1 - Sostituzione con caldaie a condensazione"
            risultati["tipo_intervento_ct"] = tipo_intervento
            risultati["durata_incentivo"] = "2 anni"
            risultati["ammissibile"] = True
            risultati["motivazione"] = "Caldaia a condensazione ammissibile (tipologia B.1). Durata incentivo: 2 anni."

        # --- Scaldacqua pompa di calore ---
        elif "scaldacqua" in tipo_lower or "acs" in tipo_lower:
            tipo_intervento = "B.3 - Scaldacqua a pompa di calore"
            risultati["tipo_intervento_ct"] = tipo_intervento
            risultati["durata_incentivo"] = "2 anni"
            risultati["ammissibile"] = True
            risultati["motivazione"] = "Scaldacqua a pompa di calore ammissibile (tipologia B.3)."

        else:
            risultati["ammissibile"] = None
            risultati["motivazione"] = f"Tipo impianto '{tipo_impianto}' non riconosciuto. Consultare il DM 16/02/2016 per la classificazione corretta."

        yield risultati
        
        stato = "✅ AMMISSIBILE" if risultati["ammissibile"] else ("❌ NON AMMISSIBILE" if risultati["ammissibile"] is False else "⚠️ DA VERIFICARE")
        yield f"Verifica ammissibilità completata: {stato}. {risultati['motivazione']}"


    # ─────────────────────────────────────────────────────────
    # TOOL 2: Stima incentivo
    # ─────────────────────────────────────────────────────────
    @tool(tree=tree, end=False, status="💰 Calcolo incentivo stimato...")
    async def stima_incentivo(
        tipo_intervento: str,
        potenza_kw: float = None,
        superficie_mq: float = None,
        zona_climatica: str = None,
        tipo_soggetto: str = "privato"
    ):
        """
        Stima l'incentivo annuo e totale ottenibile con il Conto Termico GSE.
        
        Usa questo tool quando l'utente chiede:
        - "Quanto incentivo posso ottenere?"
        - "Qual è il valore dell'incentivo per...?"
        - "Quanto mi rimborsa il GSE?"
        - "Calcola l'incentivo per il mio impianto"
        
        Parametri:
        - tipo_intervento: tipo intervento CT (pompa di calore, solare termico, biomassa, ecc.)
        - potenza_kw: potenza termica nominale in kW (per pompe di calore e biomassa)
        - superficie_mq: superficie collettori in m² (per solare termico)
        - zona_climatica: zona climatica A/B/C/D/E/F
        - tipo_soggetto: "privato" o "PA" (Pubblica Amministrazione)
        """

        # Tariffe incentivo (€/anno per kW o m²) - dati semplificati da DM 16/02/2016
        # In produzione queste tariffe andrebbero lette dalla collection Normative
        tariffe = {
            "pompa di calore": {
                "tariffa_base_kwh": 110,   # €/kW/anno indicativo
                "durata_anni": 5,
                "min_kw": 5, "max_kw": 2000
            },
            "solare termico": {
                "tariffa_base_mq": 245,    # €/m²/anno indicativo
                "durata_anni": 5,
                "min_mq": 1.5
            },
            "biomassa": {
                "tariffa_base_kwh": 95,    # €/kW/anno indicativo
                "durata_anni": 5,
                "min_kw": 5, "max_kw": 2000
            },
            "caldaia condensazione": {
                "tariffa_base_kwh": 65,    # €/kW/anno indicativo
                "durata_anni": 2,
                "min_kw": 5
            },
            "scaldacqua pompa di calore": {
                "incentivo_fisso_anno": 300,  # € fissi/anno indicativo
                "durata_anni": 2,
            }
        }

        tipo_lower = tipo_intervento.lower()
        risultato = {"tipo_intervento": tipo_intervento}

        # Moltiplicatore PA (PA ha incentivi leggermente più alti)
        moltiplicatore_pa = 1.15 if tipo_soggetto.lower() == "pa" else 1.0

        for chiave, dati in tariffe.items():
            if chiave in tipo_lower:
                durata = dati["durata_anni"]

                if chiave == "solare termico" and superficie_mq:
                    annuo = dati["tariffa_base_mq"] * superficie_mq * moltiplicatore_pa
                    risultato["incentivo_annuo_eur"] = round(annuo, 2)
                    risultato["incentivo_totale_eur"] = round(annuo * durata, 2)
                    risultato["durata_anni"] = durata
                    risultato["base_calcolo"] = f"{superficie_mq} m² × {dati['tariffa_base_mq']} €/m²/anno"

                elif chiave == "scaldacqua pompa di calore":
                    annuo = dati["incentivo_fisso_anno"] * moltiplicatore_pa
                    risultato["incentivo_annuo_eur"] = round(annuo, 2)
                    risultato["incentivo_totale_eur"] = round(annuo * durata, 2)
                    risultato["durata_anni"] = durata
                    risultato["base_calcolo"] = "Incentivo fisso per categoria B.3"

                elif potenza_kw:
                    annuo = dati["tariffa_base_kwh"] * potenza_kw * moltiplicatore_pa
                    risultato["incentivo_annuo_eur"] = round(annuo, 2)
                    risultato["incentivo_totale_eur"] = round(annuo * durata, 2)
                    risultato["durata_anni"] = durata
                    risultato["base_calcolo"] = f"{potenza_kw} kW × {dati['tariffa_base_kwh']} €/kW/anno"

                else:
                    risultato["nota"] = f"Specificare la potenza in kW (o i m² per solare termico) per ottenere una stima precisa."
                    risultato["formula"] = f"Incentivo annuo ≈ {dati.get('tariffa_base_kwh', dati.get('tariffa_base_mq'))} × [kW o m²] per {durata} anni"

                risultato["avvertenza"] = "⚠️ Stima indicativa. Il valore definitivo è calcolato dal GSE in sede di istruttoria."
                break
        else:
            yield Error(f"Tipo di intervento '{tipo_intervento}' non riconosciuto. Specificare: pompa di calore, solare termico, biomassa, caldaia a condensazione, scaldacqua pompa di calore.")
            return

        yield risultato
        
        if "incentivo_totale_eur" in risultato:
            yield (f"Stima incentivo Conto Termico: "
                   f"€{risultato['incentivo_annuo_eur']:,.0f}/anno per {risultato['durata_anni']} anni "
                   f"= totale circa €{risultato['incentivo_totale_eur']:,.0f}. "
                   f"Valore indicativo, da confermare con GSE.")


    # ─────────────────────────────────────────────────────────
    # TOOL 3: Checklist documentale
    # ─────────────────────────────────────────────────────────
    @tool(tree=tree, end=False, status="📋 Genero checklist documentazione...")
    async def checklist_documentale(
        tipo_intervento: str,
        tipo_soggetto: str = "privato",
        tipo_accesso: str = "diretto"
    ):
        """
        Genera la lista completa dei documenti richiesti per una domanda al Conto Termico GSE.
        
        Usa questo tool quando l'utente chiede:
        - "Quali documenti devo presentare?"
        - "Cosa serve per la domanda GSE?"
        - "Checklist documentazione Conto Termico"
        - "Quali documenti mancano per presentare la domanda?"
        
        Parametri:
        - tipo_intervento: tipo intervento (pompa di calore, solare termico, ecc.)
        - tipo_soggetto: "privato" o "PA"
        - tipo_accesso: "diretto" (incentivo < 5.000 €/anno) o "prenotazione" (incentivo ≥ 5.000 €/anno)
        """

        # Documenti base (tutti gli interventi)
        documenti_base = [
            {"doc": "Relazione tecnica descrittiva", "obbligatorio": True, "note": "Firmata da tecnico abilitato (ingegnere, perito, geometra)"},
            {"doc": "Documentazione fotografica ante-operam", "obbligatorio": True, "note": "Foto del vecchio impianto prima della sostituzione"},
            {"doc": "Documentazione fotografica post-operam", "obbligatorio": True, "note": "Foto del nuovo impianto installato"},
            {"doc": "Fatture/ricevute pagamento tracciabili", "obbligatorio": True, "note": "No contanti. Bonifico, carta o altro mezzo tracciabile"},
            {"doc": "Schede tecniche componenti (con marcatura CE)", "obbligatorio": True, "note": "Del produttore, in italiano o con traduzione"},
            {"doc": "Dichiarazione di conformità impianto", "obbligatorio": True, "note": "Modello CPI per impianti termici o dichiarazione D.M. 37/2008"},
        ]

        # Documenti specifici per tipo impianto
        documenti_specifici = []

        tipo_lower = tipo_intervento.lower()

        if "pompa di calore" in tipo_lower:
            documenti_specifici = [
                {"doc": "Certificato test EN 14511 o EHPA Gold", "obbligatorio": True, "note": "Attestante COP ≥ soglia minima per la zona climatica"},
                {"doc": "Documentazione dismissione vecchio generatore", "obbligatorio": True, "note": "Foto + dichiarazione tecnico dello smaltimento"},
            ]

        elif "solare" in tipo_lower:
            documenti_specifici = [
                {"doc": "Certificazione Solar Keymark", "obbligatorio": True, "note": "O certificazione europea equivalente EN 12975"},
                {"doc": "Schema dell'impianto idraulico", "obbligatorio": True, "note": "Planimetria con posizionamento collettori"},
            ]

        elif "biomassa" in tipo_lower or "pellet" in tipo_lower:
            documenti_specifici = [
                {"doc": "Certificato emissioni EN 303-5", "obbligatorio": True, "note": "Classe 5 (5 stelle) obbligatoria per nuove installazioni"},
                {"doc": "Analisi combustibile (se non pellet certificato)", "obbligatorio": False, "note": "Per biomassa non certificata"},
            ]

        # Documenti aggiuntivi per PA
        documenti_pa = []
        if tipo_soggetto.lower() == "pa":
            documenti_pa = [
                {"doc": "APE pre-intervento", "obbligatorio": True, "note": "Attestato Prestazione Energetica prima dei lavori"},
                {"doc": "APE post-intervento", "obbligatorio": True, "note": "Attestato Prestazione Energetica dopo i lavori"},
                {"doc": "Delibera/determinazione di affidamento lavori", "obbligatorio": True, "note": "Atto amministrativo di approvazione dell'intervento"},
            ]

        # Documenti per procedura a prenotazione
        documenti_prenotazione = []
        if tipo_accesso.lower() == "prenotazione":
            documenti_prenotazione = [
                {"doc": "Domanda di prenotazione preventiva", "obbligatorio": True, "note": "Da inviare PRIMA dell'avvio lavori"},
                {"doc": "Preventivo dettagliato lavori", "obbligatorio": True, "note": "Con stima dell'incentivo annuo atteso"},
            ]

        checklist_completa = {
            "tipo_intervento": tipo_intervento,
            "tipo_soggetto": tipo_soggetto,
            "procedura": tipo_accesso,
            "documenti_base": documenti_base,
            "documenti_specifici": documenti_specifici,
            "documenti_pa": documenti_pa,
            "documenti_prenotazione": documenti_prenotazione,
            "totale_documenti": len(documenti_base) + len(documenti_specifici) + len(documenti_pa) + len(documenti_prenotazione),
            "scadenza_invio": "Entro 60 giorni dalla data di fine lavori (accesso diretto)" if tipo_accesso == "diretto" else "Prenotazione PRIMA dei lavori, poi 12 mesi per completare"
        }

        yield checklist_completa
        
        obbligatori = sum(1 for d in documenti_base + documenti_specifici + documenti_pa + documenti_prenotazione if d.get("obbligatorio"))
        yield f"Checklist generata: {obbligatori} documenti obbligatori per {tipo_intervento} ({tipo_soggetto.upper()}). Scadenza: {checklist_completa['scadenza_invio']}"


    # ─────────────────────────────────────────────────────────
    # TOOL 4: Controlla stato pratica
    # ─────────────────────────────────────────────────────────
    @tool(tree=tree, end=False, status="🔎 Cerco la pratica nel sistema...")
    async def controlla_stato_pratica(
        codice_pratica: str,
        client_manager=None
    ):
        """
        Recupera le informazioni e lo stato di una pratica Conto Termico tramite codice pratica.
        
        Usa questo tool quando l'utente chiede:
        - "Qual è lo stato della pratica CT-XXXX-XXXXX?"
        - "Dammi informazioni sulla pratica..."
        - "Cosa manca alla pratica X?"
        - "La pratica X è approvata?"
        
        Parametri:
        - codice_pratica: il codice univoco della pratica (es. CT-2024-001234)
        - client_manager: client Weaviate iniettato da Elysia
        """

        if client_manager is None:
            yield Error("Client Weaviate non disponibile. Configurare la connessione Weaviate.")
            return

        try:
            with client_manager.connect_to_client() as client:
                pratiche = client.collections.get("Pratiche")

                # Filtra per codice pratica
                from weaviate.classes.query import Filter
                results = pratiche.query.fetch_objects(
                    filters=Filter.by_property("codice_pratica").equal(codice_pratica),
                    limit=1
                )

                if not results.objects:
                    yield Error(f"Pratica '{codice_pratica}' non trovata nel sistema.")
                    return

                pratica = results.objects[0].properties

                yield {
                    "pratica_trovata": True,
                    "dettagli": pratica
                }

                stato = pratica.get("stato", "N/D")
                mancanti = pratica.get("documenti_mancanti", [])
                incentivo = pratica.get("incentivo_totale_stimato", "N/D")

                msg = f"Pratica {codice_pratica}: stato '{stato}'."
                if mancanti:
                    msg += f" Documenti mancanti: {', '.join(mancanti)}."
                if isinstance(incentivo, (int, float)):
                    msg += f" Incentivo totale stimato: €{incentivo:,.0f}."

                yield msg

        except Exception as e:
            yield Error(f"Errore nel recupero della pratica: {str(e)}")

    return tree
