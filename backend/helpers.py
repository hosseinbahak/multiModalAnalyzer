# backend/utils/helpers.py
"""
Helper functions and type definitions for the multimodal analysis system.
"""
from typing import TypedDict, Optional

class ToolState(TypedDict):
    """
    Type definition for the state passed between agents and tools.
    """
    history: str
    use_tool: bool
    tool_exec: str
    tools_list: str
    image_path: Optional[str]
    pdf_path: Optional[str]

def clip_history(history: str, max_chars: int = 8000) -> str:
    """
    Clip the conversation history to the specified maximum number of characters.
    
    Args:
        history: The conversation history text
        max_chars: Maximum number of characters to keep
        
    Returns:
        The clipped history string
    """
    if len(history) > max_chars:
        return history[-max_chars:]
    return history