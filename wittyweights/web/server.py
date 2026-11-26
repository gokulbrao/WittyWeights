"""
WittyWeights Web Server:
1. GET  /             -> Monospaced typewriter landing page with email onboarding form.
2. POST /subscribe    -> Saves subscriber to StateManager & sends welcome email via Resend.
3. GET  /api/latest   -> Returns latest dispatch text.
4. POST /api/dispatch -> Webhook for Cloud Scheduler (Mon-Fri 07:00) to execute & send.
Zero external dependencies required (uses standard library http.server).
"""

import os
import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

from wittyweights.state import StateManager
from wittyweights.email_dispatcher import EmailDispatcher
from wittyweights.orchestrator import NewsletterOrchestrator


class WittyWeightsHandler(BaseHTTPRequestHandler):

    def _get_latest_dispatch(self) -> str:
        latest_file = os.path.join("output", "latest.md")
        if os.path.exists(latest_file):
            try:
                with open(latest_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Strip container div if present for clean text preview
                    content = content.replace("<div style=\"font-family: 'Courier New', Courier, monospace; line-height: 1.5; color: #111;\">\n", "")
                    content = content.replace("\n</div>", "")
                    return content.strip()
            except Exception:
                pass
        return "DISPATCH PENDING: Next issue compiles Monday at 07:00."

    def _render_landing_page(self, message: str = "") -> str:
        latest_text = self._get_latest_dispatch()
        alert_html = f"<div class='alert'>{message}</div>" if message else ""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WITTYWEIGHTS // Applied AI Dispatch</title>
  <style>
    body {{
      background-color: #f7f6f2;
      color: #1a1a1a;
      font-family: 'Courier New', Courier, monospace;
      line-height: 1.6;
      margin: 0;
      padding: 30px 20px;
    }}
    .container {{
      max-width: 740px;
      margin: 0 auto;
      background: #ffffff;
      padding: 40px;
      border: 1px solid #d5d3ca;
      box-shadow: 0 2px 5px rgba(0,0,0,0.04);
    }}
    h1 {{
      font-size: 22px;
      letter-spacing: 1.5px;
      margin: 0 0 8px 0;
      text-transform: uppercase;
      border-bottom: 2px solid #1a1a1a;
      padding-bottom: 8px;
    }}
    .meta {{
      font-size: 12px;
      color: #555;
      margin-bottom: 24px;
      text-transform: uppercase;
    }}
    .signup-box {{
      background: #faf9f6;
      border: 1px dashed #bbb;
      padding: 24px;
      margin: 24px 0;
    }}
    .signup-title {{
      font-weight: bold;
      font-size: 14px;
      margin-bottom: 8px;
      text-transform: uppercase;
    }}
    .signup-desc {{
      font-size: 13px;
      color: #444;
      margin-bottom: 16px;
    }}
    form {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }}
    input[type="email"] {{
      flex: 1;
      min-width: 250px;
      padding: 12px 14px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 14px;
      border: 1px solid #999;
      background: #fff;
      outline: none;
    }}
    input[type="email"]:focus {{
      border-color: #1a1a1a;
    }}
    button {{
      background: #1a1a1a;
      color: #fff;
      border: 1px solid #1a1a1a;
      padding: 12px 24px;
      font-family: 'Courier New', Courier, monospace;
      font-size: 13px;
      font-weight: bold;
      letter-spacing: 1px;
      cursor: pointer;
      text-transform: uppercase;
    }}
    button:hover {{
      background: #333;
    }}
    .alert {{
      background: #eef7ee;
      border: 1px solid #4caf50;
      color: #2e7d32;
      padding: 12px;
      margin-bottom: 20px;
      font-size: 13px;
    }}
    pre {{
      background: #fafafa;
      border: 1px solid #e8e8e8;
      padding: 20px;
      font-size: 12px;
      line-height: 1.5;
      overflow-x: auto;
      white-space: pre-wrap;
      word-break: break-word;
    }}
    .footer {{
      margin-top: 32px;
      font-size: 11px;
      color: #777;
      text-align: center;
      border-top: 1px solid #e5e5e5;
      padding-top: 16px;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>WITTYWEIGHTS // DISPATCH WIRE</h1>
    <div class="meta">FREQUENCY: MON-FRI AT 07:00 • APPLIED AI & SYSTEMS • ZERO FLUFF</div>

    {alert_html}

    <div class="signup-box">
      <div class="signup-title">SUBSCRIBE TO THE WIRE DISPATCH</div>
      <div class="signup-desc">
        Delivered directly to your inbox every weekday morning at 07:00. Five verified production engineering, InsurTech, and model optimization dispatches that survived scrutiny.
      </div>
      <form action="/subscribe" method="POST">
        <input type="email" name="email" placeholder="colleague@domain.com" required autocomplete="email">
        <button type="submit">SUBSCRIBE</button>
      </form>
    </div>

    <div style="font-size: 13px; font-weight: bold; margin-bottom: 8px;">LATEST DISPATCH ARCHIVE:</div>
    <pre>{latest_text}</pre>

    <div class="footer">
      WITTYWEIGHTS WIRE • RUNNING SERVERLESS ON GOOGLE CLOUD PLATFORM • ALL RIGHTS RESERVED
    </div>
  </div>
</body>
</html>"""

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/?"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            msg = query.get("msg", [""])[0]

            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(self._render_landing_page(message=msg).encode("utf-8"))

        elif self.path == "/api/latest":
            latest = self._get_latest_dispatch()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(latest.encode("utf-8"))

        elif self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": "healthy"}')

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")

        # 1. User Onboarding / Sign-up
        if self.path == "/subscribe":
            email = ""
            if "application/json" in self.headers.get("Content-Type", ""):
                try:
                    data = json.loads(body)
                    email = data.get("email", "")
                except Exception:
                    email = ""
            else:
                form_data = urllib.parse.parse_qs(body)
                email = form_data.get("email", [""])[0]

            state = StateManager()
            success, msg = state.add_subscriber(email, source="landing_page")

            # Dispatch welcome email with latest edition
            if success:
                dispatcher = EmailDispatcher()
                latest_text = self._get_latest_dispatch()
                dispatcher.dispatch_welcome(email, latest_issue_text=latest_text)

            if "application/json" in self.headers.get("Content-Type", ""):
                self.send_response(200 if success else 400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                res = json.dumps({"success": success, "message": msg})
                self.wfile.write(res.encode("utf-8"))
            else:
                redirect_url = f"/?msg={urllib.parse.quote(msg)}"
                self.send_response(303)
                self.send_header("Location", redirect_url)
                self.end_headers()

        # 2. Cloud Scheduler Webhook (Runs Mon-Fri at 07:00)
        elif self.path == "/api/dispatch":
            orchestrator = NewsletterOrchestrator()
            issue = orchestrator.run_pipeline(verbose=False)

            # Record stories in Firestore to prevent repetition
            state = StateManager()
            state.record_published_stories(issue.top_5_stories, issue.issue_number)

            # Email active subscribers via Resend
            subscribers = state.get_active_subscribers()
            dispatcher = EmailDispatcher()
            dispatch_results = dispatcher.dispatch_issue(
                recipients=subscribers,
                issue_number=issue.issue_number,
                markdown_content=issue.markdown_content
            )

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_payload = {
                "status": "success",
                "issue_number": issue.issue_number,
                "recipients_count": len(subscribers),
                "dispatch": dispatch_results
            }
            self.wfile.write(json.dumps(response_payload).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")


def run_server(port: int = 8080):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, WittyWeightsHandler)
    print(f"🚀 WittyWeights Server running on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run_server(port)
