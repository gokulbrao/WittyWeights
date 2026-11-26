#!/usr/bin/env python3
"""
WittyWeights Unified CLI & Service Runner
Usage:
    python3 run_newsletter.py                     # Compiles the latest issue (auto-increments)
    python3 run_newsletter.py --serve [--port 8080] # Starts web landing page & signup server
    python3 run_newsletter.py --dispatch          # Compiles & emails subscribers (Cloud Run Job / Cron)
    python3 run_newsletter.py --subscribe email@domain.com # Adds a subscriber manually
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wittyweights.orchestrator import NewsletterOrchestrator
from wittyweights.state import StateManager
from wittyweights.email_dispatcher import EmailDispatcher


def main():
    state = StateManager()
    default_next_issue = max(1, state.get_latest_issue_number() + 1)

    parser = argparse.ArgumentParser(description="WittyWeights Unified CLI & Service Runner")
    parser.add_argument("--issue", type=int, default=default_next_issue, help=f"Issue number (default: {default_next_issue})")
    parser.add_argument("--serve", action="store_true", help="Start web landing page & signup server")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8080)), help="Port for web server (default: 8080)")
    parser.add_argument("--dispatch", action="store_true", help="Execute Mon-Fri scheduled run and email subscribers")
    parser.add_argument("--subscribe", type=str, help="Add a subscriber email and send welcome dispatch")
    parser.add_argument("--live", action="store_true", help="Attempt live RSS polling")
    parser.add_argument("--quiet", action="store_true", help="Suppress verbose output")

    args = parser.parse_args()

    dispatcher = EmailDispatcher()

    # Mode 1: Start Web Server (Cloud Run Service)
    if args.serve:
        from wittyweights.web.server import run_server
        run_server(port=args.port)
        return

    # Mode 2: Manual Subscription
    if args.subscribe:
        success, msg = state.add_subscriber(args.subscribe, source="cli")
        print(f"Subscription status for {args.subscribe}: {msg}")
        if success:
            latest_file = os.path.join("output", "latest.md")
            latest_text = ""
            if os.path.exists(latest_file):
                with open(latest_file, "r", encoding="utf-8") as f:
                    latest_text = f.read()
            sent, send_msg = dispatcher.dispatch_welcome(args.subscribe, latest_issue_text=latest_text)
            print(f"Welcome email: {send_msg}")
        return

    # Mode 3: Scheduled Dispatch (Cloud Run Job / Cloud Scheduler)
    if args.dispatch:
        print(f"🕒 Running Scheduled Mon-Fri Dispatch for Issue #{args.issue}...")
        orchestrator = NewsletterOrchestrator()
        issue = orchestrator.run_pipeline(issue_number=args.issue, try_live_feeds=args.live, verbose=not args.quiet)

        # Record stories to prevent repetition
        state.record_published_stories(issue.top_5_stories, issue.issue_number)

        # Dispatch emails
        subscribers = state.get_active_subscribers()
        print(f"📬 Sending to {len(subscribers)} active subscribers...")
        results = dispatcher.dispatch_issue(
            recipients=subscribers,
            issue_number=issue.issue_number,
            markdown_content=issue.markdown_content
        )
        print(f"✅ Dispatch complete: {results['sent']} sent, {results['failed']} failed.")
        return

    # Mode 4: Default Issue Compilation
    orchestrator = NewsletterOrchestrator()
    issue = orchestrator.run_pipeline(
        issue_number=args.issue,
        try_live_feeds=args.live,
        verbose=not args.quiet
    )

    # Automatically commit published items to deduplication state so tomorrow won't repeat
    state.record_published_stories(issue.top_5_stories, issue.issue_number)

    print(f"🎉 Newsletter Issue #{issue.issue_number} compiled successfully!")
    print("📍 Open: output/latest.md or run 'python3 run_newsletter.py --serve' to preview the web page.\n")


if __name__ == "__main__":
    main()
