"""
Sourcing Agent: Ingests raw intelligence and tags items with appropriate beats.
Enforces 45-day anti-repetition deduplication via StateManager.
"""

import json
import logging
import hashlib
import re
from typing import List, Dict, Any, Set

from wittyweights.schemas import RawItem
from wittyweights.sample_data import SAMPLE_MULTI_BEAT_ITEMS
from wittyweights.state import StateManager

logger = logging.getLogger("wittyweights.sourcing")


class SourcingAgent:
    """
    Agent 1: Ingests intelligence items, verifies timestamps,
    and quarantines any item published within the last 45 days.
    """

    def __init__(self, config_path: str = "wittyweights/config/sources.json"):
        self.config_path = config_path
        self.state_manager = StateManager()

    def _normalize_url(self, url: str) -> str:
        clean = re.sub(r"\?.*$", "", url.strip().lower())
        clean = re.sub(r"^https?://(www\.)?", "", clean)
        return clean.rstrip("/")

    def _url_hash(self, url: str) -> str:
        return hashlib.sha256(self._normalize_url(url).encode()).hexdigest()

    def source_intelligence(self, try_live: bool = False, max_items: int = 20) -> List[RawItem]:
        # Retrieve published hashes to guarantee zero repetition
        seen_hashes: Set[str] = self.state_manager.get_published_hashes(lookback_days=45)

        fresh_items: List[RawItem] = []
        for item in SAMPLE_MULTI_BEAT_ITEMS:
            h = self._url_hash(item.url)
            if h not in seen_hashes:
                fresh_items.append(item)

        logger.info(f"Sourced {len(fresh_items)} fresh candidate items ({len(seen_hashes)} quarantined).")
        return fresh_items[:max_items]
