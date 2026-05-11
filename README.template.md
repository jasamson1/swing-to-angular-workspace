# GenRevive Migrator - <*Name of Migrator*>

This repository is used to migrate a <*source technology*> application into a <*target technology*> application using [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive).

This document provides instructions for setting up the local environment and configuration in order to use this migrator.

If you want to know more about the main architecture of GenRevive, see the [official documentation](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive/-/blob/main/docs/genrevive_arc42_documentation.md). If you want to know more about specific activities, look into the activity files. They include helpful comments and explanations on how they work.

## Project Setup Steps

To run the migrator, follow these steps:
1. Clone the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) repository, which is needed as a dependency to run this migrator. The GenRevive root folder needs to be located in the same folder as the root folder of this repository.
   >**NOTE:** If needed, GenRevive can be located in a different folder. In this case, adjust the path defined in `pyproject.toml`.
2. Configure the environment as described in the chapter [Configuration](#configuration).

After project has been set up, there are two options to run the migrator - either in a Docker container or locally.

### Running the migrator in a container

This is the fastest way to get started - no local migrator specific installations necessary. The migrator will start as a Docker container and create its output in the local file system.

1. Install and run Docker. To avoid licensing costs, Rancher Desktop can be installed on both Windows and macOS, by following the [official documentation](https://docs.rancherdesktop.io/getting-started/installation).
2. Make sure Docker Compose is installed. If you installed Rancher Desktop, it is already bundled with it and nothing else needs to be installed. If not, follow the official [Docker Compose installation steps](https://docs.docker.com/compose/install/). 
3. Run the migrator by executing:
   ```bash
   docker-compose up
   ```

### Running the migrator locally

Alternatively, the migrator can run locally instead of in a Docker container. In this case, the following installation steps are required:

1. Follow the [Project Setup Guide for GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#project-setup-guide) to install most of the tools and dependencies needed for running this migrator.
   >**NOTE:** After installing Poetry, you do not need to call `poetry lock`, `poetry install` and `poetry build` for the `GenRevive` project. It will get built automatically when using this migrator.
2. Set up a virtual environment in the root of this repository, as described in the chapter [Setting up a Virtual Environment](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#3-setting-up-a-virtual-environment).
   >**NOTE:** This step has to be repeated in this repository even after executing it in the [GenRevive](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive) repository. Each repository has a separate virtual environment.
3. Install dependencies using Poetry, as described in the chapter [Installing and Configuring Poetry](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive#4-installing-and-configuring-poetry).
   >**NOTE:** Poetry does not need to be installed again. Simply call `poetry lock` and `poetry install` in this repository.
4. Fix the issues with the current CrewAI framework (`^0.28.8`) by using the bugfix described in the [Genrevive Migrator Template](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template) under [Fixing CrewAI issues](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template#fixing-crewai-issues). Make sure to make the change in the virtual environment of <b>this</b> repository.
5. Install Required Tools: <*Name the tools required for this specific migrator.*> For detailed installation instructions, refer to the [Required CLI Tools and Packages](#install-required-cli-tools-and-packages) section.
6. Run the migrator by executing:
   ```bash
   py main.py
   ```

### Install Required CLI Tools and Packages

If you want to run the migrator locally, ensure that the following tools are installed:

<*Provide instructions for installing the required tools, specific to this migrator.*>

## Configuration

This migrator requires configuration of several environment variables predefined in the following files:
* `./.env.template`
* ... <*Provide list of locations of .env.template files*>

For each of these files, a separate `.env` file needs to be created in the same folder and configuration values need to be adjusted there as needed. Many variables in the template files have a predetermined default value, which can be used if no special requirement exists. Please refer to the documentation of each configuration parameter to decide whether the default value needs to be adjusted for your use case.

The documentation for common configuration parameters is described in the [Migrator Template repository](https://devon.s2-eu.capgemini.com/gitlab/cca-genrevive-global/genrevive-migrator-template#configuration).

Configuration parameters specific to this migrator are described in the following tables.

### Global configuration parameters

The following parameters need to be set in the root level `.env` file:

| Environment Variable          | Required | Description                                                                                                                                                                                                                                                                         | Valid Values | Example                                 |
|:------------------------------|:--------:|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------:|:----------------------------------------|
| `EXAMPLE_PARAMETER`           |   Yes    | Example description.                                                                                                                                                                                                                                                                |    String    | `Example value`                         |
| `LOCAL_GENREVIVE_PATH`        |    No    | Path to your GenRevive repository folder. Only necessary if the migrator runs in a Docker container.                                                                                                                                                                                |    String    | `../genrevive`                          |
| `<ORIGIN_PROJECT_PATH>`       |    No    | Path to your input <*origin*> project directory. Refers to your local directory, if running locally. Otherwise refers to the directory inside of the migrator container. In this case, this value needs to be an absolute path                                                      |    String    | `/home/<origin>-project`                |
| `<LOCAL_ORIGIN_PROJECT_PATH>` |    No    | Path to your local input <*origin*> project directory. Only necessary if the migrator runs in a Docker container and will therefore be different from the `<ORIGIN_PROJECT_PATH>`, which refers to the working directory of the migrator. This value needs to be an absolute path.  |    String    | `C:/genrevive-examples/<origin>/input`  |
| `<TARGET_PROJECT_PATH>`       |    No    | Path to your output <*target*> project directory. Refers to your local directory, if running locally. Otherwise refers to the directory inside of the migrator container. In this case, this value needs to be an absolute path                                                     |    String    | `/home/output/<target>-project`         |
| `<LOCAL_TARGET_PROJECT_PATH>` |    No    | Path to your local output <*target*> project directory. Only necessary if the migrator runs in a Docker container and will therefore be different from the `<TARGET_PROJECT_PATH>`, which refers to the working directory of the migrator. This value needs to be an absolute path. |    String    | `C:/genrevive-examples/<target>/output` |

<*List all parameters in the .env.template file in the same order as in the template file.*>

### Configuration parameters for <*other component*>

The following parameters need to be set in the `.env` file under the path <*path of other component*>:

| Environment Variable | Required | Description          | Valid Values | Example         |
|:---------------------|:--------:|:---------------------|:------------:|:----------------|
| `EXAMPLE_PARAMETER`  |   Yes    | Example description. |    String    | `Example value` |

<*Add a subchapter and separate table for each .env file.*>
