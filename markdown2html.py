#!/usr/bin/python3
"""
this script is to convert the marcdown syntax to html syntax
"""

import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("STDERR Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    fileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if not fileName:
        print("STDER Missing <filename>")
        sys.exit(1)
    else:
        print("nothing")
        sys.exit(0)
