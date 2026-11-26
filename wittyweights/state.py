"""
State Engine:
1. DeduplicationEngine: Stores SHA-256 hashes of published stories to guarantee zero repetition (45-day window).
2. SubscriberManager: Manages subscriber email signups and onboarding status.
Supports both GCP Firestore and local JSON file persistence for offline/local testing.
"""

import os
import json
import hashlib
import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Set, Optional, Any, Tuple


class StateManager:
    """
    Manages persistent state:
    - Published story hashes (to prevent duplicates)
    - Subscriber list
    - Edition history
    Uses Firestore when available (GCP), otherwise falls back to local JSON files in data/
    """

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(self.data_dir, exist_ok=True)
        self.published_file = os.path.join(self.data_dir, "published_items.json")
        self.subscribers_file = os.path.join(self.data_dir, "subscribers.json")
        self.firestore_client = self._init_firestore()

    def _init_firestore(self):
        """Attempts to initialize GCP Firestore client if credentials exist."""
        if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("K_SERVICE"):
            try:
                from google.cloud import firestore
                return firestore.Client()
            except Exception:
                return None
        return None

    def _normalize_url(self, url: str) -> str:
        clean = re.sub(r"\?.*$", "", url.strip().lower())
        clean = re.sub(r"^https?://(www\.)?", "", clean)
        return clean.rstrip("/")

    def _url_hash(self, url: str) -> str:
        return hashlib.sha256(self._normalize_url(url).encode()).hexdigest()

    # --- DEDUPLICATION (45-DAY SLIDING WINDOW) ---

    def get_published_hashes(self, lookback_days: int = 45) -> Set[str]:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=lookback_days)).isoformat()
        hashes: Set[str] = set()

        if self.firestore_client:
            try:
                docs = self.firestore_client.collection("published_items").where("published_at", ">=", cutoff).stream()
                for doc in docs:
                    hashes.add(doc.id)
                return hashes
            except Exception:
                pass

        # Local fallback
        if os.path.exists(self.published_file):
            try:
                with open(self.published_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item_hash, meta in data.items():
                        if meta.get("published_at", "") >= cutoff:
                            hashes.add(item_hash)
            except Exception:
                pass

        return hashes

    def get_latest_issue_number(self) -> int:
        if os.path.exists(self.published_file):
            try:
                with open(self.published_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    issues = [v.get("issue_number", 0) for v in data.values()]
                    if issues:
                        return max(issues)
            except Exception:
                pass
        return 0

    def record_published_stories(self, stories: list, issue_number: int):
        now_str = datetime.now(timezone.utc).isoformat()
        records: Dict[str, Any] = {}

        for story in stories:
            h = self._url_hash(story.canonical_url)
            records[h] = {
                "headline": story.headline,
                "canonical_url": story.canonical_url,
                "beat": story.beat,
                "issue_number": issue_number,
                "published_at": now_str
            }

        # Write to Firestore if available
        if self.firestore_client:
            try:
                batch = self.firestore_client.batch()
                for h, data in records.items():
                    ref = self.firestore_client.collection("published_items").document(h)
                    batch.set(ref, data)
                batch.commit()
            except Exception:
                pass

        # Write to local JSON
        existing = {}
        if os.path.exists(self.published_file):
            try:
                with open(self.published_file, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            except Exception:
                existing = {}

        existing.update(records)
        with open(self.published_file, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=2)

    # --- SUBSCRIBER MANAGEMENT ---

    def add_subscriber(self, email: str, source: str = "web_signup") -> Tuple[bool, str]:
        email_clean = email.strip().lower()
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email_clean):
            return False, "Invalid email address format."

        email_hash = hashlib.sha256(email_clean.encode()).hexdigest()
        now_str = datetime.now(timezone.utc).isoformat()
        record = {
            "email": email_clean,
            "active": True,
            "source": source,
            "subscribed_at": now_str
        }

        # Firestore
        if self.firestore_client:
            try:
                ref = self.firestore_client.collection("subscribers").document(email_hash)
                doc = ref.get()
                if doc.exists and doc.to_dict().get("active"):
                    return True, "Already subscribed."
                ref.set(record)
            except Exception:
                pass

        # Local JSON
        subscribers = {}
        if os.path.exists(self.subscribers_file):
            try:
                with open(self.subscribers_file, "r", encoding="utf-8") as f:
                    subscribers = json.load(f)
            except Exception:
                subscribers = {}

        if email_hash in subscribers and subscribers[email_hash].get("active"):
            return True, "Already subscribed."

        subscribers[email_hash] = record
        with open(self.subscribers_file, "w", encoding="utf-8") as f:
            json.dump(subscribers, f, indent=2)

        return True, "Subscribed successfully."

    def get_active_subscribers(self) -> List[str]:
        emails: List[str] = []

        if self.firestore_client:
            try:
                docs = self.firestore_client.collection("subscribers").where("active", "==", True).stream()
                for doc in docs:
                    data = doc.to_dict()
                    if "email" in data:
                        emails.append(data["email"])
                if emails:
                    return emails
            except Exception:
                pass

        # Local JSON
        if os.path.exists(self.subscribers_file):
            try:
                with open(self.subscribers_file, "r", encoding="utf-8") as f:
                    subscribers = json.load(f)
                    for _, data in subscribers.items():
                        if data.get("active") and "email" in data:
                            emails.append(data["email"])
            except Exception:
                pass

        return emails
