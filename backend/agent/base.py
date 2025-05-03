"""
Base class for all agents in the multimodal analysis system.
"""
from abc import ABC, abstractmethod
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from backend.utils.helpers import ToolState, clip_history
import json

class AgentBase(ABC):
    """
    Abstract base class for all agent implementations.
    All concrete agents should inherit from this class.
    """
    def __init__(self, state: ToolState):
        """
        Initialize the agent with a state.
        
        Args:
            state: The current tool state
        """
        self.state = state

    @abstractmethod
    def get_prompt_template(self) -> str:
        """
        Return the prompt template specific to this agent.
        Must be implemented by all subclasses.
        
        Returns:
            The prompt template string
        """
        pass

    def execute(self) -> ToolState:
        """
        Execute the agent's task and update the state.
        
        Returns:
            The updated tool state
        """
        # Clip the history to the last 8000 characters
        self.state["history"] = clip_history(self.state["history"])
        
        # Define the prompt template
        template = self.get_prompt_template()
        prompt = PromptTemplate.from_template(template)        
        
        # Initialize the LLM
        llm = ChatOllama(model="gemma2:27b", format="json", temperature=0)
        llm_chain = prompt | llm | StrOutputParser()
        
        # Generate response
        generation = llm_chain.invoke({
            "history": self.state["history"], 
            "use_tool": self.state["use_tool"],
            "tools_list": self.state["tools_list"]
        })
        
        # Parse the response
        data = json.loads(generation)
        self.state["use_tool"] = data.get("use_tool", False)        
        self.state["tool_exec"] = generation

        # Update history
        self.state["history"] += "\n" + generation
        self.state["history"] = clip_history(self.state["history"])

        return self.state