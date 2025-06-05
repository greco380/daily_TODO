import pytest

from daily_todo.aggregator import aggregate


def test_aggregate_sorting():
    item1 = {'title': 'First', 'due': '2023-01-02'}
    item2 = {'title': 'Second', 'due': '2023-01-01'}
    result = aggregate([[item1], [item2]])
    assert result == [item2, item1]
