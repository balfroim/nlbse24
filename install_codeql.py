import requests
import zipfile
import os
from constants.paths import DOWNLOAD_CODEQLZIP_PATH, DOWNLOAD_CODEQLZIP_URL, QUERIES_MIDDLE_PATH
from constants.queries import METHOD_EXTRACT_QLL
import logging


def download_codeql_zip(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as file:
            file.write(response.content)
        logging.info("CodeQL CLI downloaded successfully.")
    else:
        logging.info("Failed to download CodeQL CLI.")


def extract_codeql_zip(path):
    with zipfile.ZipFile(path, "r") as zip_ref:
        zip_ref.extractall("./")
    logging.info("CodeQL CLI extracted successfully.")


def install_method_extract_qll():
    os.makedirs(os.path.join(*QUERIES_MIDDLE_PATH), exist_ok=True)
    with open(os.path.join(*QUERIES_MIDDLE_PATH, "method_extract.qll"), "w") as file:
        file.write(METHOD_EXTRACT_QLL)
    logging.info("method_extract.qll installed successfully.")

def delete_codeql_zip(path):
    os.remove(path)
    logging.info("CodeQL CLI deleted successfully.")

def install_codeql():
    download_codeql_zip(DOWNLOAD_CODEQLZIP_URL, DOWNLOAD_CODEQLZIP_PATH)
    extract_codeql_zip(DOWNLOAD_CODEQLZIP_PATH)
    install_method_extract_qll()
    delete_codeql_zip(DOWNLOAD_CODEQLZIP_PATH)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[logging.StreamHandler(),])
    install_codeql()