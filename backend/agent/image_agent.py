# backend/agent/image_agent.py
"""
Implementation of the ImageAnalysisAgent for analyzing images.
"""
from backend.agent.base import AgentBase
from backend.utils.helpers import ToolState

class ImageAnalysisAgent(AgentBase):
    """
    Agent specialized in analyzing image content.
    """
    def get_prompt_template(self) -> str:
        """
        Define the prompt template for the Image Analysis Agent.
        
        Returns:
            The prompt template string
        """
        return """
            History: {history}
            Available tools: {tools_list}
            
            You are an Image Analysis Agent. Based on the user's request:
            1. If the user mentions an image or asks for image analysis, use the analyze_image tool
            2. Use the context from the PDF (if available) to provide a detailed description of the image
            3. Format your response as JSON:
            {{"function": "analyze_image", "args": ["<file_path>", "<instruction>"]}}
            
            Only respond if the request involves image analysis.
            """