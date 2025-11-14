#!/usr/bin/python3
"""
Convert Markdown syntax to HTML.
"""

import sys
import os
import re
import hashlib


def apply_inline_formatting(text):
    """Apply bold, emphasis, md5, and remove-c rules."""

    # Bold: **text**
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Emphasis: __text__
    text = re.sub(r"__(.*?)__", r"<em>\1</em>", text)

    # MD5: [[text]]
    def md5_replace(match):
        content = match.group(1)
        return hashlib.md5(content.encode()).hexdigest()

    text = re.sub(r"\[\[(.*?)\]\]", md5_replace, text)

    # Remove letter c/C: ((text))
    def remove_c(match):
        content = match.group(1)
        return re.sub(r"[cC]", "", content)

    text = re.sub(r"\(\((.*?)\)\)", remove_c, text)

    return text


def convert_headings(line):
    heading_level = line.count("#")
    if 1 <= heading_level <= 6:
        content = apply_inline_formatting(
            line[heading_level:].strip()
        )
        return f"<h{heading_level}>{content}</h{heading_level}>"
    return None


def convert_unordered_list(md_list):
    html_list = ["<ul>"]
    for item in md_list:
        content = apply_inline_formatting(item[1:].strip())
        html_list.append(f"<li>{content}</li>")
    html_list.append("</ul>")
    return html_list


def convert_ordered_list(md_list):
    html_list = ["<ol>"]
    for item in md_list:
        content = apply_inline_formatting(item[1:].strip())
        html_list.append(f"<li>{content}</li>")
    html_list.append("</ol>")
    return html_list


def convert_paragraph(lines):
    text = " ".join(lines)
    text = apply_inline_formatting(text)
    return f"<p>{text}</p>"


def main_function(md_file, html_file):
    html_lines = []
    list_lines = []
    in_list = False

    paragraph = []

    with open(md_file, "r") as file:
        for line in file:
            stripped = line.strip()

            # empty line ends paragraph
            if stripped == "":
                if paragraph:
                    html_lines.append(convert_paragraph(paragraph))
                    paragraph = []
                continue

            # Headings
            if stripped.startswith("#"):
                if paragraph:
                    html_lines.append(convert_paragraph(paragraph))
                    paragraph = []

                heading_html = convert_headings(stripped)
                html_lines.append(heading_html)
                continue

            # Unordered list
            if stripped.startswith('-'):
                if paragraph:
                    html_lines.append(convert_paragraph(paragraph))
                    paragraph = []

                list_lines.append(stripped)
                in_list = True
                current_list_type = "ul"
                continue

            # Ordered list
            if stripped.startswith('*'):
                if paragraph:
                    html_lines.append(convert_paragraph(paragraph))
                    paragraph = []

                list_lines.append(stripped)
                in_list = True
                current_list_type = "ol"
                continue

            # End of list
            if in_list and not (stripped.startswith('-')
                                or stripped.startswith('*')):
                if current_list_type == "ul":
                    html_lines.extend(convert_unordered_list(list_lines))
                else:
                    html_lines.extend(convert_ordered_list(list_lines))

                list_lines = []
                in_list = False

            # Normal text → paragraph
            paragraph.append(stripped)

        # End of file cleanup
        if paragraph:
            html_lines.append(convert_paragraph(paragraph))

        if in_list:
            if current_list_type == "ul":
                html_lines.extend(convert_unordered_list(list_lines))
            else:
                html_lines.extend(convert_ordered_list(list_lines))

    with open(html_file, "w") as file:
        file.write("\n".join(html_lines))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr,
        )
        sys.exit(1)

    md = sys.argv[1]
    html = sys.argv[2]

    if not os.path.isfile(md):
        print("Missing " + md, file=sys.stderr)
        sys.exit(1)

    main_function(md, html)
