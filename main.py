#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging.config
import os.path
import sys
import yaml

from pixsort.common import *
from pixsort.pixsort import PixSorter


# ===========================================================
#  SYMBOLIC CONSTANTS
# ===========================================================
HELP = "Rename pix(image and video) files using timestamp information for sorting them. Timestamp can be extracted from: file name, exif (if present) or file stat."


# ===========================================================
#  GLOBAL VARIABLES
# ===========================================================
logger = None


# ===========================================================
#  MAIN FUNCTION
# ===========================================================
if __name__ == "__main__":

    # Parse command-line
    parser = argparse.ArgumentParser(prog="python3 main.py", description=HELP)

    parser.add_argument('-i', '--in', metavar="IN_DIR", required=True,
            dest="arg_in_dir", help="directory path which contains pix files.")
    parser.add_argument('-o', '--out', metavar="OUT_DIR", nargs="?", default="done",
            dest="arg_out_dir", help="directory path for saving renamed pix files.")
    parser.add_argument('-r', '--recursive', required=False,
            dest="arg_recursive", default=False, action="store_true",
            help="recursively traverse sub-directories")
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

    logger = logging.getLogger(ENV)
    logger.info("<< Start Pixsort >>")

    # Run pixsort job
    sorter = PixSorter()
    sorter.set_options(out_dir=args.arg_out_dir, recursive=args.arg_recursive,
                       uppercase=args.arg_uppercase, apply=args.arg_apply)

    sorter.run(args.arg_in_dir)

    sys.exit(0)
