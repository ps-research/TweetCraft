"""
TweetCraft: Advanced Multi-Agent Tweet Thread Generator
Main Streamlit application entry point.

Built with LangGraph + OpenAI GPT-4o + Tavily
"""

import streamlit as st
import time

from src.ui.main_ui import init_streamlit, render_header, render_api_keys, render_topic_input, render_agent_status
from src.ui.sidebar import render_sidebar
from src.ui.results import render_results, render_success_message
from src.workflow.thread_workflow import create_thread_workflow


def main():
    """Main Streamlit application"""
    init_streamlit()
    
    # Header
    render_header()
    
    # API Keys section (moved to main area)
    openai_key, tavily_key, keys_valid = render_api_keys()
    
    st.divider()
    
    # Sidebar customization
    num_tweets, style, word_limit, customizations = render_sidebar()
    
    # Main content
    topic = render_topic_input()
    
    # Generate button
    generate_button = st.button("✨ Generate Thread", type="primary", use_container_width=True)
    
    # Only allow generation if keys are valid
    if generate_button:
        if not topic:
            st.error("Please enter a topic!")
            return
        
        if not keys_valid:
            st.error("Please provide valid API keys above!")
            return
        
        try:
            # Initialize workflow
            workflow = create_thread_workflow(openai_key, tavily_key)
            
            # Prepare initial state
            initial_state = {
                "topic": topic,
                "style": style,
                "num_tweets": num_tweets,
                "word_limit": word_limit,
                "customizations": customizations,
                "research_data": None,
                "strategy_plan": None,
                "draft_tweets": None,
                "polished_tweets": None,
                "analytics_insights": None,
                "current_agent": "research",
                "quality_score": None,
                "needs_revision": False,
                "iteration_count": 0
            }
            
            # Progress container
            progress_container = st.empty()
            status_container = st.empty()
            
            # Execute workflow
            final_state = None
            for i, state in enumerate(workflow.stream(initial_state)):
                current_agent = list(state.keys())[0]
                current_state = state[current_agent]
                
                progress = min((i + 1) * 16.67, 100)
                
                with progress_container.container():
                    render_agent_status(current_agent, progress)
                
                time.sleep(1)  # Animation delay
                final_state = current_state
            
            # Clear progress and show results
            progress_container.empty()
            status_container.empty()
            
            if final_state:
                render_results(final_state)
                
                # Success message
                quality_score = final_state.get("quality_score", "N/A")
                render_success_message(quality_score)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your API keys and try again.")


if __name__ == "__main__":
    main()