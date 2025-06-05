from __future__ import annotations

from typing import Iterable, List, Dict


def aggregate(items: Iterable[Iterable[Dict]]) -> List[Dict]:
    """Merge lists of tasks/events into a single list."""
    merged = []
    for collection in items:
        merged.extend(collection)
    # sort by due date/time if available
    merged.sort(key=lambda x: x.get("due") or "")
    return merged
