# -*- coding: utf-8 -*-
import logging
import os.path
from threading import Lock

from pixsort.common import ENV


# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logger.getLogger(ENV)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixHistory:
    """
    Renaming work history writer
    """

    def __init__(self, history_dir):
        """
        Initialization
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

    def close(self):
        """
        Close the history file
        """
        self.lock.acquire()

        if self.history:
            self.history.close()
            self.history = None

        self.lock.release()

    def write(self, line):
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
