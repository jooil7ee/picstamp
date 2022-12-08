# -*- coding: utf-8 -*-
import re
import logging
import os.path
import exifread
from datetime import datetime

from pixsort.common import ENV
from pixsort.pixfinder import PixFinder
from pixsort.pixtype import PX_TYPE, PixTypeMapper
from pixsort.pixwork import PixWorkerGroup
from pixsort.pixstamp import STAMP_STYLE, TSINFO_TYPE, PixStamp


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
    (re.compile(r"[A-Za-z_]*(\d{8})[-_]?(\d{6})(\d{0,3})\w*\.\w+", re.IGNORECASE),
     TSINFO_TYPE.STANDARD),

    # timestruct based file name (e.g. macos screenshots)
    (re.compile(r"[A-Za-z_]*(\d{4})-?(\d{2})-?(\d{2})[ \w]*(\d{1,2})\.(\d{2})\.(\d{2}).*\.\w+", re.IGNORECASE),
     TSINFO_TYPE.TIMESTRUCT),

    # UNIX epoch seconds
    (re.compile(r"(\d{10})\w*\.\w+", re.IGNORECASE), TSINFO_TYPE.EPOCH_SECS),
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
        self.opts = {
            'style': STAMP_STYLE.STANDARD,
            'num_workers': 1,
            'recursive': False,
            'uppercase': False,
            'history_dir': None,
            'apply': False,
        }

        # reaming workers
        self.workers = None

    def set_options(self, **kwargs):
        """
        Set options: uppercase
        """
        for (k, v) in kwargs.items():
            self.opts[k] = v

    def run(self, in_dir):
        """
        Rename pix files in a given directory
        """
        if not os.path.exists(in_dir):
            logger.error(f"Input directory does not exist: {in_dir}")
            return

        # Create renaming workers
        self.workers = PixWorkerGroup(self.opts['num_workers'])
        self.workers.enable_history(self.opts['history_dir'])

        # Scan and process pix files one by one
        finder = PixFinder()
        finder.find(in_dir, self.opts['recursive'])

        logger.info(f"Inspect pix files in {in_dir}")

        while not finder.empty():
            x = finder.pop()

            # inspect each file and create a stamp for it
            stamp = self.__inspect(x)

            if stamp is not None:
                logger.info(f" * {stamp} ({stamp.desc}) <-- {os.path.split(x)[-1]}")
                self.workers.add_work(stamp, x)

        # Do renaming works
        logger.info(f"Start {self.opts['num_workers']} worker(s) for renaming")
        self.workers.start(self.opts['uppercase'], self.opts['apply'])

        # close history
        self.workers.close_history()

        logger.info("Complete")

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
            style = self.opts['style'].fmt

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
