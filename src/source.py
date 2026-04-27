from __future__ import annotations
from typing import Any, List
from src.task import Task


class GeneratorTaskSource:
    """
    Источник, генерирующий таски
    """

    def __init__(self, count: int):
        if count < 0:
            raise ValueError("count не может быть отрицательным")
        self.count = count  # количество задач

    def get_tasks(self) -> List[Task]:
        """
        Генерируем таски
        """
        tasks = []

        for task_id in range(self.count):
            task = Task(
                task_id=task_id,
                payload=f"Сгенерированный таск с id {task_id}",
                priority=(task_id % 5) + 1,  # приоритет от 1 до 5
                status="not_started",
            )
            tasks.append(task)

        return tasks


class ApiTaskSource:
    """
    API-заглушка
    """

    def __init__(self) -> None:
        self._fake_response: List[dict[str, Any]] = [
            {
                "id": 13,
                "payload": {"description": "Получить отчет", "user_id": 666},
                "priority": 2,
                "status": "not_started",
            },
            {
                "id": 14,
                "payload": {"description": "Отправить письмо начальнику", "user_id": 42},
                "priority": 3,
                "status": "in_progress",
            },
        ]

    def get_tasks(self) -> List[Task]:
        tasks: List[Task] = []
        for item in self._fake_response:
            tasks.append(
                Task(
                    task_id=item["id"],
                    payload=item["payload"],
                    priority=item["priority"],
                    status=item["status"],
                )
            )
        return tasks