"""
Workflow setup and graph definition for the multimodal analysis system.
"""
from typing import Literal
import json
from langgraph.graph import StateGraph, END

from backend.utils.helpers import ToolState
from backend.agent.chat_agent import ChatAgent
from backend.agent.tool_agent import ToolAgent
from backend.agent.image_agent import ImageAnalysisAgent
from backend.agent.pdf_agent import PDFAnalysisAgent
from backend.tools.registry import tool_registry

# Define the function for executing tools based on agent output
def ToolExecutor(state: ToolState) -> ToolState:
    """
    Execute the selected tool based on the tool_exec field in the state.
    
    Args:
        state: The current tool state
        
    Returns:
        The updated tool state after tool execution
        
    Raises:
        ValueError: If no tool_exec data is available or if the tool is not found
    """
    if not state["tool_exec"]:
        raise ValueError("No tool_exec data available to execute.")
    
    choice = json.loads(state["tool_exec"])
    tool_name = choice["function"]
    args = choice["args"]
    
    if tool_name not in tool_registry:
        raise ValueError(f"Tool {tool_name} not found in registry.")
    
    result = tool_registry[tool_name](*args)
    state["history"] += f"\nExecuted {tool_name} with result: {result}"
    state["history"] = state["history"][-8000:] if len(state["history"]) > 8000 else state["history"]
    state["use_tool"] = False
    state["tool_exec"] = ""
    return state

# Define the image_agent function
def image_agent(state: ToolState) -> ToolState:
    """
    Execute the image analysis agent.
    
    Args:
        state: The current tool state
        
    Returns:
        The updated tool state
    """
    return ImageAnalysisAgent(state).execute()

# Define the pdf_agent function
def pdf_agent(state: ToolState) -> ToolState:
    """
    Execute the PDF analysis agent.
    
    Args:
        state: The current tool state
        
    Returns:
        The updated tool state
    """
    return PDFAnalysisAgent(state).execute()

# Define the chat_agent function
def chat_agent(state: ToolState) -> ToolState:
    """
    Execute the chat agent.
    
    Args:
        state: The current tool state
        
    Returns:
        The updated tool state
    """
    return ChatAgent(state).execute()

# Define the tool_agent function
def tool_agent(state: ToolState) -> ToolState:
    """
    Execute the tool agent.
    
    Args:
        state: The current tool state
        
    Returns:
        The updated tool state
    """
    return ToolAgent(state).execute()

# Workflow Setup
def setup_workflow():
    """
    Set up the workflow graph for processing user requests.
    
    Returns:
        The compiled workflow
    """
    workflow = StateGraph(ToolState)
    
    # Add agents
    workflow.add_node("chat_agent", chat_agent)
    workflow.add_node("tool_agent", tool_agent)
    workflow.add_node("tool", ToolExecutor)
    workflow.add_node("image_agent", image_agent)
    workflow.add_node("pdf_agent", pdf_agent)

    workflow.set_entry_point("chat_agent")

    def check_agent_type(state: ToolState) -> Literal["pdf", "image", "tool", "none"]:
        """
        Determine the next agent to use based on the current state.
        
        Args:
            state: The current tool state
            
        Returns:
            The type of agent to use next
        """
        history = state.get("history", "").lower()
        if ".pdf" in history:
            return "pdf"
        elif any(word in history for word in ["analyze image", "describe image"]):
            return "image"
        elif state.get("use_tool"):
            return "tool"
        return "none"

    workflow.add_conditional_edges(
        "chat_agent",
        check_agent_type,
        {
            "pdf": "pdf_agent",
            "image": "image_agent",
            "tool": "tool_agent",
            "none": END
        }
    )

    workflow.add_edge('pdf_agent', 'tool')
    workflow.add_edge('image_agent', 'tool')
    workflow.add_edge('tool_agent', 'tool')
    workflow.add_edge('tool', END)

    return workflow.compile()