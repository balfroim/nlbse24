import logging
import shutil
import subprocess
from typing import List
from contextlib import contextmanager
import os

class CommandRunner:

    @classmethod
    def _get_param_error(cls, params):
        """
        Returns an error message indicating that a parameter error occurred, and providing more details about the expected data type of the parameter.
        """
        param_types = [type(param).__name__ for param in params]
        formatted_types = [
            param_type.lower() if param_type == 'str' else param_type.upper()
            for param_type in param_types
        ]
        return f"Parameter error: expected str, but got {' '.join(formatted_types)}"

    @classmethod
    def _get_cmd_error(cls, cmd, *params, stderr, stdout):
        """
        Returns an error message indicating that the command failed, and providing the command and its parameters, and the error message from the command's output.
        """
        return f"Command failed: {cmd} {' '.join(params)}\n{stderr}\n{stdout}"

    @classmethod
    def run(cls, cmd: str, *params: List[str]):
        logging.info(f"Run: {cmd} {' '.join(params)}")
        try:
            result = subprocess.run([cmd, *params], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        except TypeError as e:
            error = cls._get_param_error(params)
            logging.error(error)
            raise RuntimeError(error) from e
        if result.returncode != 0:
            error = cls._get_cmd_error(cmd, *params, stderr=result.stderr, stdout=result.stdout)
            logging.error(error)
            raise RuntimeError(error)
        logging.info(result.stdout)
        return result.stdout
    
    @classmethod
    def write_to_file(cls, path: str, content: str):
        with open(path, "w") as file:
            file.write(content)
        logging.info(f"Written {len(content)} characters to {path}")

    @classmethod
    def read_from_file(cls, path: str):
        with open(path, "r", encoding="utf-8", errors='ignore') as file:
            content = file.read()
        logging.info(f"Read {len(content)} characters from {path}")
        return content
    
    @classmethod
    def copy(cls, source: str, target: str):
        logging.info(f"Copying {source} to {target}")
        try:
            shutil.copy(source, target)
        except Exception as e:
            logging.error(f"Failed to copy {source} to {target}: {e}")
        
    @classmethod
    @contextmanager
    def chdir(cls, path: str):
        old = os.getcwd()
        try:
            os.chdir(path)
            yield
        finally:
            os.chdir(old)

    @classmethod
    def package_to_source_path(cls, package: str) -> str:
        return package.replace(".", "/") + ".java"