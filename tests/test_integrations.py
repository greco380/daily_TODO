import sys
import datetime as dt
from types import SimpleNamespace

import pytest

# Provide minimal stubs for google modules so imports succeed without the
# real dependencies installed.
sys.modules['google'] = SimpleNamespace()

class DummyCreds:
    @classmethod
    def from_service_account_file(cls, path, scopes=None):
        return cls()

sys.modules['google.oauth2'] = SimpleNamespace(service_account=SimpleNamespace(Credentials=DummyCreds))
sys.modules['google.oauth2.service_account'] = SimpleNamespace(Credentials=DummyCreds)
sys.modules['googleapiclient'] = SimpleNamespace()
sys.modules['googleapiclient.discovery'] = SimpleNamespace(build=lambda *a, **k: None)
sys.modules['requests'] = SimpleNamespace(get=lambda *a, **k: None)

from daily_todo.integrations import google_calendar, trello, asana


class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data

    def raise_for_status(self):
        pass

    def json(self):
        return self._json


def test_trello(monkeypatch):
    expected = [{
        'id': '1', 'name': 'card', 'due': dt.date.today().isoformat()
    }]

    def fake_get(url, params=None, timeout=None):
        return DummyResponse(expected)

    monkeypatch.setattr(trello.requests, 'get', fake_get, raising=False)

    tasks = trello.get_tasks_due_today('key', 'token')
    assert tasks[0]['title'] == 'card'


def test_asana(monkeypatch):
    expected = {
        'data': [
            {'gid': '1', 'name': 'task', 'due_on': dt.date.today().isoformat()}
        ]
    }

    def fake_get(url, headers=None, params=None, timeout=None):
        return DummyResponse(expected)

    monkeypatch.setattr(asana.requests, 'get', fake_get, raising=False)

    tasks = asana.get_tasks_due_today('token')
    assert tasks[0]['title'] == 'task'


def test_google_calendar(monkeypatch):
    events = [{
        'id': '1', 'summary': 'meet',
        'start': {'dateTime': '2023-01-01T00:00:00Z'}
    }]

    class DummyEvents:
        def list(self, **kwargs):
            return self

        def execute(self):
            return {'items': events}

    class DummyService:
        def events(self):
            return DummyEvents()

    def fake_build(*args, **kwargs):
        return DummyService()

    def fake_creds(path, scopes=None):
        return object()

    monkeypatch.setattr(google_calendar, 'build', fake_build, raising=False)
    monkeypatch.setattr(google_calendar.Credentials, 'from_service_account_file', fake_creds, raising=False)

    result = google_calendar.get_today_events('creds.json')
    assert result[0]['title'] == 'meet'
