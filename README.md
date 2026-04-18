# 🛡️ AI Incident Response Assistant

**Transform chaotic incident logs into structured, actionable recovery plans in seconds.**
A production-grade SRE co-pilot built for high-stakes environments, featuring a long-term knowledge base and ultra-fast LLM analysis.

---

## 🚀 Key Features

- **🧠 Deep Knowledge Base**: Integrated with **Supabase** to store and retrieve historical incidents.
- **🔍 Intentional Similarity Matching**: Automatically finds the top 3 most relevant past incidents to provide grounding context for the AI.
- **⚡ Ultra-Fast Analysis**: Powered by **Groq (Mixtral-8x7b)** for sub-10s response times.
- **📐 9-Step Expert Pipeline**: A strict architectural flow ensuring reliability, from data retrieval to automated persistence.
- **💎 Premium Design**: A sleek, dark-themed dashboard using **TailwindCSS** and **Glassmorphism** for a state-of-the-art feel.
- **🛡️ Demo Reliability**: Built-in fallback responses and validation layers to ensure a flawless demo every time.

---

## 🛠️ Tech Stack

- **Backend**: Python / Flask (Serverless-optimized)
- **Intelligence**: Groq API (LLM Infrastructure)
- **Database**: Supabase (Persistent Incident Vault)
- **Frontend**: Vanilla JS / TailwindCSS (Zero-dependency UI)
- **Deployment**: Vercel ready

---

## 📂 Architecture

Designed for 60-second clarity. The system follows a clean "Command Center" pattern:

```text
/app          ➔ Route Handlers & Factory
/services     ➔ Intelligence Pipeline, Matcher Engine, & Repository
/utils        ➔ Sanitization & Formatting helpers
/config       ➔ Central Settings & AI Personas
/templates    ➔ Premium Dashboard UI
app.py        ➔ Modern Entry Point
```

---

## 🏁 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file with your credentials:
   ```env
   GROQ_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_service_role_key
   ```

3. **Run Locally**:
   ```bash
   python app.py
   ```

---

## 🧠 The Pipeline (How it works)

When an incident is submitted, the **IncidentPipeline** triggers a 5-stage orchestration:
1. **Retrieve**: Fetch historical data from the Supabase Vault.
2. **Rank**: Identify the most relevant past cases using the **Similarity Engine**.
3. **Analyze**: Ingest current logs + past context into the **Incident Expert**.
4. **Sanitize**: Format the LLM output into strict, validated JSON.
5. **Learn**: Auto-persist the new discovery back to the Knowledge Base.

---

## 🏆 Hackathon Winning Edge

- **Context-Aware**: Unlike generic LLM tools, this system *remembers* past outages.
- **Deterministic UX**: Every action (Immediate, Resolution, Summary) is designed to be executable.
- **Speed**: Built on Groq to ensure the "Wow" factor during live demos.

---

**Built by Antigravity for the GNIT-HACKATHON.** 🚀
