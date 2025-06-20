"""
Supervisor Agent - Quality control and workflow decisions.
"""

import re
from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState


class SupervisorAgent:
    """🎯 Quality control and workflow decisions"""
    
    def __init__(self, llm):
        """
        Initialize the Supervisor Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute quality control phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with quality assessment
        """
        polished_tweets = state["polished_tweets"]
        topic = state["topic"]
        style = state["style"]
        word_limit = state["word_limit"]
        iteration_count = state.get("iteration_count", 0)
        
        evaluation_prompt = f"""
        Evaluate this tweet thread for quality:
        
        Topic: {topic}
        Style: {style}
        Word limit per tweet: {word_limit}
        
        Tweets:
        {chr(10).join([f"{i+1}. {tweet}" for i, tweet in enumerate(polished_tweets)])}
        
        Rate this thread on:
        1. Engagement potential (1-10)
        2. Content quality (1-10)
        3. Style consistency (1-10)
        4. Flow and structure (1-10)
        5. Call-to-action effectiveness (1-10)
        
        Provide an overall score (1-10) and brief feedback.
        If score is below 7 and iteration count < 2, recommend revision.
        
        Format: SCORE: X.X | FEEDBACK: ... | REVISION_NEEDED: Yes/No
        """
        
        evaluation = self.llm.invoke([
            SystemMessage(content="You are a social media expert who evaluates content quality objectively."),
            HumanMessage(content=evaluation_prompt)
        ]).content
        
        # Parse evaluation
        score_match = re.search(r'SCORE:\s*(\d+\.?\d*)', evaluation)
        score = float(score_match.group(1)) if score_match else 7.0
        
        revision_match = re.search(r'REVISION_NEEDED:\s*(Yes|No)', evaluation, re.IGNORECASE)
        needs_revision = revision_match.group(1).lower() == 'yes' if revision_match else False
        
        if needs_revision and iteration_count < 2:
            return {
                **state,
                "quality_score": score,
                "needs_revision": True,
                "iteration_count": iteration_count + 1,
                "current_agent": "writer"  # Send back to writer
            }
        else:
            return {
                **state,
                "quality_score": score,
                "needs_revision": False,
                "current_agent": "analytics"
            }