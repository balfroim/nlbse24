import requests
import zipfile
import os
from constants.paths import QUERIES_MIDDLE_PATH, CODEQL_REPO
from constants.code import EXTRACT_METHODS_QLL
from controllers.command_runner import CommandRunner
import logging


def download_codeql_zip(url):
    CommandRunner.run("git", "clone", url)

def install_method_extract_qll():
    os.makedirs(os.path.join(*QUERIES_MIDDLE_PATH), exist_ok=True)
    CommandRunner.write_to_file(os.path.join(*QUERIES_MIDDLE_PATH, "method_extract.qll"), EXTRACT_METHODS_QLL)

def install_codeql():
    download_codeql_zip(CODEQL_REPO)
    install_method_extract_qll()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(),])
    install_codeql()