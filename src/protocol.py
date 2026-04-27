from typing import List, Protocol, runtime_checkable
from src.task import Task


@runtime_checkable
class TaskSource(Protocol):
    """
    Протокол источников задач, класс, который реализует
    метод get_tasks будет считаться источником команд
    """

    def get_tasks(self) -> List[Task]:
        "Получить список задач"
        pass
