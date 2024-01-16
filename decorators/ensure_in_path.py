import os
import logging
from dotenv import load_dotenv

load_dotenv()

def ensure_in_path(path: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            paths = os.environ["PATH"].split(":")
            if path not in paths:
                logging.info(f"Adding {path} to PATH")
                paths.append(path)
                os.environ["PATH"] = ":".join(paths)
            return func(*args, **kwargs)
        return wrapper
    return decorator