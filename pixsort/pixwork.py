# -*- coding: utf-8 -*-
import logging
from collections import deque
from threading import Thread

from pixsort.common import *
from pixsort.pixstamp import PixStampGroup


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixWorkQueue:
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


class PixWorkerGroup:
    """
    Group of renaming workers.
    """
    worker_count_max = 8

    def __init__(self, num_workers=1):
        """
        Initialization
        """
        self.index = {}
        self.workq = []
        self.count = 0

        # create work queues and put them into a set
        if 0 < num_workers <= self.worker_count_max:
            self.num_workers = num_workers
        else:
            self.num_workers = 1

        for i in range(self.num_workers):
            self.workq.append(PixWorkQueue(index=self.index))

    def add_work(self, pixstamp, path) -> object:
        """
        Create a renaming work for a given pixstamp. If duplicated, they are merged.
        """
        key = f"{pixstamp.fmt}/{pixstamp.stamp}"

        if key not in self.index:
            # create a new pixstamp group
            next_queue = self.workq[self.count % self.size]
            next_queue.push(PixStampGroup(pixstamp.fmt, pixstamp.stamp))
            self.count += 1

        # append a path to pixstamp group
        psg = self.index[key]
        psg.paths.append(path)

        return psg

    def start(self, apply=False):
        """
        Start renaming workers. Each worker processes its own work queue.
        """
        workers = []

        for i in range(self.num_workers):
            worker = Thread(
                    target=PixWorkerGroup.__process,
                    args=(i, self.workq[i], apply))

            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()

    @staticmethod
    def __process(tid, queue, apply):
        """
        Do renaming works
        """
        while not queue.empty():
            psg = queue.pop()
            print(f" > {psg}")

            if apply:
                # do a renamaing work
                pass
