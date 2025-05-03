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

# backend/agent/tool_agent.py
"""
Implementation of the ToolAgent for selecting and executing tools.
"""
import json
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from backend.agent.base import AgentBase
from backend.utils.helpers import ToolState, clip_history

class ToolAgent(AgentBase):
    """
    Agent for selecting and executing tools based on the user's request.
    """
    def get_prompt_template(self) -> str:
        """
        Define the prompt template for the Tool Agent.
        
        Returns:
            The prompt template string
        """
        return """
            History: {history}
            Available tools: {tools_list}
            Image path: {image_path}
            PDF path: {pdf_path}
            Based on the history and available image/PDF, choose the appropriate tool and arguments.
            Output in the format:
            {{"function": "<function>", "args": [<arg1>,<arg2>, ...]}}
        """

    def execute(self) -> ToolState:
        """
        Execute the tool agent's task with additional image and PDF path information.
        
        Returns:
            The updated tool state
        """
        self.state["history"] = clip_history(self.state["history"])
        template = self.get_prompt_template()
        prompt = PromptTemplate.from_template(template)        
        
        llm = ChatOllama(model="gemma2:27b", format="json", temperature=0)
        llm_chain = prompt | llm | StrOutputParser()
        
        generation = llm_chain.invoke({
            "history": self.state["history"], 
            "use_tool": self.state["use_tool"],
            "tools_list": self.state["tools_list"],
            "image_path": self.state["image_path"] or "No image provided",
            "pdf_path": self.state["pdf_path"] or "No PDF provided"
        })
        
        data = json.loads(generation)
        self.state["use_tool"] = True
        self.state["tool_exec"] = generation
        self.state["history"] += "\n" + generation
        self.state["history"] = clip_history(self.state["history"])
        
        return self.state

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