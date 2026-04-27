import pytest
from src.task import Task
from src.queue import TaskQueue

def test_create_empty_queue():
    queue = TaskQueue()
    assert len(queue) == 0
    assert queue.is_empty() is True


def test_create_queue_with_tasks():
    tasks = [
        Task(task_id=1, payload="task1", priority=2, status="not_started"),
        Task(task_id=2, payload="task2", priority=4, status="in_progress"),
        Task(task_id=3, payload="task3", priority=1, status="completed"),
    ]
    queue = TaskQueue(tasks)
    assert len(queue) == 3
    assert queue.is_empty() is False


def test_add_task():
    queue = TaskQueue()
    task = Task(task_id=1, payload="test")
    queue.add(task)
    assert len(queue) == 1
    assert queue[0] == task


def test_add_multiple_tasks():
    queue = TaskQueue()
    tasks = [Task(task_id=i, payload=f"task{i}") for i in range(13)]
    for task in tasks:
        queue.add(task)
    assert len(queue) == 13

def test_iteration():
    tasks = [
        Task(task_id=1, payload="task1"),
        Task(task_id=2, payload="task2"),
        Task(task_id=3, payload="task3"),
    ]
    queue = TaskQueue(tasks)
    
    collected = []
    for task in queue:
        collected.append(task)
    
    assert len(collected) == 3
    assert collected == tasks


def test_iteration_with_list():
    tasks = [
        Task(task_id=1, payload="task1"),
        Task(task_id=2, payload="task2"),
    ]
    queue = TaskQueue(tasks)
    result = list(queue)
    assert result == tasks


def test_multiple_iterations():
    tasks = [
        Task(task_id=1, payload="task1"),
        Task(task_id=2, payload="task2"),
    ]
    queue = TaskQueue(tasks)
    
    first_pass = list(queue)
    second_pass = list(queue)
    third_pass = list(queue)
    
    assert first_pass == tasks
    assert second_pass == tasks
    assert third_pass == tasks


def test_iteration_empty_queue():
    queue = TaskQueue()
    collected = list(queue)
    assert collected == []


def test_iterator_exhaustion():
    tasks = [Task(task_id=1, payload="task1")]
    queue = TaskQueue(tasks)
    
    iterator = iter(queue)
    assert next(iterator).id == 1
    
    with pytest.raises(StopIteration):
        next(iterator)


def test_iterator_returns_new_instance():
    queue = TaskQueue([Task(task_id=1, payload="task1")])
    
    iter1 = iter(queue)
    iter2 = iter(queue)
    
    assert iter1 is not iter2

def test_filter_by_status():
    tasks = [
        Task(task_id=1, payload="task1", status="not_started"),
        Task(task_id=2, payload="task2", status="in_progress"),
        Task(task_id=3, payload="task3", status="not_started"),
        Task(task_id=4, payload="task4", status="completed"),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.filter_by_status("not_started"))
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_by_status_no_matches():
    tasks = [
        Task(task_id=1, payload="task1", status="completed"),
        Task(task_id=2, payload="task2", status="failed"),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.filter_by_status("not_started"))
    assert len(result) == 0


def test_filter_by_status_empty_queue():
    queue = TaskQueue()
    result = list(queue.filter_by_status("not_started"))
    assert result == []


def test_filter_by_status_is_lazy():
    tasks = [Task(task_id=1, payload="task1", status="not_started")]
    queue = TaskQueue(tasks)
    
    result = queue.filter_by_status("not_started")
    # Проверяем что это генератор, а не список
    assert hasattr(result, "__next__")
    assert hasattr(result, "__iter__")


def test_filter_by_priority():
    tasks = [
        Task(task_id=1, payload="task1", priority=2),
        Task(task_id=2, payload="task2", priority=5),
        Task(task_id=3, payload="task3", priority=2),
        Task(task_id=4, payload="task4", priority=1),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.filter_by_priority(2))
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 3


def test_filter_by_priority_no_matches():
    tasks = [
        Task(task_id=1, payload="task1", priority=3),
        Task(task_id=2, payload="task2", priority=1),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.filter_by_priority(5))
    assert len(result) == 0


def test_filter_by_priority_is_lazy():
    queue = TaskQueue([Task(task_id=1, payload="task1", priority=3)])
    
    result = queue.filter_by_priority(3)
    assert hasattr(result, "__next__")


