import os
import shutil
from datetime import datetime
from pathlib import Path


def main():

    while True:
        source_path = input("\nВведите путь к исходному файлу: ").strip()
        if not os.path.exists(source_path):
            print("Ошибка: Файл не найден.")
            continue
        if not os.path.isfile(source_path):
            print("Ошибка: Указанный путь не является файлом.")
            continue
        if not os.access(source_path, os.R_OK):
            print("Ошибка: Нет прав на чтение файла.")
            continue
        break

    while True:
        backup_dir = input("Введите путь к папке для сохранения: ").strip()
        if not os.path.exists(backup_dir):
            create = input("Папка не существует. Создать? (y/n): ").strip().lower()
            if create == 'y':
                try:
                    os.makedirs(backup_dir)
                    print("Папка создана.")
                except Exception as e:
                    print(f"Ошибка создания папки: {e}")
                    continue
            else:
                continue
        if not os.path.isdir(backup_dir):
            print("Ошибка: Указанный путь не является папкой.")
            continue
        if not os.access(backup_dir, os.W_OK):
            print("Ошибка: Нет прав на запись в папку.")
            continue
        break

    stem = Path(source_path).stem
    suffix = Path(source_path).suffix
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_name = f"{stem}_{timestamp}_backup{suffix}"
    backup_path = os.path.join(backup_dir, backup_name)

    try:
        shutil.copy2(source_path, backup_path)

        if os.path.exists(backup_path):
            print("\nУспешно!")
            print(f"Исходный файл: {source_path}")
            print(f"Резервная копия: {backup_path}")
        else:
            print("Ошибка: Файл копии не был создан.")

    except PermissionError:
        print("Ошибка: Нет прав доступа для копирования.")
    except FileNotFoundError:
        print("Ошибка: Исходный файл не найден.")
    except shutil.SameFileError:
        print("Ошибка: Исходный файл и файл копии совпадают.")
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПроцесс прерван пользователем.")