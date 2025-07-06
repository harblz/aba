import os
from django.conf import settings
from pathlib import Path


home = Path.home()
def load_secret(var: str, default=None) -> str:
    if var in os.environ:
        return os.environ.get(var)

    filepath = None
    if "SECRETS_DIR" in os.environ:
        filepath = Path(f"{os.environ.get("SECRETS_DIR")}/{var.lower()}")
    else:
        filepath = home / ".secrets/abarocks" / var
    if filepath.exists():
        with open(filepath, "r") as s:
            return s.read().strip()

    if default is not None:
        return str(default)

    raise ValueError(f"Secret '{var}' not found in environment, file system, or defaults")
