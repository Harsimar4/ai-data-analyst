# AI-Powered Data Analytics Assistant (GenAI)
Ask questions about any CSV dataset in plain English and get computed answers with business insights.
## Run
```
pip install pandas
python analyst.py     # CLI demo on the sample sales data
python app.py         # web app -> http://localhost:8000
```
## How it works
- Intent engine detects total / average / count / top-N / group-by questions and the columns they refer to
- pandas computes the exact answer (no hallucinated numbers)
- Optional: set `OPENAI_API_KEY` to have an LLM polish answers into narrative insights
## Tech
Python, pandas, Natural Language Processing, LLM Integration, HTML

## React Frontend
The web UI is a React app (in `frontend/`, built with Vite):
```
cd frontend && npm install && npm run build   # or: npm run dev  (dev server with API proxy)
python app.py                                  # serves the built React app + /api/ask
```
## Tech (full)
React.js, JavaScript, Python, pandas, LLM Integration, REST API, Vite
