"""
LangGraph workflow management for the TweetCraft multi-agent system.
"""

from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI

from ..models.state import ThreadGenerationState
from ..agents.research import ResearchAgent
from ..agents.strategy import StrategyAgent
from ..agents.writer import WriterAgent
from ..agents.editor import EditorAgent
from ..agents.supervisor import SupervisorAgent
from ..agents.analytics import AnalyticsAgent


def create_thread_workflow(openai_api_key: str, tavily_api_key: str):
    """
    Creates the LangGraph workflow for tweet thread generation.
    
    Args:
        openai_api_key (str): OpenAI API key
        tavily_api_key (str): Tavily API key for search
        
    Returns:
        Compiled LangGraph workflow
    """
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        api_key=openai_api_key,
        temperature=0.7
    )
    
    # Initialize agents
    research_agent = ResearchAgent(llm, tavily_api_key)
    strategy_agent = StrategyAgent(llm)
    writer_agent = WriterAgent(llm)
    editor_agent = EditorAgent(llm)
    supervisor_agent = SupervisorAgent(llm)
    analytics_agent = AnalyticsAgent(llm)
    
    # Define routing logic
    def route_workflow(state: ThreadGenerationState) -> str:
        """
        Determine the next step in the workflow based on current state.
        
        Args:
            state (ThreadGenerationState): Current workflow state
            
        Returns:
            str: Next node in the workflow
        """
        current_agent = state.get("current_agent", "research")
        
        if current_agent == "complete":
            return END
        elif state.get("needs_revision", False):
            return "writer"  # Go back to writer for revision
        else:
            return current_agent
    
    # Create the workflow graph
    workflow = StateGraph(ThreadGenerationState)
    
    # Add nodes
    workflow.add_node("research", research_agent)
    workflow.add_node("strategy", strategy_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("editor", editor_agent)
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("analytics", analytics_agent)
    
    # Add edges
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "strategy")
    workflow.add_edge("strategy", "writer")
    workflow.add_edge("writer", "editor")
    workflow.add_edge("editor", "supervisor")
    
    # Conditional edges from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda state: "writer" if state.get("needs_revision", False) else "analytics"
    )
    
    workflow.add_edge("analytics", END)
    
    return workflow.compile()