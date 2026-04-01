# Базовая обработка исключений

try:
    with open("non_existent.txt", "r", encoding="utf-8") as file:
        content = file.read()
        print(content)
except FileNotFoundError:
    print("Ошибка: Файл не найден!")
except PermissionError:
    print("Ошибка: Нет прав доступа к файлу!")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")

# Несколько типов исключений


def safe_divide(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Ошибка: Деление на ноль!")
        return None
    except TypeError:
        print("Ошибка: Некорректный тип данных!")
        return None


print(safe_divide(10, 2))  # 5.0
print(safe_divide(10, 0))  # Ошибка: Деление на ноль!
print(safe_divide("10", 2))  # Ошибка: Некорректный тип данных!

# Обработка ошибок при работе с файлами


def read_and_process_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            # Обработка данных — например, подсчёт строк
            print(f"Файл {filename} содержит {len(lines)} строк")
            return lines
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return []
    except PermissionError:
        print(f"Ошибка: Нет доступа к файлу '{filename}'.")
        return []
    except UnicodeDecodeError:
        print(f"Ошибка: Неверная кодировка файла '{filename}'.")
        return []
    except Exception as e:
        print(f"Неизвестная ошибка при работе с файлом: {e}")
        return []


data = read_and_process_file("exeption.txt")
