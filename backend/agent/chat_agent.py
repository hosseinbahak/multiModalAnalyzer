# backend/agent/chat_agent.py
"""
Implementation of the ChatAgent for handling general conversation.
"""
from backend.agent.base import AgentBase
from backend.utils.helpers import ToolState

class ChatAgent(AgentBase):
    """
    Agent for handling general conversation and deciding if a tool should be used.
    """
    def get_prompt_template(self) -> str:
        """
        Define the prompt template for the Chat Agent.
        
        Returns:
            The prompt template string
        """
        return """
            Available tools: {tools_list}
            Question: {history}
            As ChatAgent, decide if we need to use a tool or not.
            If we don't need a tool, just reply; otherwise, let the ToolAgent handle it.
            Output the JSON in the format: {{"scenario": "your reply", "use_tool": True/False}}
        """