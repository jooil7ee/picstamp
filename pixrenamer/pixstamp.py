# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from enum import Enum


#===========================================================
# GLOBAL VARIABLES
#===========================================================
logger = logging.getLogger("pixrenamer")


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


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixStamp:
    """
    Timestamp information of a media file
    """
    def __init__(self, tag):
        """
        Initialization
        """
        self.tag = tag
        self.ts = datetime.fromtimestamp(0)
        self.seq = 0
        self.ext = ""

    def format(self, style=STAMP_STYLE.STANDARD, uppercase=False) -> str:
        """
        construct a pixstamp in a given style
        """
        formatted_stamp = ""

        if STAMP_STYLE.STANDARD == style:
            msec_s = self.ts.strftime("%f")[:3]
            formatted_stamp = "%s_%s_%s%03d%s" % (self.tag,
                                                  self.ts.strftime("%Y%m%d_%H%M%S"),
                                                  msec_s,
                                                  self.seq,
                                                  self.ext)

        return formatted_stamp if not uppercase else formatted_stamp.upper()

    @staticmethod
    def new(tag, ts_info_style, info) -> object:
        """
        Make a new pixstamp with a given information
        """
        try:
            stamp = PixStamp(tag)

            if TS_INFO_STYLE.STANDARD == ts_info_style:
                date_s, time_s, usec_s, ext = info
                usec_s = (usec_s + "000000")[:6]
                stamp.ts = datetime.strptime(f"{date_s}_{time_s}.{usec_s}", "%Y%m%d_%H%M%S.%f")
                stamp.ext = f".{ext}"

            elif TS_INFO_STYLE.EPOCH_SECS == ts_info_style:
                secs_s, ext = info
                stamp.ts = datetime.fromtimestamp(int(secs_s))
                stamp.ext = f".{ext}"

        except ValueError:
            logger.error(f"Wrong timestamp information: {info}")
            stamp = None

        return stamp
