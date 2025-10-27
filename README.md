# Chat with Multiple PDFs (Streamlit × LangChain × Hugging Face × FAISS)

Build an intelligent assistant that lets you **upload multiple PDFs**, **index their content**, and **ask questions** conversationally.
The app uses **Sentence-Transformers** for embeddings, **FAISS** for vector search, and a local **Flan-T5** model (via Hugging Face Transformers) for generation.
On top of that, we route questions through **format templates** (report, email, resume, etc.) and **choose the best formatted answer** using **parallel generation**.

<p align="center">
  <img src="docs/screenshot-ui.png" alt="App Screenshot" width="800">
</p>

---

## ✨ Features

* 📤 Upload **multiple PDFs** at once
* ✂️ Smart **text chunking** with overlap
* 🔎 **FAISS** vector store backed by **Sentence-Transformers**
* 🤖 **Flan-T5** (CPU/GPU) for response generation
* 🧭 **Zero-shot** router to pick the right **output format/template**
* 🧵 **Parallel generation** across candidate formats → picks the best
* 💬 Clean **chat UI** with custom **HTML/CSS templates**
* 🖥️ Optional docs pages for each module (HTML visualizations)

---

## 🧭 Table of Contents

* [Project Structure](#-project-structure)
* [Requirements](#-requirements)
* [Quick Start](#-quick-start)
* [Environment Variables](#-environment-variables)
* [How It Works](#-how-it-works)
* [File-by-File Overview](#-file-by-file-overview)
* [CLI Commands](#-cli-commands)
* [Docs / HTML Previews](#-docs--html-previews)
* [Performance Notes](#-performance-notes)
* [Troubleshooting](#-troubleshooting)
* [FAQ](#-faq)
* [Contributing](#-contributing)
* [License](#-license)

---

## 📁 Project Structure

```text
my_project/
├─ app.py                     # Streamlit app (step-by-step UI + pipeline)
├─ auto_formatter.py          # Detects intent (summary, email, report...) & returns prompt blocks
├─ format_router.py           # Zero-shot routing + master template registry
├─ parallel_generate.py       # Runs multiple formatted generations in parallel and scores them
├─ htmlTemplates.py           # Chat message HTML/CSS (user/bot bubble templates)
├─ requirements.txt           # Python dependencies
├─ style.css                  # Optional extra styling for Streamlit
├─ .env                       # Environment variables (private keys/settings) — DO NOT COMMIT
├─ __pycache__/               # Python cache (auto-created)
└─ venv/                      # Virtual environment (optional; not committed)
```

> You also have HTML documentation pages (optional) you can put under `docs/`:
>
> * `docs/index.html` (step-by-step guide)
> * `docs/htmlTemplates.html`
> * `docs/parallel_generate.html`
> * `docs/auto_formatter.html`
> * `docs/format_router.html`

---

## 📦 Requirements

* Python **3.9+** recommended
* (Optional) **CUDA-capable GPU** for faster generation (Flan-T5 will still run on CPU)
* Disk space: First run will download models (few GB)

Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```txt
streamlit
torch
transformers
PyPDF2
langchain
langchain-community
python-dotenv
faiss-cpu
sentence-transformers
```

---

## 🚀 Quick Start

1. **Create & activate** a virtual environment (recommended):

   ```bash
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate

   # Windows (Powershell)
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

2. **Install** dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) **Set environment variables** in `.env` (see below).

4. **Run** the app:

   ```bash
   streamlit run app.py
   ```

5. Open the **Streamlit UI**, upload PDFs, click **Process**, then start chatting!

---

## 🔐 Environment Variables

Create a file named `.env` in `my_project/` (never commit secrets).
Add values as needed (most setups work without any API keys):

```env
# Example placeholders (only if you later switch to hosted APIs/models)
HUGGINGFACEHUB_API_TOKEN=
OPENAI_API_KEY=
```

> The current app runs with **local models** (Flan-T5 & sentence-transformers) by default.

---

## 🧠 How It Works

1. **Upload PDFs → Extract Text**
   `PyPDF2` reads text from each PDF page.

2. **Split into Chunks**
   LangChain’s `CharacterTextSplitter` creates overlapping chunks for context retention.

3. **Embed & Index**
   **Sentence-Transformers** → embeddings.
   **FAISS** → fast vector search for relevant chunks.

4. **Format Routing**

   * `format_router.py` uses **zero-shot classification** (`facebook/bart-large-mnli`) to predict the best **format label(s)** for your query.
   * Returns templates (email, report, resume outline, etc.).

5. **Parallel Generation**

   * `parallel_generate.py` builds **RetrievalQA** chains per candidate template.
   * Runs them **in parallel**, then **scores** & picks the best output.

6. **Conversational Chain**

   * Uses **Flan-T5** via `transformers` and `HuggingFacePipeline`.
   * Maintains **chat memory** with `ConversationBufferMemory`.

7. **UI Rendering**

   * Streamlit front-end with custom **chat bubbles** from `htmlTemplates.py`.
   * Optional `style.css` for extra polish.

---

## 🗂 File-by-File Overview

* **`app.py`**
  The main Streamlit app:

  * Upload PDFs, process, build vector store, initialize the conversation chain
  * Text input for questions
  * Calls `generate_parallel()` and renders chat using `htmlTemplates.py`

* **`auto_formatter.py`**

  * `detect_format_type(query)`: infers intent (e.g., *summary*, *email_reply*, *ml_pipeline*)
  * `get_format_prompt(format_type)`: returns a concise, structured template

* **`format_router.py`**

  * Label set (`FORMAT_LABELS`) + **template catalog** (`TEMPLATES`)
  * Zero-shot classifier (`facebook/bart-large-mnli`) to rank the best formats
  * `route_formats(query, top_k)` and `template_for(label)`

* **`parallel_generate.py`**

  * Builds a **RetrievalQA** chain per candidate template
  * Executes them with `ThreadPoolExecutor`
  * `score_output()` prefers more completely filled templates
  * Returns the **best** formatted answer

* **`htmlTemplates.py`**

  * HTML/CSS for **user** and **bot** message bubbles
  * Simple avatar + message layout

* **`style.css`**

  * Optional additional CSS loaded into Streamlit

* **`.env`**

  * Place environment variables here (not committed)

---

## 🧪 CLI Commands

```bash
# Run the app
streamlit run app.py

# Freeze dependencies (optional)
pip freeze > requirements.txt

# Lint (optional)
python -m pip install ruff
ruff check .
```

---

## 📚 Docs / HTML Previews

You can host polished docs for each module in `docs/` and open them in a browser:

* `docs/index.html` – Full step-by-step guide with dark mode, copy buttons
* `docs/htmlTemplates.html` – Visual preview of chat bubbles
* `docs/parallel_generate.html` – Styled code + description
* `docs/auto_formatter.html` – Styled code + description
* `docs/format_router.html` – Styled code + description

Add screenshots under `docs/` and link them here.

---

## ⚡ Performance Notes

* **First run downloads models** (Flan-T5 and sentence-transformers). This can take a few minutes and several GB of disk.
* **GPU** (CUDA) is auto-detected. If available, generation runs much faster:

  * Verify with `torch.cuda.is_available()` inside Python.
* To reduce memory or speed up:

  * Use a smaller model (e.g., `google/flan-t5-base`) in `app.py`.
  * Lower `max_new_tokens` in the pipeline.
  * Reduce chunk size or number of candidates in `generate_parallel()`.

---

## 🛠 Troubleshooting

* **Blank answers / poor context**
  Make sure PDFs actually contain selectable text (not only scanned images). For scanned docs, you’ll need OCR (e.g., `pytesseract`) — not included here.

* **FAISS / Sentence-Transformers import errors**
  Ensure `faiss-cpu` and `sentence-transformers` are installed and match your Python version.

* **CUDA not used**
  Check CUDA toolkit + compatible PyTorch. If unavailable, app falls back to CPU automatically.

* **Slow first response**
  Models and weights are loaded on first use; subsequent runs are faster.

---

## ❓ FAQ

**Q: Do I need API keys?**
A: No. This project uses **local** Hugging Face models by default.

**Q: Can I switch to OpenAI or hosted Hugging Face Inference API?**
A: Yes. You’ll need to adapt `app.py` to use a different LLM wrapper and supply keys in `.env`.

**Q: Can I add more output formats?**
A: Absolutely! Add labels in `FORMAT_LABELS` and a new entry in `TEMPLATES`.
They’ll be discoverable via the zero-shot router automatically.

---

## 🤝 Contributing

PRs are welcome!

* Keep functions small and well-documented.
* Follow the current file layout and naming.
* If adding new templates, include a short description and test prompt in your PR.

---

## 📜 License

This project is licensed under the **MIT License**.
See `LICENSE` for details.

---

## 🙌 Credits

* [Streamlit](https://streamlit.io/)
* [LangChain](https://python.langchain.com/)
* [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)
* [Sentence-Transformers](https://www.sbert.net/)
* [FAISS](https://github.com/facebookresearch/faiss)

---

### 🧷 Badges (optional)

You can add these to the top of the README after you publish:

```md
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-📦-0A0A0A)
![Transformers](https://img.shields.io/badge/Transformers-Face-FFCC4D)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
```
 
