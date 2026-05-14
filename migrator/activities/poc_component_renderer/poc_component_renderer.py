import os
from pathlib import Path
from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.common.logger import log_activity_execution

from utils.component_provider import ComponentProvider
from genrevive.helpers.angular.angular_component_creator import create_angular_component


class PocComponentRenderer(BaseActivity):
    """
    Displays the Poc Component on the home screen.
    This is a temporary activity only to be used in the Demo PoC, where only one component is generated, so there is
    no need for a router.
    """

    def __init__(self):
        self.app_component_path = Path(os.path.join(os.environ["ANGULAR_PROJECT_PATH"], 'src', 'app', 'app.component.html'))

    @log_activity_execution
    def execute(self):
        with open(self.app_component_path, 'w') as file:
            file.write('<app-poc></app-poc>')
