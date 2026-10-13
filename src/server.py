import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
from src.config import FIREWALL_HOST, FIREWALL_PORT, SIMILARITY_THRESHOLD
from src.firewall_core import check_user_input
import time
from src.analytics import log_request, get_analytics_stats

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Firewall Dashboard</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #000000;
      --bg-panel: #0a0a0a;
      --border: #27272a;
      --border-hover: #3f3f46;
      --text: #ededed;
      --text-muted: #a1a1aa;
      --primary: #ededed;
      --primary-invert: #000000;
      --success: #10b981;
      --danger: #ef4444;
      --warning: #f59e0b;
      --font-sans: 'Inter', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }
    
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: var(--font-sans);
      margin: 0;
      padding: 4rem 2rem;
      display: flex;
      justify-content: center;
      min-height: 100vh;
      box-sizing: border-box;
      -webkit-font-smoothing: antialiased;
    }
    
    .container {
      width: 100%;
      max-width: 900px;
    }
    
    .header {
      margin-bottom: 2.5rem;
    }
    
    .header h1 {
      font-weight: 600;
      font-size: 1.5rem;
      letter-spacing: -0.02em;
      margin: 0 0 0.5rem 0;
    }
    
    .header p {
      color: var(--text-muted);
      margin: 0;
      font-size: 0.95rem;
    }
    
    .grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    
    @media (max-width: 768px) {
      .grid { grid-template-columns: 1fr; }
    }
    
    .panel {
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
    }
    
    .panel-header {
      font-size: 0.875rem;
      font-weight: 500;
      color: var(--text-muted);
      margin-bottom: 1rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    textarea {
      width: 100%;
      height: 120px;
      background: #000;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text);
      font-family: var(--font-mono);
      font-size: 0.875rem;
      padding: 0.75rem;
      box-sizing: border-box;
      resize: none;
      margin-bottom: 1rem;
      transition: border-color 0.15s ease;
    }
    
    textarea:focus {
      outline: none;
      border-color: var(--text-muted);
    }
    
    button {
      background: var(--primary);
      color: var(--primary-invert);
      border: 1px solid var(--primary);
      padding: 0.6rem 1rem;
      border-radius: 6px;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      width: 100%;
      transition: background 0.15s ease, color 0.15s ease;
    }
    
    button:hover:not(:disabled) {
      background: transparent;
      color: var(--primary);
    }
    
    button:disabled {
      background: var(--border);
      border-color: var(--border);
      color: var(--text-muted);
      cursor: not-allowed;
    }
    
    .vis-box {
      background: #000;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1rem;
      font-family: var(--font-mono);
      font-size: 0.8125rem;
      flex-grow: 1;
      height: 220px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    
    .log-line { 
      line-height: 1.5;
    }
    
    .log-info { color: #60a5fa; }
    .log-success { color: var(--success); }
    .log-danger { color: var(--danger); }
    .log-warning { color: var(--warning); }
    .log-dim { color: var(--text-muted); }
    
    .status-badge {
      padding: 0.75rem;
      margin-top: 1rem;
      border-radius: 6px;
      font-weight: 500;
      font-size: 0.875rem;
      display: none;
      align-items: center;
      gap: 0.5rem;
      border: 1px solid var(--border);
      background: #000;
    }
    
    .status-badge::before {
      content: '';
      display: block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }
    
    .status-allow { display: flex; color: var(--success); }
    .status-allow::before { background: var(--success); }
    
    .status-block { display: flex; color: var(--danger); }
    .status-block::before { background: var(--danger); }
    
    .analytics-panel {
      margin-top: 1.5rem;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
    }
    
    .stat-card {
      background: #000;
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
    }
    
    .stat-value {
      font-size: 1.5rem;
      font-weight: 600;
      margin-top: 0.5rem;
    }
    
    @media (max-width: 768px) {
      .analytics-panel { grid-template-columns: 1fr 1fr; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Firewall Engine</h1>
      <p>Semantic & Cognitive Policy Evaluation</p>
    </div>
    
    <div class="grid">
      <div class="panel">
        <div class="panel-header">Evaluation Input</div>
        <form id="f">
          <textarea id="prompt" name="prompt" required placeholder="Enter payload to evaluate..."></textarea>
          <button type="submit" id="submit-btn">Run Evaluation</button>
        </form>
        <div id="status-badge" class="status-badge"></div>
      </div>
      
      <div class="panel">
        <div class="panel-header">System Telemetry</div>
        <div class="vis-box" id="vis-box">
          <div class="log-line log-dim">> Ready for input</div>
        </div>
      </div>
    </div>
    
    <div class="panel" style="margin-top: 1.5rem;">
      <div class="panel-header" style="display: flex; justify-content: space-between; align-items: center;">
        <span>Analytics Dashboard</span>
        <button id="refresh-stats-btn" style="width: auto; padding: 0.3rem 0.6rem; font-size: 0.75rem;">Refresh</button>
      </div>
      <div class="analytics-panel">
        <div class="stat-card">
          <span class="log-dim">Total Requests</span>
          <span class="stat-value" id="stat-total">0</span>
        </div>
        <div class="stat-card">
          <span class="log-success">Allowed</span>
          <span class="stat-value" id="stat-allowed">0</span>
        </div>
        <div class="stat-card">
          <span class="log-danger">Blocked</span>
          <span class="stat-value" id="stat-blocked">0</span>
        </div>
        <div class="stat-card">
          <span class="log-warning">Avg Latency</span>
          <span class="stat-value" id="stat-latency">0ms</span>
        </div>
      </div>
    </div>
  </div>

  <script>
    const form = document.getElementById("f");
    const visBox = document.getElementById("vis-box");
    const btn = document.getElementById("submit-btn");
    const badge = document.getElementById("status-badge");
    
    function log(text, className = "log-dim") {
      const el = document.createElement("div");
      el.className = "log-line " + className;
      el.innerHTML = text;
      visBox.appendChild(el);
      visBox.scrollTop = visBox.scrollHeight;
      return el;
    }
    
    function delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    async function loadStats() {
      try {
        const res = await fetch("/api/analytics");
        const data = await res.json();
        document.getElementById("stat-total").textContent = data.total_requests;
        document.getElementById("stat-allowed").textContent = data.allowed_requests;
        document.getElementById("stat-blocked").textContent = data.blocked_requests;
        document.getElementById("stat-latency").textContent = data.average_latency_ms + "ms";
      } catch (e) {
        console.error("Failed to load stats", e);
      }
    }
    
    document.getElementById("refresh-stats-btn").addEventListener("click", loadStats);
    // Load stats on init
    loadStats();

    let conversationHistory = [];

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const prompt = document.getElementById("prompt").value;
      
      btn.disabled = true;
      btn.textContent = "Evaluating...";
      badge.className = "status-badge";
      visBox.innerHTML = "";
      
      log("> RECV: Request intercepted", "log-info");
      const l1Log = log("... [L1] Querying vector index", "log-warning");
      
      const fetchPromise = fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt, history: conversationHistory }),
      }).then(r => r.json());
      
      await delay(600); 
      
      let layer1Passed = true;
      let finalData = null;
      
      const raceResult = await Promise.race([
        fetchPromise,
        delay(100).then(() => "pending")
      ]);
      
      if (raceResult !== "pending") {
         finalData = raceResult;
         if (finalData.reason && finalData.reason.includes("Layer 1")) {
             layer1Passed = false;
         }
      }
      
      if (!layer1Passed) {
         l1Log.innerHTML = "[L1] Match Found";
         l1Log.className = "log-line log-danger";
         log("> Score: " + finalData.score.toFixed(4), "log-danger");
         if (finalData.details) { log("> Detail: " + finalData.details, "log-dim"); }
      } else {
         l1Log.innerHTML = "[L1] Passed";
         l1Log.className = "log-line log-success";
         log("> Detail: Semantic similarity within safe threshold.", "log-dim");
         
         const l2Log = log("... [L2] Routing to cognitive evaluator", "log-warning");
         
         if (!finalData) {
            finalData = await fetchPromise;
         }
         
         await delay(600); 
         
         if (finalData.status === "BLOCK") {
             l2Log.innerHTML = "[L2] Policy Violation";
             l2Log.className = "log-line log-danger";
             log("> Reason: " + finalData.reason, "log-danger");
             if (finalData.details) { log("> Detail:<br>&nbsp;&nbsp;" + finalData.details.replace(/\\n/g, "<br>&nbsp;&nbsp;"), "log-dim"); }
             log("> Fingerprint dynamically injected", "log-info");
         } else {
             l2Log.innerHTML = "[L2] Passed";
             l2Log.className = "log-line log-success";
             if (finalData.details) { log("> Detail:<br>&nbsp;&nbsp;" + finalData.details.replace(/\\n/g, "<br>&nbsp;&nbsp;"), "log-dim"); }
         }
      }
      
      log("---", "log-dim");
      if (finalData.status === "BLOCK") {
          log("Result: BLOCKED", "log-danger");
          badge.className = "status-badge status-block";
          badge.textContent = "Blocked";
      } else {
          log("Result: ALLOWED", "log-success");
          badge.className = "status-badge status-allow";
          badge.textContent = "Allowed";
          conversationHistory.push({ role: "user", content: prompt });
          conversationHistory.push({ role: "assistant", content: "Simulated safe response." });
          log("> Context updated: " + conversationHistory.length/2 + " turns in history.", "log-dim");
      }
      
      btn.disabled = false;
      btn.textContent = "Run Evaluation";
      
      // Refresh stats automatically after request
      setTimeout(loadStats, 500);
    });
  </script>
