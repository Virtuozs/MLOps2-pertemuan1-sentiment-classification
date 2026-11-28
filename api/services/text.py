"""Builds the model input exactly as in training (notebook Section 3 and 12.3)."""

import re

# A title that only restates the rating, such as "Five Stars" or "4.0 out of 5 stars".
DEFAULT_TITLE = (
    r"^\s*(?:([1-5])(?:\.0)?\s*(?:out of 5\s*)?stars?"
    r"|(one|two|three|four|five)\s*stars?)\s*[.!]*\s*$"
)
_DEFAULT_TITLE_RE = re.compile(DEFAULT_TITLE, flags=re.IGNORECASE)


def build_input(title: str, text: str) -> str:
    """Join title and text with ' . ', blanking a star-only title first."""
    if _DEFAULT_TITLE_RE.match(title):
        title = ""
    return title + " . " + text
