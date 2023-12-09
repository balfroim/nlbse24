# nlbse24

## Prerequisites for Running This Project

Before running this project, ensure you have the following tools installed:
- `codeql`: https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli
- `defects4J`: https://github.com/rjust/defects4j
- `poetry`: https://python-poetry.org/

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

### Scripts

- [generate_codetours.py](./generate_codetours.py): Creates code tours using the generated stack traces.
- [generate_stacktraces.py](./generate_stacktraces.py): Generates stack traces for each project versions.

### Data Resources

- [stacktraces](./stacktraces): Contains generated stack traces for each project version.
- [defects4j-bugs](./data/defects4j-bugs.json): Provides extracted information about Defects4J projects, sourced from Sobreira (2018).
- [selected_tours.json](./selected_tours.json): Details about the selected code tours.
- [tours](./tours): Stores all generated code tours.


