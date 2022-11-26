# -*- coding: utf-8 -*-
import logging
from collections import deque

from pixsort.common import *


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================

class IndexedQueue
    """
    Simple queue with index
    """
    def __init__(self, index=None):
        """
        Initialization
        """
        self.queue = deque()
        self.count = 0

        if index is not None:
            self.index = index
        else:
            self.index = {}

    def empty(self):
        """
        Check if this queue is empty or not
        """
        return True if (not self.queue) else False

    def push(self, elem):
        """
        Push an element with index key.
        """
        self.queue.append(elem)
        self.count += 1

        self.index[elem.key()] = elem

    def pop(self):
        """
        Pop one element. Also update index.
        """
        elem = None

        if self.queue:
            elem = self.queue.popleft()
            self.index.pop(elem.key())

        return elem


class PixWorkQueue
    """
    Set of indexed queues for renaming works
    """
    set_size_max = 10
    
    def __init__(self, size=1):
        """
        Initialization
        """
        self.index = {}
        self.qset = []
        self.count = 0

        # create queues and put them into a set
        if 0 < size <= self.set_size_max:
            self.size = size
        else:
            self.size = 1

        for i in range(self.size):
            self.qset.append(IndexedQueue(index=self.index))

    def empty(self):
        """
        Check if all queues are empty or not
        """
        return all(list(map(lambda q: q.empty(), self.qset)))

    def push(self, pixstamp, path) -> object:
        """
        push a stamp with path to the queue. If duplicated, they are merged.
        """
        key = f"{pixstamp.fmt}/{pixstamp.stamp}"

        if key not in self.index:
            # create a new pixstamp group
            next_queue = self.qset[self.count % self.size]
            next_queue.push(PixStampGroup(pixstamp.fmt, pixstamp.stamp))
            self.count += 1

        # append a path to pixstamp group
        psg = self.index[key]
        psg.paths.append(path)

        return psg

    def assign_to(self, ....):
        """
        Pop an pix stamp group.
        """
        psg = None

        if self.empty():
            psg = self.stamps.popleft()
            self.map.pop(psg.key())

        return psg
