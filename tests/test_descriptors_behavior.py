from datetime import datetime
from src.task import Task

import pytest

from src.descriptors import IdDescriptor, TimeCreatedDescriptor
from src.exceptions import StatusTransitionError


def test_id_descriptor_uses_private_storage_name():
    class Testik:
        id = IdDescriptor()

    d = Testik()
    d.id = 13

    assert d.id == 13
    assert d.__dict__["_id"] == 13


def test_non_data_descriptor():
    class Testik:
        created_at = TimeCreatedDescriptor()

    d = Testik()
    fallback = d.created_at
    assert isinstance(fallback, datetime)

    d.created_at = "ttt"
    assert d.created_at == "ttt"


def test_status_descriptor_checks_transition_rules():
    task = Task(task_id=1, payload="13", status="not_started")
    task.status = "in_progress"
    with pytest.raises(StatusTransitionError):
        task.status = "not_started"
