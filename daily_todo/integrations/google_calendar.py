from __future__ import annotations

import datetime as dt
from typing import List, Dict

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def get_today_events(credentials_path: str) -> List[Dict]:
    """Fetch today's events from Google Calendar."""
    creds = Credentials.from_service_account_file(credentials_path, scopes=[
        "https://www.googleapis.com/auth/calendar.readonly"
    ])
    service = build("calendar", "v3", credentials=creds)
    now = dt.datetime.now(dt.timezone.utc)
    start = dt.datetime.combine(now.date(), dt.time.min, tzinfo=dt.timezone.utc)
    end = start + dt.timedelta(days=1)
    events = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start.isoformat(),
            timeMax=end.isoformat(),
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
        .get("items", [])
    )
    results = []
    for e in events:
        results.append(
            {
                "source": "google_calendar",
                "id": e.get("id"),
                "title": e.get("summary"),
                "due": e.get("start", {}).get("dateTime", e.get("start", {}).get("date")),
                "type": "meeting",
            }
        )
    return results
