# -*- coding: utf-8 -*-
import os.path
import logging
from threading import Thread
from collections import deque

from app.common import ENV
from app.pixstamp import PixStampGroup
from app.pixhistory import PixHistory


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
        # set operation mode
        if apply:
            logger.info(f"Start {self.num_workers} worker(s) in apply mode with history logging")
            target = PixWorkerGroup.__process
            self.history = PixHistory(".")
        else:
            logger.info(f"Start {self.num_workers} worker(s) in preview mode")
            target = PixWorkerGroup.__preview

        # create wrokers
        workers = []

        for i in range(self.num_workers):
            worker = Thread(target=target, args=(i, self.workq[i], self.history, uppercase))
            workers.append(worker)

            # start a worker as thread
            worker.start()

        for worker in workers:
            worker.join()

    def close(self):
        """
        Clean up resources
        """
        if self.history:
            self.history.close()

    @staticmethod
    def __process(tid, queue, history, uppercase):
        """
        Do renaming works
        """
        while not queue.empty():
            psg = queue.pop()
            psg.sort_paths()
            seq = 0

            for from_path in psg.paths:
                base, x = os.path.split(from_path)
                y = "%s%03d.%s" % (psg.stamp, seq, psg.fmt)
                seq += 1

                if uppercase:
                    y = y.upper()

                # compare old(x) and new(y) file names
                if x == y:
                    logger.info(" [X] %-30s <-- %s (@%s)" % ("---", x, base))
                else:
                    # rename pix file and write history
                    logger.info(f" [A] {y} <-- {x} (@{base})")

                    to_path = os.path.join(base, y)
                    os.rename(from_path, to_path)

                    history.writeline(from_path, to_path)

    @staticmethod
    def __preview(tid, queue, history, uppercase):
        """
        Preview renaming works. (not applied)
        """
        while not queue.empty():
            psg = queue.pop()
            psg.sort_paths()
            seq = 0

            for from_path in psg.paths:
                base, x = os.path.split(from_path)
                y = "%s%03d.%s" % (psg.stamp, seq, psg.fmt)
                seq += 1

                if uppercase:
                    y = y.upper()

                # compare old(x) and new(y) file names
                if x == y:
                    logger.info(" [X] %-30s <-- %s (@%s)" % ("---", x, base))
                else:
                    logger.info(f" [P] {y} <-- {x} (@{base})")
