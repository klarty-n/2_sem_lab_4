from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.task import Task


@runtime_checkable
class TaskHandler(Protocol):
    """
    Контракт обработчика задач
    """

    def supports(self, task: Task) -> bool:
        """Вернет True, если обработчик умеет обработать задачу, иначе False"""

    async def handle(self, task: Task) -> None:
        """Выполняет обработку задачи"""