def test_get_tasks_higher_priority():
    """Тест генератора задач с высоким приоритетом"""
    tasks = [
        Task(task_id=1, payload="task1", priority=1),
        Task(task_id=2, payload="task2", priority=4),
        Task(task_id=3, payload="task3", priority=5),
        Task(task_id=4, payload="task4", priority=3),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.get_tasks_higher_priority(min_priority=4))
    assert len(result) == 2
    assert result[0].id == 2
    assert result[1].id == 3


def test_get_tasks_by_statuses():
    """Тест генератора задач по списку статусов"""
    tasks = [
        Task(task_id=1, payload="task1", status="not_started"),
        Task(task_id=2, payload="task2", status="in_progress"),
        Task(task_id=3, payload="task3", status="completed"),
        Task(task_id=4, payload="task4", status="failed"),
    ]
    queue = TaskQueue(tasks)
    
    result = list(queue.get_tasks_by_statuses(["not_started", "failed"]))
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 4

def test_remove_task_by_id():
    tasks = [
        Task(task_id=1, payload="task1"),
        Task(task_id=2, payload="task2"),
        Task(task_id=3, payload="task3"),
    ]
    queue = TaskQueue(tasks)
    
    result = queue.remove(2)
    assert result is True
    assert len(queue) == 2
    assert list(queue) == [tasks[0], tasks[2]]


def test_remove_nonexistent_task():
    queue = TaskQueue([Task(task_id=1, payload="task1")])
    result = queue.remove(999)
    assert result is False
    assert len(queue) == 1


def test_clear_queue():
    tasks = [Task(task_id=i, payload=f"task{i}") for i in range(5)]
    queue = TaskQueue(tasks)
    
    queue.clear()
    assert len(queue) == 0
    assert queue.is_empty() is True

def test_large_queue_iteration():
    """Тест итерации большого количества задач"""
    tasks = [Task(task_id=i, payload=f"task{i}", priority=(i % 5) + 1) for i in range(1300)]
    queue = TaskQueue(tasks)
    
    count = 0
    for task in queue:
        count += 1
    assert count == 1300


def test_large_queue_filtering():

    tasks = [Task(task_id=i, payload=f"task{i}", priority=(i % 5) + 1) for i in range(1000)]
    queue = TaskQueue(tasks)
    
    result = list(queue.filter_by_priority(3))
    # Приоритет 3 встречается у каждого 5-го элемента
    assert len(result) == 200


def test_large_queue_memory_efficiency():
    tasks = [Task(task_id=i, payload=f"task{i}", status="not_started") for i in range(1300)]
    queue = TaskQueue(tasks)
    
    # Генератор не создает копию списка
    filtered = queue.filter_by_status("not_started")
    # Проверяем что это итератор, а не список
    assert not isinstance(filtered, list)


def test_queue_repr():
    queue = TaskQueue([Task(task_id=1, payload="task1")])
    assert "TaskQueue(tasks=1)" in repr(queue)


def test_iteration_with_sum_compatibility():
    tasks = [
        Task(task_id=1, payload="task1", priority=2),
        Task(task_id=2, payload="task2", priority=3),
        Task(task_id=3, payload="task3", priority=5),
    ]
    queue = TaskQueue(tasks)
    
    total = sum(task.priority for task in queue)
    assert total == 10


def test_chained_filters():
    tasks = [
        Task(task_id=1, payload="task1", priority=4, status="not_started"),
        Task(task_id=2, payload="task2", priority=4, status="in_progress"),
        Task(task_id=3, payload="task3", priority=2, status="not_started"),
        Task(task_id=4, payload="task4", priority=5, status="not_started"),
    ]
    queue = TaskQueue(tasks)
    
    # Сначала фильтруем по статусу, потом по приоритету
    not_started = list(queue.filter_by_status("not_started"))
    high_priority_not_started = [t for t in not_started if t.priority >= 4]
    
    assert len(high_priority_not_started) == 2
    assert high_priority_not_started[0].id == 1
    assert high_priority_not_started[1].id == 4


def test_queue_with_all_statuses():
    tasks = [
        Task(task_id=1, payload="task1", status="not_started"),
        Task(task_id=2, payload="task2", status="in_progress"),
        Task(task_id=3, payload="task3", status="completed"),
        Task(task_id=4, payload="task4", status="failed"),
    ]
    queue = TaskQueue(tasks)
    
    for status in ["not_started", "in_progress", "completed", "failed"]:
        result = list(queue.filter_by_status(status))
        assert len(result) == 1