"""
Text processing utilities for tweet extraction and formatting.
"""

import re
from typing import List


def extract_tweets_from_content(content: str, expected_count: int) -> List[str]:
    """
    Extract individual tweets from AI-generated content.
    
    Args:
        content (str): The content containing numbered tweets
        expected_count (int): Expected number of tweets
        
    Returns:
        List[str]: List of extracted tweet texts
    """
    lines = content.strip().split('\n')
    tweets = []
    
    for line in lines:
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('Tweet')):
            # Remove numbering and clean up
            tweet = re.sub(r'^\d+\.?\s*', '', line)
            tweet = re.sub(r'^Tweet\s*\d+:?\s*', '', tweet, flags=re.IGNORECASE)
            if tweet:
                tweets.append(tweet.strip())
    
    # Ensure we have the right number of tweets
    if len(tweets) != expected_count:
        # Fallback: split content more aggressively
        all_text = content.replace('\n', ' ')
        sentences = [s.strip() for s in all_text.split('.') if s.strip()]
        tweets = sentences[:expected_count]
    
    return tweets[:expected_count]


def count_words(text: str) -> int:
    """Count words in a text string."""
    return len(text.split())


def count_characters(text: str) -> int:
    """Count characters in a text string."""
    return len(text)