# -*- coding: utf-8 -*-
import glob
import logging
import os.path
import re

from pixsort.common import *
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
    (re.compile("[A-Za-z_]*(\d{8})_?(\d{6})(\d{0,6})\w*\.(\w+)", re.IGNORECASE),
     TS_INFO_STYLE.STANDARD),

    # UNIX epoch seconds
    (re.compile("(\d{10})\w*\.(\w+)", re.IGNORECASE), TS_INFO_STYLE.EPOCH_SECS),
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
        logger.info(f"Processing files in {in_dir}")
        media_files = glob.glob(os.path.join(in_dir, "*"))
        media_files.sort()

        for x in media_files:
            if os.path.isdir(x):
                logger.debug(f"- skipping a directory: {x}")
                continue

            # test for exif


            # inspect the file name
            *dir_name, file_name = x.rsplit("/")
            stamp = self.__inspect(file_name)

            if not stamp:
                continue

            # create a renaming work and add it to batch queue
            #renaming = RenamingWork(x, stamp.format(uppercase=self.options['uppercase']))

            #self.batch_queue.append(renaming)
            #if self.batch_size <= len(self.batch_queue):
            #    self.__do_batch()
            ##seq = history.add(new_file_name, file_name)
            stamp_str = stamp.format(style=self.options['style'], uppercase=self.options['uppercase'])
            print(f"+ {stamp_str}  <= {file_name}")

        #if 0 < len(self.batch_queue):
        #    self.__do_batch()

    def __inspect(self, file_name):
        """
        Do pattern matching and extract timestamp information.
        """
        n = file_name.replace("-", "_")

        for p, x in NAME_PATTERNS:
            is_matched = p.match(n)
            if is_matched:
                logger.debug(f"{file_name}  --> {x}")
                return PixStamp.new(x, is_matched.groups())


        logger.error(f"{file_name}  --> {TS_INFO_STYLE.UNKNOWN}")

        return None

    def __do_batch(self):
        """
        Process jobs in the queue all at once.
        """
        logger.debug("Process batch queue:")

        while 0 < len(self.batch_queue):
            work = self.batch_queue.pop(0)
            work.execute(apply=self.options['apply'])
