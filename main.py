#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import logging.config
import os.path
import sys
import yaml

from app.common import ENV
from app.pixsort import PixSorter


# ===========================================================
#  SYMBOLIC CONSTANTS
# ===========================================================
HELP = "Rename pix(image and video) files using timestamp information for sorting them. \
Timestamp can be extracted from: file name, exif (if present) or file stat."


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
                        dest="in_dir",
                        help="directory path which contains pix files.")

    parser.add_argument('-r', '--recursive', required=False, default=False,
                        dest="recursive", action="store_true",
                        help="recursively traverse sub-directories")

    parser.add_argument('-u', '--uppercase', required=False, default=False,
                        dest="uppercase", action="store_true", help="rename to uppercase name")

    parser.add_argument('-w', '--workers', required=False, default=1, type=int,
                        dest="num_workers", help="number of renaming workers")

    parser.add_argument('-a', '--apply', required=False, default=False,
                        dest="apply", action="store_true",
                        help="launch renaming workers or just show plan")

    args = parser.parse_args()

    # Set logger
    if os.path.exists("resources/logging.conf"):
        with open("resources/logging.conf", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

            # create log directory if not exists
            log_dir = os.path.split(config['handlers']['logfile']['filename'])[0]

            if not os.path.exists(log_dir):
                os.mkdir(log_dir)

            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(ENV)
    logger.info(args)
    logger.info("<< Start Pixsort >>")

    # Run pixsort job
    sorter = PixSorter()
    sorter.set_options(recursive=args.recursive,
                       uppercase=args.uppercase,
                       num_workers=args.num_workers,
                       apply=args.apply)

    sorter.run(args.in_dir)

    sys.exit(0)
