from __future__ import annotations

import re
from typing import List, Dict


KEYWORDS = {"deadline", "meeting", "urgent", "today"}


def highlight_keywords(text: str) -> str:
    pattern = re.compile(r"(\b" + "|".join(map(re.escape, KEYWORDS)) + r"\b)", re.I)
    return pattern.sub(lambda m: f"**{m.group(0)}**", text)


def format_email(summary: str, items: List[Dict]) -> str:
    body_lines = ["Today's Agenda:\n"]
    for item in items:
        body_lines.append(f"- {item['title']} ({item['due']})")
    body_lines.append("\nSummary:\n" + highlight_keywords(summary))
    return "\n".join(body_lines)
