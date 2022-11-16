# -*- coding: utf-8 -*-
import logging
from PIL import Image
from datetime import datetime

from pixsort.common import *


#===========================================================
# GLOBAL VARIABLES
#===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# DATA TYPES
# ===========================================================
class PIX_TYPE(Enum):
    """
    Media file types
    """
    UNKNOWN = 0
    IMAGE = 1
    VIDEO = 2

    @staticmethod
    def map(ext) -> Enum:
        if ext in ['png', 'jpg', 'jpeg', 'gif']:
            return PIX_TYPE.IMAGE

        elif ext in ['mp4', 'mov']:
            return PIX_TYPE.VIDEO

        return PIX_TYPE.UNKNOWN

    @staticmethod
    def str(pix_type) -> str:
        if PIX_TYPE.IMAGE == pix_type:
            return "img"

        elif PIX_TYPE.VIDEO == pix_type:
            return "mov"

        return "unknown"




# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class ExifReader:
    """
    Exif information Reader for images
    """
    @staticmethod
    def get_datetime(im_type, im_path):
        """
        return the Exif DateTimeOriginal value as Python datetime
        """
        # JPEG and TIFF
        if im_type in ["JPEG", "TIFF"]:
            with open(im_path, "rb") as f:
                exif = exifread.process_file(f):
                if "EXIF DateTimeOriginal" in exif.keys():
                    return datetime.strptime(
                        exif["EXIF DateTimeOriginal"].values, "%Y:%m:%d %H:%M:%S")

        elif im_type in ["PNG"]:


        else:
            logger.error(f"Unsupported media type {im_type}")


        return formatted_stamp if not uppercase else formatted_stamp.upper()
