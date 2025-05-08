import os
from django.conf import settings


def load_secret(var: str, default=None) -> str:
    filepath = settings.BASE_DIR / "secrets" / var
    if var in os.environ:
        return os.environ.get(var)

    if filepath.exists():
        with open(filepath, "r") as s:
            return s.read().strip()

    if default is not None:
        return str(default)

    raise ValueError(f"Secret '{var}' not found in environment, file system, or defaults")
