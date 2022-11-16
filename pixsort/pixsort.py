# -*- coding: utf-8 -*-
import glob
import logging
import os.path
from datetime import datetime
import exifread
import re

from pixsort.common import *
from pixsort.pixtype import *
from pixsort.pixstamp import PixStamp, TS_INFO_STYLE, STAMP_STYLE
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
    (re.compile("[A-Za-z_]*(\d{8})_?(\d{6})(\d{0,6})\w*\.\w+", re.IGNORECASE),
     TS_INFO_STYLE.STANDARD),

    # UNIX epoch seconds
    (re.compile("(\d{10})\w*\.\w+", re.IGNORECASE), TS_INFO_STYLE.EPOCH_SECS),
)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixSorter:
    """
    Timestamp-based media file sorter
    """

    def __init__(self, batch_size=100):
        """
        Initialization
        """
        self.options = {
            'out_dir': None,
            'uppercase': False,
            'apply': False,
            'style': STAMP_STYLE.STANDARD
        }

        self.batch_queue = []
        self.batch_size = batch_size

    def set_options(self, **kwargs):
        """
        Set options: uppercase
        """
        for (k, v) in kwargs.items():
            self.options[k] = v

    def run(self, in_dir):
        """
        Rename media files in a given directory
        """
        if not os.path.exists(in_dir):
            logger.error(f"Input directory does not exist: {in_dir}")
            return

        # Scan and process media files one by one
        media_files = glob.glob(os.path.join(in_dir, "*"))
        media_files.sort()

        for x in media_files:
            if os.path.isdir(x):
                logger.debug(f"- skipping a directory: {x}")
                continue

            # inspect media file
            stamp = self.__inspect(x)

            if not stamp:
                continue

            # create a renaming work and add it to batch queue
            #renaming = RenamingWork(x, stamp.format(uppercase=self.options['uppercase']))

            #self.batch_queue.append(renaming)
            #if self.batch_size <= len(self.batch_queue):
            #    self.__do_batch()
            ##seq = history.add(new_file_name, file_name)
            stamp_str = stamp.format(style=self.options['style'], uppercase=self.options['uppercase'])
            print(f" - {stamp_str} ({stamp.desc})  <= {x} ")

        #if 0 < len(self.batch_queue):
        #    self.__do_batch()

    def __inspect(self, pix_path) -> object:
        """
        Do pattern matching and extract timestamp information. Rules are
         - a) try to extract from file name
         - b) if not, try to extract from exif (for JPEG and TIFF)
         - c) if not, extract from file stat (for PNG files)
        """
        pix_type = PixTypeMapper.map(pix_path)
        *_, pix_name = pix_path.replace("-", "_").rsplit("/")

        # extract timestamp information to create pixstamp
        if pix_type is not PX_TYPE.UNKNOWN:

            # rule1: match with file name patterns

            for p, style in NAME_PATTERNS:
                is_matched = p.match(pix_name)
                if is_matched:
                    return PixStamp.new(style, is_matched.groups(), pix_type, "R1")

            # rule2: check exif information
            if pix_type in [PX_TYPE.JPG, PX_TYPE.TIF]:
                exif = exifread.process_file(open(pix_path, "rb"))
                if "EXIF DateTimeOriginal" in exif.keys():
                    style = TS_INFO_STYLE.DATETIME_OBJ
                    dt_obj = datetime.strptime(
                        exif["EXIF DateTimeOriginal"].values, "%Y:%m:%d %H:%M:%S")
                    return PixStamp.new(style, dt_obj, pix_type, "R2")

            # rule3: using file stats
            stat = os.stat(pix_path)
            if 0 < stat.st_mtime:
                style = TS_INFO_STYLE.EPOCH_SECS
                return PixStamp.new(style, int(stat.st_mtime), pix_type, "R3")

        # failed to extract timestamp information
        logger.error(f"Inspection failed: {pix_path}")

        return None

    def __do_batch(self):
        """
        Process jobs in the queue all at once.
        """
        logger.debug("Process batch queue:")

        while 0 < len(self.batch_queue):
            work = self.batch_queue.pop(0)
            work.execute(apply=self.options['apply'])
