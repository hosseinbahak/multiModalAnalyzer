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

# backend/tools/registry.py
"""
Tool registry for registering and managing available tools.
"""
import inspect
import json
from typing import Dict, List, Any, Callable

# Tool registry to hold information about tools
tool_registry: Dict[str, Callable] = {}
tool_info_registry: List[Dict[str, Any]] = []

def tool(func: Callable) -> Callable:
    """
    Decorator to register tools in the tool registry.
    
    Args:
        func: The function to register as a tool
        
    Returns:
        The original function
    """
    signature = inspect.signature(func)
    docstring = func.__doc__ or ""
    params = [
        {"name": param.name, "type": param.annotation}
        for param in signature.parameters.values()
    ]
    tool_info = {
        "name": func.__name__,
        "description": docstring,
        "parameters": params
    }
    tool_registry[func.__name__] = func
    tool_info_registry.append(tool_info)
    return func

def get_tools_list() -> str:
    """
    Get a JSON string representation of all registered tools.
    
    Returns:
        JSON string with tool names and descriptions
    """
    return json.dumps([
        {
            "name": tool["name"],
            "description": tool["description"]
        }
        for tool in tool_info_registry
    ])

def execute_tool(tool_name: str, args: list) -> str:
    """
    Execute a registered tool by name with the given arguments.
    
    Args:
        tool_name: The name of the tool to execute
        args: The arguments to pass to the tool
        
    Returns:
        The result of the tool execution
        
    Raises:
        ValueError: If the tool is not found in the registry
    """
    if tool_name not in tool_registry:
        raise ValueError(f"Tool {tool_name} not found in registry.")
    
    return tool_registry[tool_name](*args)