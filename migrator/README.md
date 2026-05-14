# GenRevive Migrator Swing to Angular

This repository provides a template for developing migrators using [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive). 

This repository includes essential components and configurations required to build a customized migrator for specific migration scenarios.

## Prerequisites

Before starting with this template, get familiar with [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) `README.md`.
>**NOTE:** If you want to contribute to GenRevive during migrator development, you should also set up the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) project.

You will neet to go through the same [project setup steps](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#project-setup-guide) as for the GenRevive project.

Mostly in use is the feature branch feature/updated.

## Specific Project Setup Steps

To start the migrator development, follow these steps:
>**NOTE:** You will find detailed step descriptions in [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) `README.md`
1. Installing Python 3.12
   >**NOTE:** If you already have Python 3.12 installed, you can skip this step.
2. Installing Visual Studio Build Tools
   >**NOTE:** If you already have Visual Studio Build Tools installed, you can skip this step.
3. Setting up a virtual environment
   >**NOTE:** You will need to set up a virtual environment in your new migrator project directory.
4. Installing and configuring Poetry
   >**NOTE:** If you already have Poetry installed, you will still need to call `poetry lock` and `poetry install` in your migrator project directory.
5. Integrating the project with PyCharm CE (optional)
6. Install other CLI's, tools, packages, that are required for your specific migrator
   >**NOTE:** In this project you should use angular-cli version 16.0.0.
   >**NOTE:** You have to use (https://github.com/Sultanow/websocket_swing.git) branch genai-poc for the input files.
   >**NOTE:** You have to install openapi generator using npm install -g @openapitools/openapi-generator-cli.
7. Running your migrator
   >**NOTE:** To start your migrator, simply run the `main.py` by calling `py main.py` in your migrator project directory.
   >**NOTE:** To test the logic, start a mock server as a docker container using `docker run -p 8080:80 kennethreitz/httpbin`.
8. Fixing CrewAI issues
   >**NOTE:** See [Fixing CrewAI issues](#fixing-crewai-issues) section.

## Migrator Architecture

The architecture of the migrator is organized into the following components:

### 1. Controller

The `Controller` (or `main.py` file) is the central component responsible for managing the migration process. It orchestrates the execution of various activities required for the migration.

### 2. Activities

Activities are the building blocks of the migration process. Each activity represents a specific transformation or migration step. There are two main types of activities:

- **Base Activities**: These are standard transformation/migration steps that do not require Gen-AI involvement.
  
- **GenAI Activities**: These activities leverage Gen-AI and the crewAI Framework to transform/migrate the inputs into the target technologies. GenAI activities utilize predefined prompts and cookbooks to guide the migration process.

### 3. Migrator specific utilities

These utilities are specific to the migrator and are required only for the specific migration scenario.

## Migrator Development

During migrator development, keep in mind:

### Handle `pyproject.toml` file

- Adjust the project name by replacing the `<origin2target>` placeholder.
- Adjust the description.
- You can add the names of authors and maintainers
- If you need to add additional dependencies (e.g. for your utilities), add them to the `[tool.poetry.dependencies]` section.
- For the `genrevive` dependency:
  - ensure that the `genrevive` repository is located next to your migrator repository.
  - If you're importing `genrevive` as an archive, place the `dist/` directory with the archives next to your migrator repository.
  - Alternatively, you can adjust the `path` attribute in the dependency definition.
 
### Handle `main.py` file

- `main.py` is the starting point of your migrator.
- The simplest version of `main.py` takes care of logging and starts the individual activities successively.
- You may consider designing and adding a mechanism to enable or disable the execution of each activity.

### Creating Activities

You can adjust or create new activities to fit the specific needs of your migration scenario.
Add your new activities within the `activities/` directory. 

#### Creating Base Activities

- Create a new Python package in the `activities/` directory.
- Create a new Python file in the new package with the name of the activity.
- The new Python class should inherit the BaseActivity class
- You will need to override and implement the `execute` method.
- Use the `@log_activity_execution` decorator to log the start and the end of activity execution.
- Use the `__init__` method to get needed inputs and initialize the activity.

#### Creating GenAI Activities

- Create a new Python package in the `activities/` directory.
- Create a new Python file in the new package with the name of the activity.
- The new Python class should inherit the GenAIActivity class
- You will need to override and implement the `setup_...` methods.
- Use the `__init__` method to set default values and call `super().__init__()`.
   > **_NOTE:_** `super().__init__()` calls your overridden `setup_...` methods.
- There is already a default implementation of the `execute` method in the `GenAIActivity` class.
It expects that all agents and tasks are already collected into corresponding arrays and 'kicks off' the crew work.
   > **_NOTE:_** You can override the `execute` method to add your own functionality.
- To made use of prompts and cookbooks create corresponding directories and distribute the markdown files accordingly.
- You can create separate `.env.template` and `.env` files for each activity.
- You can use own `AgentProvider` utility to create agents.
- Setup/collect tasks in the logical execution order.
   > **_NOTE:_** The crewai keeps the results of previous tasks as a context for the next task.

### Handle utilities

- You can add and implement your own utilities in the `utils/` package.
- Usually, you will create some utilities to:
  - extract and process inputs from origin project
  - process generated interim result
  - make 'static' adjustments to the target project

### Handle code duplication

- If, during the development of multiple migrators, you find yourself duplicating the same code for different migrators, consider reaching out to the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) team.
- The team can assist in integrating the required functionality into the `core` or `helpers` packages.
- This situation frequently arises when working with migrators that utilize the same origin or target technology.

### Create README.md from provided template
To add a usage manual for the newly developed migrator, copy the `README.template.md` from this repository and rename it to `README.md`. Make sure to replace all placeholders, marked as <*placeholder*> and add any specific configuration parameters.

## Configuration

Migrator requires configuration of several environment variables.
There should be one "global" `.env` file containing environment variable values that are shared across thw whole migrator.
There could be "activity-local" `.env` files that contain environment variable values that are specific to the activity

The values in the `.env` files are often specific to the local environment, so they aren't committed to the repository.
Use `.env.template` files as a base — copy, rename, and fill them with your environment-specific values.

| Environment Variable      | Required | Description                                      | Valid Values | Example                              |
|:--------------------------|:--------:|:-------------------------------------------------|:------------:|:-------------------------------------|
| `AZURE_OPENAI_VERSION`    |   Yes    | Version of the Azure OpenAI service.             |    String    | `2024-04-01-preview`                 |
| `AZURE_OPENAI_DEPLOYMENT` |   Yes    | Deployment model for Azure OpenAI service.       |    String    | `gpt-4o`                             |
| `AZURE_OPENAI_ENDPOINT`   |   Yes    | Endpoint URL for Azure OpenAI service.           | String (URL) | `https://api.openai.azure.com`       |
| `AZURE_OPENAI_KEY`        |   Yes    | API key for Azure OpenAI service.                |    String    | `your_api_key`                       |
| `DELETING_OUTPUT`         |   Yes    | Enable deleting the content of the output folder before a new run. |    Boolean   | `true`                               |
| `LANGCHAIN_TRACING_V2`    |    No    | Enable monitoring and tracing through LangSmith. |   Boolean    | `true`                               |
| `LANGCHAIN_ENDPOINT`      |    No    | Endpoint URL for LangSmith API.                  | String (URL) | `https://api.smith.langchain.com`    |
| `LANGCHAIN_API_KEY`       |    No    | API key for LangSmith API.                       |    String    | `your_api_key`                       |
| `LANGCHAIN_PROJECT`       |    No    | Project name (traces storing location).          |    String    | `genrevive-migrator-<origin2target>` |
| `OTEL_SDK_DISABLED`       |    No    | Disable OpenTelemetry.                           |   Boolean    | `true`                               |
| `LOG_PATH`                |   Yes    | Path to log file.                                |    String    | `./logfile.log`                      |
| `ORIGIN_TECHNOLOGY`       |   Yes    | Name of technology to migrate from.              |    String    | `Oracle ADF`                         |
| `TARGET_TECHNOLOGY`       |   Yes    | Name of technology to migrate to.                |    String    | `Angular TypeScript`                 |
| `ORIGIN_INPUT`            |   Yes    | Short description of inputs.                     |    String    | `ADF JSPX inputs`                    |
| `TARGET_OUTPUT`           |   Yes    | Short description of outputs.                    |    String    | `Angular components`                 |
| `COMPILER_TECHNOLOGY`     |   Yes    | Name of compilation tool (compiler) used.        |    String    | `Angular TypeScript`                 |

>**NOTE:** It is a sensible approach to use environment variables for configuring different paths to input and output directories or files.

## Fixing CrewAI issues

The Version of CrewAI framework that is currently used (`^0.28.8`) contains some issues.

### CrewAI Bugfix 1 - Using 'callback' option for tasks; Callback is not triggered

- Locate the `crewai` directory in virtual environment of your project. Probably somewhere under `./venv/Lib/`.
- Open the `crew.py` file.
- Replace line 346 as follows:

```diff
- task.callback = self.task_callback
+ self.task_callback = task.callback
```

### CrewAI Bugfix 2 - Using 'output_file' option for tasks; CrewAI code save file with wrong encoding

- Locate the `crewai` directory in virtual environment of your project. Probably somewhere under `./venv/Lib/`.
- Open the `task.py` file.
- Replace line 284 as follows:

```diff
- with open(self.output_file, "w") as file:
+ with open(self.output_file, "w", encoding='utf-8') as file:
```

## Further Documentation

Refer to the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) `/docs` for more detailed architecture documentation and guidelines.

---

This repository is a starting point for developing your custom migrator.
Adapt it to your project needs and extend it to cover your specific migration scenario.
