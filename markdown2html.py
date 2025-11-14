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


def convert_ordered_list(marcdown_list):
    html_list = ["<ol>"]
    for list_item in marcdown_list:
        html_list.append(f"<li>{list_item[1:].strip()}</li>")
    html_list.append("</ol>")
    return html_list


def mainFunction(fileName, outputFileName):
    html_lines = []
    markdown_list_lines = []
    in_list = False

    with open(fileName, "r") as file:
        for line in file:
            line = line.strip()
            # headings
            if line.startswith("#"):
                html_lines.append(convertHeadings(line))

            # unordered lists
            if line.startswith('-'):
                markdown_list_lines.append(line)
                in_list = True

            if in_list and not line.startswith('-'):
                html_lines.extend(convert_unordered_list(markdown_list_lines))
                markdown_list_lines = []
                in_list = False

            # ordered lists
            if line.startswith('*'):
                markdown_list_lines.append(line)
                in_list = True
            if in_list and not line.startswith('*'):
                html_lines.extend(convert_ordered_list(markdown_list_lines))
                markdown_list_lines = []
                in_list = False

        # outside the loop
        if in_list:
            if markdown_list_lines[0].startswith('-'):
                html_lines.extend(convert_unordered_list(markdown_list_lines))
            elif markdown_list_lines[0].startswith('*'):
                html_lines.extend(convert_ordered_list(markdown_list_lines))

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
