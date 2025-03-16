"""
Insights generation and processing module for Meeting Sidekick.
This module provides functions for formatting and presenting insights to users.
"""

def format_insight_for_display(insight):
    """
    Format a single insight for display in the CLI.
    
    Args:
        insight (dict): Insight dictionary with 'title' and 'detail' keys
        
    Returns:
        str: Formatted insight string
    """
    title = insight.get('title', 'Insight')
    detail = insight.get('detail', 'No detail provided')
    
    formatted = f"[bold cyan]💡 {title}[/bold cyan]\n"
    formatted += f"[italic]{detail}[/italic]"
    
    return formatted

def categorize_insights(insights):
    """
    Categorize insights based on their content.
    This is a placeholder function that could be expanded to categorize
    insights into different types (technical, business, action recommendation, etc.)
    
    Args:
        insights (list): List of insight dictionaries
        
    Returns:
        dict: Dictionary with categorized insights
    """
    # This is a simple placeholder implementation
    # In a more advanced version, this could use NLP to categorize insights
    categories = {
        "facts": [],
        "suggestions": [],
        "other": []
    }
    
    for insight in insights:
        detail = insight.get('detail', '').lower()
        
        if "suggest" in detail or "should" in detail or "could" in detail:
            categories["suggestions"].append(insight)
        elif "fact" in detail or "data" in detail or "according to" in detail:
            categories["facts"].append(insight)
        else:
            categories["other"].append(insight)
            
    return categories

def prioritize_insights(insights, conversation_context=None):
    """
    Prioritize insights based on their relevance to the current conversation.
    
    Args:
        insights (list): List of insight dictionaries
        conversation_context (list, optional): List of recent conversation texts
        
    Returns:
        list: Prioritized list of insights
    """
    # This is a simple placeholder implementation
    # In a more advanced version, this could use semantic similarity
    # to prioritize insights based on their relevance to the conversation
    return insights  # For now, just return the insights as-is
