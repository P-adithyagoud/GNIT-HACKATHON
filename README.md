# AI Incident Response Assistant — Phase 2

A production-grade MVP for analyzing DevOps incidents in seconds using Groq's ultra-fast LLM inference.

## Key Improvements (Phase 2)

- **Groq API** — Ultra-low latency inference (5-10 seconds)
- **Strict JSON** — No parsing, structured responses guaranteed
- **TailwindCSS** — Modern responsive UI with dark mode
- **Demo Safety** — Hardcoded fallback response (never breaks demo)
- **Bonus Features** — Copy results, retry analysis, example incident
- **Color-Coded Output** — Visual hierarchy (red causes, blue fixes, amber immediate)

## Tech Stack

- **Backend**: Flask + Groq API
- **Frontend**: HTML + TailwindCSS + Vanilla JS
- **LLM**: Groq (Mixtral-8x7b-32768)
- **Deployment**: Local development server

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Get Groq API key (free)
# Visit: https://console.groq.com/keys

# 3. Create .env
echo "GROQ_API_KEY=gsk_your_key_here" > .env

# 4. Run
python app.py

# 5. Open
# http://localhost:5000
```

## How It Works

1. User pastes incident details (logs, errors, descriptions)
2. Click "Analyze Incident"
3. Backend sends to Groq API with strict JSON prompt
4. LLM returns structured response in <10 seconds
5. Frontend displays formatted results with color coding

## Response Format

```json
{
  "root_causes": [
    "Connection pool exhaustion",
    "Inefficient query patterns"
  ],
  "resolution_steps": [
    "Immediately rollback middleware",
    "Monitor API latency",
    "Verify connection pool recovery"
  ],
  "priority_actions": {
    "immediate": [
      "Trigger rollback automation",
      "Alert database team"
    ],
    "short_term": [
      "Analyze code changes",
      "Stress test locally"
    ],
    "long_term": [
      "Implement circuit breaker",
      "Add monitoring"
    ]
  },
  "confidence": "High"
}
```

## Fallback System

If the API fails, the system automatically returns a demo response:
- User sees realistic incident analysis
- Demo never breaks
- Fallback note displayed subtly

## Features

✅ Instant analysis with Groq's fast inference  
✅ Structured JSON output (no parsing errors)  
✅ Copy results to clipboard  
✅ Retry analysis button  
✅ Example incident pre-filled  
✅ Color-coded output (UX hierarchy)  
✅ Confidence badge (High/Medium/Low)  
✅ Responsive TailwindCSS design  
✅ Dark mode support  
✅ Demo-safe fallback response  

## Project Structure

```
├── app.py                    # Flask backend
├── requirements.txt          # Dependencies
├── .env                      # API key (create this)
├── .env.example             # Template
├── templates/
│   └── index.html           # TailwindCSS UI
└── static/
    └── script.js            # Client logic
```

## Configuration

### Environment Variables

```env
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

Get free key: https://console.groq.com/keys

### Tuning

Edit `SYSTEM_PROMPT` in `app.py` to change LLM behavior:
- Adjust temperature (currently 0.2 for deterministic)
- Change max_tokens (currently 500)
- Modify response format requirements

## Demo Flow (Hackathon)

**Total time: 2 minutes**

```
1. Open app (0 sec)
   → Clean, professional interface

2. Click "Use Example" (2 sec)
   → Shows realistic API latency incident

3. Click "Analyze" (15 sec)
   → Loading spinner + "Analyzing production issue..."

4. Results appear (5 sec)
   → Color-coded sections
   → Confidence badge
   → Immediate actions highlighted

5. Click "Copy Result" (3 sec)
   → Formatted report copied

6. Say the magic words:
   "This turns 30 minutes of troubleshooting into 30 seconds of structured insight."
```

## Performance

- API response time: 5-10 seconds (Groq inference)
- Frontend rendering: <200ms
- Total: 5-10 seconds end-to-end
- Demo stable: Fallback ensures no failures

## Limitations

- No database (in-memory only)
- No authentication (local dev only)
- No RAG (knowledge base)
- No incident history
- No external integrations

## Troubleshooting

### API Key Issues
```bash
# Check .env exists and is correct
cat .env
# Should show: GROQ_API_KEY=gsk_...
```

### Port Already in Use
```bash
# Change port in app.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Use 5001 instead
```

### Slow Responses
- Check internet connection
- Verify Groq API quota at https://console.groq.com
- Model may be throttled — try again in a few seconds

### JSON Parse Errors
- Built-in fallback handles this
- Check LLM response in Flask logs
- Retry automatically shown to user

## Example Incidents

### Database Outage
```
Connection timeout after 30s
Services: API, Analytics, Auth
Failed queries: SELECT * FROM users (999 concurrent)
Last deployment: 2 hours ago (ORM upgrade)
```

### Memory Leak
```
Memory: 87% → 98% in 2 hours
Service: video-processor
Restart: temporary fix (returns in ~4h)
New code: streaming pipeline refactored
```

### API Latency Spike
```
Response time: 200ms → 2500ms after deployment
Error rate: 0.1% → 5%
CPU: 82% (high)
Deployment: middleware v2.1 → v3.0 (15 min ago)
```

## Next Steps

- [ ] Add incident history (Redis cache)
- [ ] Export to PDF/Markdown
- [ ] Slack integration
- [ ] Custom prompt templates
- [ ] Multi-user chat mode
- [ ] Metrics dashboard

## Design Philosophy

**Perception > Complexity**
- Simple, fast, useful > Feature-rich, slow
- Demo clarity first
- Reliability (fallback) over features

**SaaS Feel**
- TailwindCSS for modern look
- Dark mode for credibility
- Smooth animations
- Error handling that doesn't break

**Production-Ready Code**
- Input validation
- Error handling
- Graceful fallback
- Clean, readable ~400 lines

---

**Built for hackathon impact.** 🚀

Questions? Check the code — it's clean and well-commented.

