# Лабораторная работа №4
## Асинхронный исполнитель задач

## Запуск программы
```bash
python -m src.main
```

### Что добавлено (ЛР4)
- `src/async_queue.py` — асинхронная очередь задач на базе `asyncio.Queue`
- `src/async_protocols.py` — контракт обработчика `TaskHandler` через `typing.Protocol`
- `src/async_executor.py` — исполнитель задач `AsyncTaskExecutor` (async/await, воркеры, контекстный менеджер, централизованное логирование/ошибки)
- `src/resources.py` — пример управления ресурсом через async context manager
- `src/handlers_async.py` — примеры расширяемых обработчиков (и с ресурсом)
- `tests/test_async_executor_lab4.py` — тесты


## Структура проекта
```
2_sem_lab_3/
├── src/
│   ├── main.py                         # Точка входа 
│   ├── task.py                         # Класс Task 
│   ├── queue.py                        # TaskQueue и TaskQueueIterator 
│   ├── descriptors.py                  # Пользовательские дескрипторы 
│   ├── exceptions.py                   # Исключения
│   ├── source.py                       # Источники задач 
│   ├── handler.py                      # Обработчик источников
│   ├── protocol.py                     # Protocol контракта источника 
│   ├── logger.py                       # Логирование
│   └── demonstration_test_for_main.py  # Запуск тестов
└── tests/
    ├── test.py               
    ├── tests/test_async_executor_lab4.py         
    ├── test_task_model.py              
    ├── test_descriptors_behavior.py    
    ├── test_sources_and_handler.py     
    └── test_queue.py                   
```

