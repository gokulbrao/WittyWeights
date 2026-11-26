"""
Resend Email Dispatcher:
Delivers the monospaced WittyWeights daily dispatch via the Resend API.
Supports Resend sandbox (onboarding@resend.dev), verified domains, and offline simulation mode.
"""

import os
import json
import logging
import urllib.request
import urllib.error
from typing import List, Dict, Any, Tuple

logger = logging.getLogger("wittyweights.email")


class EmailDispatcher:
    """
    Handles email transmission via Resend HTTP API.
    Zero external dependencies required (uses urllib.request).
    """

    def __init__(self):
        self.api_key = os.environ.get("RESEND_API_KEY", "").strip()
        # In sandbox mode, Resend requires 'onboarding@resend.dev'
        self.from_email = os.environ.get("FROM_EMAIL", "onboarding@resend.dev").strip()
        self.api_url = "https://api.resend.com/emails"

    def _render_html(self, text_content: str) -> str:
        """Formats the typewriter text into an email-client-friendly container."""
        # Sanitize HTML tags in text_content to prevent rendering collisions
        safe_content = text_content.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WittyWeights Dispatch</title>
</head>
<body style="margin: 0; padding: 20px; background-color: #f6f6f6; font-family: 'Courier New', Courier, monospace;">
  <div style="max-width: 680px; margin: 0 auto; background-color: #ffffff; padding: 32px; border: 1px solid #e0e0e0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <pre style="font-family: 'Courier New', Courier, monospace; font-size: 13px; line-height: 1.6; color: #111111; white-space: pre-wrap; word-break: break-word; margin: 0;">{safe_content}</pre>
  </div>
</body>
</html>"""

    def _send_resend_request(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        if not self.api_key:
            # Simulation / Dry Run
            preview_path = os.path.join("output", "email_preview.html")
            os.makedirs("output", exist_ok=True)
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(payload.get("html", ""))
            return True, f"SIMULATION: Saved outgoing email preview to {preview_path}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "WittyWeights/1.0"
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.api_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_body = response.read().decode("utf-8")
                res_json = json.loads(res_body)
                email_id = res_json.get("id", "ok")
                return True, f"Sent successfully (Resend ID: {email_id})"
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            return False, f"Resend API error {e.code}: {err_msg}"
        except Exception as e:
            return False, f"Email transport error: {str(e)}"

    def dispatch_issue(self, recipients: List[str], issue_number: int, markdown_content: str) -> Dict[str, Any]:
        """Sends the daily dispatch to the subscriber list."""
        if not recipients:
            return {"sent": 0, "failed": 0, "message": "No active recipients."}

        subject = f"WITTYWEIGHTS // DISPATCH #{issue_number:02d}"
        html_body = self._render_html(markdown_content)

        results = {"sent": 0, "failed": 0, "details": []}

        for email in recipients:
            payload = {
                "from": f"WittyWeights <{self.from_email}>",
                "to": [email],
                "subject": subject,
                "html": html_body,
                "text": markdown_content
            }
            success, msg = self._send_resend_request(payload)
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1
            results["details"].append({"email": email, "status": "sent" if success else "failed", "info": msg})

        return results

    def dispatch_welcome(self, recipient: str, latest_issue_text: str = "") -> Tuple[bool, str]:
        """Sends immediate confirmation & welcome dispatch to a newly onboarded subscriber."""
        subject = "WITTYWEIGHTS // SUBSCRIPTION CONFIRMED"
        divider = "-" * 72
        welcome_text = f"""WITTYWEIGHTS // WELCOME CONFIRMATION
------------------------------------------------------------------------
You are now subscribed to WittyWeights.

SCHEDULE: Monday through Friday at 07:00.
STANDARD: Zero PR fluff. Zero benchmark theatre. High-signal applied AI.
TOPICS:   Production Systems, InsurTech Risk, Model Optimization.

Below is our latest dispatch for your reference.
{divider}

{latest_issue_text}
"""
        html_body = self._render_html(welcome_text)
        payload = {
            "from": f"WittyWeights <{self.from_email}>",
            "to": [recipient],
            "subject": subject,
            "html": html_body,
            "text": welcome_text
        }
        return self._send_resend_request(payload)
