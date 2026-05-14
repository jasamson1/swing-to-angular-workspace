import os

from crewai import Agent
from dotenv import load_dotenv
from genrevive.core.agent_factory import AgentFactory
from genrevive.core.common_tools.save_file_tool import save_file_tool
from genrevive.helpers.angular.angular_build_tool import angular_build_tool


class AgentProvider:

    def __init__(self, agent_factory):
        load_dotenv(override=True)
        self.agent_factory = agent_factory
        self.origin_technology = os.environ["ORIGIN_TECHNOLOGY"]
        self.target_technology = os.environ["TARGET_TECHNOLOGY"]
        self.origin_input = os.environ["ORIGIN_INPUT"]
        self.target_output = os.environ["TARGET_OUTPUT"]
        self.compiler_technology = os.environ["COMPILER_TECHNOLOGY"]
        self.agent_model = os.environ["AGENT_MODEL"]

        self.se_tools = []
        self.sr_tools = []
        self.devops_tools = [angular_build_tool(cache_success_only=True), save_file_tool]
        
    def software_engineer(self) -> Agent:
        return AgentFactory().software_engineer(self.origin_technology, 
                                                self.target_technology, 
                                                self.origin_input,
                                                self.target_output, 
                                                self.se_tools,
                                                crew_ai_llm=True,
                                                llm=self.agent_model,
                                                allow_delegation=False)

    def software_reviewer(self) -> Agent:
        return AgentFactory().software_reviewer(self.target_technology, 
                                                self.sr_tools,
                                                crew_ai_llm=True,
                                                llm=self.agent_model)

    def devops_engineer(self) -> Agent:
        return AgentFactory().devops_engineer(self.target_technology, 
                                              self.compiler_technology,
                                              self.devops_tools,                                            
                                              crew_ai_llm=True, 
                                              llm=self.agent_model)