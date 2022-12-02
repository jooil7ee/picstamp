# -*- coding: utf-8 -*-
import os.path
from threading import Thread, Lock
from collections import deque

from pixsort.pixstamp import PixStampGroup


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
        self.history = None

        # create work queues and put them into a set
        if 0 < num_workers <= self.worker_count_max:
            self.num_workers = num_workers
        else:
            self.num_workers = 1

        for i in range(self.num_workers):
            self.workq.append(PixWorkQueue(index=self.index))

    def enable_history(self, history_dir):
        """
        Enable work history. Create a history file at the given directory.
        """
        if not os.path.exists(history_dir):
            os.mkdir(history_dir)

        history_file = f"history-%s.log" % time.strftime("%Y%m%d-%H%M%S", time.localtime())

        # create a history file
        try:
            self.history = open(os.path.join(history_dir, history_file), "w") 
        except:
            logger.error(f"Cannot create a history file at {history_dir}")
            self.history = open(history_filem "w")

        # create a lock for writing
        self.lock = Threading.Lock()

    def close_history(self):
        """
        Close the history file
        """
        if self.history:
            self.history.close()

    def write_history(self, history_line):
        """
        Write an history line
        """
        if self.history:
            lock.acquire()

            try:
                # write a history line
                self.history.write(history_line) 

            except:
                logger.error("Cannot write a history line")

            lock.release()

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

    def write_history(self):
        """
        Write work history line.
        """
        


    def start(self, uppercase, apply=False):
        """
        Start renaming workers. Each worker processes its own work queue.
        """
        workers = []

        for i in range(self.num_workers):
            worker = Thread(target=PixWorkerGroup.__process,
                            args=(i, self.workq[i], uppercase, apply))

            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()

    @staticmethod
    def __process(tid, queue, uppercase, apply):
        """
        Do renaming works
        """
        while not queue.empty():
            psg = queue.pop()
            seq = 0

            for path in psg.paths:
                base, x = os.path.split(path)
                y = "%s%03d.%s" % (psg.stamp, seq, psg.fmt)
                seq += 1

                if uppercase:
                    y = y.upper()

                print(f" * [W{tid}] {psg.key()}:  {y} <-- {x}  (@{base})")

                if apply:
                    # do the renaming work
                   pass

