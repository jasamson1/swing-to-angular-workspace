import os

from utils.agent_provider import AgentProvider

from collections import namedtuple

from dotenv import load_dotenv
from genrevive.core.callbacks import save_code_blocks
from genrevive.core.gen_ai_activity import GenAIActivity
from genrevive.core.task_factory import TaskFactory
from genrevive.helpers.common.file_utils import FileUtils

from utils.component_provider import ComponentProvider


class CodeGenerationCrew(GenAIActivity):
    def __init__(self):
        load_dotenv(override=True)
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]

        self.software_engineer = None
        self.software_reviewer = None
        self.devops_engineer = None
        super().__init__()

    def setup_agents(self):
        agent_provider = AgentProvider(self.agent_factory)
        self.software_engineer = agent_provider.software_engineer()
        self.software_reviewer = agent_provider.software_reviewer()
        self.devops_engineer = agent_provider.devops_engineer()
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

        for component in components:
            self.__append_template_task(component.prompt)
            self.__append_component_task(component.prompt)
            self.__append_scss_task(component.prompt)
            self.__append_review_task(component.prompt)
            self.__append_devops_task()

    def __append_template_task(self, input: str):
        self.tasks.append(TaskFactory().task_code_translation(
            agent=self.software_engineer,
            prompt=self.se_prompt,
            cookbook=self.se_cookbook,
            input=input,
            target_technology_names=["HTML", "Angular"],
            target_file_path=f"{self.angular_project_path}/src/app/components/<filename>/",
            callback=save_code_blocks
        ))

    def __append_component_task(self, input: str):
        self.tasks.append(TaskFactory().task_code_translation(
            agent=self.software_engineer,
            prompt=self.se_prompt,
            cookbook=self.se_cookbook,
            input=input,
            target_technology_names=["HTML", "Angular", "Typescript"],
            target_file_path=f"{self.angular_project_path}/src/app/components/<filename>/",
            callback=save_code_blocks
        ))

    def __append_scss_task(self, input: str):
        self.tasks.append(TaskFactory().task_code_translation(
            agent=self.software_engineer,
            prompt=self.se_prompt,
            cookbook=self.se_cookbook,
            input=input,
            target_technology_names=["Typescript", "HTML", "Angular", "SCSS"],
            target_file_path=f"{self.angular_project_path}/src/app/components/<filename>/",
            callback=save_code_blocks
        ))

    def __append_review_task(self, input: str):
        self.tasks.append(TaskFactory().task_code_review(
            agent=self.software_reviewer,
            prompt=self.sr_prompt,
            cookbook=self.sr_cookbook,
            input=input,
            target_technology_names=["Typescript", "HTML", "Angular", "SCSS"],
            target_file_path=f"{self.angular_project_path}/src/app/components/<filename>/",
            callback=save_code_blocks
         ))

    def __append_devops_task(self):
        self.tasks.append(TaskFactory().task_code_build(
            devops_engineer=self.devops_engineer,
            devops_prompt=self.devops_prompt
        ))

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


