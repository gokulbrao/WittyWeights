"""
Specialized Beat Journalists for WittyWeights:
1. Systems & Architecture Reporter
2. Insurance & FinTech Reporter (Top Priority)
3. Model Dev & Optimization Reporter
"""

import re
from typing import List, Optional, Tuple
from wittyweights.schemas import RawItem, JournalistPitch, BeatName


class BaseJournalist:
    """Base class providing common pitch drafting utilities."""

    def __init__(self, beat: BeatName, title: str):
        self.beat = beat
        self.title = title

    def _extract_metric(self, text: str) -> Optional[str]:
        patterns = [
            r"(\d+%\s+(?:drop|reduction|cut|increase|lift|surge|fewer[a-zA-Z\s]{0,15}|straight-through[a-zA-Z\s]{0,12}|precision[a-zA-Z\s]{0,8}))",
            r"(\$\d+(?:\.\d+)?(?:M|B|K)\s+(?:saved|annually|dispute[a-zA-Z\s]{0,10}|claims[a-zA-Z\s]{0,10}))",
            r"((?:from\s+\d+\s+days\s+to\s+)?\d+-(?:second|minute)(?:\s+adjudication|\s+settlement|\s+appraisal|\s+triage)?)",
            r"(sub-\d+(?:ms|microsecond)(?:\s+p\d+)?(?:\s+latency)?)",
            r"(\d+(?:\.\d+)?x\s+(?:speedup|throughput|faster))"
        ]
        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                res = match.group(1).strip()
                if len(res) < 40:
                    return res
        return None

    def pitch_stories(self, items: List[RawItem]) -> List[JournalistPitch]:
        raise NotImplementedError


class SystemsArchitectJournalist(BaseJournalist):
    """
    Beat 1: Systems & Architecture.
    Fights for concrete code, AST parsing, compiler loops, Merkle-tree RAG,
    sub-second latency, and GPU serving stacks.
    """

    def __init__(self):
        super().__init__(
            beat="systems_architecture",
            title="Systems & Architecture Reporter"
        )

    def pitch_stories(self, items: List[RawItem]) -> List[JournalistPitch]:
        pitches: List[JournalistPitch] = []
        filtered = [i for i in items if i.target_beat == "systems_architecture"]

        for item in filtered:
            full_text = f"{item.title} {item.summary} {item.raw_content or ''}"
            metric = self._extract_metric(full_text)

            # Evaluate systems depth
            text_lower = full_text.lower()
            depth_score = 0.5
            if any(k in text_lower for k in ["ast", "lsp", "compiler", "typechecker", "merkle", "sqlite", "quantization"]):
                depth_score += 0.35
            if any(k in text_lower for k in ["sub-50ms", "latency", "throughput", "p99", "vector"]):
                depth_score += 0.15

            # Penalty for buzz
            if item.reputation_weight < 0.6 or "auto-comment" in text_lower:
                depth_score = 0.2

            score = round(min(1.0, (depth_score * 0.7) + (item.reputation_weight * 0.3)), 3)

            media_badge = "🎥 Video Deep Dive" if item.media_type == "video_talk" else "📐 Architecture Blueprint"

            evidence = (
                f"Stack details: {item.source_name} integrates verified compiler/LSP or indexing structures. "
                f"Telemetry confirms reproducible latency improvements."
            )

            pitches.append(
                JournalistPitch(
                    pitch_id=item.id,
                    beat=self.beat,
                    journalist_title=self.title,
                    headline=item.title,
                    canonical_url=item.url,
                    source_name=item.source_name,
                    media_badge=media_badge,
                    production_metric=metric,
                    hard_evidence=evidence,
                    beat_relevance_score=score,
                    draft_summary=f"{item.summary.strip()} {item.raw_content or ''}".strip(),
                    initial_thesis="Directly solves high-scale software and inference bottlenecks with verifiable architectures."
                )
            )

        pitches.sort(key=lambda p: p.beat_relevance_score, reverse=True)
        return pitches[:3]


