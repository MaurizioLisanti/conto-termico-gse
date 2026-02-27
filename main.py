"""
main.py
=======
Applicazione Conto Termico GSE - Powered by Elysia
"""

import os
import subprocess
from dotenv import load_dotenv

load_dotenv()


def setup_elysia():
    """Configura Elysia e importa i dati."""
    from elysia import configure, Tree

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
        print("✅ Configurato con OpenAI")
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
        raise EnvironmentError("❌ Nessun API key LLM trovato.")

    # Importa i dati in Weaviate
    print("📥 Importazione dati in corso...")
    subprocess.run(["python", "import_data.py"], check=False)
    print("✅ Dati importati")

    # Inizializzazione Tree
    # NOTA: il preprocessing si fa dall'interfaccia web cliccando "Analyze"
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

    from tools import register_tools
    tree = register_tools(tree)
    print("✅ Tool personalizzati registrati")

    return tree


def run_web_mode(port: int = 8000):
    """Avvia l'interfaccia web di Elysia."""
    print(f"\n🌐 Avvio Conto Termico GSE su http://localhost:{port}")
    print("⚙️  Inizializzazione in corso...")
    setup_elysia()
    print("🚀 Avvio server Elysia...")
    subprocess.run(["elysia", "start", "--port", str(port)])


if __name__ == "__main__":
    run_web_mode(port=8000)
 
