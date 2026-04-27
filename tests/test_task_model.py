import pytest

from src.exceptions import IdError, PayloadError, PriorityError, StatusError, StatusTransitionError
from src.task import Task


def test_task_defaults():
    task = Task(task_id=1, payload="demo")

    assert task.id == 1
    assert task.payload == "demo"
    assert task.priority == 3
    assert task.status == "not_started"
    assert task.is_ready_for_start is True


def test_task_invalid_id_raises_error():
    with pytest.raises(IdError):
        Task(task_id=-1, payload="demo")


def test_task_invalid_priority_raises_error():
    with pytest.raises(PriorityError):
        Task(task_id=1, payload="demo", priority=10)


def test_task_invalid_status_raises_error():
    with pytest.raises(StatusError):
        Task(task_id=1, payload="demo", status="unknown")


def test_task_payload_none_raises_error():
    with pytest.raises(PayloadError):
        Task(task_id=1, payload=None)


def test_transition_valid_and_invalid():
    task = Task(task_id=2, payload="13", status="not_started")
    task.transition_to("in_progress")
    assert task.status == "in_progress"
    assert task.is_ready_for_start is False

    with pytest.raises(StatusTransitionError):
        task.transition_to("not_started")


def test_time_and_string_representations():
    task = Task(task_id=13, payload={"k": "v"})
    assert isinstance(task.time_from_start_in_seconds, float)
    assert task.time_from_start_in_seconds >= 0
    assert "Task(id=13" in repr(task)
    assert "payload={'k': 'v'}" in str(task)
