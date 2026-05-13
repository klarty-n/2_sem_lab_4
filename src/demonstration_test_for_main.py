from src.logger import log_info

def run_tests() -> None:
    """
    Запуск тестов
    """
    log_info("Запуск тестов")
    import os
    os.system('pytest ../tests/test.py -v')
    os.system('pytest ../tests/test_task_model.py -v')
    os.system('pytest ../tests/test_descriptors_behavior.py -v')
    os.system('pytest ../tests/test_sources_and_handler.py -v')
    os.system('pytest ../tests/test_queue.py -v')
    os.system('pytest ../tests/test_async_executor.py -v')
    
    log_info("Тесты пройдены")
