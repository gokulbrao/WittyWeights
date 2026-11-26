"""
Pydantic data schemas for Multi-Journalist Newsroom:
- 3 Specialized Beat Journalists
- Adversarial 'So What?' Challenger
- Cross-Beat Peer Debate
- Flexible Top-5 Slate Selection
- Editorial & Publishing
"""

from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

BeatName = Literal["systems_architecture", "insurance_fintech", "model_dev_optimization"]


class RawItem(BaseModel):
    id: str
    source_name: str
    source_category: str
    reputation_weight: float
    title: str
    url: str
    published_date: str
    summary: str
    media_type: Literal["blog", "case_study", "video_talk", "tooling_release", "research_paper"] = "blog"
    target_beat: Optional[BeatName] = None
    raw_content: Optional[str] = None


class JournalistPitch(BaseModel):
    pitch_id: str
    beat: BeatName
    journalist_title: str
    headline: str
    canonical_url: str
    source_name: str
    media_badge: str
    production_metric: Optional[str] = None
    hard_evidence: str  # Stack, claims/actuarial data, or FLOP/quantization numbers
    beat_relevance_score: float = Field(ge=0.0, le=1.0)
    draft_summary: str
    initial_thesis: str


class ChallengerEvaluation(BaseModel):
    pitch_id: str
    challenge_question: str
    defense_response: str
    pragmatism_score: float = Field(ge=0.0, le=1.0)
    second_order_impact: str
    vetoed: bool = False
    veto_reason: Optional[str] = None


class PeerDebateChallenge(BaseModel):
    from_beat: BeatName
    to_pitch_id: str
    challenger_name: str
    challenge_critique: str
    journalist_defense: str
    score_delta: float = 0.0  # e.g., +0.05 for strong defense, -0.05 for weak


class RankedStory(BaseModel):
    pitch: JournalistPitch
    challenger_eval: ChallengerEvaluation
    peer_challenges: List[PeerDebateChallenge] = []
    composite_score: float
    rank: int = 0
    selected_for_top_5: bool = False


class EditedStory(BaseModel):
    rank: int
    pitch_id: str
    headline: str
    source_name: str
    canonical_url: str
    beat: BeatName
    beat_label: str  # e.g., "InsurTech & Autonomous Claims", "Systems & Architecture"
    media_badge: str
    production_metric: Optional[str] = None
    body: str  # Exactly 2 crisp sentences
    the_so_what: str  # 1 sharp builder takeaway
    word_count: int
    verified: bool = True


class NewsletterIssue(BaseModel):
    issue_number: int
    date_str: str
    edition_title: str
    intro_summary: str
    top_5_stories: List[EditedStory]
    beat_breakdown: Dict[str, int]  # Flexible count per beat
    debated_items_count: int
    rejected_items_count: int
    markdown_content: str
