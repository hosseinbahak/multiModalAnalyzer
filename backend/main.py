#!/usr/bin/env python3
"""
Main entry point for the multimodal analysis backend.
"""
from typing import Optional
import json
from backend.workflow import setup_workflow
from backend.tools.registry import get_tools_list
from backend.utils.helpers import ToolState
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to path

# Initialize the workflow
workflow = setup_workflow()

# Get the tools list
tools_list = get_tools_list()

# Question function to execute the workflow
def process_question(
    history: str, 
    image_path: Optional[str] = None, 
    pdf_path: Optional[str] = None
) -> dict:
    """
    Process a user question with optional image and PDF attachments.
    
    Args:
        history: The conversation history text
        image_path: Optional path to an image file
        pdf_path: Optional path to a PDF file
        
    Returns:
        The final state after processing
    """
    initial_state = ToolState(
        history=history,
        use_tool=False,
        tool_exec="",
        tools_list=tools_list,
        image_path=image_path,
        pdf_path=pdf_path
    )

    # Execute the workflow and collect the final state
    final_state = None
    for state in workflow.stream(initial_state):
        if "Error" in state.get("history", ""):
            print(f"Error encountered: {state['history']}")
            break
        final_state = state
    
    return final_state

if __name__ == "__main__":
    # Example usage for command line testing
    result = process_question(
        "Analyze this image and describe what you see.",
        image_path="./uploads/sample_image.png"
    )
    print(json.dumps(result, indent=2))