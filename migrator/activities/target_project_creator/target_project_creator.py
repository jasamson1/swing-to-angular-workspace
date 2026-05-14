import os
from pathlib import Path
from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.common.logger import log_activity_execution
from genrevive.helpers.angular.angular_project_creator import create_angular_project, add_reactive_forms_module


class TargetProjectCreator(BaseActivity):
    """
    Creates initial empty Angular project in the given version.
    """

    def __init__(self):
        self.target_project_path = os.environ["TARGET_PROJECT_PATH"]
        self.angular_app_name = os.environ["ANGULAR_APP_NAME"]
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]

    @log_activity_execution
    def execute(self):
        self.__create_target_project()

    def __create_target_project(self):
        create_angular_project(Path(self.target_project_path), self.angular_app_name, "^16.0.0", arg="--strict=false")
        add_reactive_forms_module(Path(self.angular_project_path))
