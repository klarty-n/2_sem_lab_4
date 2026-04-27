from datetime import datetime
from typing import Any
from src.exceptions import StatusTransitionError
from src.descriptors import (
    IdDescriptor,
    PayloadDescriptor,
    PriorityDescriptor,
    StatusDescriptor,
    TimeCreatedDescriptor,
)


class Task:
    """
    модель задачи
    """

    _transitions_in_tasks = {
        "not_started": {"in_progress", "failed"},
        "in_progress": {"completed", "failed"},
        "completed": set(),
        "failed": set(),
    }

    id = IdDescriptor()
    priority = PriorityDescriptor()
    status = StatusDescriptor()
    payload = PayloadDescriptor()
    created_at = TimeCreatedDescriptor()    # non-data дескриптор

    def __init__(self, task_id: int | None = None, payload: Any = None, priority: int = 3, status: str = "not_started") -> None:
        self.id = task_id
        self.payload = payload
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()

    def _can_transition(self, current_status: str, new_status: str) -> bool:
        return new_status in self._transitions_in_tasks[current_status]

    @property
    def is_ready_for_start(self) -> bool:
        """
        Вычисляемое свойство, используем property: готовность задачи к выполнению
        """
        return self.status == "not_started"

    @property
    def time_from_start_in_seconds(self) -> float:
        """
        Вычисляемое свойство, используем property: время с создания задачи в секундах
        """
        return (datetime.now() - self._created_at).total_seconds()
    
    def transition_to(self, new_status: str) -> None:
        """
        Переводит задачу в новый статус с проверкой допустимых переходов
        """
        if new_status not in self._transitions_in_tasks[self.status]:
            raise StatusTransitionError(
                f"Недопустимый переход статуса: {self.status} -> {new_status}"
            )
        self.status = new_status

    def __repr__(self) -> str:
        return f"Task(id={self.id}, payload={repr(self.payload)}, priority={self.priority}, status='{self.status}')"
    def __str__(self) -> str:
        return f"Task(id={self.id}, payload={self.payload}, priority={self.priority}, status={self.status})"