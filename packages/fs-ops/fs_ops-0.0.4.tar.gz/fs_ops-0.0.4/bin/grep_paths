#! /usr/bin/python
import argparse
from pprint import pprint
from pathlib import Path

p = argparse.ArgumentParser(description="Grep paths.")
p.add_argument("folder",
               help="Folder to look into.")

p.add_argument("patterns",
               nargs="+",
               help="Patterns to match.")

args = p.parse_args()

try:
    d = Path(args.folder)
    for patt in args.patterns:
        for p in d.glob(patt):
            print(p)
except Exception as e:
    print(e)