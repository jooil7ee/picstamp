# -*- coding: utf-8 -*-
from enum import Enum
from datetime import datetime

# ===========================================================
# DATA TYPES
# ===========================================================
class STAMP_TYPE(Enum):
    '''
    PicStamp formats
    '''
    DEFAULT = 0   # <TAG>_<YYYYMMDD_HHMMSS>_<SEQ>.<EXT>
    SECONDS = 1   # <TAG>_<EPOCH SECONDS>_<SEQ>.<EXT>


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class Stamp:
    '''
    Timestamp information of a media file
    '''
    def __init__(self, tag):
        '''
        Initialization
        '''
        self.tag = tag
        self.uppercase = True
        self.info = None
        self.ext = None

    def set(self, date_s, time_s, ext):
        '''
        Set timestamp information
        '''
        self.info = datetime.strptime(f"{date_s}_{time_s}", "%Y%m%d_%H%M%S")
        self.ext = ext.lower()

    def set_from_seconds(self, secs_s, ext):
        '''
        Set timestamp information from UNIX epoch seconds
        '''
        self.info = datetime.fromtimestamp(int(secs_s))
        self.ext = ext.lower()

    def get(self, style=STAMP_TYPE.DEFAULT):
        '''
        construct a file name in a given picstamp format
        '''
        seq = 1
        return "%s_%s_%03d.%s" % (
            self.tag, self.info.strftime("%Y%m%d_%H%M%S"), seq, self.ext)