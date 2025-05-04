"""
Main backend processing module for the multimodal analysis system.
"""
import json
from typing import Dict, Optional, Any

from backend.utils.helpers import ToolState, clip_history
from backend.tools import get_tools_list
from backend.workflow import setup_workflow

def process_question(question: str, image_path: Optional[str] = None, pdf_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Process a user question with optional image or PDF file.
    
    Args:
        question: The user's question or instruction
        image_path: Optional path to an uploaded image file
        pdf_path: Optional path to an uploaded PDF file
        
    Returns:
        The updated tool state after processing
    """
    # Initialize the state
    state = ToolState(
        history=question,
        use_tool=False,
        tool_exec="",
        tools_list=get_tools_list(),
        image_path=image_path,
        pdf_path=pdf_path
    )
    
    try:
        # Setup and run the workflow
        workflow = setup_workflow()
        result = workflow.invoke(state)
        
        # Ensure the history is properly clipped
        result["history"] = clip_history(result["history"])
        
        return result
    except Exception as e:
        # Handle any errors gracefully
        return {
            "history": f"Error processing query: {str(e)}",
            "use_tool": False,
            "tool_exec": "",
            "tools_list": get_tools_list(),
            "image_path": image_path,
            "pdf_path": pdf_path
        }