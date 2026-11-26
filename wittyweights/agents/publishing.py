"""
Publishing Agent (Old Typewriter / Clean Wire Edition):
Renders in clean monospace / typewriter font.
Zero icons. Zero sales pitch. Zero newsroom metadata.
Just the 5 verified dispatches and dry builder takeaways.
"""

import os
from datetime import datetime, timezone
from typing import List, Dict
from wittyweights.schemas import EditedStory, NewsletterIssue, ChallengerEvaluation, RankedStory


class PublishingAgent:
    """
    Publishing Manager for WittyWeights.
    Produces clean, unadorned, typewriter-styled Markdown.
    """

    def __init__(self, output_dir: str = "output/editions"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def format_newsletter(
        self,
        issue_number: int,
        top_5_stories: List[EditedStory],
        beat_breakdown: Dict[str, int],
        all_evaluations: List[ChallengerEvaluation],
        ranked_stories: List[RankedStory]
    ) -> NewsletterIssue:
        now = datetime.now(timezone.utc)
        date_str = now.strftime("%d %b %Y").upper()
        file_date_str = now.strftime("%Y_%m_%d")

        divider = "-" * 72

        md_lines = []
        md_lines.append("<div style=\"font-family: 'Courier New', Courier, monospace; line-height: 1.5; color: #111;\">\n")
        md_lines.append(f"WITTYWEIGHTS // DISPATCH #{issue_number:02d}")
        md_lines.append(f"DATE: {date_str}")
        md_lines.append("TOPIC: APPLIED AI & SYSTEMS ENGINEERING IN PRODUCTION")
        md_lines.append(divider)
        md_lines.append("")
        md_lines.append("Five technical developments from this week that survived scrutiny. No PR releases, no benchmark theatre.")
        md_lines.append("")
        md_lines.append(divider)
        md_lines.append("")

        for idx, story in enumerate(top_5_stories, 1):
            md_lines.append(f"[{idx:02d}] {story.headline.upper()}")
            md_lines.append(f"Source: {story.source_name} ({story.beat_label})")
            if story.production_metric:
                md_lines.append(f"Metric: {story.production_metric}")
            md_lines.append(f"Reference: {story.canonical_url}")
            md_lines.append("")
            md_lines.append(story.body)
            md_lines.append("")
            md_lines.append(f"The takeaway: {story.the_so_what}")
            md_lines.append("")
            md_lines.append(divider)
            md_lines.append("")

        md_lines.append("END OF DISPATCH.")
        md_lines.append("Forward to an engineer who appreciates signal over noise.")
        md_lines.append("\n</div>")

        full_markdown = "\n".join(md_lines)

        issue_path = os.path.join(self.output_dir, f"issue_{file_date_str}.md")
        latest_path = os.path.join("output", "latest.md")
        os.makedirs("output", exist_ok=True)

        with open(issue_path, "w", encoding="utf-8") as f:
            f.write(full_markdown)

        with open(latest_path, "w", encoding="utf-8") as f:
            f.write(full_markdown)

        return NewsletterIssue(
            issue_number=issue_number,
            date_str=date_str,
            edition_title=f"WittyWeights Dispatch #{issue_number:02d}",
            intro_summary="Five verified applied AI developments.",
            top_5_stories=top_5_stories,
            beat_breakdown=beat_breakdown,
            debated_items_count=len(all_evaluations),
            rejected_items_count=0,
            markdown_content=full_markdown
        )
