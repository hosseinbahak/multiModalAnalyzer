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
            
            As ChatAgent, you have two responsibilities:
            1. If the user is asking about an image or PDF file, set use_tool to True and leave the actual analysis to the specialized agents
            2. If the user is just having a general conversation, provide a helpful response directly
            
            You must output valid JSON in the following format:
            {{"scenario": "your human-readable response here", "use_tool": true/false}}
            
            If use_tool is true, your "scenario" field should inform the user that you're analyzing their file.
            If use_tool is false, your "scenario" field should be your complete, helpful response to their question.
            Never include the JSON structure or field names in your scenario text - just the actual response.
        """