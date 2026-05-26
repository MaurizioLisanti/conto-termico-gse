#!/usr/bin/env python3
"""Extract structured data from GSE PDF documents using OpenRouter API."""

import json
import os
import sys
from pathlib import Path

import pdfplumber
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

RAW_DIR = Path("raw")
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

PDF_TO_JSON = {
    "decreto_dm_16_02_2016.pdf":             "decreto_dm_16_02_2016.json",
    "allegato_criteri_ammissibilita.pdf":    "allegato_criteri_ammissibilita.json",
    "regole_applicative_ct.pdf":             "regole_applicative_ct.json",
    "ct3_webinar_2026.pdf":                  "ct3_webinar_2026.json",
    "guida_ct_pubblica_amministrazione.pdf": "guida_ct_pubblica_amministrazione.json",
    "mappa_ct_imprese_privati.pdf":          "mappa_ct_imprese_privati.json",
    "pompe_di_calore_regole_applicative.pdf":"pompe_di_calore_regole_applicative.json",
}

EXTRACTION_PROMPT = (
    "Sei un esperto di normativa energetica italiana.\n"
    "Analizza questo documento ufficiale GSE sul Conto Termico.\n"
    "Estrai e struttura in JSON:\n"
    "- Tipo documento e data\n"
    "- Tutte le sezioni con titolo e contenuto\n"
    "- Interventi ammissibili con codice (B.1, B.2 ecc)\n"
    "- Requisiti tecnici (COP, certificazioni, soglie)\n"
    "- Tariffe incentivo per tipo intervento\n"
    "- Zone climatiche e relativi requisiti\n"
    "Rispondi SOLO con JSON valido, nessun testo aggiuntivo."
)

JSON_SCHEMA_HINT = """{
  "source": "nome_file.pdf",
  "tipo": "decreto | regole_applicative | allegato | guida",
  "data_documento": "YYYY-MM-DD",
  "versione": "CT 2.0 | CT 3.0",
  "sezioni": [{"titolo": "...", "contenuto": "...", "pagina": 1, "tags": []}],
  "interventi": [{"codice": "B.1", "descrizione": "...", "requisiti": [], "incentivo": {}, "zone_climatiche": []}],
  "tariffe": [],
  "requisiti_tecnici": [],
  "citations": []
}"""

MAX_TEXT_CHARS = 30000


def extract_text_from_pdf(pdf_path: Path) -> str:
    texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()
            if text:
                texts.append(f"--- Pagina {page_num} ---\n{text}")
    return "\n\n".join(texts)


def _strip_fences(raw: str) -> str:
    if raw.startswith("```json"):
        raw = raw[7:]
    elif raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()


def _parse_json_robust(raw: str) -> dict:
    """Try json.loads; if it fails due to truncation, attempt simple repair."""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass
    # Find last valid top-level object boundary
    depth = 0
    last_close = -1
    in_string = False
    escape = False
    for i, ch in enumerate(raw):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                last_close = i
    if last_close > 0:
        try:
            return json.loads(raw[: last_close + 1])
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Cannot parse JSON from response (len={len(raw)})")


def extract_json_from_pdf(client: OpenAI, pdf_name: str, pdf_text: str) -> dict:
    if len(pdf_text) > MAX_TEXT_CHARS:
        pdf_text = pdf_text[:MAX_TEXT_CHARS] + "\n\n[... testo troncato ...]"

    user_content = (
        f"Documento: {pdf_name}\n\n"
        f"{EXTRACTION_PROMPT}\n\n"
        f"Schema atteso:\n{JSON_SCHEMA_HINT}\n\n"
        f"Testo del documento:\n{pdf_text}"
    )

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-001",
        messages=[{"role": "user", "content": user_content}],
        temperature=0.1,
        max_tokens=8192,
    )

    raw = response.choices[0].message.content.strip()
    cleaned = _strip_fences(raw)
    data = _parse_json_robust(cleaned)
    data["source"] = pdf_name
    return data


def _fallback_record(pdf_name: str, error: str = "") -> dict:
    record = {
        "source": pdf_name,
        "tipo": "sconosciuto",
        "data_documento": None,
        "versione": None,
        "sezioni": [],
        "interventi": [],
        "tariffe": [],
        "requisiti_tecnici": [],
        "citations": [],
    }
    if error:
        record["error"] = error
    return record


def main() -> None:
    api_key = os.getenv("OPENROUTER_API_KEY", "").strip().rstrip(".")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY non trovata nel .env")
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    results = []
    errors = []

    for pdf_name, json_name in PDF_TO_JSON.items():
        pdf_path = RAW_DIR / pdf_name
        json_path = DATA_DIR / json_name

        if not pdf_path.exists():
            print(f"SKIP: {pdf_name} non trovato")
            continue

        print(f"Elaborazione: {pdf_name} ...", flush=True)

        try:
            pdf_text = extract_text_from_pdf(pdf_path)
            if not pdf_text.strip():
                print(f"  WARN: nessun testo estratto, salvo record vuoto")
                data = _fallback_record(pdf_name)
            else:
                print(f"  testo: {len(pdf_text):,} caratteri", flush=True)
                data = extract_json_from_pdf(client, pdf_name, pdf_text)
                n_int = len(data.get("interventi") or [])
                print(f"  OK — interventi: {n_int}")
        except Exception as exc:
            msg = str(exc)
            print(f"  ERROR: {msg}")
            errors.append(f"{pdf_name}: {msg}")
            data = _fallback_record(pdf_name, msg)

        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        results.append(data)

    # Merge
    all_interventi = [
        iv
        for doc in results
        for iv in (doc.get("interventi") or [])
        if isinstance(iv, dict)
    ]

    dataset_completo = {
        "documenti": results,
        "interventi": all_interventi,
        "totale_documenti": len(results),
        "totale_interventi": len(all_interventi),
    }

    completo_path = DATA_DIR / "dataset_completo.json"
    with open(completo_path, "w", encoding="utf-8") as fh:
        json.dump(dataset_completo, fh, ensure_ascii=False, indent=2)

    print(f"\nCompletato: {len(results)} documenti elaborati")
    print(f"Interventi totali: {len(all_interventi)}")
    print(f"Dataset: {completo_path}")

    if errors:
        print(f"\nErrori ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
