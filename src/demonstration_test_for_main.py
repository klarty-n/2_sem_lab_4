from src.logger import log_info
import subprocess
import sys

def run_tests() -> None:
    """
    Запуск тестов 
    """
    log_info("Запуск тестов...")

    result = subprocess.run([sys.executable, "-m", "pytest", "-v", "--tb=short"])
    
    if result.returncode == 0:
        log_info("Все тесты пройдены успешно")
    else:
        log_info(f"Тесты завершены с ошибками (код {result.returncode})")
