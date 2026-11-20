"""Tiny HTML scraping helpers."""

import re


def bold_texts(html):
    """Text inside every <b>...</b> pair, in document order."""
    return re.findall(r"<b>(.*)</b>", html)
