# -*- coding: utf-8 -*-
import time
import logging
import os.path
from threading import Lock as WriteLock

from app.common import ENV


# ===========================================================
# SYMBOLIC CONSTANTS
# ===========================================================
HEADER = """#!/bin/bash

if [[ "$#" == 1 && "$1" == "do" ]]; then
  pixwork() { mv -fv "$1" "$2"; }
elif [[ "$#" == 1 && "$1" == "undo" ]]; then
  pixwork() { mv -fv "$2" "$1"; }
else
  echo "Usage: $0 {do|undo}"; exit 0
fi

"""

# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger(ENV)


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class PixHistory:
    """
    Renaming work history writer
    """

    def __init__(self, history_dir="."):
        """
        Initialization
        """
        if not os.path.exists(history_dir):
            os.mkdir(history_dir)

        history_file = "history-%s.sh" % time.strftime("%Y%m%d-%H%M%S", time.localtime())

        # create a history file
        try:
            self.history = open(os.path.join(history_dir, history_file), "w")
        except Exception:
            logger.error(f"Cannot create a history file at {history_dir}")
            self.history = open(history_file, "w")

        # write header
        self.history.write(HEADER)

        # create a lock for writing
        self.lock = WriteLock()

        logger.info(f"Start to write history logs to {history_file}")

    def close(self):
        """
        Close the history file
        """
        self.lock.acquire()

        if self.history:
            self.history.close()
            self.history = None

        self.lock.release()

    def writeline(self, from_path, to_path):
        """
        Write an history line
        """
        if self.history:
            self.lock.acquire()
            try:
                # write a history line
                self.history.write(f"pixwork '{from_path}' '{to_path}'\n")

            except Exception:
                logger.error("Cannot write a history line")

            self.lock.release()
