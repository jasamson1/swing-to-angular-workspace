import os
from crewai.tasks import TaskOutput
from utils.pydantic_outputs import ViewGenerationOutput
from typing import cast


def save_files(component_name: str, output: TaskOutput):
    pydantic_output = cast(ViewGenerationOutput, output.pydantic)
    component = component_name.lower()

    directory_path = os.path.join(
        os.path.join(os.environ["ANGULAR_PROJECT_PATH"], 'src', 'app', 'components', component))

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    _write_file(directory_path, f'{component}.component.html', pydantic_output.template)
    _write_file(directory_path, f'{component}.component.ts', pydantic_output.component)
    _write_file(directory_path, f'{component}.component.scss', pydantic_output.styling)


def _write_file(directory_path: str, file_name: str, content: str):
    with open(os.path.join(directory_path, file_name), 'w', encoding='utf-8') as file:
        print(f"Saving file {file_name} to {directory_path}")
        file.write(content)
