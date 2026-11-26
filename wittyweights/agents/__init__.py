"""
Agent exports for WittyWeights Multi-Beat Newsroom.
"""

from wittyweights.agents.sourcing import SourcingAgent
from wittyweights.agents.journalists import (
    SystemsArchitectJournalist,
    InsuranceFintechJournalist,
    ModelDevJournalist
)
from wittyweights.agents.so_what import SoWhatAgent
from wittyweights.agents.newsroom import NewsroomDebateCoordinator
from wittyweights.agents.editor import EditorAgent
from wittyweights.agents.publishing import PublishingAgent

__all__ = [
    "SourcingAgent",
    "SystemsArchitectJournalist",
    "InsuranceFintechJournalist",
    "ModelDevJournalist",
    "SoWhatAgent",
    "NewsroomDebateCoordinator",
    "EditorAgent",
    "PublishingAgent"
]
