"""AI Data Analyst - API server (Python standard library + pandas).
Serves the React frontend build (frontend/dist) and a JSON API:
  POST /api/ask  {"question": "..."}  ->  {"answer": "..."}
Run: python app.py  ->  http://localhost:8000
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import os, json, mimetypes
from analyst import DataAnalyst

BASE = os.path.dirname(__file__)
A = DataAnalyst(os.path.join(BASE, "sales.csv"))
DIST = os.path.join(BASE, "frontend", "dist")

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/ask":
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            out = json.dumps({"answer": A.ask(body.get("question", ""))}).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.end_headers()
            self.wfile.write(out)
        else:
            self.send_response(404); self.end_headers()
    def do_GET(self):
        rel = unquote(self.path.split("?")[0]).lstrip("/") or "index.html"
        fp = os.path.join(DIST, rel)
        if not os.path.isfile(fp): fp = os.path.join(DIST, "index.html")
        if not os.path.isfile(fp):
            self.send_response(200); self.send_header("Content-Type", "text/html"); self.end_headers()
            self.wfile.write(b"React build not found - run: cd frontend && npm install && npm run build")
            return
        data = open(fp, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(fp)[0] or "text/html"); self.end_headers()
        self.wfile.write(data)

if __name__ == "__main__":
    print("AI Data Analyst running at http://localhost:8000")
    HTTPServer(("localhost", 8000), H).serve_forever()
