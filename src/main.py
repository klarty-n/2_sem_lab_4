from src.logger import log_info, log_error
from src.source import GeneratorTaskSource
from src.handler import hendler_task_source
from src.demonstration_test_for_main import run_tests
from src.demo_async import run_demo_sync

def main() -> None:
    """
    Точка входа
    :return: ничего не возвращает
    """

    log_info("Начинается работа программы")

    while True:
        try:
            print("\nВыберите действие:")
            print("1 Сгенерировать задачи")
            print("2 Запустить асинхронную обработку")
            print("3 Запустить тесты")
            print("4 Выйти")

            choice = input("ヽ(♡‿♡)ノ Введите номер действия: ").strip()

            if choice == "1":
                try:
                    count = int(input("Введите количество задач для генерации: "))
                    if count <= 0:
                        print("Количество задач должно быть положительным числом")
                        continue

                    log_info(f"Создаем источник с {count} задачами")

                    generator_source = GeneratorTaskSource(count)

                    log_info("Получаем задачи из источника")
                    tasks = hendler_task_source(generator_source)

                    print("\nСгенерированные задачи:")
                    for task in tasks:
                        print(f"Id: {task.id}, Payload: {task.payload}")

                    log_info(f"Получено {len(tasks)} задач")

                except ValueError:
                    print("Пожалуйста, введите корректное число")
                    continue

            elif choice == "2":
                try:
                    count = int(input("Сколько задач сгенерировать для демо?: "))
                except ValueError:
                    count = 5
                print("Запуск...")
                run_demo_sync(generated_count=count)

            elif choice == "3":
                print("Запуск тестов...")
                run_tests()

            elif choice == "4":
                msg = "\nВыход из программы (＿ ＿*) Z z z"
                print(msg)
                log_info(msg)
                break

            else:
                print("Пожалуйста, введите 1, 2, 3 или 4")

        except KeyboardInterrupt:
            log_info("Работа прервана")
            break
        except Exception as e:
            log_error(f"Ошибка в работе программы: {str(e)}")
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
