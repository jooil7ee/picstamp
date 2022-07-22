#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging.config
import os.path
import sys

import yaml

from pixsort.pixsort import PixSorter


# ===========================================================
#  SYMBOLIC CONSTANTS
# ===========================================================
TAGS = (
    "img",  # High quality image file
    "isr",  # Low or Medium quality image file
    "mov",  # High quality video file
    "msr",  # Low or medium quality video file
)


# ===========================================================
#  GLOBAL VARIABLES
# ===========================================================
logger = None


# ===========================================================
#  MAIN FUNCTION
# ===========================================================
if __name__ == "__main__":

    # Parse command-line
    parser = argparse.ArgumentParser(
            prog="python3 main.py",
            description="Rename media files using timestamp information for sorting them")

    parser.add_argument('-i', '--in', metavar="IN_DIR", required=True,
            help="directory path which contains media files.")
    parser.add_argument('-o', '--out', metavar="OUT_DIR", nargs="?", default="done",
            help="directory path for saving renamed media files.")
    parser.add_argument('-u', '--uppercase', required=False,
            dest="arg_uppercase", default=False, action="store_true",
            help="use uppercase name")
    parser.add_argument('-a', '--apply', required=False,
            dest="arg_apply", default=False, action="store_true",
            help="apply changes or just show plan")

    args = parser.parse_args()

    print(args)

    # Set logger
    if os.path.exists("resources/logging.conf"):
        with open("resources/logging.conf", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("pixsort")
    logger.info("<< Start Pixsort >>")

    # Run pixsort job
    sorter = PixSorter()
    sorter.set_options(uppercase=args.arg_uppercase, apply=args.arg_apply)
    sorter.run(args.in_dir)

    sys.exit(0)
