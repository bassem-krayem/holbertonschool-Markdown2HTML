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
        return line


def convert_unordered_list(marcdown_list):
    html_list = ["<ul>"]
    for list_item in marcdown_list:
        html_list.append(f"<li>{list_item[1:].strip()}</li>")
    html_list.append("</ul>")
    return html_list


def mainFunction(fileName, outputFileName):
    html_lines = []
    markdown_list_lines = []

    with open(fileName, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                html_lines.append(convertHeadings(line))
            elif line.startswith("-"):
                markdown_list_lines.append(line)

    html_lines.extend(convert_unordered_list(markdown_list_lines))

    with open(outputFileName, "w") as file:
        file.write("\n".join(html_lines))


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
