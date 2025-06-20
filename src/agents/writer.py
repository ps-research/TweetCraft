"""
Writer Agent - Creates compelling tweet content.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState
from ..utils.text_processing import extract_tweets_from_content


class WriterAgent:
    """✍️ Creates compelling tweet content"""
    
    def __init__(self, llm):
        """
        Initialize the Writer Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute writing phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with draft tweets
        """
        strategy_plan = state["strategy_plan"]
        research_data = state["research_data"]
        topic = state["topic"]
        style = state["style"]
        num_tweets = state["num_tweets"]
        word_limit = state["word_limit"]
        
        writing_prompt = f"""
        Using this strategy plan:
        {strategy_plan}
        
        And this research:
        {research_data}
        
        Write a {num_tweets}-tweet thread about "{topic}" in {style} style.
        
        REQUIREMENTS:
        - Each tweet max {word_limit} words
        - Must be engaging and {style}
        - Include relevant emojis
        - Strong hook in first tweet
        - Clear flow between tweets
        - Compelling call-to-action at the end
        
        Return ONLY the tweets, numbered 1-{num_tweets}, nothing else.
        """
        
        draft_content = self.llm.invoke([
            SystemMessage(content=f"You are an expert {style} content writer who creates viral social media content."),
            HumanMessage(content=writing_prompt)
        ]).content
        
        # Extract individual tweets
        tweets = extract_tweets_from_content(draft_content, num_tweets)
        
        return {
            **state,
            "draft_tweets": tweets,
            "current_agent": "editor"
        }