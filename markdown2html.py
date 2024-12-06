#!/usr/bin/python3
"""
this script is to convert the marcdown syntax to html syntax
"""

import sys
import os


def convertHeadings(line):
    headingLevel = line.count("#")

    if headingLevel >= 1 and headingLevel <= 6:
        return (f"<h{headingLevel}>"
                f"{line[headingLevel:].strip()}</h{headingLevel}>")
    else:
        return line  # Return the line unchanged if it's not a heading


def mainFunction(fileName, outputFileName):
    htmlList = []

    with open(fileName, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                htmlList.append(convertHeadings(line))

    with open(outputFileName, "w") as file:
        file.write("\n".join(htmlList))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    fileName = sys.argv[1]
    outputFileName = sys.argv[2]

    if not os.path.isfile(fileName):
        print("Missing " + fileName, file=sys.stderr)
        sys.exit(1)
    else:
        mainFunction(fileName, outputFileName)
