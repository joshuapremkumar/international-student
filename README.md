# 🌍 Degree Abroad Analyzer

AI-powered multi-agent system that analyzes the best countries to study any degree abroad.

## What It Does

Enter a degree (e.g. *Computer Science*, *MBA*, *Medicine*) and get a ranked breakdown of the best destination countries including:

| Signal | Source |
|---|---|
| Best countries + job demand | Tavily (web search) |
| Post-study work visa rules | Tavily (web search) |
| Salary benchmarks | Tavily (web search) |
| Country ranking + risk score | Tinyfish (AI reasoning) |

---

## Architecture — Multi-Agent Pipeline

```
User Input (degree)
       │
       ▼
  Orchestrator
       │
  ┌────┴────────────────────────┐
  │                             │
Phase 1               Phase 2 (parallel fan-out)
Research Agent     Visa Agent + Salary Agent
(Tavily)           (Tavily, async per country)
  │                             │
  └────────────┬────────────────┘
               │
          Merged Context
               │
               ▼
          ROI Agent
         (Tinyfish)
               │
               ▼
      Ranked CountryResults
   (job demand, salary, visa, risk)
```

---

## Project Structure

```
degree-abroad-analyzer/
├── backend/
│   ├── main.py                  # FastAPI entrypoint
│   ├── config.py                # Settings from .env
│   ├── agents/
│   │   ├── orchestrator.py      # Pipeline coordinator
│   │   ├── research_agent.py    # Tavily: best countries
│   │   ├── visa_agent.py        # Tavily: visa rules
│   │   ├── salary_agent.py      # Tavily: salary data
│   │   └── roi_agent.py         # Tinyfish: ranking + risk
│   ├── services/
│   │   ├── tavily_client.py     # Tavily async wrapper
│   │   ├── tinyfish_client.py   # Tinyfish OpenAI-compat client
│   │   └── cache.py             # TTL in-memory cache
│   ├── models/
│   │   ├── request.py           # AnalyzeRequest schema
│   │   └── response.py          # AnalysisResult + CountryResult
│   ├── prompts/
│   │   ├── research_prompt.py
│   │   ├── visa_prompt.py
│   │   ├── salary_prompt.py
│   │   └── roi_prompt.py
│   └── api/routes/
│       └── analyze.py           # POST /api/v1/analyze
├── frontend/
│   ├── app.py                   # Streamlit main app
│   ├── api_client.py            # HTTP client → FastAPI
│   └── components/
│       ├── input_form.py        # Degree input + slider
│       ├── country_card.py      # Styled country result card
│       └── risk_badge.py        # Color-coded risk badge
├── logs/                        # JSON structured logs
├── requirements.txt
└── .env.example
```

---

## Tech Stack

- **FastAPI** — async Python backend
- **Streamlit** — interactive frontend UI
- **Tavily API** — real-time web search (research, visa, salary)
- **Tinyfish API** — AI reasoning model (OpenAI-compatible)
- **Pydantic v2** — request/response validation
- **httpx** — async HTTP client
- **asyncio** — concurrent agent fan-out

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/joshuapremkumar/international-student.git
cd international-student
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and fill in your API keys
```

### 3. Run the backend

```bash
cd degree-abroad-analyzer
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Run the frontend

```bash
cd degree-abroad-analyzer
streamlit run frontend/app.py --server.port 8501
```

Open **http://localhost:8501** in your browser.

---

## API

### `POST /api/v1/analyze`

```json
{
  "degree": "Computer Science",
  "top_n": 5
}
```

**Response:**
```json
{
  "degree": "Computer Science",
  "cached": false,
  "generated_at": "2026-03-17T23:30:00Z",
  "countries": [
    {
      "country": "United States",
      "rank": 1,
      "job_demand_score": 9.2,
      "average_salary_usd": 115000,
      "post_study_visa": "OPT + STEM OPT – up to 3 years",
      "visa_difficulty": "Moderate",
      "risk_score": 3.1,
      "summary": "..."
    }
  ]
}
```

Swagger UI: **http://localhost:8000/docs**

---

## License

MIT
