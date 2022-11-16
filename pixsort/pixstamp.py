# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from enum import Enum

from pixsort.common import *
from pixsort.pixtype import *


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
    DATETIME_OBJ = 3    # datetime object

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
    def __init__(self):
        """
        Initialization
        """
        self.ts = datetime.fromtimestamp(0)
        self.seq = 0
        self.type = None
        self.desc = ""

    def format(self, style=STAMP_STYLE.STANDARD, uppercase=False) -> str:
        """
        construct a pixstamp in a given style
        """
        formatted_stamp = ""

        pix_cls = "img" if (self.type.cls is PX_CLS.IMAGE) else "mov"

        if STAMP_STYLE.STANDARD == style:
            msec_s = self.ts.strftime("%f")[:3]
            formatted_stamp = "%s_%s_%s%03d.%s" % (pix_cls,
                                                   self.ts.strftime("%Y%m%d_%H%M%S"),
                                                   msec_s,
                                                   self.seq,
                                                   self.type.fmt)

        return formatted_stamp if (not uppercase) else formatted_stamp.upper()

    @staticmethod
    def new(style, info, pix_type, desc ="") -> object:
        """
        Make a new pixstamp with a given information
        """
        try:
            stamp = PixStamp()

            # set type and description
            stamp.type = pix_type
            stamp.desc = desc

            # construct timestamp
            if TS_INFO_STYLE.STANDARD == style:
                date_s, time_s, usec_s = info
                usec_s = (usec_s + "000000")[:6]
                stamp.ts = datetime.strptime(f"{date_s}_{time_s}.{usec_s}", "%Y%m%d_%H%M%S.%f")

            elif TS_INFO_STYLE.EPOCH_SECS == style:
                if isinstance(info, list) or isinstance(info, tuple):
                    sec_s, *_ = info
                else:
                    sec_s = info

                stamp.ts = datetime.fromtimestamp(int(sec_s))

            elif TS_INFO_STYLE.DATETIME_OBJ == style:
                stamp.ts = info

        except ValueError:
            logger.error(f"Wrong timestamp information: {info}")
            stamp = None


        return stamp