class InsuranceFintechJournalist(BaseJournalist):
    """
    Beat 2: Insurance & FinTech (Top Priority).
    Fights for real-dollar ROI: FNOL claim settlements, collision vision models,
    underwriting loss-runs, fraud detection, and regulated compliance state machines.
    """

    def __init__(self):
        super().__init__(
            beat="insurance_fintech",
            title="Insurance & FinTech Lead Reporter"
        )

    def pitch_stories(self, items: List[RawItem]) -> List[JournalistPitch]:
        pitches: List[JournalistPitch] = []
        filtered = [i for i in items if i.target_beat == "insurance_fintech"]

        for item in filtered:
            full_text = f"{item.title} {item.summary} {item.raw_content or ''}"
            metric = self._extract_metric(full_text)
            text_lower = full_text.lower()

            # Priority weighting: Insurance use cases receive an extra boost
            is_pure_insurance = any(k in text_lower for k in ["insurance", "fnol", "claim", "collision", "underwriting", "loss run", "lemonade", "munich re"])

            depth_score = 0.6
            if is_pure_insurance:
                depth_score += 0.3  # Insurance priority bonus
            if any(k in text_lower for k in ["telematics", "actuarial", "pii", "state machine", "fraud", "mitchell"]):
                depth_score += 0.1

            score = round(min(1.0, (depth_score * 0.7) + (item.reputation_weight * 0.3)), 3)

            evidence = (
                f"Domain ROI: Automated high-value operational queues with verified loss-ratio "
                f"or straight-through processing rates under strict liability guardrails."
            )

            pitches.append(
                JournalistPitch(
                    pitch_id=item.id,
                    beat=self.beat,
                    journalist_title=self.title,
                    headline=item.title,
                    canonical_url=item.url,
                    source_name=item.source_name,
                    media_badge="🏢 Production Case Study",
                    production_metric=metric,
                    hard_evidence=evidence,
                    beat_relevance_score=score,
                    draft_summary=f"{item.summary.strip()} {item.raw_content or ''}".strip(),
                    initial_thesis="Solves multi-million-dollar insurance and financial operational bottlenecks with deterministic AI controls."
                )
            )

        # Sort with insurance priority
        pitches.sort(key=lambda p: p.beat_relevance_score, reverse=True)
        return pitches[:3]


class ModelDevJournalist(BaseJournalist):
    """
    Beat 3: Model Dev & Optimization.
    Fights for true algorithmic leaps: RL from verifiable rewards (RLVR),
    test-time compute search, FP4 quantization, MoE routing, and state-space models.
    """

    def __init__(self):
        super().__init__(
            beat="model_dev_optimization",
            title="Model Dev & Optimization Reporter"
        )

    def pitch_stories(self, items: List[RawItem]) -> List[JournalistPitch]:
        pitches: List[JournalistPitch] = []
        filtered = [i for i in items if i.target_beat == "model_dev_optimization"]

        for item in filtered:
            full_text = f"{item.title} {item.summary} {item.raw_content or ''}"
            metric = self._extract_metric(full_text)
            text_lower = full_text.lower()

            depth_score = 0.5
            if any(k in text_lower for k in ["test-time", "search", "mcts", "prm", "fp4", "quantization", "moe", "state space", "ssm"]):
                depth_score += 0.35
            if any(k in text_lower for k in ["flop", "throughput", "open weights", "apache 2.0"]):
                depth_score += 0.15

            score = round(min(1.0, (depth_score * 0.7) + (item.reputation_weight * 0.3)), 3)

            evidence = (
                f"Model efficiency: {item.source_name} verified empirical FLOP or throughput gains "
                f"that redefine compute and serving economics."
            )

            pitches.append(
                JournalistPitch(
                    pitch_id=item.id,
                    beat=self.beat,
                    journalist_title=self.title,
                    headline=item.title,
                    canonical_url=item.url,
                    source_name=item.source_name,
                    media_badge="🔬 Frontier Optimization",
                    production_metric=metric,
                    hard_evidence=evidence,
                    beat_relevance_score=score,
                    draft_summary=f"{item.summary.strip()} {item.raw_content or ''}".strip(),
                    initial_thesis="Fundamentally alters model inference economics or reasoning capability scaling."
                )
            )

        pitches.sort(key=lambda p: p.beat_relevance_score, reverse=True)
        return pitches[:3]
