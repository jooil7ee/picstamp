# -*- coding: utf-8 -*-
import logging
from collections import deque

from pixsort.common import *
from pixsort.pixstamp import PixStamp


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixStampGroup:
    """
    Pix stamp gorup
    """
    def __init__(self, fmt, stamp):
        self.fmt = fmt
        self.stamp = stamp
        self.paths = []

    def __str__(self):
        return f"{self.fmt}/{self.stamp}: {self.paths}"


class PixStampGroupManager:
    """
    Manages pix stamp groups
    """
    def __init__(self):
        """
        Initialization
        """
        self.stamps = deque()
        self.map = {}

    def empty(self):
        """
        Check if list is empty or not
        """
        return True if (not self.stamps) else False

    def add(self, stamp, path) -> object:
        """
        add a stamp with path to the map. If duplicated, they are merged.
        """
        psg_key = str(stamp)

        if psg_key not in self.map:
            logger.debug(f"Create a new stamp group: {psg_key}")
            self.map[psg_key] = PixStampGroup(stamp.fmt, stamp.stamp)
            self.stamps.append(self.map[psg_key])

        self.map[psg_key].paths.append(path)

    def pop(self):
        """
        Pop an pix stamp group.
        """
        if self.stamps:
            return self.stamps.popleft()

        return None
