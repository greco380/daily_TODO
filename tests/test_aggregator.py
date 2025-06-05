from daily_todo.aggregator import aggregate


def test_merge_and_deduplicate():
    data = [
        [
            {"id": "1", "title": "Task A", "due": "2021-01-01", "source": "trello"},
            {"id": "2", "title": "Task B", "due": "2021-01-02", "source": "trello"},
        ],
        [
            {"id": "1", "title": "Task A", "due": "2021-01-01", "source": "trello"},
        ],
        [
            {"id": "3", "title": "Task A", "due": "2021-01-01", "source": "asana"},
        ],
    ]
    result = aggregate(data)
    assert len(result) == 2
    # result sorted by due so first item is Task A
    assert result[0]["title"] == "Task A"
    assert sorted(result[0]["source"] if isinstance(result[0]["source"], list) else [result[0]["source"]]) == ["asana", "trello"]

