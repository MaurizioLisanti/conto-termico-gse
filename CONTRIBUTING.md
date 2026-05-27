# Contribuire al progetto / Contributing to the project

---

## 🇮🇹 Italiano

### Benvenuto!

Benvenuto nel progetto **Conto Termico GSE — Assistente AI con Elysia**.
Questo progetto è sviluppato nell'ambito di **Linux PropLUG**, l'associazione
Linux di Baronissi che promuove il software libero e open source.

🌐 Sito dell'associazione: [https://proplug.it](https://proplug.it)

### Come contribuire

1. **Fork** del repository su GitHub
2. Crea un **branch** per la tua feature o fix:
   ```bash
   git checkout -b feature/nome-feature
   ```
3. Scrivi il codice seguendo gli standard del progetto (vedi sotto)
4. Esegui i test prima di aprire una PR:
   ```bash
   pytest tests/ -q
   ```
5. Apri una **Pull Request** verso il branch `main` con una descrizione chiara

### Standard del codice

- **Commenti in italiano** — il dominio è italiano, i commenti devono esserlo
- **Docstring obbligatorie** per ogni funzione pubblica:
  ```python
  def calcola_incentivo(potenza_kw: float, zona: str) -> float:
      """Calcola l'incentivo stimato per una pompa di calore.

      Args:
          potenza_kw: Potenza nominale in kW.
          zona: Zona climatica (A-F).

      Returns:
          Incentivo annuo stimato in euro.
      """
  ```
- Segui la formattazione **PEP 8**
- Usa nomi di variabili descrittivi in italiano o inglese (coerente con il file esistente)

### Segnalare bug o idee

Apri una **Issue** su GitHub descrivendo:
- Cosa hai fatto
- Cosa ti aspettavi
- Cosa è successo invece

---

## 🇬🇧 English

### Welcome!

Welcome to the **Conto Termico GSE — AI Assistant with Elysia** project.
This project is developed as part of **Linux PropLUG**, the Naples Linux
association promoting free and open source software.

🌐 Association website: [https://proplug.it](https://proplug.it)

### How to contribute

1. **Fork** the repository on GitHub
2. Create a **branch** for your feature or fix:
   ```bash
   git checkout -b feature/feature-name
   ```
3. Write code following the project standards (see below)
4. Run tests before opening a PR:
   ```bash
   pytest tests/ -q
   ```
5. Open a **Pull Request** against the `main` branch with a clear description

### Code standards

- **Comments in Italian** — the domain is Italian, comments must be too
- **Docstrings required** for every public function (see Italian section for example)
- Follow **PEP 8** formatting
- Use descriptive variable names in Italian or English (consistent with the existing file)

### Reporting bugs or ideas

Open a **Issue** on GitHub describing:
- What you did
- What you expected
- What happened instead

---

*Progetto sviluppato nell'ambito di Linux PropLUG — [https://proplug.it](https://proplug.it)*
