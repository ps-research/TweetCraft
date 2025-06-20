"""
State definitions for the TweetCraft multi-agent system.
"""

from typing import Dict, List, Optional, TypedDict


class ThreadGenerationState(TypedDict):
    """State that flows through all agents in the workflow"""
    
    # Input parameters
    topic: str
    style: str
    num_tweets: int
    word_limit: int
    customizations: Dict
    
    # Agent outputs
    research_data: Optional[str]
    strategy_plan: Optional[str]
    draft_tweets: Optional[List[str]]
    polished_tweets: Optional[List[str]]
    analytics_insights: Optional[Dict]
    
    # Workflow control
    current_agent: str
    quality_score: Optional[float]
    needs_revision: bool
    iteration_count: int