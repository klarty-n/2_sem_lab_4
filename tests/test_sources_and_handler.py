import pytest

from src.handler import get_all_tasks, hendler_task_source
from src.protocol import TaskSource
from src.source import ApiTaskSource, GeneratorTaskSource
from src.task import Task


def test_generator_negative_count_raises():
    with pytest.raises(ValueError):
        GeneratorTaskSource(-1)


def test_api_source_returns_task_objects():
    source = ApiTaskSource()
    tasks = source.get_tasks()

    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)
    assert tasks[0].id == 13
    assert tasks[1].status == "in_progress"


def test_handler_rejects_non_protocol_source():
    with pytest.raises(TypeError):
        hendler_task_source(object())


def test_get_all_tasks_with_mixed_sources():
    sources = [GeneratorTaskSource(2), ApiTaskSource()]
    all_tasks = get_all_tasks(sources)

    assert len(all_tasks) == 4
    assert [t.id for t in all_tasks] == [0, 1, 13, 14]


def test_protocol_runtime_check():
    class Source:
        def get_tasks(self):
            return [Task(task_id=99, payload="ok")]

    src = Source()
    assert isinstance(src, TaskSource)
