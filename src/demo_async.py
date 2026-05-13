from __future__ import annotations

import asyncio

from src.async_executor import AsyncTaskExecutor
from src.async_queue import AsyncTaskQueue
from src.handlers_async import ExternalClientHandler, FailingHandler, PayloadEchoHandler
from src.logger import log_info
from src.source import ApiTaskSource, GeneratorTaskSource


async def run_demo(generated_count: int = 5) -> None:
    """
    Демонстрация работы исполнителя асинхрнного, берём задачи из источников и обрабатываем их асинхронно через executor/handlers
    """

    sources = [GeneratorTaskSource(generated_count), ApiTaskSource()]
    tasks = []
    for src in sources:
        tasks.extend(src.get_tasks())

    # Добавили одну "падающую" задачу, чтобы увидеть обработку ошибок
    tasks.append(type(tasks[0])(task_id=999, payload="__fail__", priority=5, status="not_started"))

    q = AsyncTaskQueue()
    handlers = [FailingHandler(), ExternalClientHandler(), PayloadEchoHandler()]

    async with AsyncTaskExecutor(q, handlers, workers=3) as ex:
        await ex.submit_many(tasks)
        await ex.drain_and_stop()

    succ = [t for t in tasks if t.status == "completed"]
    fail = [t for t in tasks if t.status == "failed"]
    log_info(f"demo завершено: обработано успешно={len(succ)}, не удалось обработать={len(fail)}")
    print(f"demo завершено: обработано успешно={len(succ)}, не удалось обработать={len(fail)}")


def run_demo_sync(generated_count: int = 5) -> None:
    asyncio.run(run_demo(generated_count=generated_count))

