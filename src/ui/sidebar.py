"""
Sidebar UI components for TweetCraft customization panel.
"""

import streamlit as st
from typing import Dict, Tuple


def render_sidebar() -> Tuple[int, str, int, Dict]:
    """
    Render the customization sidebar.
    
    Returns:
        Tuple containing: num_tweets, style, word_limit, customizations
    """
    with st.sidebar:
        st.header("⚙️ Customization Panel")
        
        # Tweet count
        num_tweets = st.slider(
            "Number of Tweets",
            min_value=2,
            max_value=7,
            value=5,
            help="How many tweets in the thread"
        )
        
        # Style selection
        style = st.selectbox(
            "Thread Style",
            [
                "Professional & Informative",
                "Casual & Conversational", 
                "Humorous & Entertaining",
                "Thought-provoking & Deep"
            ],
            help="Choose the tone and style"
        )
        
        # Word limit
        word_limit = st.slider(
            "Words per Tweet",
            min_value=15,
            max_value=50,
            value=35,
            help="Maximum words per tweet"
        )
        
        # Advanced options
        with st.expander("🔧 Advanced Options"):
            include_hashtags = st.checkbox("Include hashtag suggestions", value=True)
            include_analytics = st.checkbox("Generate engagement insights", value=True)
            max_iterations = st.slider("Max revision iterations", 1, 3, 2)
        
        customizations = {
            "include_hashtags": include_hashtags,
            "include_analytics": include_analytics,
            "max_iterations": max_iterations
        }
        
        return num_tweets, style, word_limit, customizations