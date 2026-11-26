"""
Orchestrator: Multi-Beat Newsroom Pipeline
Coordinates:
- 1 Sourcing Agent
- 3 Specialized Beat Journalists (Systems, Insurance/FinTech, Model Dev)
- 1 'So What?' Challenger & Newsroom Debate Coordinator
- 1 Editor Agent
- 1 Publishing Agent
"""

import logging
from wittyweights.agents.sourcing import SourcingAgent
from wittyweights.agents.journalists import (
    SystemsArchitectJournalist,
    InsuranceFintechJournalist,
    ModelDevJournalist
)
from wittyweights.agents.newsroom import NewsroomDebateCoordinator
from wittyweights.agents.editor import EditorAgent
from wittyweights.agents.publishing import PublishingAgent
from wittyweights.schemas import NewsletterIssue

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("wittyweights.orchestrator")


class NewsletterOrchestrator:
    """
    Coordinates the 3-journalist newsroom, cross-beat debate, and flexible Top-5 publication.
    """

    def __init__(self, config_path: str = "wittyweights/config/sources.json"):
        self.sourcing_agent = SourcingAgent(config_path=config_path)
        self.systems_journalist = SystemsArchitectJournalist()
        self.insurance_journalist = InsuranceFintechJournalist()
        self.model_journalist = ModelDevJournalist()
        self.debate_coordinator = NewsroomDebateCoordinator()
        self.editor_agent = EditorAgent()
        self.publishing_agent = PublishingAgent()

    def run_pipeline(
        self,
        issue_number: int = 1,
        try_live_feeds: bool = False,
        verbose: bool = True
    ) -> NewsletterIssue:
        if verbose:
            print("\n" + "=" * 70)
            print("📰  WITTYWEIGHTS: 3-BEAT NEWSROOM & TOP-5 DEBATE PIPELINE")
            print("=" * 70 + "\n")

        # Step 1: Ingest
        if verbose:
            print("📡 [Sourcing Agent] Ingesting intelligence across systems, insurance & models...")
        raw_items = self.sourcing_agent.source_intelligence(try_live=try_live_feeds)
        if verbose:
            print(f"   ✓ Sourced {len(raw_items)} candidate intelligence items.\n")

        # Step 2: 3 Beat Journalists Pitch
        if verbose:
            print("📝 [3 Beat Journalists] Pitching candidate stories from the field...")
        sys_pitches = self.systems_journalist.pitch_stories(raw_items)
        ins_pitches = self.insurance_journalist.pitch_stories(raw_items)
        mod_pitches = self.model_journalist.pitch_stories(raw_items)
        all_pitches = sys_pitches + ins_pitches + mod_pitches

        if verbose:
            print(f"   ✓ Systems & Architecture Reporter: {len(sys_pitches)} pitches")
            print(f"   ✓ Insurance & FinTech Lead Reporter: {len(ins_pitches)} pitches (Priority Beat)")
            print(f"   ✓ Model Dev & Optimization Reporter: {len(mod_pitches)} pitches")
            print(f"   → Total candidate newsroom pool: {len(all_pitches)} stories.\n")

        # Step 3: Newsroom Debate & Flexible Top-5 Selection
        if verbose:
            print("⚔️  [Newsroom Debate & Challenger] Cross-examining pitches & running peer debate...")
        top_5_ranked, evaluations, beat_breakdown = self.debate_coordinator.conduct_debate_and_select(all_pitches)

        if verbose:
            print("   ✓ Debate complete! Dynamic Top-5 slate selected:")
            for s in top_5_ranked:
                print(f"      #{s.rank} [{s.pitch.beat}] {s.pitch.headline[:55]}... (Score: {s.composite_score})")
            print(f"   📊 Dynamic Mix: {beat_breakdown['insurance_fintech']} Insurance, "
                  f"{beat_breakdown['systems_architecture']} Systems, "
                  f"{beat_breakdown['model_dev_optimization']} Model Dev.\n")

        # Step 4: Editorial Polish
        if verbose:
            print("✒️  [Editor Agent] Polishing Top 5 into WittyWeights format (succinct & witty)...")
        edited_stories = self.editor_agent.edit_top_5(top_5_ranked)
        if verbose:
            print(f"   ✓ Editorial complete on all {len(edited_stories)} stories.\n")

        # Step 5: Publishing
        if verbose:
            print("📦 [Publishing Agent] Formatting Top-5 issue into email-ready Markdown (.md)...")
        issue = self.publishing_agent.format_newsletter(
            issue_number=issue_number,
            top_5_stories=edited_stories,
            beat_breakdown=beat_breakdown,
            all_evaluations=evaluations,
            ranked_stories=top_5_ranked
        )
        if verbose:
            print(f"   ✓ Published WittyWeights Issue #{issue_number} successfully!")
            print(f"   📁 Output file: output/latest.md")
            print("=" * 70 + "\n")

        return issue
