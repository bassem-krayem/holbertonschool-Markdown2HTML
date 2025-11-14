#!/usr/bin/python3
"""
this script is to convert the markdown syntax to html syntax
"""

import sys
import os


def convertHeadings(line):
    headingLevel = line.count("#")
    if 1 <= headingLevel <= 6:
        return f"<h{headingLevel}>{line[headingLevel:].strip()}</h{headingLevel}>"
    return line


def convert_unordered_list(markdown_list):
    html_list = ["<ul>"]
    for list_item in markdown_list:
        html_list.append(f"<li>{list_item[1:].strip()}</li>")
    html_list.append("</ul>")
    return html_list


def convert_ordered_list(markdown_list):
    html_list = ["<ol>"]
    for list_item in markdown_list:
        html_list.append(f"<li>{list_item[1:].strip()}</li>")
    html_list.append("</ol>")
    return html_list


def flush_list(html_lines, list_lines, list_type):
    """Flush the collected list_lines into html_lines depending on list_type."""
    if not list_lines:
        return
    if list_type == "ul":
        html_lines.extend(convert_unordered_list(list_lines))
    elif list_type == "ol":
        html_lines.extend(convert_ordered_list(list_lines))


def flush_paragraph(html_lines, paragraph_lines):
    """Flush paragraph_lines into html_lines using <p> and <br /> between lines."""
    if not paragraph_lines:
        return
    html_lines.append("<p>")
    for i, l in enumerate(paragraph_lines):
        if i > 0:
            html_lines.append("<br />")
        html_lines.append(l)
    html_lines.append("</p>")


def mainFunction(fileName, outputFileName):
    html_lines = []
    list_lines = []
    list_type = None  # "ul", "ol", or None
    paragraph_lines = []
    in_paragraph = False
    in_list = False

    with open(fileName, "r") as file:
        for raw in file:
            line = raw.rstrip("\n")       # keep internal spaces, remove trailing newline
            s = line.strip()              # stripped content for checks

            # blank line -> close paragraph and lists
            if s == "":
                if in_paragraph:
                    flush_paragraph(html_lines, paragraph_lines)
                    paragraph_lines = []
                    in_paragraph = False
                if in_list:
                    flush_list(html_lines, list_lines, list_type)
                    list_lines = []
                    list_type = None
                    in_list = False
                continue

            # list item detection
            if s.startswith("-") or s.startswith("*"):
                marker = s[0]
                # if currently in a paragraph, close it before starting a list
                if in_paragraph:
                    flush_paragraph(html_lines, paragraph_lines)
                    paragraph_lines = []
                    in_paragraph = False

                # starting a new list or continuing same type
                if not in_list:
                    in_list = True
                    list_type = "ul" if marker == "-" else "ol"
                    list_lines = []
                else:
                    # list type changed: flush previous then start new
                    if (marker == "-" and list_type != "ul") or (marker == "*" and list_type != "ol"):
                        flush_list(html_lines, list_lines, list_type)
                        list_lines = []
                        list_type = "ul" if marker == "-" else "ol"

                list_lines.append(s)
                continue

            # heading detection
            if s.startswith("#"):
                # close any open list or paragraph first
                if in_paragraph:
                    flush_paragraph(html_lines, paragraph_lines)
                    paragraph_lines = []
                    in_paragraph = False
                if in_list:
                    flush_list(html_lines, list_lines, list_type)
                    list_lines = []
                    list_type = None
                    in_list = False

                html_lines.append(convertHeadings(s))
                continue

            # normal paragraph text
            # close any open list first
            if in_list:
                flush_list(html_lines, list_lines, list_type)
                list_lines = []
                list_type = None
                in_list = False

            paragraph_lines.append(s)
            in_paragraph = True

        # end of file: flush any open blocks
        if in_paragraph:
            flush_paragraph(html_lines, paragraph_lines)
        if in_list:
            flush_list(html_lines, list_lines, list_type)

    with open(outputFileName, "w") as file:
        file.write("\n".join(html_lines))


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
        mainFunction(fileName, outputFileName)
