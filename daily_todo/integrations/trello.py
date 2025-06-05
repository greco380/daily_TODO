from __future__ import annotations

import datetime as dt
from typing import List, Dict

import requests


TRELLO_API_BASE = "https://api.trello.com/1"


def get_tasks_due_today(api_key: str, token: str) -> List[Dict]:
    """Retrieve Trello cards due today."""
    today = dt.date.today().isoformat()
    url = f"{TRELLO_API_BASE}/members/me/cards"
    params = {
        "key": api_key,
        "token": token,
        "due": "day",
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    cards = response.json()
    tasks = []
    for card in cards:
        due = card.get("due")
        if due and due.startswith(today):
            tasks.append(
                {
                    "source": "trello",
                    "id": card.get("id"),
                    "title": card.get("name"),
                    "due": due,
                    "type": "task",
                }
            )
    return tasks
