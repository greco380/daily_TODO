from __future__ import annotations

import datetime as dt
from typing import List, Dict

import requests


ASANA_API_BASE = "https://app.asana.com/api/1.0"


def get_tasks_due_today(access_token: str) -> List[Dict]:
    """Retrieve Asana tasks assigned to the user due today."""
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    today = dt.date.today().isoformat()
    url = f"{ASANA_API_BASE}/tasks"
    params = {
        "assignee": "me",
        "completed_since": "now",
        "opt_fields": "name,due_on",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    items = response.json().get("data", [])
    tasks = []
    for item in items:
        due = item.get("due_on")
        if due == today:
            tasks.append(
                {
                    "source": "asana",
                    "id": item.get("gid"),
                    "title": item.get("name"),
                    "due": due,
                    "type": "task",
                }
            )
    return tasks
