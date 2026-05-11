import os

import yaml

from utils.pydantic_outputs import *

from collections import namedtuple
from functools import partial

from dotenv import load_dotenv
from genrevive.core.agent_factory import AgentFactory
from genrevive.core.gen_ai_activity import GenAIActivity
from genrevive.core.task_factory import TaskFactory
from genrevive.helpers.angular.angular_build_tool import angular_build_tool
from genrevive.helpers.common.file_utils import FileUtils

from crewai import Crew, Task

from utils.component_provider import ComponentProvider
from utils.file_saver import save_files


class CodeGenerationCrew(GenAIActivity):
    def __init__(self):
        load_dotenv(override=True)
        self.origin_technology = os.environ["ORIGIN_TECHNOLOGY"]
        self.target_technology = os.environ["TARGET_TECHNOLOGY"]
        self.origin_input = os.environ["ORIGIN_INPUT"]
        self.target_output = os.environ["TARGET_OUTPUT"]
        self.compiler_technology = os.environ["COMPILER_TECHNOLOGY"]
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]
        self.angular_src_path = self.angular_project_path + '/src' # path without node_modules
        self.agent_model = os.environ["AGENT_MODEL"]

        self.software_engineer = None
        self.software_reviewer = None
        self.devops_engineer = None

        self.se_tools = []
        self.sr_tools = []
        self.devops_tools = [angular_build_tool(cache_success_only=True)]

        super().__init__()

    def setup_agents(self):
        self.software_engineer = AgentFactory().software_engineer(self.origin_technology, self.target_technology,
                                                                  self.origin_input,
                                                                  self.target_output,
                                                                  self.se_tools,
                                                                  crew_ai_llm=True,
                                                                  llm=self.agent_model,
                                                                  allow_delegation=False
                                                                  )

        self.software_reviewer = AgentFactory().software_reviewer(self.target_technology, self.sr_tools,
                                                                  crew_ai_llm=True,
                                                                  llm=self.agent_model)

        self.devops_engineer = AgentFactory().devops_engineer(self.target_technology, self.compiler_technology,
                                                              self.devops_tools,
                                                              crew_ai_llm=True, llm=self.agent_model)

        self.agents = [self.software_engineer, self.software_reviewer, self.devops_engineer]

    def setup_general_configuration(self):
        pass

    def setup_cookbooks_and_prompts(self):
        self.se_prompt = FileUtils.read_file(os.environ["SE_PROMPT_FILE"])
        self.se_cookbook = FileUtils.read_file(os.environ["SE_COOKBOOK_FILE"])

        self.sr_prompt = FileUtils.read_file(os.environ["SR_PROMPT_FILE"])
        self.sr_cookbook = FileUtils.read_file(os.environ["SR_COOKBOOK_FILE"])

        self.devops_prompt = FileUtils.read_file(os.environ["DEVOPS_PROMPT_FILE"])

    def setup_tasks(self):
        components = self.__extract_component_strings()

        task_factory = TaskFactory()
        for component in components:
            self.tasks.append(self.__template_task(component, task_factory))
            self.tasks.append(self.__component_task(component, task_factory))
            self.tasks.append(self.__scss_task(component, task_factory))
            self.tasks.append(self.__review_task(component, task_factory))
            self.tasks.append(self.__devops_task(component, task_factory))

    def __template_task(self, component, task_factory):
        expected_output_html = f"""\
        Please find the target HTML file for the given component, delete the placeholder content inside and fill it with
        the HTML, which is equivalent to the provided view in both functionality and styling."""
        return task_factory.task_code_translation(agent=self.software_engineer,
                                                                 prompt=self.se_prompt,
                                                                 cookbook=self.se_cookbook,
                                                                 input=component.prompt,
                                                                 target_technology_names=["HTML", "Angular"],
                                                                 target_file_path="",
                                                                 callback=None,
                                                                 output_pydantic=TemplateOutput,
                                                                 expected_output=expected_output_html)

    def __component_task(self, component, task_factory):
        expected_output_tsx = f"""\
        Please find the target TS file for the given component, delete the placeholder content inside and fill it with 
        code for the Typescript Angular component integrated with the previously generated HTML template, which is 
        equivalent in behavior to the provided Java component."""
        return task_factory.task_code_translation(agent=self.software_engineer,
                                           prompt=self.se_prompt,
                                           cookbook=self.se_cookbook,
                                           input=component.prompt,
                                           target_technology_names=["HTML", "Angular",
                                                                    "Typescript"],
                                           target_file_path="",
                                           callback=None,
                                           output_pydantic=TypeScriptComponentOutput,
                                           expected_output=expected_output_tsx)

    def __scss_task(self, component, task_factory):
        expected_output_scss = f"""\
        Please find the target SCSS file for the given component, delete the placeholder content inside and fill it with
        the styling suitable for the previously created HTML and TS files for this component so that it is equivalent in 
        style and behavior to the provided input component and uses the ng-bootstrap library."""
        return task_factory.task_code_translation(agent=self.software_engineer,
                                                                  prompt=self.se_prompt,
                                                                  cookbook=self.se_cookbook,
                                                                  input=component.prompt,
                                                                  target_technology_names=["Typescript", "HTML",
                                                                                           "Angular", "SCSS"],
                                                                  target_file_path="",
                                                                  callback=None,
                                                                  output_pydantic=ViewGenerationOutput,
                                                                  expected_output=expected_output_scss,
                                                                  )

    def __review_task(self, component, task_factory):
        expected_output_review = f"""\
        Output the fixed migrated Angular component, template and styling for the Swing input component."""
        return task_factory.task_code_translation(agent=self.software_reviewer,
                                                  prompt=self.sr_prompt,
                                                  cookbook=self.sr_cookbook,
                                                  input=component.prompt,
                                                  target_technology_names=["Typescript", "HTML",
                                                                           "Angular", "SCSS"],
                                                  target_file_path="",
                                                  callback=partial(save_files, component.component_name),
                                                  output_pydantic=ViewGenerationOutput,
                                                  expected_output=expected_output_review,
                                                  )

    def __devops_task(self, component, task_factory):
        return TaskFactory().task_code_build(
            devops_engineer=self.devops_engineer,
            devops_prompt=self.devops_prompt
        )

    def __extract_component_strings(self) -> []:
        componentFiles = ComponentProvider().extract_components()
        componentStr = []
        ComponentInput = namedtuple('ComponentInput', 'component_name prompt')

        for component in componentFiles:
            viewContent = FileUtils.read_file(component.view_file)
            presenterContent = FileUtils.read_file(component.presenter_file)
            modelContent = FileUtils.read_file(component.model_file)

            prompt = f"""\
---
This is the content of the input file named {component.componentName}View.java:

{viewContent}

---
This is the content of the input file named {component.componentName}Presenter.java:

{presenterContent}

---
This is the content of the input file named {component.componentName}Model.java:

{modelContent}
---
"""
            componentStr.append(ComponentInput(component.componentName, prompt))

        return componentStr


