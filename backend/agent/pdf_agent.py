# backend/agent/pdf_agent.py
"""
Implementation of the PDFAnalysisAgent for analyzing PDF documents.
"""
from backend.agent.base import AgentBase
from backend.utils.helpers import ToolState

class PDFAnalysisAgent(AgentBase):
    """
    Agent specialized in extracting and analyzing content from PDF documents.
    """
    def get_prompt_template(self) -> str:
        """
        Define the prompt template for the PDF Analysis Agent.
        
        Returns:
            The prompt template string
        """
        return """
            History: {history}
            Available tools: {tools_list}
            
            You are a PDF Analysis Agent specialized in extracting data from PDF documents.
            If the user's request involves analyzing a PDF:
            1. Use the analyze_pdf_page tool to extract data
            2. Format your response as JSON:
            {{"function": "analyze_pdf_page", "args": ["<pdf_path>", <page_number>, "<instruction>"]}}
            
            Only respond if the request involves PDF analysis.
            """