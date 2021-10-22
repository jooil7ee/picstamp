# -*- coding: utf-8 -*-
import argparse
import logging.config
import os.path
import sys

import yaml

from pixrenamer.pixrenamer import PixRenamer

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
            description='Rename media files using timestamp information')
    parser.add_argument('-t', '--tag', required=True,
            dest="arg_tag", choices=TAGS, default=None,
            help="tag for type of input files")
    parser.add_argument('-u', '--uppercase', required=False,
            dest="arg_uppercase", default=False, action="store_true",
            help="use uppercase names")
    parser.add_argument('-a', '--apply', required=False,
            dest="arg_apply", default=False, action="store_true",
            help="apply changes or just show plan")
    parser.add_argument('-i', '--in_dir', metavar="INPUT_DIR", nargs="?",
            default="in",
            help="directory path which contains image and video files.")

    args = parser.parse_args()

    # Set logger
    if os.path.exists("resources/logging.conf"):
        with open("resources/logging.conf", "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger("pixrenamer")
    logger.info("<< Start Pixrenamer >>")

    # Run picstamping job
    renamer = PixRenamer(args.arg_tag)
    renamer.set_options(uppercase=args.arg_uppercase, apply=args.arg_apply)
    renamer.run(args.in_dir)

    sys.exit(0)