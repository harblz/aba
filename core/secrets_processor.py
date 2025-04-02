import os


def load_secret(var: str, default=None) -> str:
    if var not in os.environ and default:
        return str(default)
    elif (filepath := os.environ.get(var)).startswith("/run/secrets/"):
        with open(filepath, "r") as s:
            return s.read()
    else:
        return os.environ.get(var)
