from __future__ import annotations
import asyncio
from collections.abc import AsyncIterator
from src.task import Task

# маркер для остановки
_STOP = object()

class AsyncTaskQueue:
    """
    Асинхронная очередь задач поверх 'asyncio.Queue'
    """

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: asyncio.Queue[object] = asyncio.Queue(maxsize=maxsize)
        # флаг для закрытия очереди
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    def qsize(self) -> int:
        return self._queue.qsize()

    async def put(self, task: Task) -> None:
        if self._closed:
            raise RuntimeError("Нельзя добавлять задачи: очередь закрыта")
        await self._queue.put(task)

    async def get(self) -> Task:
        item = await self._queue.get()
        if item is _STOP:
            # задачу не удаляем из очереди, но говорим, что она обработана
            self._queue.task_done()
            # бросаем исключение для остановки итерации
            raise StopAsyncIteration
        # возвращаем задачу, если это не стоп сигнал
        return item  

    def task_done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        # ждем пока все задачи будут обработаны
        await self._queue.join()

    async def close(self, executors: int = 1) -> None:
        """
        Закрывает очередь: отправляет столько сигналов остановки, сколько исполнителей
        """
        if self._closed:
            return
        self._closed = True
        for _ in range(max(executors, 1)):
            await self._queue.put(_STOP)

    def __aiter__(self) -> AsyncIterator[Task]:
        return self._iter()

    async def _iter(self) -> AsyncIterator[Task]:
        while True:
            try:
                task = await self.get()
            except StopAsyncIteration:
                return
            # возвращаем задачу, если это не стоп сигнал
            yield task

