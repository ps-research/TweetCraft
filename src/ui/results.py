"""
Results UI components for displaying generated tweet threads.
"""

import streamlit as st

from ..models.state import ThreadGenerationState


def render_results(state: ThreadGenerationState):
    """
    Render the final results including tweets and analytics.
    
    Args:
        state (ThreadGenerationState): Final workflow state with generated content
    """
    if not state.get("polished_tweets"):
        return
    
    tweets = state["polished_tweets"]
    
    st.header("🧵 Your Generated Thread")
    
    # Thread preview
    for i, tweet in enumerate(tweets, 1):
        with st.container():
            st.markdown(f"""
            <div style="
                border: 1px solid #e1e5e9;
                border-radius: 12px;
                padding: 16px;
                margin: 8px 0;
                background: white;
            ">
                <strong>Tweet {i}/{len(tweets)}</strong><br>
                {tweet}<br>
                <small style="color: #657786;">
                    {len(tweet.split())} words | {len(tweet)} characters
                </small>
            </div>
            """, unsafe_allow_html=True)
    
    # Copy functionality
    full_thread = "\n\n".join([f"{i+1}. {tweet}" for i, tweet in enumerate(tweets)])
    st.text_area("📋 Copy Full Thread", full_thread, height=200)
    
    # Analytics insights
    if state.get("analytics_insights"):
        st.subheader("📊 Analytics Insights")
        insights = state["analytics_insights"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            if "hashtags" in insights:
                st.write("**Recommended Hashtags:**")
                if isinstance(insights["hashtags"], list):
                    st.write(" ".join([f"#{tag}" for tag in insights["hashtags"]]))
                else:
                    st.write(insights["hashtags"])
        
        with col2:
            if "posting_times" in insights:
                st.write("**Best Posting Times:**")
                st.write(insights["posting_times"])
        
        if "optimization_tips" in insights:
            st.write("**Optimization Tips:**")
            st.write(insights["optimization_tips"])


def render_success_message(quality_score: float):
    """
    Render success message with quality score.
    
    Args:
        quality_score (float): Quality score from supervisor agent
    """
    st.success(f"✅ Thread generated successfully! Quality Score: {quality_score}/10")