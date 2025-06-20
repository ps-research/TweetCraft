"""
API key validation utilities for TweetCraft.
"""

import openai
from tavily import TavilyClient


def validate_openai_api_key(api_key: str) -> bool:
    """
    Validate OpenAI API key by attempting to list models.
    
    Args:
        api_key (str): The OpenAI API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        client.models.list()
        return True
    except openai.AuthenticationError:
        return False
    except Exception:
        return False


def validate_tavily_api_key(api_key: str) -> bool:
    """
    Validate Tavily API key by performing a test search.
    
    Args:
        api_key (str): The Tavily API key to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        client = TavilyClient(api_key=api_key)
        # Test with a simple search
        result = client.search("test", max_results=1)
        return True
    except Exception:
        return False