from src.source import GeneratorTaskSource
from src.protocol import TaskSource
from src.task import Task
from src.handler import hendler_task_source, get_all_tasks

def test_generator_source_creation():
    """Тест источника задач, который генерирует их"""
    source = GeneratorTaskSource(5)
    assert source.count == 5

def test_get_tasks():
    """Тест на получения задач из генератора"""

    count = 13
    source = GeneratorTaskSource(count)
    tasks = source.get_tasks()

    assert len(tasks) == count
    assert all(isinstance(task, Task) for task in tasks)

    for task_id in range(count):
        assert tasks[task_id].id == task_id
        assert tasks[task_id].payload == f"Сгенерированный таск с id {task_id}"


def test_handler_task_source():
    """Тест обработки источника задач"""
    source = GeneratorTaskSource(13)
    tasks = hendler_task_source(source)

    assert len(tasks) == 13
    assert isinstance(tasks[0], Task)
    assert tasks[0].id == 0
    assert tasks[0].payload == "Сгенерированный таск с id 0"

def test_get_all_tasks():
    """Тест получения тасков из всех источников"""
    sources = [GeneratorTaskSource(2), GeneratorTaskSource(3)]
    all_tasks = get_all_tasks(sources)

    assert len(all_tasks) == 5
    assert all(isinstance(task, Task) for task in all_tasks)

    expected = [0, 1, 0, 1, 2]
    real = [task.id for task in all_tasks]
    assert real == expected


def test_protocol_compliance():
    """Тест соответствия протоколу"""
    source = GeneratorTaskSource(1)
    assert isinstance(source, TaskSource)


def test_empty_source():
    """Тест пустого источника"""
    source = GeneratorTaskSource(0)
    tasks = source.get_tasks()

    assert len(tasks) == 0
