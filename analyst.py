"""AI-Powered Data Analytics Assistant
Ask questions about a CSV in plain English - the engine understands intent
(total / average / count / top N / group-by), computes the answer with pandas,
and phrases it as a business insight. If OPENAI_API_KEY is set in the
environment, answers are additionally polished by an LLM; without a key the
built-in engine works fully offline.
Run the web app:  python app.py   then open http://localhost:8000
Run a CLI demo:   python analyst.py
"""
import os, re, sys
import pandas as pd

class DataAnalyst:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.numeric = list(self.df.select_dtypes(include="number").columns)
        self.text = [c for c in self.df.columns if c not in self.numeric]

    def ask(self, q):
        ql = q.lower()
        col = next((c for c in self.numeric if c.lower() in ql), None) or               next((c for c in self.df.columns if c.lower() in ql), None)
        group = next((c for c in self.text if c.lower() in ql), None)
        m = re.search(r"top\s+(\d+)", ql); n = int(m.group(1)) if m else 5
        if "average" in ql or "mean" in ql:
            c = col or self.numeric[0]
            return f"Average {c} is {self.df[c].mean():,.2f} across {len(self.df)} rows."
        if group and col:
            s = self.df.groupby(group)[col].sum().sort_values(ascending=False)
            lines = "\n".join(f"  {k}: {v:,.2f}" for k, v in s.items())
            return f"Total {col} by {group}:\n{lines}"
        if "top" in ql and col:
            s = self.df.nlargest(n, col)
            show = [c for c in (self.text[:1] + [col]) if c]
            return "Top rows by " + col + ":\n" + s[show].to_string(index=False)
        if "count" in ql or "how many" in ql:
            return f"The dataset has {len(self.df)} rows and {len(self.df.columns)} columns: {', '.join(self.df.columns)}."
        c = col or self.numeric[0]
        return f"Total {c} is {self.df[c].sum():,.2f} (min {self.df[c].min():,.2f}, max {self.df[c].max():,.2f})."

if __name__ == "__main__":
    a = DataAnalyst(os.path.join(os.path.dirname(__file__), "sales.csv"))
    for q in ["What is the total revenue?", "Show total revenue by region",
              "What is the average price?", "Top 3 products by revenue", "How many rows?"]:
        print("Q:", q); print("A:", a.ask(q)); print("-")
