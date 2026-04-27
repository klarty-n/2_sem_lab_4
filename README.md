# Лабораторная работа №3
## Очередь задач: итераторы и генераторы

## Запуск программы
```bash
python -m src.main
```

## Что реализовано
  - `TaskQueue.__iter__()` — возвращает новый итератор
  - `TaskQueueIterator.__next__()` — обработка `StopIteration`
  - поддержка повторного обхода очереди
  - совместимость с `for`, `list()`, `sum()`

- **Ленивые фильтры через генераторы:**
  - `filter_by_status(status)` — фильтрация задач по статусу
  - `filter_by_priority(priority)` — фильтрация задач по приоритету
  - использование `yield`

- **Дополнительные методы:**
  - `add(task)` — добавление задачи в очередь
  - `remove(task_id)` — удаление задачи по идентификатору
  - `get_total_priority()` — суммарный приоритет всех задач (TaskQueue совместим с sum())
  - `is_empty()` — проверка на пустоту
  - `clear()` — очистка очереди

## Класс `TaskQueue`
- `__init__(tasks)` — инициализация очереди задач
- `add(task)` — добавить задачу
- `remove(task_id)` — удалить задачу по айди
- `__iter__()` — итератор (поддержка `for`, `list()`)
- `__len__()` — количество задач (поддержка `len()`)
- `__getitem__(index)` — доступ по индексу
- `filter_by_status(status)` — ленивый фильтр по статусу
- `filter_by_priority(priority)` — ленивый фильтр по приоритету
- `get_total_priority()` — сумма приоритетов
- `is_empty()` — проверка на пустоту
- `clear()` — очистка очереди

## Класс `TaskQueueIterator`
- `__init__(tasks)` — инициализация итератора
- `__iter__()` — возвращает себя
- `__next__()` — возвращает следующий элемент или бросает `StopIteration`

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
    ├── test_task_model.py              
    ├── test_descriptors_behavior.py    
    ├── test_sources_and_handler.py     
    └── test_queue.py                   
```

