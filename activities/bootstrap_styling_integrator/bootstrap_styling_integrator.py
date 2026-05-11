import os
import logging
import json

from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.common.logger import log_activity_execution


class BootstrapStylingIntegrator(BaseActivity):
    """
    Integrates Bootstrap CSS and JS.
    """

    def __init__(self):
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]

    @log_activity_execution
    def execute(self):
        try:
            bootstrap_css = "node_modules/bootstrap/dist/css/bootstrap.css"
            with open(os.path.join(self.angular_project_path, 'angular.json'), 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Get the project name (assuming first listed project is the target)
            project_name = next(iter(data['projects']))
            styles = data['projects'][project_name]['architect']['build']['options'].get('styles', [])

            # Add Bootstrap CSS if not already in the list
            if bootstrap_css not in styles:
                styles.append(bootstrap_css)
                data['projects'][project_name]['architect']['build']['options']['styles'] = styles

                # Write back to the file
                with open(os.path.join(self.angular_project_path, 'angular.json'), 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                logging.info(f"Added Bootstrap CSS to styles in {project_name}.")
            else:
                logging.info(f"Bootstrap CSS was not added to styles in {project_name}, as it was already included.")

        except Exception as e:
            logging.error(f"An error occurred during execution: {e}")
