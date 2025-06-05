import sys
from types import SimpleNamespace

# Provide a minimal openai stub so the module can be imported without the
# actual dependency installed.
sys.modules['openai'] = SimpleNamespace(ChatCompletion=SimpleNamespace(create=None))

from daily_todo.llm import summarize


def test_summarize(monkeypatch):
    called = {}

    def fake_create(**kwargs):
        called['kwargs'] = kwargs
        return {
            'choices': [
                {'message': {'content': 'result summary'}}
            ]
        }

    monkeypatch.setattr('openai.ChatCompletion.create', fake_create)

    data = [
        {'title': 'Task1', 'due': '2023-01-01'},
        {'title': 'Task2', 'due': '2023-01-02'}
    ]

    result = summarize(data, api_key='key')

    assert result == 'result summary'
    assert called['kwargs']['model'] == 'gpt-3.5-turbo'
    assert any('Task1' in m['content'] for m in called['kwargs']['messages'])
