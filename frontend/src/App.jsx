import React, { useState } from "react";

export default function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [history, setHistory] = useState([]);
  const examples = [
    "What is the total revenue?",
    "Show total revenue by region",
    "What is the average price?",
    "Top 3 products by revenue",
  ];

  async function ask(q) {
    const text = q || question;
    if (!text) return;
    setAnswer("Thinking...");
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setHistory((h) => [{ q: text, a: data.answer }, ...h]);
  }

  return (
    <div style={{ fontFamily: "sans-serif", maxWidth: 760, margin: "40px auto", padding: 20 }}>
      <h1>AI-Powered Data Analytics Assistant</h1>
      <p>Ask questions about the sales dataset in plain English. Answers are computed from the data with pandas, then phrased as insights.</p>
      <div>
        <input value={question} onChange={(e) => setQuestion(e.target.value)}
          placeholder="e.g. Show total revenue by region" style={{ width: "75%", padding: 10 }} />
        <button onClick={() => ask()} style={{ padding: 10, marginLeft: 8 }}>Ask AI</button>
      </div>
      <div style={{ marginTop: 10 }}>
        {examples.map((ex) => (
          <button key={ex} onClick={() => ask(ex)} style={{ marginRight: 6, marginTop: 6 }}>{ex}</button>
        ))}
      </div>
      {answer && <pre style={{ background: "#f4f4f4", padding: 16, marginTop: 20, whiteSpace: "pre-wrap" }}>{answer}</pre>}
      {history.length > 0 && (
        <div style={{ marginTop: 24 }}>
          <h3>History</h3>
          {history.map((h, i) => <p key={i}><b>Q:</b> {h.q}</p>)}
        </div>
      )}
    </div>
  );
}
