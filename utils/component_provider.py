import os
import logging

from pathlib import Path

from genrevive.helpers.common.file_utils import FileUtils

class ComponentFile:
    def __init__(self, component_name, view_file, presenter_file, model_file):
        self.componentName = component_name
        self.view_file = view_file
        self.presenter_file = presenter_file
        self.model_file = model_file

class ComponentProvider:
    """Class to extract components based on the input MVP Swing classes."""
    def __init__(self):
        pass

    def extract_components(self) -> list[ComponentFile]:
        view_files = FileUtils.find_files_in_directory("View.java", os.environ["ORIGIN_PROJECT_PATH"])
        model_files = FileUtils.find_files_in_directory("Model.java", os.environ["ORIGIN_PROJECT_PATH"])
        presenter_files = FileUtils.find_files_in_directory("Presenter.java", os.environ["ORIGIN_PROJECT_PATH"])

        components = []
        for view_file in view_files:
            component_name = Path(view_file).stem[:-4]
            matching_model_files = [currentFile for currentFile in model_files if component_name in currentFile]
            matching_presenter_files = [currentFile for currentFile in presenter_files if component_name in currentFile]

            if matching_model_files and matching_presenter_files:
                components.append(
                    ComponentFile(component_name, view_file, matching_presenter_files[0], matching_model_files[0]))
            else:
                logging.info("Warning: no matching model and/or presenter files found for view " + view_file)

        return components

