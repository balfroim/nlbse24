import os

def ensure_in_path(path: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if path not in os.environ["PATH"]:
                os.environ["PATH"] = f"{os.environ['PATH']}:{path}"
            return func(*args, **kwargs)
        return wrapper
    return decorator