from daily_todo.email_formatter import highlight_keywords, format_email


def test_highlight_keywords():
    text = 'urgent meeting today'
    assert highlight_keywords(text) == '**urgent** **meeting** **today**'


def test_format_email():
    summary = 'An urgent task'
    items = [
        {'title': 'Task', 'due': '2023-01-01'}
    ]
    body = format_email(summary, items)
    assert 'Task (2023-01-01)' in body
    assert '**urgent**' in body
