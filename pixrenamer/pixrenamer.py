# -*- coding: utf-8 -*-
import re
import glob
import os.path
import logging
from enum import Enum
from pixrenamer.pixstamp import Stamp, STAMP_TYPE
from pixrenamer.nameinspector import NameInspector


#===========================================================
# GLOBAL VARIABLES
#===========================================================
logger = logging.getLogger("pixrenamer")


#===========================================================
# SYMBOLIC CONSTANTS
#===========================================================
# Name patterns expressed as regular expressions
NAME_PATTERNS = (
    # standard timestamp-based file name
    ("default", re.compile("(\d{8})_(\d{6})\w*\.(\w+)", re.IGNORECASE)),
    # UNIX epoch seconds
    ("seconds", re.compile("(\d{10})\w*\.(\w+)", re.IGNORECASE)),
    # Kakao Talk
    ("default", re.compile("kakaotalk_(\d{8})_(\d{6})\w*\.(\w+)", re.IGNORECASE)),
)


#===========================================================
# CLASS IMPLEMENTATIONS
#===========================================================
class PixRenamer:
    '''
    Timestamp-based media file renamer
    '''
    def __init__(self, tag):
        '''
        Initialization
        '''
        self.tag = tag
        self.options = {'uppercase': False}

    def set_options(self, **kwargs):
        """
        Set options: uppercase
        """
        for (k, v) in kwargs.items():
            self.options[k] = v

    def process(self, in_dir):
        '''
        Rename files in a given directory
        '''
        if not os.path.exists(in_dir):
            logger.error(f"Input directory does not exist: {in_dir}")
            return

        history = RenameHistory()
        stamp = Stamp(
            self.tag if not self.options['uppercase'] else self.tag.upper())

        # Processing media files one by one
        logger.info(f"Processing files in {in_dir}")
        for x in glob.glob(os.path.join(in_dir, "*")):
            if os.path.isdir(x):
                logger.debug(f"- skipping a directory: {x}")
                continue

            # inspect the file name
            dir_name, file_name = x.rsplit("/")
            style, info = NameInspector.inspect(file_name)

            if "default" == style:
                stamp.set(*info)
            elif "seconds" == style:
                stamp.set_from_seconds(*info)
            else:
                print(f"- {file_name} - failed")
                continue

            new_file_name = stamp.get()

            seq = history.add(new_file_name, file_name)
            print(f"+ {new_file_name}  <= {file_name}")

