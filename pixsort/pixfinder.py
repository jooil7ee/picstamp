# -*- coding: utf-8 -*-
import os
import glob
from collections import deque

from pixsort.common import *


# ==========================================================
# CLASS IMPLEMETATIONS
# ==========================================================
class PixFinder:
    """
    Find pix files in a given directory recursively.
    """
    def __init__(self):
        """
        Initialization
        """
        self.files = None
        self.size = 0

    def empty(self):
        """
        Check if queue is empty or not
        """
        return True if (not self.files) else False

    def pop(self):
        """
        Pop an pix file path from the queue.
        """
        if self.files:
            self.size -= 1
            return self.files.popleft()

        return None

    def find(self, path, recursive=False) -> object:
        """
        Find all pix files in a given directory recursively.
        """
        self.files = deque()
        self.size = 0

        files = glob.glob(os.path.join(path, "*"))

        for x in files:
            if os.path.isdir(x):
                if recursive: 
                    self.__find_subdir(x)
            else:
                self.files.append(x)
                self.size += 1

    def __find_subdir(self, path):
        """
        Scan a given directory.
        """
        files = glob.glob(os.path.join(path, "*"))

        for x in files:
            if os.path.isdir(x):
                self.__find_subdir(x)

            self.files.append(x)
            self.size += 1
