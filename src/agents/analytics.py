"""
Analytics Agent - Provides engagement insights and recommendations.
"""

import json
from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState


class AnalyticsAgent:
    """📊 Provides engagement insights and recommendations"""
    
    def __init__(self, llm):
        """
        Initialize the Analytics Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute analytics phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with analytics insights
        """
        polished_tweets = state["polished_tweets"]
        topic = state["topic"]
        style = state["style"]
        
        analytics_prompt = f"""
        Analyze this tweet thread for engagement optimization:
        
        {chr(10).join([f"{i+1}. {tweet}" for i, tweet in enumerate(polished_tweets)])}
        
        Provide insights on:
        1. Best posting times
        2. Hashtag recommendations (3-5 relevant hashtags)
        3. Engagement prediction (estimated likes, retweets, replies)
        4. Target audience analysis
        5. Optimization suggestions
        
        Format as JSON with keys: posting_times, hashtags, engagement_prediction, target_audience, optimization_tips
        """
        
        analytics_response = self.llm.invoke([
            SystemMessage(content="You are a social media analytics expert who provides data-driven insights."),
            HumanMessage(content=analytics_prompt)
        ]).content
        
        # Try to parse JSON, fallback to text if needed
        try:
            analytics_data = json.loads(analytics_response)
        except:
            analytics_data = {"raw_insights": analytics_response}
        
        return {
            **state,
            "analytics_insights": analytics_data,
            "current_agent": "complete"
        }