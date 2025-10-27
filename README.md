<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Chat with Multiple PDFs — Download & Run Guide</title>

<style>
:root{
  --bg:#0b1020; --card:#0f172a; --text:#e5e7eb; --muted:#9ca3af;
  --primary:#60a5fa; --primary2:#818cf8; --accent:#22d3ee;
  --border:#1f2937; --code:#0b0f1d; --codeText:#e5e7eb; --good:#34d399;
  --shadow:0 18px 40px rgba(0,0,0,.35); --radius:14px;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0; background:var(--bg); color:var(--text);
  font-family: "Inter","Segoe UI",Roboto,Arial,sans-serif; line-height:1.7;
}
a{color:var(--primary); text-decoration:none}
a:hover{text-decoration:underline}
.container{max-width:1100px; margin:0 auto; padding:24px}
header{
  background: linear-gradient(120deg, var(--primary), var(--primary2));
  padding:64px 24px; text-align:center; color:#fff; position:relative; overflow:hidden;
}
header::after{
  content:""; position:absolute; inset:auto -20% -40% -20%;
  height:300px; background:radial-gradient(closest-side, rgba(255,255,255,.18), transparent 70%);
}
h1{margin:0; font-size:clamp(1.8rem,3.4vw,2.6rem)}
.subtitle{margin-top:.5rem; color:#eef2ff; opacity:.92}
.btns{margin-top:18px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap}
.btn{
  display:inline-flex; align-items:center; gap:.5rem;
  background:rgba(255,255,255,.12); color:#fff; padding:12px 16px; border-radius:12px;
  border:1px solid rgba(255,255,255,.35); font-weight:600; text-decoration:none;
  transition:.15s transform ease, .2s background ease, .2s border ease;
}
.btn:hover{transform:translateY(-1px); background:rgba(255,255,255,.18)}
.btn svg{width:18px; height:18px}
.badge{display:inline-block; padding:2px 8px; border-radius:999px; background:#0ea5e9; color:#001; font-weight:700; margin-left:8px}

.card{
  background:var(--card); border:1px solid var(--border); border-radius:var(--radius);
  box-shadow:var(--shadow); padding:24px; margin:20px 0;
}
.card h2{margin-top:0; font-size:1.25rem; color:#c7d2fe}
.grid{display:grid; grid-template-columns: 1fr 1fr; gap:18px}
@media (max-width: 900px){ .grid{grid-template-columns: 1fr} }

.note{
  background:#0b3a4d; border-left:6px solid var(--accent); border-radius:10px;
  padding:12px 14px; color:#d8f2ff; margin:14px 0;
}

pre{
  background:var(--code); color:var(--codeText); border:1px solid var(--border);
  padding:16px; border-radius:12px; overflow-x:auto; font-size:.95rem; line-height:1.6; margin:12px 0;
}
.codewrap{position:relative}
.copy{
  position:absolute; top:10px; right:10px; background:rgba(255,255,255,.08);
  color:#fff; border:1px solid rgba(255,255,255,.25); padding:6px 10px; font-size:.8rem;
  border-radius:8px; cursor:pointer;
}
.copy:hover{background:rgba(255,255,255,.16)}

.step{display:flex; gap:10px; align-items:center}
.step .num{
  width:28px; height:28px; display:grid; place-items:center;
  border-radius:8px; background:rgba(96,165,250,.18); color:#93c5fd; font-weight:800;
  border:1px solid rgba(96,165,250,.35);
}

.kbd{background:#0b1224; border:1px solid #1f2b45; padding:2px 6px; border-radius:6px; font-family:monospace}
.li{margin:.35rem 0}
.check{color:var(--good); margin-right:.3rem}

.video{
  aspect-ratio:16/9; width:100%; border:none; border-radius:12px; overflow:hidden;
  box-shadow:var(--shadow); border:1px solid var(--border);
}

footer{
  text-align:center; color:var(--muted); padding:28px 24px; border-top:1px solid var(--border);
}
.top{position:fixed; right:16px; bottom:16px; background:linear-gradient(135deg, var(--primary), var(--primary2));
  color:#fff; border:none; padding:12px 14px; border-radius:12px; box-shadow:0 10px 24px rgba(37,99,235,.35); cursor:pointer; display:none}
.top.show{display:block}
</style>
</head>

<body>
<header>
  <h1>Chat with Multiple PDFs — Download & Run</h1>
  <p class="subtitle">Streamlit × LangChain × Hugging Face × FAISS — open-source chatbot with step-by-step setup.</p>
  <div class="btns">
    <a class="btn" href="https://github.com/khof-star/LangChain-DocAssistant" target="_blank" rel="noopener">
      <!-- GitHub icon -->
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 .5a12 12 0 0 0-3.79 23.4c.6.11.82-.26.82-.58v-2.2c-3.34.73-4.04-1.61-4.04-1.61-.55-1.39-1.35-1.76-1.35-1.76-1.1-.75.08-.74.08-.74 1.22.08 1.86 1.26 1.86 1.26 1.08 1.86 2.84 1.32 3.53 1 .11-.79.42-1.32.76-1.62-2.66-.31-5.47-1.33-5.47-5.93 0-1.31.47-2.38 1.24-3.22-.12-.31-.54-1.56.12-3.25 0 0 1.01-.32 3.3 1.23a11.5 11.5 0 0 1 6 0c2.28-1.55 3.29-1.23 3.29-1.23.67 1.69.25 2.94.13 3.25.77.84 1.23 1.91 1.23 3.22 0 4.61-2.82 5.61-5.51 5.91.43.37.81 1.1.81 2.22v3.29c0 .32.21.7.83.58A12 12 0 0 0 12 .5Z"/></svg>
      GitHub Repo
    </a>
    <a class="btn" href="https://youtu.be/KhuUDgpnO54" target="_blank" rel="noopener">
      <!-- YouTube icon -->
      <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.6A3 3 0 0 0 .5 6.2 31.5 31.5 0 0 0 0 12a31.5 31.5 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.6 9.4.6 9.4.6s7.5 0 9.4-.6a3 3 0 0 0 2.1-2.1A31.5 31.5 0 0 0 24 12a31.5 31.5 0 0 0-.5-5.8ZM9.75 15.5v-7l6 3.5-6 3.5Z"/></svg>
      Watch Setup Video
    </a>
  </div>
</header>

<div class="container">

  <div class="card">
    <h2>What is this?</h2>
    <p>
      A ready-to-run, open-source chatbot that lets you <strong>upload multiple PDFs</strong>, builds a <strong>FAISS</strong> vector store,
      retrieves context with <strong>LangChain</strong>, and generates answers with a local <strong>Hugging Face</strong> model.
    </p>
    <ul>
      <li class="li"><span class="check">✔</span> Clean Streamlit UI with chat bubbles</li>
      <li class="li"><span class="check">✔</span> Zero-shot format routing (emails, summaries, reports…)</li>
      <li class="li"><span class="check">✔</span> Parallel candidate generation to pick the best answer</li>
    </ul>
  </div>

  <div class="grid">
    <div class="card">
      <h2>Quick Start (Download & Run)</h2>

      <div class="step"><span class="num">1</span>Open the GitHub repo</div>
      <p><a href="https://github.com/khof-star/LangChain-DocAssistant" target="_blank" rel="noopener">github.com/khof-star/LangChain-DocAssistant</a><br/>
      Click <span class="kbd">Code</span> → <span class="kbd">Download ZIP</span> (or clone).</p>

      <div class="step"><span class="num">2</span>Unzip & open folder in VS Code</div>

      <div class="step"><span class="num">3</span>Create a virtual environment</div>
      <div class="codewrap">
        <button class="copy" data-copy="c1">Copy</button>
<pre id="c1"><code>python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate</code></pre>
      </div>

      <div class="step"><span class="num">4</span>Install dependencies</div>
      <div class="codewrap">
        <button class="copy" data-copy="c2">Copy</button>
<pre id="c2"><code>pip install -r requirements.txt</code></pre>
      </div>

      <div class="step"><span class="num">5</span>Create <code>.env</code> (optional but recommended)</div>
      <p>Put it in the project root if you use provider APIs:</p>
      <div class="codewrap">
        <button class="copy" data-copy="c3">Copy</button>
<pre id="c3"><code>OPENAI_API_KEY=your_openai_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here</code></pre>
      </div>

      <div class="step"><span class="num">6</span>Run the app</div>
      <div class="codewrap">
        <button class="copy" data-copy="c4">Copy</button>
<pre id="c4"><code>streamlit run app.py</code></pre>
      </div>

      <div class="note">First run will download models (e.g., <strong>google/flan-t5-large</strong>). GPU is used automatically if available.</div>
    </div>

    <div class="card">
      <h2>Video Tutorial</h2>
      <p>Prefer watching? Follow along with the full walkthrough:</p>
      <iframe class="video" src="https://www.youtube.com/embed/KhuUDgpnO54" title="YouTube video" allowfullscreen></iframe>
      <p style="margin-top:.6rem">
        Or open in YouTube: <a href="https://youtu.be/KhuUDgpnO54" target="_blank" rel="noopener">https://youtu.be/KhuUDgpnO54</a>
      </p>
    </div>
  </div>

  <div class="card">
    <h2>Folder Structure</h2>
    <div class="codewrap">
      <button class="copy" data-copy="c5">Copy</button>
<pre id="c5"><code>my_project/
├─ app.py                  # Streamlit UI + pipeline wiring
├─ parallel_generate.py    # Run multiple templates in parallel, pick best
├─ format_router.py        # Zero-shot route → template (facebook/bart-large-mnli)
├─ auto_formatter.py       # Detect intent & provide format prompts
├─ htmlTemplates.py        # Chat bubble HTML/CSS for Streamlit rendering
├─ style.css               # Extra UI styles (optional)
├─ requirements.txt        # All Python dependencies
├─ .env                    # API keys / tokens (optional)
└─ __pycache__/            # Auto-generated</code></pre>
    </div>
  </div>

  <div class="card">
    <h2>Common Issues & Fixes</h2>
    <ul>
      <li class="li"><strong>Model download is slow</strong> → it’s normal on first run. Keep the terminal open.</li>
      <li class="li"><strong>CUDA not used</strong> → verify GPU with <code>torch.cuda.is_available()</code>. Otherwise runs on CPU.</li>
      <li class="li"><strong>Port already in use</strong> → run <code>streamlit run app.py --server.port 8502</code></li>
      <li class="li"><strong>PDF text empty</strong> → some PDFs are scanned. Use OCR to extract text first.</li>
    </ul>
  </div>

  <div class="card">
    <h2>License & Credits</h2>
    <p>MIT © 2025 — Navin Bharti</p>
    <p>Source: <a href="https://github.com/khof-star/LangChain-DocAssistant" target="_blank" rel="noopener">khof-star/LangChain-DocAssistant</a></p>
  </div>

</div>

<button class="top" id="topBtn" title="Back to top">↑ Top</button>

<footer>
  Built with Streamlit · LangChain · HuggingFace · FAISS &nbsp;•&nbsp; View the code on
  <a href="https://github.com/khof-star/LangChain-DocAssistant" target="_blank" rel="noopener">GitHub</a>
</footer>

<script>
document.querySelectorAll('.copy').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    const id = btn.getAttribute('data-copy');
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(()=>{
      const old = btn.textContent; btn.textContent='Copied!';
      setTimeout(()=>btn.textContent=old, 1200);
    });
  });
});
const topBtn = document.getElementById('topBtn');
window.addEventListener('scroll', ()=>{ topBtn.classList.toggle('show', window.scrollY>500); });
topBtn.addEventListener('click', ()=>window.scrollTo({top:0, behavior:'smooth'}));
</script>
</body>
</html>
