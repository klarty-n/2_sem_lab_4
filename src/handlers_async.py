from __future__ import annotations

import asyncio
from typing import Any

from src.async_protocols import TaskHandler
from src.logger import log_info
from src.resources import ClientSession
from src.task import Task


class PayloadEchoHandler:
    """
    Обработчик который принимает задачи, где payload — str
    """

    def supports(self, task: Task) -> bool:
        return isinstance(task.payload, str)

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0)
        log_info(f"echo: {task.payload}")


class ExternalClientHandler:
    """
    Обработчик, который использует ресурс через async context manager
    """

    def supports(self, task: Task) -> bool:
        return isinstance(task.payload, dict) and "description" in task.payload

    async def handle(self, task: Task) -> None:
        payload: Any = task.payload
        async with ClientSession() as client:
            _ = await client.do_work(payload)


class FailingHandler:
    """
    Пример обработчика для демонстрации централизованной обработки ошибок
    """

    def supports(self, task: Task) -> bool:
        return task.payload == "__fail__"

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(0)
        raise RuntimeError("error :(")

