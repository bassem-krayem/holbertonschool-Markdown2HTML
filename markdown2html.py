#!/usr/bin/python3
"""
This script converts Markdown syntax to HTML syntax.
"""

import sys
import os


def convertHeadings(line):
    heading_level = line.count("#")
    if 1 <= heading_level <= 6:
        content = line[heading_level:].strip()
        return (
            f"<h{heading_level}>"
            f"{content}"
            f"</h{heading_level}>"
        )
    return line


def convert_unordered_list(markdown_list):
    html_list = ["<ul>"]
    for item in markdown_list:
        html_list.append(
            f"<li>{item[1:].strip()}</li>"
        )
    html_list.append("</ul>")
    return html_list


def convert_ordered_list(markdown_list):
    html_list = ["<ol>"]
    for item in markdown_list:
        html_list.append(
            f"<li>{item[1:].strip()}</li>"
        )
    html_list.append("</ol>")
    return html_list


def flush_list(html_lines, list_lines, list_type):
    """Flush collected list lines into HTML."""
    if not list_lines:
        return
    if list_type == "ul":
        html_lines.extend(
            convert_unordered_list(list_lines)
        )
    elif list_type == "ol":
        html_lines.extend(
            convert_ordered_list(list_lines)
        )


def flush_paragraph(html_lines, para_lines):
    """Flush paragraph lines into HTML with <br />."""
    if not para_lines:
        return

    html_lines.append("<p>")
    for i, line in enumerate(para_lines):
        if i > 0:
            html_lines.append("<br />")
        html_lines.append(line)
    html_lines.append("</p>")


def mainFunction(file_name, output_name):
    html_lines = []
    list_lines = []
    list_type = None

    para_lines = []
    in_paragraph = False
    in_list = False

    with open(file_name, "r") as file:
        for raw in file:
            line = raw.rstrip("\n")
            stripped = line.strip()

            # Blank line → close blocks
            if stripped == "":
                if in_paragraph:
                    flush_paragraph(html_lines, para_lines)
                    para_lines = []
                    in_paragraph = False

                if in_list:
                    flush_list(html_lines, list_lines, list_type)
                    list_lines = []
                    list_type = None
                    in_list = False
                continue

            # List items
            if stripped.startswith("-") or stripped.startswith("*"):
                marker = stripped[0]

                if in_paragraph:
                    flush_paragraph(html_lines, para_lines)
                    para_lines = []
                    in_paragraph = False

                if not in_list:
                    in_list = True
                    list_type = (
                        "ul" if marker == "-" else "ol"
                    )
                    list_lines = []
                else:
                    # Switch list type
                    if (
                        marker == "-" and list_type != "ul"
                    ) or (
                        marker == "*" and list_type != "ol"
                    ):
                        flush_list(
                            html_lines, list_lines, list_type
                        )
                        list_lines = []
                        list_type = (
                            "ul" if marker == "-" else "ol"
                        )

                list_lines.append(stripped)
                continue

            # Headings
            if stripped.startswith("#"):
                if in_paragraph:
                    flush_paragraph(html_lines, para_lines)
                    para_lines = []
                    in_paragraph = False

                if in_list:
                    flush_list(html_lines, list_lines, list_type)
                    list_lines = []
                    list_type = None
                    in_list = False

                html_lines.append(
                    convertHeadings(stripped)
                )
                continue

            # Normal paragraph text
            if in_list:
                flush_list(html_lines, list_lines, list_type)
                list_lines = []
                list_type = None
                in_list = False

            para_lines.append(stripped)
            in_paragraph = True

        # End of file: flush remaining
        if in_paragraph:
            flush_paragraph(html_lines, para_lines)

        if in_list:
            flush_list(html_lines, list_lines, list_type)

    with open(output_name, "w") as file:
        file.write("\n".join(html_lines))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
        )
        sys.exit(1)

    file_name = sys.argv[1]
    output_name = sys.argv[2]

    if not os.path.isfile(file_name):
        print(
            "Missing " + file_name,
            file=sys.stderr
        )
        sys.exit(1)

    mainFunction(file_name, output_name)
