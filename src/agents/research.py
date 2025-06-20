"""
Research Agent - Gathers comprehensive information about the topic.
"""

import streamlit as st
from tavily import TavilyClient
from langchain_core.messages import HumanMessage, SystemMessage

from ..models.state import ThreadGenerationState


class ResearchAgent:
    """🔍 Gathers comprehensive information about the topic"""
    
    def __init__(self, llm, tavily_api_key: str):
        """
        Initialize the Research Agent.
        
        Args:
            llm: Language model instance
            tavily_api_key (str): Tavily API key for web search
        """
        self.llm = llm
        self.tavily_api_key = tavily_api_key
    
    def __call__(self, state: ThreadGenerationState) -> ThreadGenerationState:
        """
        Execute research phase of the workflow.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            ThreadGenerationState: Updated state with research data
        """
        topic = state["topic"]
        style = state["style"]
        
        # Multi-angle research queries
        search_queries = [
            f"{topic} latest trends 2025",
            f"{topic} statistics facts data",
            f"{topic} expert opinions insights",
            f"{topic} case studies examples"
        ]
        
        research_results = []
        
        # Initialize Tavily client
        try:
            tavily_client = TavilyClient(api_key=self.tavily_api_key)
            
            for query in search_queries:
                try:
                    results = tavily_client.search(query, max_results=3)
                    research_results.extend(results.get('results', []))
                except Exception as e:
                    st.warning(f"Search failed for: {query}")
        except Exception as e:
            st.error(f"Tavily client initialization failed: {str(e)}")
            return {
                **state,
                "research_data": "Research unavailable due to API error",
                "current_agent": "strategy"
            }
        
        # Synthesize research with LLM
        synthesis_prompt = f"""
        Analyze this research data about "{topic}" and create a comprehensive summary:
        
        Research Results: {research_results}
        
        Please provide:
        1. Key facts and statistics
        2. Current trends and developments
        3. Different perspectives/angles
        4. Compelling hooks or interesting points
        5. Credible sources and data points
        
        Style context: The final thread will be {style} in tone.
        Focus on information that would work well for that style.
        """
        
        research_summary = self.llm.invoke([
            SystemMessage(content="You are an expert researcher who synthesizes information clearly and comprehensively."),
            HumanMessage(content=synthesis_prompt)
        ]).content
        
        return {
            **state,
            "research_data": research_summary,
            "current_agent": "strategy"
        }