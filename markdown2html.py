#!/usr/bin/python3
"""
this script is to convert the marcdown syntax to html syntax
"""

import sys
import os
import re
import hashlib


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
    paragraph_lines = []
    in_un = False
    in_or = False
    in_paragraph = False

    with open(fileName, "r") as file:
        for line in file:
            line = line.strip()

            # Hash
            match = re.search(r"\[\[(.*?)\]\]", line)
            if match:
                hash_object = hashlib.md5(match.group(1).encode()).hexdigest()
                line = re.sub(r"(\[\[.*?\]\])", hash_object, line)

            match = re.search(r"\(\((.*?)\)\)", line)
            if match:
                remove_C_and_c = (
                    match.group(1).replace('C', '').replace('c', '')
                )
                line = re.sub(r"(\(\(.*?\)\))", remove_C_and_c, line)
            # Bold
            if re.search(r"\*\*.*?\*\*", line):
                line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)

            # emphasis text
            if re.search(r"__.*?__", line):
                line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)

            # headings
            if line.startswith("#"):
                html_lines.append(convertHeadings(line))

            # unordered lists
            if line.startswith('-'):
                markdown_list_lines.append(line)
                in_un = True

            if in_un and not line.startswith('-'):
                html_lines.extend(convert_unordered_list(markdown_list_lines))
                markdown_list_lines = []
                in_un = False

            # ordered lists
            if line.startswith('*'):
                markdown_list_lines.append(line)
                in_or = True
            if in_or and not line.startswith('*'):
                html_lines.extend(convert_ordered_list(markdown_list_lines))
                markdown_list_lines = []
                in_or = False

            # paragraphs
            if re.match(r'^[A-Za-z0-9<]', line):
                paragraph_lines.append(line)
                in_paragraph = True
            if in_paragraph and not re.match(r'^[A-Za-z0-9]', line):
                for p_line in range(len(paragraph_lines) - 1):
                    paragraph_lines[p_line] += '<br/>'
                html_lines.append(f"<p>{''.join(paragraph_lines)}</p>")
                paragraph_lines = []
                in_paragraph = False

        # outside the loop
        if in_un or in_or:
            if in_un:
                html_lines.extend(convert_unordered_list(markdown_list_lines))
            if in_or:
                html_lines.extend(convert_ordered_list(markdown_list_lines))
        if in_paragraph:
            for p_line in range(len(paragraph_lines) - 1):
                paragraph_lines[p_line] += '<br/>'
            html_lines.append(f"<p>{''.join(paragraph_lines)}</p>")
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
