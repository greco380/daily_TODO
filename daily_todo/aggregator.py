from __future__ import annotations

from typing import Iterable, List, Dict, Set


def aggregate(items: Iterable[Iterable[Dict]]) -> List[Dict]:
    """Merge lists of tasks/events into a single list.

    The function keeps track of IDs seen per source so duplicate records from
    the same provider are ignored.  Items that share the same title and due date
    across different sources are merged and their sources combined for
    traceability.  The returned list is sorted by the ``due`` field when
    available.
    """

    merged: List[Dict] = []
    seen_ids: Dict[str, Set[str]] = {}

    for collection in items:
        for item in collection:
            source = item.get("source")
            item_id = item.get("id")

            if source and item_id:
                ids = seen_ids.setdefault(source, set())
                if item_id in ids:
                    # Skip exact duplicates from the same source
                    continue
                ids.add(item_id)

            title = item.get("title")
            due = item.get("due")

            existing = None
            for current in merged:
                if current.get("title") == title and current.get("due") == due:
                    existing = current
                    break

            if existing is not None:
                if source:
                    existing_source = existing.get("source")
                    if existing_source is None:
                        existing["source"] = source
                    elif isinstance(existing_source, list):
                        if source not in existing_source:
                            existing_source.append(source)
                    elif existing_source != source:
                        existing["source"] = [existing_source, source]
                continue

            merged.append(dict(item))

    merged.sort(key=lambda x: x.get("due") or "")
    return merged
