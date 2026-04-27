from typing import List
from src.task import Task
from src.protocol import TaskSource
from src.logger import log_info, log_error


def hendler_task_source(source: TaskSource) -> List[Task]:
    """
    Обработка задач из источника
    :param source: источник задач
    :return: список задач
    """
    if not isinstance(source, TaskSource):
        error_msg = "Источник не соответствует контракту TaskSource"
        log_error(error_msg)
        raise TypeError(error_msg)

    log_info(f"Обработка источника задач: {type(source).__name__}")
    tasks = source.get_tasks()
    log_info(f"Получили {len(tasks)} задач из источника {type(source).__name__}")
    return tasks


def get_all_tasks(sources: List[TaskSource]) -> List[Task]:
    """
    Получение задач из всех источников
    :param sources: источники
    :return: список задач
    """
    log_info(f"Обработка задач из {len(sources)} источников")
    all_tasks = []

    for source in sources:
        tasks = hendler_task_source(source)
        all_tasks.extend(tasks)

    log_info(f"Все источники обработаны, всего задач: {len(all_tasks)}")

    return all_tasks
