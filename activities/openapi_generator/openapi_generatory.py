import os
import logging

from genrevive.core.base_activity import BaseActivity
from genrevive.helpers.angular.angular_openapi import generate_client
from genrevive.helpers.common.logger import log_activity_execution


class OpenApiGenerator(BaseActivity):
    """
    This activity facilitates the generation of necessary files in an Angular project based on an
    OpenAPI specification. This class takes an OpenAPI JSON file as input and utilizes a CLI tool to automatically
    generate the corresponding Angular services, models, and other related files required to interact with the
    API defined in the OpenAPI specification.
    """

    def __init__(self):
        self.openapi_file_path = os.environ["OPENAPI_FILE_PATH"]
        self.angular_project_path = os.environ["ANGULAR_PROJECT_PATH"]
        self.generator_options = {
            "ngVersion": "16.2.12",
            "npmName": os.environ["ANGULAR_APP_NAME"],
            "providedInRoot": "true",
            "withInterfaces": "true",
            "configurationModulePrefix": "config",
            "fileNaming": "kebab-case",
            "stringEnums": "true",
            "server": "http://localhost:8080"
        }

    @log_activity_execution
    def execute(self):
        generate_client(self.openapi_file_path, self.angular_project_path, self.generator_options)
        self.add_http_client_module()

    def add_http_client_module(self):
        app_module_file_path = os.path.join(self.angular_project_path, 'src', 'app', 'app.module.ts')
        logging.info(f"Starting to adapt the Angular module: {app_module_file_path}")

        # Read the existing app.module.ts file
        with open(app_module_file_path, 'r') as f:
            lines = f.readlines()

        # Find the last import statement
        last_import_index = None
        for i, line in enumerate(lines):
            if line.startswith("import "):
                last_import_index = i

        # Add import of HttpClientModule at the end of imports
        if last_import_index is not None:
            lines.insert(last_import_index + 1, "import { HttpClientModule } from '@angular/common/http';\n")
        else:
            lines.insert(0, "import { HttpClientModule } from '@angular/common/http';")

        # Find the imports array
        start_index = None
        end_index = None
        for i, line in enumerate(lines):
            if 'imports:' in line and '[' in line:
                start_index = i + 1
            if start_index and ']' in line:
                end_index = i
                break

        # Insert the HttpClientModule into the imports array
        if start_index and end_index:
            lines = lines[:start_index] + ["    HttpClientModule,\n"] + lines[start_index:]
            with open(app_module_file_path, 'w') as f:
                f.writelines(lines)
            logging.info(f"Successfully adapted the Angular module: {app_module_file_path}")
        else:
            logging.error("Failed to find the declarations array in app.module.ts")