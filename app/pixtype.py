# -*- coding: utf-8 -*-
import logging
from enum import Enum
from dataclasses import dataclass
from PIL import Image, UnidentifiedImageError

from app.common import ENV


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ==========================================================
# DATA TYPES
# ==========================================================
@dataclass
class PX_CLS:
    """
    Pix file classes
    """
    IMAGE: str = "img"
    VIDEO: str = "mov"


class PX_TYPE(Enum):
    """
    Pix file types
    """
    UNKNOWN = (None, None)
    JPG = ("jpg", PX_CLS.IMAGE)
    TIF = ("tif", PX_CLS.IMAGE)
    PNG = ("png", PX_CLS.IMAGE)
    MP4 = ("mp4", PX_CLS.VIDEO)
    MOV = ("mov", PX_CLS.VIDEO)

    def __init__(self, fmt, cls):
        self.fmt = fmt
        self.cls = cls


# ==========================================================
# CLASS IMPLEMETATIONS
# ==========================================================
class PixTypeMapper:
    """
    Media type mapper. It maps file extensions to type objects
    """
    type_map = {
        "jpg": PX_TYPE.JPG,
        "jpeg": PX_TYPE.JPG,
        "mpo": PX_TYPE.JPG,
        "tif": PX_TYPE.TIF,
        "tiff": PX_TYPE.TIF,
        "png": PX_TYPE.PNG,
        "mp4": PX_TYPE.MP4,
        "mov": PX_TYPE.MOV,
    }

    def __new__(cls, *args, **kwargs):
        raise RuntimeError('%s should not be instantiated' % cls)

    @classmethod
    def map(cls, pix_path) -> object:
        """
        Map a given file to media type object
        """
        try:
            fmt = Image.open(pix_path).format.lower()

        except UnidentifiedImageError:
            *_, fmt = pix_path.lower().split(".")

        except FileNotFoundError:
            logger.error(f"File not found: {pix_path}")
            return PX_TYPE.UNKNOWN

        return cls.type_map[fmt] if (fmt in cls.type_map) else PX_TYPE.UNKNOWN