</body>
</html>
"""

def make_handler(model, client, llm):
    class FirewallHandler(BaseHTTPRequestHandler):
        def _send_json(self, code, payload):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlparse(self.path).path
            if path in {"/", "/index.html"}:
                body = INDEX_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if path == "/health":
                self._send_json(200, {"status": "ok"})
                return
            if path == "/api/analytics":
                self._send_json(200, get_analytics_stats())
                return
            self._send_json(404, {"status": "ERROR", "reason": "Not found"})

        def do_POST(self):
            path = urlparse(self.path).path
            if path != "/check":
                self._send_json(404, {"status": "ERROR", "reason": "Not found"})
                return
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw.decode("utf-8") or "{}")
            except json.JSONDecodeError:
                self._send_json(400, {"status": "ERROR", "reason": "Invalid JSON"})
                return
            prompt = payload.get("prompt", "")
            history = payload.get("history", [])
            if not str(prompt).strip():
                self._send_json(400, {"status": "ERROR", "reason": "Prompt is empty"})
                return
                
            start_time = time.time()
            result = check_user_input(str(prompt), model, client, llm, history=history)
            latency_ms = (time.time() - start_time) * 1000
            
            if result.get("status") in {"ALLOW", "BLOCK"}:
                reason = result.get("reason", "")
                score = result.get("score", 0.0)
                log_request(prompt, result["status"], reason, score, latency_ms)
                
            code = 200 if result.get("status") != "ERROR" else 400
            self._send_json(code, result)

        def log_message(self, format, *args):
            sys.stderr.write("%s - %s\\n" % (self.address_string(), format % args))

    return FirewallHandler


def run_server(model, client, llm):
    handler = make_handler(model, client, llm)
    server = ThreadingHTTPServer((FIREWALL_HOST, FIREWALL_PORT), handler)
    print("\\n" + "=" * 50)
    print("RAG prompt firewall (HTTP)")
    print("=" * 50)
    print(f"Threshold: {SIMILARITY_THRESHOLD}")
    print(f"Open http://127.0.0.1:{FIREWALL_PORT}/ to type a prompt.")
    print(f"POST JSON to http://127.0.0.1:{FIREWALL_PORT}/check  {{\"prompt\": \"...\"}}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\\nStopping.")
    finally:
        server.server_close()
