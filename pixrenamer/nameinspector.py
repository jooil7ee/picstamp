# -*- coding: utf-8 -*-
from enum import Enum
from datetime import datetime


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


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class NameInspector:
    '''
    File name inspector
    '''
    @staticmethod
    def inspect(cls, file_name):
        '''
        Do pattern matching and extract timestamp information
        '''
        n = file_name.replace("-", "_")

        for x, p in NAME_PATTERNS:
            is_matched = p.match(n)
            if is_matched:
                return (x, is_matched.groups())

        return ("unknown",())