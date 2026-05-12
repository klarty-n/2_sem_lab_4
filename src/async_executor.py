from __future__ import annotations

import asyncio
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional

from src.async_protocols import TaskHandler
from src.async_queue import AsyncTaskQueue
from src.logger import log_error, log_info
from src.task import Task


class NoHandlerError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class ExecutorStats:
    processed: int = 0
    succeeded: int = 0
    failed: int = 0


class AsyncTaskExecutor:
    """
    Асинхронный исполнитель задач (ЛР4).

    - Берёт задачи из `AsyncTaskQueue`
    - Выбирает обработчик по `supports()`
    - Обрабатывает задачи через `await handler.handle(task)`
    - Управляет жизненным циклом воркеров через async context manager
    - Логирует старт/ошибки централизованно
    """

    def __init__(
        self,
        queue: AsyncTaskQueue,
        handlers: Iterable[TaskHandler],
        *,
        workers: int = 2,
        worker_name_prefix: str = "worker",
    ) -> None:
        self._queue = queue
        self._handlers = list(handlers)
        self._workers = max(1, int(workers))
        self._worker_name_prefix = worker_name_prefix

        self._tasks: list[asyncio.Task[None]] = []
        self._stats = ExecutorStats()
        self._lock = asyncio.Lock()
        self._stopping = asyncio.Event()

    @property
    def stats(self) -> ExecutorStats:
        return self._stats

    async def __aenter__(self) -> AsyncTaskExecutor:
        log_info(f"Executor start: workers={self._workers}")
        self._stopping.clear()
        self._tasks = [
            asyncio.create_task(self._worker_loop(i), name=f"{self._worker_name_prefix}-{i}")
            for i in range(self._workers)
        ]
        return self

    async def __aexit__(self, exc_type, exc, tb) -> Optional[bool]:
        await self.stop()
        return None

    async def submit(self, task: Task) -> None:
        await self._queue.put(task)

    async def submit_many(self, tasks: Iterable[Task]) -> None:
        for t in tasks:
            await self.submit(t)

    async def drain_and_stop(self) -> None:
        """
        Дождаться обработки всех задач в очереди и остановить воркеры.
        """
        await self._queue.join()
        await self.stop()

    async def stop(self) -> None:
        if self._stopping.is_set():
            return
        self._stopping.set()

        await self._queue.close(executors=self._workers)
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        log_info(
            "Executor stop: "
            f"processed={self._stats.processed}, ok={self._stats.succeeded}, failed={self._stats.failed}"
        )

    def _select_handler(self, task: Task) -> TaskHandler:
        for h in self._handlers:
            try:
                if h.supports(task):
                    return h
            except Exception as e:
                log_error(f"Handler supports() error: {type(h).__name__}: {e}")
        raise NoHandlerError(f"Нет обработчика для задачи id={task.id}")

    async def _worker_loop(self, worker_id: int) -> None:
        async for task in self._queue:
            try:
                await self._process_one(task, worker_id=worker_id)
            finally:
                self._queue.task_done()

    async def _process_one(self, task: Task, *, worker_id: int) -> None:
        async with self._lock:
            self._stats = ExecutorStats(
                processed=self._stats.processed + 1,
                succeeded=self._stats.succeeded,
                failed=self._stats.failed,
            )

        log_info(f"worker={worker_id} start task id={task.id}")

        try:
            task.transition_to("in_progress")
            handler = self._select_handler(task)
            await handler.handle(task)
            task.transition_to("completed")

            async with self._lock:
                self._stats = ExecutorStats(
                    processed=self._stats.processed,
                    succeeded=self._stats.succeeded + 1,
                    failed=self._stats.failed,
                )

            log_info(f"worker={worker_id} done task id={task.id}")
        except Exception as e:
            try:
                task.transition_to("failed")
            except Exception:
                pass

            async with self._lock:
                self._stats = ExecutorStats(
                    processed=self._stats.processed,
                    succeeded=self._stats.succeeded,
                    failed=self._stats.failed + 1,
                )

            log_error(f"worker={worker_id} task id={getattr(task, 'id', '?')} failed: {e}")

