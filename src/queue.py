from __future__ import annotations
from typing import Iterator
from src.task import Task

class TaskQueueIterator:
    """
    Итератор для очереди задач
    Поддерживает корректную обработку StopIteration
    """

    def __init__(self, tasks: list[Task]) -> None:
        self._tasks = tasks
        self._index = 0

    def __iter__(self) -> TaskQueueIterator:
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._tasks):
            raise StopIteration("Задачи в очереди закончились")
        task = self._tasks[self._index]
        self._index += 1
        return task


class TaskQueue:
    """
    Очередь задач
    """

    def __init__(self, tasks: list[Task] | None = None) -> None:
        """
        Инициализация очереди задач
        """
        self._tasks: list[Task] = list(tasks) if tasks is not None else []

    def add(self, task: Task) -> None:
        """
        Добавляет задачу в очередь
        """
        self._tasks.append(task)

    def remove(self, task_id: int) -> bool:
        """
        Удаляет задачу по идентификатору
        
        :param task_id: идентификатор задачи
        :return: True если задача удалена, False если не найдена
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                self._tasks.pop(i)
                return True
        return False

    def __iter__(self) -> TaskQueueIterator:
        """
        Возвращает новый итератор для прохода по очереди
        (Каждый вызов - новый генератор, поэтому можно повторно обходить очерердь)
        """
        return TaskQueueIterator(self._tasks)

    def __len__(self) -> int:
        """
        Возвращает количество задач в очереди
        """
        return len(self._tasks)

    def __getitem__(self, index: int) -> Task:
        """
        Возвращает задачу по индексу
        """
        return self._tasks[index]

    def __repr__(self) -> str:
        return f"TaskQueue(tasks={len(self._tasks)})"

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """
        Ленивый фильтр задач по статусу

        :param status: статус для фильтрации
        :return: генератор с задачами указанного статуса
        """
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, priority: int) -> Iterator[Task]:
        """
        Ленивый фильтр задач по приоритету
        
        :param priority: приоритет для фильтрации
        :return: генератор с задачами указанного приоритета
        """
        for task in self._tasks:
            if task.priority == priority:
                yield task

    def get_tasks_higher_priority(self, min_priority: int = 4) -> Iterator[Task]:
        """
        Ленивый генератор задач с высоким приоритетом
        
        :param min_priority: минимальный приоритет (по умолчанию 4)
        :return: генератор с задачами высокого приоритета
        """
        for task in self._tasks:
            if task.priority >= min_priority:
                yield task

    def get_tasks_by_statuses(self, statuses: list[str]) -> Iterator[Task]:
        """
        Ленивый генератор задач с указанными статусами
        
        :param statuses: список статусов для фильтрации
        :return: генератор с задачами указанных статусов
        """
        for task in self._tasks:
            if task.status in statuses:
                yield task

    def get_total_priority(self) -> int:
        """
        Вычисляет суммарный приоритет всех задач в очереди
        
        :return: сумма приоритетов всех задач
        """
        return sum(task.priority for task in self)

    def is_empty(self) -> bool:
        """
        Проверяет, пуста ли очередь
        
        :return: True если очередь пуста
        """
        return len(self._tasks) == 0

    def clear(self) -> None:
        """
        Очищает очередь
        """
        self._tasks.clear()