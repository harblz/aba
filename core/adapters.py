from io import BytesIO
from allauth.mfa.adapter import DefaultMFAAdapter
from core.utilities import make_with_bg


class MFAAdapter(DefaultMFAAdapter):
    def build_totp_svg(self, url: str) -> str:
        from core.utilities import CustomSvgPathImage

        img = make_with_bg(url, image_factory=CustomSvgPathImage)
        buf = BytesIO()
        img.save(buf)
        return buf.getvalue().decode("utf8")
