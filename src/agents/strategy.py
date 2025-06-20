"""
Strategy Agent - Plans the thread structure and strategy.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState


class StrategyAgent:
    """📋 Plans the thread structure and strategy"""
    
    def __init__(self, llm):
        """
        Initialize the Strategy Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute strategy planning phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with strategy plan
        """
        research_data = state["research_data"]
        topic = state["topic"]
        style = state["style"]
        num_tweets = state["num_tweets"]
        word_limit = state["word_limit"]
        
        strategy_prompt = f"""
        Based on this research about "{topic}":
        {research_data}
        
        Create a strategic plan for a {num_tweets}-tweet thread with {style} style.
        Each tweet should be around {word_limit} words max.
        
        Please provide:
        1. HOOK STRATEGY: How to grab attention in tweet 1
        2. FLOW STRUCTURE: What each tweet should cover
        3. ENGAGEMENT TACTICS: How to maximize engagement
        4. CALL-TO-ACTION: How to end the thread
        5. KEY MESSAGING: Main points to emphasize
        
        Format as a detailed numbered plan for each tweet.
        """
        
        strategy_plan = self.llm.invoke([
            SystemMessage(content="You are a viral content strategist who understands social media psychology and engagement."),
            HumanMessage(content=strategy_prompt)
        ]).content
        
        return {
            **state,
            "strategy_plan": strategy_plan,
            "current_agent": "writer"
        }