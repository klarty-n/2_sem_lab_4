import asyncio
import pytest
from src.async_executor import AsyncTaskExecutor, NoHandlerError
from src.async_queue import AsyncTaskQueue
from src.handlers_async import ExternalClientHandler, FailingHandler, PayloadEchoHandler
from src.task import Task


def test_async_queue_put_get_and_close():
    # тест для put get и close
    async def scenario():
        q = AsyncTaskQueue()
        t = Task(task_id=1, payload="i dont know what to write")
        await q.put(t)
        got = await q.get()
        assert got.id == 1
        q.task_done()

        await q.close(executors=1)

        # проверяем что работа очереди завершилась корректно 
        with pytest.raises(StopAsyncIteration):
            await q.get()

    asyncio.run(scenario())


def test_executor_processes_tasks_and_sets_statuses():
    async def scenario():
        q = AsyncTaskQueue()
        handlers = [FailingHandler(), PayloadEchoHandler(), ExternalClientHandler()]

        tasks = [
            Task(task_id=1, payload="hello"),
            Task(task_id=2, payload={"description": "teeeeest"}),
            Task(task_id=3, payload="__fail__"),
        ]

        async with AsyncTaskExecutor(q, handlers, workers=2) as ex:
            await ex.submit_many(tasks)
            await ex.drain_and_stop()

        assert tasks[0].status == "completed"
        assert tasks[1].status == "completed"
        assert tasks[2].status == "failed"
        assert ex.stats.processed == 3
        assert ex.stats.succeeded == 2
        assert ex.stats.failed == 1

    asyncio.run(scenario())


def test_executor_raises_nohandler_in_handler_selection():
    async def scenario():
        q = AsyncTaskQueue()
        handlers = [PayloadEchoHandler()]

        async with AsyncTaskExecutor(q, handlers, workers=1) as ex:
            task = Task(task_id=10, payload={"noooo": "handler"})
            # тестируем ожидаемое поведение выбора обработчика:
            with pytest.raises(NoHandlerError):
                ex._select_handler(task) 

            await ex.stop()

    asyncio.run(scenario())

