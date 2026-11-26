"""
Journalist Agent (Applied AI Edition):
Evaluates real-world ROI, production architecture, implementation depth,
and metrics (latency drop, cost cut, win-rate).
"""

from typing import List, Tuple, Optional
import re
from wittyweights.schemas import RawItem, JournalistStory


class JournalistAgent:
    """
    Agent 2: Applied AI Technology Reporter.
    Assesses concrete implementation viability, architectural rigor, and verified metrics.
    """

    def __init__(self):
        pass

    def _extract_metric(self, text: str) -> Optional[str]:
        """Extracts concise production metrics."""
        patterns = [
            r"(\d+%\s+(?:drop|reduction|cut|increase|lift|surge|fewer[a-zA-Z\s]{0,15}|straight-through[a-zA-Z\s]{0,12}))",
            r"(\$\d+(?:\.\d+)?(?:M|B|K)\s+(?:saved|annually|dispute[a-zA-Z\s]{0,10}|claims[a-zA-Z\s]{0,10}))",
            r"((?:from\s+\d+\s+days\s+to\s+)?\d+-second(?:\s+adjudication|\s+settlement|\s+appraisal)?)",
            r"(sub-\d+(?:ms|microsecond)(?:\s+p\d+)?(?:\s+latency)?)",
            r"(\d+x\s+(?:speedup|throughput))"
        ]
        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                res = match.group(1).strip()
                if len(res) < 40:
                    return res
        return None

    def _evaluate_applied_item(self, item: RawItem) -> Tuple[str, float, Optional[str], str, str]:
        text = f"{item.title} {item.summary} {item.raw_content or ''}".lower()

        metric = self._extract_metric(f"{item.title} {item.summary} {item.raw_content or ''}")

        if item.media_type == "video_talk":
            category = "Video Deep Dive"
            arch = "Technical conference session / architecture breakdown"
            thesis = "Provides a deep, pragmatic architectural walkthrough from an elite practitioner."
            roi_score = 0.94
        elif any(k in text for k in ["merkle", "vector", "quantization", "embedding", "indexing", "sub-50ms"]):
            category = "Production Blueprint"
            arch = "Large-scale search, indexing & storage architecture"
            thesis = "High-scale engineering blueprint that solves real-time indexing or retrieval bottlenecks."
            roi_score = 0.92
        elif any(k in text for k in [
            "copilot", "dispatch", "chargeback", "workflow", "state machine", "slm", "compiler",
            "fnol", "insurance", "collision", "claim", "lemonade", "appraisal"
        ]):
            category = "Applied Workflow"
            arch = "Production agent loop with deterministic domain verification"
            thesis = "Replaces manual back-office or high-cost human queues with deterministic AI workflows."
            roi_score = 0.95
        else:
            category = "Tooling & Evals"
            arch = "Developer tooling release"
            thesis = "Tooling release with practical developer utility."
            roi_score = 0.75

        # Penalize low-credibility buzz / spam
        if item.reputation_weight < 0.6 or "auto-comment" in text:
            roi_score = 0.3
            category = "Applied Workflow"
            arch = "Trivial prompt wrapper"
            thesis = "Spam bot disguised as an AI agent with zero engineering rigor."

        return category, roi_score, metric, arch, thesis

    def compile_pitches(self, raw_items: List[RawItem]) -> List[JournalistStory]:
        stories: List[JournalistStory] = []

        for item in raw_items:
            category, roi_score, metric, arch, thesis = self._evaluate_applied_item(item)

            full_tech_text = f"{item.summary.strip()} {item.raw_content or ''}".strip()

            story = JournalistStory(
                raw_item_id=item.id,
                headline=item.title,
                canonical_url=item.url,
                source_name=item.source_name,
                source_category=item.source_category,
                reputation_weight=item.reputation_weight,
                media_type=item.media_type,
                category=category,
                applied_roi_score=roi_score,
                production_metric=metric,
                draft_summary=full_tech_text,
                architecture_nutshell=arch,
                initial_thesis=thesis
            )
            stories.append(story)

        stories.sort(key=lambda s: (s.applied_roi_score, s.reputation_weight), reverse=True)
        return stories
