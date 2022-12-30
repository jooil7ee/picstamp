# -*- coding: utf-8 -*-
import os.path
from threading import Thread, Lock
from collections import deque

from pixsort.pixstamp import PixStampGroup
from pixsort.pixhistory import PixHistory


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

    def __del__(self):
        """
        Clean-up
        """
        self.queue.clear()

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
        self.history = None

        # create work queues and put them into a set
        if 0 < num_workers <= self.worker_count_max:
            self.num_workers = num_workers
        else:
            self.num_workers = 1

        for i in range(self.num_workers):
            self.workq.append(PixWorkQueue(index=self.index))

    def open_history(self, history_dir="."):
        """
        Enable work history
        """
        self.history = PixHistory(history_dir)

    def close_history(self):
        """
        Close the history file
        """
        if self.history:
            self.history.close()

    def add_work(self, pixstamp, path) -> object:
        """
        Create a renaming work for a given pixstamp. If duplicated, they are merged.
        """
        key = f"{pixstamp.fmt}/{pixstamp.stamp}"

        if key not in self.index:
            # create a new pixstamp group
            next_queue = self.workq[self.count % self.num_workers]
            next_queue.push(PixStampGroup(pixstamp.fmt, pixstamp.stamp))
            self.count += 1

        # append a path to pixstamp group
        psg = self.index[key]
        psg.add_path(path)

        return psg

    def start(self, uppercase, apply=False):
        """
        Start renaming workers. Each worker processes its own work queue.
        """
        workers = []

        for i in range(self.num_workers):
            worker = Thread(target=PixWorkerGroup.__process,
                            args=(i, self.workq[i], self.history, uppercase, apply))
            workers.append(worker)

            # start a worker as thread
            worker.start()

        for worker in workers:
            worker.join()

    @staticmethod
    def __process(tid, queue, history, uppercase, apply):
        """
        Do renaming works
        """
        while not queue.empty():
            psg = queue.pop()
            seq = 0

            for from_path in psg.paths:
                base, x = os.path.split(from_path)
                y = f"%s%03d.%s" % (psg.stamp, seq, psg.fmt)
                seq += 1

                if uppercase:
                    y = y.upper()

                to_path = os.path.join(base, y)

                if apply:
                    # do the renaming work
                   os.rename(from_path, to_path)

                history.writeline(from_path, to_path)

