"""
Editor Agent - Polishes and optimizes the tweets.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState
from ..utils.text_processing import extract_tweets_from_content


class EditorAgent:
    """✨ Polishes and optimizes the tweets"""
    
    def __init__(self, llm):
        """
        Initialize the Editor Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute editing phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with polished tweets
        """
        draft_tweets = state["draft_tweets"]
        style = state["style"]
        word_limit = state["word_limit"]
        
        editing_prompt = f"""
        Polish these draft tweets to perfection:
        
        {chr(10).join([f"{i+1}. {tweet}" for i, tweet in enumerate(draft_tweets)])}
        
        EDITING GOALS:
        - Ensure each tweet is under {word_limit} words
        - Optimize for {style} style
        - Improve flow and transitions
        - Enhance readability and impact
        - Perfect emoji usage
        - Ensure strong engagement potential
        
        Return the polished tweets in the same numbered format.
        """
        
        polished_content = self.llm.invoke([
            SystemMessage(content="You are a master editor who perfects social media content for maximum impact and engagement."),
            HumanMessage(content=editing_prompt)
        ]).content
        
        # Extract polished tweets
        polished_tweets = extract_tweets_from_content(polished_content, len(draft_tweets))
        
        return {
            **state,
            "polished_tweets": polished_tweets,
            "current_agent": "supervisor"
        }