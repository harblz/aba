import os
from pathlib import Path

from qrcode import QRCode
from qrcode.image.svg import SvgPathImage

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

    raise ValueError(
        f"Secret '{var}' not found in environment, file system, or defaults"
    )


class CustomSvgPathImage(SvgPathImage):
    def __init__(self, *args, **kw):
        self.background = kw.pop("back_color", None)
        self.QR_PATH_STYLE["fill"] = kw.pop("fill_color", "#000000")
        super().__init__(*args, **kw)


def make_with_bg(data=None, **kwargs):
    qr = QRCode(**kwargs)
    qr.add_data(data)
    return qr.make_image(back_color="#ffffff")
