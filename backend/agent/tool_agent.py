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