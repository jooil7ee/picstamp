# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from enum import Enum

from pixsort.common import ENV


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# DATA TYPES
# ===========================================================
class TSINFO_TYPE(Enum):
    """
    Timestamp information types
    """
    UNKNOWN = 0         # unknown type
    STANDARD = 1        # date and time: (yyyymmdd, HHMMSS, msec)
    TIMESTRUCT = 2      # data and time: (yyyy, mm, dd, HH, MM, SS)
    EPOCH_SECS = 3      # epoch seconds
    DATETIME_OBJ = 4    # datetime object


class STAMP_STYLE(Enum):
    """
    Pix stamp styles
    """
    STANDARD = "%Y%m%d_%H%M%S_%f"   # date and time
    EPOCH_SECS = "%s_%f"            # epoch seconds

    def __init__(self, fmt):
        self.fmt = fmt


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixStamp:
    """
    Pixstamp for the pix file
    """
    def __init__(self, fmt, stamp, desc=""):
        self.fmt = fmt
        self.stamp = stamp
        self.desc = desc

    def __str__(self):
        return f"{self.fmt}/{self.stamp}"

    @staticmethod
    def new(style, tsi_type, tsi_data, pix_type, desc="") -> str:
        """
        Create a pixstamp object with a given timstamp information
        """
        # construct datatime object first
        dt = None

        try:
            if TSINFO_TYPE.STANDARD == tsi_type:
                date_s, time_s, usec_s = tsi_data
                usec_s = (usec_s + "000")[:3]
                dt = datetime.strptime(f"{date_s}_{time_s}.{usec_s}", "%Y%m%d_%H%M%S.%f")

            elif TSINFO_TYPE.TIMESTRUCT == tsi_type:
                dt = datetime(*list(map(int, tsi_data)))

            elif TSINFO_TYPE.EPOCH_SECS == tsi_type:
                if isinstance(tsi_data, list) or isinstance(tsi_data, tuple):
                    sec_s, *_ = tsi_data
                else:
                    sec_s = tsi_data

                dt = datetime.fromtimestamp(int(sec_s))

            elif TSINFO_TYPE.DATETIME_OBJ == tsi_type:
                dt = tsi_data

            else:
                logger.error(f"Unsupported TSI type: {tsi_type}")

            # create pixstamp object using the datatime object
            if dt is not None:
                stamp_s = "%s_%s" % (pix_type.cls, dt.strftime(style)[:-3])
                return PixStamp(pix_type.fmt, stamp_s, desc)

        except ValueError:
            logger.error(f"Invalid TSI data: {tsi_data}")

        return None


class PixStampGroup:
    """
    Pix stamp group
    """
    def __init__(self, fmt, stamp, path=None):
        self.fmt = fmt
        self.stamp = stamp
        self.paths = [path,] if path else []

    def key(self):
        """
        Return stamp group key
        """
        return f"{self.fmt}/{self.stamp}"

    def add_path(self, path):
        """
        Add a new path to this group
        """
        self.paths.append(path)

    def __str__(self):
        return f"{self.fmt}/{self.stamp}: {self.paths}"
