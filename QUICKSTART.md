# 🚀 Quick Start — Phase 2 (Groq Edition)

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env with your Groq API key
# Get free key at: https://console.groq.com
echo "GROQ_API_KEY=gsk_..." > .env

# 3. Run the app
python app.py

# 4. Open browser
# → http://localhost:5000
```

## What's New (Phase 2)

✅ **Groq API** — Ultra-low latency LLM inference  
✅ **TailwindCSS** — Modern, responsive design  
✅ **Strict JSON** — Predictable, structured responses  
✅ **Demo Safety** — Hardcoded fallback if API unavailable  
✅ **Bonus Features** — Copy results, retry, example incident  
✅ **Color-coded** — Red for causes, blue for fixes, amber for immediate actions  

## Project Files

| File | Purpose |
|------|---------|
| `app.py` | Flask + Groq API integration |
| `requirements.txt` | Python dependencies (httpx, Flask, python-dotenv) |
| `.env` | Your Groq API key (create this) |
| `templates/index.html` | TailwindCSS UI |
| `static/script.js` | Client logic with demo fallback |
| `README.md` | Full documentation |

## Key Features

🎯 **5-10 second response time** — Groq's fast inference  
📊 **Structured JSON output** — No parsing, just read the data  
🎨 **Beautiful SaaS UI** — TailwindCSS + dark mode  
🛡️ **Demo-proof** — Built-in fallback response  
⚡ **Bonus buttons** — Copy, Retry, Use Example  

## API Response Format

```json
{
  "root_causes": ["cause 1", "cause 2"],
  "resolution_steps": ["step 1", "step 2", "step 3"],
  "priority_actions": {
    "immediate": ["action 1", "action 2"],
    "short_term": ["action 1", "action 2"],
    "long_term": ["action 1"]
  },
  "confidence": "High"
}
```

## Demo Script (2 minutes)

1. Click **"Use Example"** → Pre-filled with realistic incident
2. Click **"Analyze Incident"** → API processes in 5-10 seconds
3. Show:
   - Confidence badge (color-coded)
   - Root causes (red accent)
   - Resolution steps (blue accent)
   - Priority actions (amber for immediate)
4. Click **"Copy Result"** → Copies formatted report
5. Say: **"This turns 30 minutes of troubleshooting into 30 seconds of structured insight."**

## If API Fails

The UI will automatically show a demo response (fallback built-in). Your demo won't break.

## Environment Variables

```
GROQ_API_KEY=gsk_xxxxx  (Required)
```

Get a free key: https://console.groq.com

---

Ready? `python app.py` and go to http://localhost:5000 🚀

