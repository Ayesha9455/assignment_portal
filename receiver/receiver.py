import json
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            report = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
        with open("testreport.json", "w") as f:
            json.dump(report, f, indent=2)
        print("Report received:", report.get("overall_status"), report.get("commit_sha"))
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"saved")

if __name__ == "__main__":
    print("Receiver listening on http://localhost:8000 (saves testreport.json here)")
    HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
