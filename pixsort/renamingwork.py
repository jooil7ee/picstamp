# -*- coding: utf-8 -*-
import logging
import os.path

# ===========================================================
# GLOBAL VARIABLES
# ===========================================================
logger = logging.getLogger("pixrenamer")


# ===========================================================
# CLASS IMPLEMENTATIONS
# ===========================================================
class RenamingWork:
    """
    A renaming work details
    """

    def __init__(self, source, target):
        """
        Initialization
        """
        self.source = source
        self.target = target

    def execute(self, apply=False):
        """
        Execute this renaming work
        """
        # check status of the source and the target files
        if not os.path.exists(self.source):
            logger.error(f"Source file does not exist: {self.source}")
            return False

        if os.path.exists(self.target):
            logger.error(f"Target file is already exists: {self.target}")
            return False

        # Execute this renaming work
        if apply:
            print(f"> (applying) {self.target} <= {self.source}")
        else:
            print(f"> {self.target} <= {self.source}")