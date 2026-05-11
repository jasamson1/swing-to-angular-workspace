import os
from pathlib import Path
from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.common.logger import log_activity_execution

from utils.component_provider import ComponentProvider
from genrevive.helpers.angular.angular_component_creator import create_angular_component


class ComponentGenerator(BaseActivity):
    """
    Creates initial empty Angular components using the Angular CLI based on the input Swing files.
    Using this method before letting the AI fill it with content enables us reliable integration with the App Module
    and consistency.
    """

    def __init__(self):
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]

    @log_activity_execution
    def execute(self):
        components = ComponentProvider().extract_components()
        for component in components:
            create_angular_component(Path(self.angular_project_path), component.componentName)
