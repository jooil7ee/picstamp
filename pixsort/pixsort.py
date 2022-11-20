# -*- coding: utf-8 -*-
import re
import glob
import logging
import os.path
import exifread
from datetime import datetime

from pixsort.common import *
from pixsort.pixfinder import PixFinder
from pixsort.pixtype import PixTypeMapper, PX_TYPE
from pixsort.pixstamp import PixStamp, TSINFO_TYPE, STAMP_STYLE
from pixsort.pixstampgroup import PixStampGroup, PixStampGroupManager
from pixsort.renamingwork import RenamingWork


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# SYMBOLIC CONSTANTS
# ===========================================================
# Name patterns expressed as regular expressions
NAME_PATTERNS = (
    # standard date-and-time based file name (with microseconds)
    (re.compile("[A-Za-z_]*(\d{8})[-_]?(\d{6})(\d{0,3})\w*\.\w+", re.IGNORECASE),
     TSINFO_TYPE.STANDARD),

    # timestruct based file name (e.g. macos screenshots)
    (re.compile("[A-Za-z_]*(\d{4})-?(\d{2})-?(\d{2})[ \w]*(\d{1,2})\.(\d{2})\.(\d{2}).*\.\w+", re.IGNORECASE),
     TSINFO_TYPE.TIMESTRUCT),

    # UNIX epoch seconds
    (re.compile("(\d{10})\w*\.\w+", re.IGNORECASE), TSINFO_TYPE.EPOCH_SECS),
)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixSorter:
    """
    Timestamp-based media file sorter
    """
    def __init__(self):
        """
        Initialization
        """
        self.options = {
            'out_dir': None,
            'recursive': False,
            'uppercase': False,
            'apply': False,
            'style': STAMP_STYLE.STANDARD
        }

        # pixstamp and its group manager
        self.stamper = None
        self.psg = None

    def set_options(self, **kwargs):
        """
        Set options: uppercase
        """
        for (k, v) in kwargs.items():
            self.options[k] = v

    def run(self, in_dir):
        """
        Rename pix files in a given directory
        """
        if not os.path.exists(in_dir):
            logger.error(f"Input directory does not exist: {in_dir}")
            return

        # Create a stamp group manager
        self.psg = PixStampGroupManager()

        # Scan and process pix files one by one
        finder = PixFinder()
        finder.find(in_dir, self.options['recursive'])

        while not finder.empty():
            x = finder.pop()

            # inspect each file and create a stamp for it
            stamp = self.__inspect(x)

            if stamp is not None:
                logger.info(f"{stamp} ({stamp.desc}) <-- {os.path.split(x)[-1]}")
                self.psg.add(stamp, x)

        # Do renaming works
        while not self.psg.empty():
            sg = self.psg.pop()
            print(f" > {sg}")

    def __inspect(self, pix_path) -> str:
        """
        Do pattern matching and extract timestamp information. Rules are
         - a) try to extract from file name
         - b) if not, try to extract from exif (for JPEG and TIFF)
         - c) if not, extract from file stat (for PNG files)
        """
        pix_type = PixTypeMapper.map(pix_path)
        *_, pix_name = os.path.split(pix_path)

        # extract timestamp information to create pixstamp
        if pix_type is not PX_TYPE.UNKNOWN:
            style = self.options['style'].fmt

            # rule1: match with file name patterns
            for p, tsi_type in NAME_PATTERNS:
                is_matched = p.match(pix_name)
                if is_matched:
                    return PixStamp.new(style, tsi_type, is_matched.groups(), pix_type, "R1")

            # rule2: check exif information
            if pix_type in [PX_TYPE.JPG, PX_TYPE.TIF]:
                exif = exifread.process_file(open(pix_path, "rb"))
                if "EXIF DateTimeOriginal" in exif.keys():
                    tsi_type = TSINFO_TYPE.DATETIME_OBJ
                    dt_obj = datetime.strptime(
                        exif["EXIF DateTimeOriginal"].values, "%Y:%m:%d %H:%M:%S")
                    return PixStamp.new(style, tsi_type, dt_obj, pix_type, "R2")

            # rule3: using file stats
            stat = os.stat(pix_path)
            if 0 < stat.st_mtime:
                tsi_type = TSINFO_TYPE.EPOCH_SECS
                return PixStamp.new(style, tsi_type, int(stat.st_mtime), pix_type, "R3")

        # failed to extract timestamp information
        logger.error(f"Inspection failed: {pix_name}")

        return None
