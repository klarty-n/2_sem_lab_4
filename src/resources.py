from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(slots=True)
class FakeExternalClient:
    """
    Пример какого-то внешнего ресурса
    """

    connected: bool = False

    async def connect(self) -> None:
        await asyncio.sleep(0)
        self.connected = True

    async def close(self) -> None:
        await asyncio.sleep(0)
        self.connected = False

    async def do_work(self, payload: Any) -> str:
        if not self.connected:
            raise RuntimeError("Client is not connected")
        await asyncio.sleep(0)
        return f"ok:{payload!r}"


class ClientSession:
    """
    Async context manager для управления ресурсом
    """

    def __init__(self) -> None:
        self._client: Optional[FakeExternalClient] = None

    async def __aenter__(self) -> FakeExternalClient:
        self._client = FakeExternalClient()
        await self._client.connect()
        # возвращаем клиента, когда он подключен
        return self._client

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._client is not None:
            await self._client.close()
        self._client = None


