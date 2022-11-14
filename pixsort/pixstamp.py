# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from enum import Enum

from pixsort.common import *


#===========================================================
# GLOBAL VARIABLES
#===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# DATA TYPES
# ===========================================================
class TS_INFO_STYLE(Enum):
    """
    Timestamp information styles
    """
    UNKNOWN = 0         # unknown style
    STANDARD = 1        # date and time: (YYYYMMDD, HHMMSS, MSEC)
    EPOCH_SECS = 2      # epoch seconds: (SECONDS)

class STAMP_STYLE(Enum):
    """
    PixStamp stamp styles
    """
    STANDARD = 1        # date and time: <YYYYMMDD_HHMMSS>.<MSEC>_<SEQ>.<EXT>
    EPOCH_SECS = 2      # epoch seconds: <SECONDS>.<MSEC>_<SEQ>.<EXT>

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
class PixStamp:
    """
    Timestamp information of a media file
    """
    def __init__(self):
        """
        Initialization
        """
        self.ts = datetime.fromtimestamp(0)
        self.seq = 0
        self.ext = ""

    def format(self, style=STAMP_STYLE.STANDARD, uppercase=False) -> str:
        """
        construct a pixstamp in a given style
        """
        formatted_stamp = ""
        tag_s = PIX_TYPE.str(PIX_TYPE.map(self.ext))

        if STAMP_STYLE.STANDARD == style:
            msec_s = self.ts.strftime("%f")[:3]
            formatted_stamp = "%s_%s_%s%03d.%s" % (tag_s,
                                                  self.ts.strftime("%Y%m%d_%H%M%S"),
                                                  msec_s,
                                                  self.seq,
                                                  self.ext)

        return formatted_stamp if not uppercase else formatted_stamp.upper()

    @staticmethod
    def new(tsi_style, info) -> object:
        """
        Make a new pixstamp with a given information
        """
        try:
            stamp = PixStamp()

            if TS_INFO_STYLE.STANDARD == tsi_style:
                date_s, time_s, usec_s, ext = info
                usec_s = (usec_s + "000000")[:6]
                stamp.ts = datetime.strptime(f"{date_s}_{time_s}.{usec_s}", "%Y%m%d_%H%M%S.%f")
                stamp.ext = f"{ext}".lower()

            elif TS_INFO_STYLE.EPOCH_SECS == tsi_style:
                secs_s, ext = info
                stamp.ts = datetime.fromtimestamp(int(secs_s))
                stamp.ext = f"{ext}".lower()

        except ValueError:
            logger.error(f"Wrong timestamp information: {info}")
            stamp = None

        return stamp
