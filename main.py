import logging
import sys

from dotenv import load_dotenv
from genrevive.helpers.common.logger import Logger
from genrevive.helpers.common.traces import with_traces_langfuse

from activities.bootstrap_styling_integrator.bootstrap_styling_integrator import BootstrapStylingIntegrator
from activities.component_generator.component_generator import ComponentGenerator
from activities.npm_package_installer.npm_package_installer import NpmPackageInstaller
from activities.openapi_generator.openapi_generatory import OpenApiGenerator
from activities.output_deleter.output_deleter import OutputDeleter
from activities.poc_component_renderer.poc_component_renderer import PocComponentRenderer
from activities.target_code_generator.code_generation_crew import CodeGenerationCrew
from activities.target_project_creator.target_project_creator import TargetProjectCreator

logging.root.setLevel(level=logging.INFO)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    load_dotenv()
    sys.stdout = Logger()
    with_traces_langfuse()

    OutputDeleter().execute()
    TargetProjectCreator().execute()
    OpenApiGenerator().execute()
    NpmPackageInstaller().execute()
    BootstrapStylingIntegrator().execute()
    ComponentGenerator().execute()

    # Temporary for the PoC - afterward, a routing mechanism will need to be in place
    PocComponentRenderer().execute()

    CodeGenerationCrew().execute()
