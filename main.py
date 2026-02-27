"""
main.py
=======
Applicazione Conto Termico GSE - Powered by Elysia

Avvio modalità WEB APP:
    python main.py

Avvio modalità LIBRERIA (interattivo da console):
    python main.py --console

Avvio modalità WEB su porta diversa:
    python main.py --port 8080
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()


def setup_elysia():
    """Configura e restituisce il tree Elysia pronto all'uso."""
    from elysia import configure, Tree, preprocess, preprocessed_collection_exists

    # ─── Configurazione modelli ───────────────────────────────
    # Usa GPT-4o mini per il decision agent (veloce ed economico)
    # e GPT-4o per le query Weaviate complesse
    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")

    if openai_key:
        configure(
            base_model="gpt-4.1-mini",
            base_provider="openai",
            complex_model="gpt-4.1",
            complex_provider="openai",
            wcd_url=os.environ["WCD_URL"],
            wcd_api_key=os.environ["WCD_API_KEY"],
        )
        print("✅ Configurato con OpenAI (gpt-4.1-mini / gpt-4.1)")
    elif gemini_key:
        configure(
            base_model="gemini/gemini-2.0-flash",
            base_provider="gemini",
            complex_model="gemini/gemini-2.0-pro",
            complex_provider="gemini",
            wcd_url=os.environ["WCD_URL"],
            wcd_api_key=os.environ["WCD_API_KEY"],
        )
        print("✅ Configurato con Google Gemini")
    else:
        raise EnvironmentError(
            "❌ Nessun API key LLM trovato.\n"
            "Imposta OPENAI_API_KEY o GEMINI_API_KEY nel file .env"
        )

    # ─── Pre-processing delle collection Weaviate ────────────
    # Necessario affinché Elysia capisca la struttura dei dati
    collection_names = ["Normative", "Pratiche", "Impianti"]
import subprocess
subprocess.run(["python", "import_data.py"], check=False)
print("✅ Dati importati")
    for coll_name in collection_names:
        if not preprocessed_collection_exists(collection_name=coll_name):
            print(f"⚙️  Pre-processing collection '{coll_name}'...")
            preprocess(coll_name)
            print(f"✅ '{coll_name}' pre-processata")
        else:
            print(f"ℹ️  '{coll_name}' già pre-processata")

    # ─── Inizializzazione Tree ────────────────────────────────
    tree = Tree(
        agent_description=(
            "Sei un esperto assistente specializzato nella gestione del "
            "Conto Termico GSE (Gestore Servizi Energetici). "
            "Aiuti professionisti dell'energia, aziende e privati cittadini "
            "a verificare l'ammissibilità degli impianti, calcolare gli incentivi, "
            "preparare la documentazione e monitorare lo stato delle pratiche. "
            "Rispondi sempre in italiano, in modo chiaro e preciso."
        ),
        end_goal=(
            "L'obiettivo è rispondere completamente alla domanda dell'utente "
            "sul Conto Termico GSE, fornendo informazioni accurate su "
            "ammissibilità, incentivi, documentazione e procedure."
        ),
        style=(
            "Rispondi in modo professionale ma accessibile. "
            "Usa il nome dell'intervento tecnico corretto. "
            "Cita sempre la normativa di riferimento quando pertinente. "
            "Segnala chiaramente le scadenze importanti."
        )
    )

    # ─── Registrazione tool personalizzati ───────────────────
    from tools import register_tools
    tree = register_tools(tree)
    print("✅ Tool personalizzati registrati")

    return tree, collection_names


def run_console_mode():
    """Modalità interattiva da console per test e sviluppo."""
    print("\n" + "="*60)
    print("  CONTO TERMICO GSE - Assistente AI (modalità console)")
    print("="*60)

    tree, collection_names = setup_elysia()

    print(f"\n📊 Collection disponibili: {', '.join(collection_names)}")
    print("\n💡 Esempi di domande:")
    print("  - Questa pompa di calore da 12 kW con COP 3.4 è ammissibile?")
    print("  - Quali documenti servono per un solare termico (privato)?")
    print("  - Stima l'incentivo per solare termico 24 m² in zona E")
    print("  - Stato della pratica CT-2024-001234")
    print("  - Cosa dice il DM 16/02/2016 sulla cumulabilità?")
    print("\nDigita 'esci' per uscire\n")

    while True:
        try:
            domanda = input("Tu: ").strip()
            if not domanda:
                continue
            if domanda.lower() in ["esci", "exit", "quit"]:
                print("Arrivederci!")
                break

            print("\nAssistente: ", end="", flush=True)
            response, objects = tree(
                domanda,
                collection_names=collection_names
            )
            print(response)
            print()

        except KeyboardInterrupt:
            print("\nInterrotto dall'utente")
            break
        except Exception as e:
            print(f"\n❌ Errore: {e}")


def run_web_mode(port: int = 8000):
    """Avvia l'interfaccia web di Elysia."""
    import subprocess
    print(f"\n🌐 Avvio interfaccia web Elysia su http://localhost:{port}")
    print("Premi Ctrl+C per fermare\n")

    # Prima configura il tree in background (inizializza preprocessing)
    print("⚙️  Inizializzazione in corso...")
    setup_elysia()

    # Poi avvia il web server
    cmd = ["elysia", "start", "--port", str(port)]
    subprocess.run(cmd)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--console" in args:
        run_console_mode()
    elif "--port" in args:
        idx = args.index("--port")
        port = int(args[idx + 1]) if idx + 1 < len(args) else 8000
        run_web_mode(port=port)
    else:
        # Default: web mode porta 8000
        run_web_mode(port=8000)
