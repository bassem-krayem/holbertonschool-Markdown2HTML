#!/usr/bin/python3
"""
this script is to convert the marcdown syntax to html syntax
"""

import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    fileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if not os.path.isfile(fileName):
        print("Missing " + fileName, file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)
