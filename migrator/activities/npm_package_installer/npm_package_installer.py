import os
import logging

from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.common.logger import log_activity_execution
from genrevive.helpers.npm.package_installer import local_npm_install_packages


class NpmPackageInstaller(BaseActivity):
    """
    Installs necessary NPM packages.
    By using the NPM CLI directly, no access to directories outside of /src is necessary for the AI, preventing possible
    involvement of it in the node_modules (causing Rate Limit Errors) and ensuring consistency.
    """

    def __init__(self):
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]

    @log_activity_execution
    def execute(self):
        original_path = os.getcwd()  # Store the original path before changing directory
        try:
            os.chdir(self.angular_project_path)  # Change to the Angular project directory
            local_npm_install_packages(['bootstrap@5.3.5'])
        except Exception as e:
            logging.error(f"An error occurred during execution: {e}")
        finally:
            os.chdir(original_path)  # Restore the original directory after tasks
