"""
Newsroom Debate Coordinator:
Orchestrates cross-beat peer debate among the 3 specialized journalists
and applies flexible Top-5 selection with Insurance priority weighting.
"""

from typing import List, Dict, Any, Tuple
from wittyweights.schemas import (
    JournalistPitch,
    ChallengerEvaluation,
    PeerDebateChallenge,
    RankedStory,
    BeatName
)
from wittyweights.agents.so_what import SoWhatAgent


class NewsroomDebateCoordinator:
    """
    Coordinates the 4-phase debate protocol:
    1. Collects pitches from all 3 beat journalists
    2. Runs 'So What?' Challenger cross-examination
    3. Runs Adversarial Cross-Beat Peer Review
    4. Flexibly selects the Top 5 stories based on composite score & priority weighting
    """

    def __init__(self):
        self.so_what_agent = SoWhatAgent()

    def _generate_peer_challenge(
        self,
        pitch: JournalistPitch,
        eval_data: ChallengerEvaluation
    ) -> PeerDebateChallenge:
        """
        Simulates peer challenge from competing beat reporters.
        - Systems reporter challenges Model dev on latency/deployability
        - Insurance reporter challenges Systems on business ROI
        - Model reporter challenges Insurance on architectural novelty
        """
        beat = pitch.beat
        text_lower = pitch.draft_summary.lower()

        if beat == "model_dev_optimization":
            challenger_beat = "systems_architecture"
            challenger_name = "Systems & Architecture Reporter"
            critique = "Can an engineering team deploy this without 16 H100s or massive webhook latency spikes?"
            defense = "Yes; distilled active parameters and optimized kernel runtimes keep serving within commodity GPU constraints."
            delta = 0.04

        elif beat == "systems_architecture":
            challenger_beat = "insurance_fintech"
            challenger_name = "Insurance & FinTech Reporter"
            critique = "Does this save actual business dollars or is it just developer tooling?"
            defense = "Directly slashes cloud inference spend and prevents developer downtime, saving millions annually in infrastructure costs."
            delta = 0.04

        else:  # insurance_fintech
            challenger_beat = "model_dev_optimization"
            challenger_name = "Model Dev & Optimization Reporter"
            critique = "Is this genuine multimodal AI reasoning, or legacy heuristics wrapped in an LLM prompt?"
            defense = "Couples fine-tuned segmentation models with deterministic actuarial tables and sensor telemetry; zero prompt guessing."
            delta = 0.05  # Strong defense on domain guardrails

        return PeerDebateChallenge(
            from_beat=challenger_beat,
            to_pitch_id=pitch.pitch_id,
            challenger_name=challenger_name,
            challenge_critique=critique,
            journalist_defense=defense,
            score_delta=delta
        )

    def conduct_debate_and_select(
        self,
        pitches: List[JournalistPitch]
    ) -> Tuple[List[RankedStory], List[ChallengerEvaluation], Dict[str, int]]:
        """
        Executes cross-examination, peer debate, and flexible Top-5 selection.
        """
        evaluations: List[ChallengerEvaluation] = []
        ranked_pool: List[RankedStory] = []

        for pitch in pitches:
            eval_data = self.so_what_agent.evaluate_pitch(pitch)
            evaluations.append(eval_data)

            if eval_data.vetoed:
                continue

            peer_challenge = self._generate_peer_challenge(pitch, eval_data)

            # Priority Weighting:
            # Insurance use cases get a priority bonus (+0.07) so they naturally compete
            # aggressively for top spots, but slots remain completely flexible.
            insurance_priority_bonus = 0.07 if pitch.beat == "insurance_fintech" else 0.0

            # Composite Score:
            # 30% Beat Relevance + 45% Pragmatism/Evidence + 15% Debate Defense + Priority Bonus
            composite = (
                (0.30 * pitch.beat_relevance_score) +
                (0.45 * eval_data.pragmatism_score) +
                (0.15 * (0.80 + peer_challenge.score_delta)) +
                insurance_priority_bonus
            )
            composite = round(min(1.0, composite), 3)

            ranked_pool.append(
                RankedStory(
                    pitch=pitch,
                    challenger_eval=eval_data,
                    peer_challenges=[peer_challenge],
                    composite_score=composite,
                    rank=0,
                    selected_for_top_5=False
                )
            )

        # Flexible Top 5 Selection: Sort purely by composite score
        ranked_pool.sort(key=lambda s: s.composite_score, reverse=True)

        top_5 = ranked_pool[:5]
        beat_breakdown: Dict[str, int] = {
            "systems_architecture": 0,
            "insurance_fintech": 0,
            "model_dev_optimization": 0
        }

        for idx, story in enumerate(top_5, 1):
            story.rank = idx
            story.selected_for_top_5 = True
            beat_breakdown[story.pitch.beat] += 1

        return top_5, evaluations, beat_breakdown
