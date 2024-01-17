# nlbse24

## Prerequisites for Running This Project

Before running this project, ensure you have the following tools installed:
- `codeql`: https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli
- `defects4J`: https://github.com/rjust/defects4j
- `poetry`: You'll need Poetry to install the project dependencies. If you don't have it yet, check out [poetry](https://python-poetry.org/) to get it installed. The `poetry install` command installs dependencies and should be executed only once. The `poetry shell` command activates the virtual environment and should run at the start of each session.
- `Java 8`: We recommend using [sdk man](https://sdkman.io/install) because all you have to do is execute the command `sdk env install` after `poetry shell` to easily install the exact Java version we used (8.0.362-amzn).

Don't forget to create a `.env` file with these  variables:
```bash
DEFECTS4J_HOME= # path to Defects4J
CODEQL_HOME= # path to CodeQL
OPENAI_API_KEY= # OpenAI key
```

## Repository Structure Overview

### Model-View-Controller (MVC) Components

- [models](./models): Contains data models representing failing tests, projects, queries, etc.
- [controllers](./controllers):
    - [command_runner](./controllers/command_runner.py): Executes shell commands, manages file operations and directories, with comprehensive logging and error handling.
    - [d4j_controller](./controllers/d4j_controller.py): Facilitates interactions with the Defects4J database.
    - [db_controller](./controllers/db_controller.py): Manages operations related to CodeQL databases.

### Utility Modules

- [constants](./constants): Centralizes various constant values used across the project.
  - [code](./constants/code.py): Stores essential code snippets for project setup.
  - [paths](./constants/paths.py): Maintains frequently used paths.
  - [prompts](./constants/prompts.py): Prompts for explaining code snippets.
  - [queries](./constants/queries.py): CodeQL queries for method extraction.
- [ensure_in_path](./decorators/ensure_in_path.py): Ensures that `defects4J` and `codeql` are included in the system PATH.
- [pyproject.toml](./pyproject.toml): Configures project settings, dependencies, and build specifications.
- [install_codeql](./install_codeql.py): Install codeql libraries

### Scripts

- [generate_codetours.py](./generate_codetours.py): Creates code tours using the generated stack traces.
- [generate_stacktraces.py](./generate_stacktraces.py): Generates stack traces for each project versions.

### Data Resources

- [defects4j-bugs](./data/defects4j-bugs.json): Provides extracted information about Defects4J projects, sourced from Sobreira (2018).
- [dataset](https://github.com/balfroim/nlbse24-dataset): You'll find the generated data from all the scripts


