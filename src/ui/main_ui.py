"""
Main UI components for TweetCraft application.
"""

import streamlit as st
import time
from typing import Tuple

from ..utils.api_keys import validate_openai_api_key, validate_tavily_api_key


def init_streamlit():
    """Initialize Streamlit configuration"""
    st.set_page_config(
        page_title="TweetCraft - AI Thread Generator",
        page_icon="🧵",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def render_header():
    """Render the application header"""
    st.title("🧵 TweetCraft")
    st.markdown("**Advanced Multi-Agent Tweet Thread Generator**")
    st.markdown("*Powered by LangGraph, GPT-4o, and Tavily Search*")


def render_api_keys() -> Tuple[str, str, bool]:
    """
    Render API key validation in main area.
    
    Returns:
        Tuple containing: openai_key, tavily_key, keys_valid
    """
    st.header("🔑 API Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("OpenAI API Key")
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Your OpenAI API key for GPT-4o",
            key="openai_key"
        )
        
        if openai_key:
            with st.spinner("Validating OpenAI API key..."):
                if validate_openai_api_key(openai_key):
                    st.success("✅ Valid OpenAI API key")
                    openai_valid = True
                else:
                    st.error("❌ Invalid OpenAI API key")
                    openai_valid = False
        else:
            openai_valid = False
    
    with col2:
        st.subheader("Tavily API Key")
        tavily_key = st.text_input(
            "Tavily API Key",
            type="password", 
            placeholder="tvly-...",
            help="Your Tavily API key for web search",
            key="tavily_key"
        )
        
        if tavily_key:
            with st.spinner("Validating Tavily API key..."):
                if validate_tavily_api_key(tavily_key):
                    st.success("✅ Valid Tavily API key")
                    tavily_valid = True
                else:
                    st.error("❌ Invalid Tavily API key")
                    tavily_valid = False
        else:
            tavily_valid = False
    
    return openai_key, tavily_key, openai_valid and tavily_valid


def render_topic_input() -> str:
    """
    Render topic input section.
    
    Returns:
        str: User input topic
    """
    st.header("📝 Create Your Thread")
    
    topic = st.text_area(
        "What's your thread about?",
        placeholder="Enter your topic or idea... (e.g., 'The future of AI in healthcare', 'Why remote work is changing everything')",
        height=100
    )
    
    return topic


def render_agent_status(current_agent: str, progress: int):
    """
    Render animated agent status.
    
    Args:
        current_agent (str): Currently active agent
        progress (int): Progress percentage
    """
    agents = {
        "research": {"emoji": "🔍", "name": "Research Agent", "desc": "Gathering intelligence..."},
        "strategy": {"emoji": "📋", "name": "Strategy Agent", "desc": "Planning thread structure..."},
        "writer": {"emoji": "✍️", "name": "Writer Agent", "desc": "Crafting compelling content..."},
        "editor": {"emoji": "✨", "name": "Editor Agent", "desc": "Polishing to perfection..."},
        "supervisor": {"emoji": "🎯", "name": "Supervisor Agent", "desc": "Quality control check..."},
        "analytics": {"emoji": "📊", "name": "Analytics Agent", "desc": "Optimizing for engagement..."}
    }
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.progress(progress / 100)
    
    with col2:
        if current_agent in agents:
            agent_info = agents[current_agent]
            st.markdown(f"""
            **{agent_info['emoji']} {agent_info['name']}**  
            *{agent_info['desc']}*
            """)
        
        # Show all agents with status
        status_cols = st.columns(6)
        for i, (agent_key, agent_info) in enumerate(agents.items()):
            with status_cols[i]:
                if agent_key == current_agent:
                    st.markdown(f"🟢 {agent_info['emoji']}")
                elif progress > (i * 16.67):
                    st.markdown(f"✅ {agent_info['emoji']}")
                else:
                    st.markdown(f"⚪ {agent_info['emoji']}")