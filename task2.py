import json
import os
import sys

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "database": "mydb",
    "host": "localhost",
    "port": 5432,
    "use_ssl": False
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Файл {CONFIG_FILE} не найден. Создан файл конфига")
        try:
            save_config(DEFAULT_CONFIG)
            print("Файл конфига создан.")
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Ошибка создания файла: {e}")
            sys.exit(1)

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            print("Конфигурация загружена.")
            return config
    except json.JSONDecodeError as e:
        print(f"Ошибка JSON в файле конфигурации: {e}")
        sys.exit(1)
    except PermissionError:
        print("Ошибка: Нет прав на чтение файла конфигурации.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке конфигурации: {e}")
        sys.exit(1)


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        print("Конфигурация сохранена.")
    except PermissionError:
        print("Ошибка: Нет прав на запись в файл конфигурации.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при сохранении конфигурации: {e}")
        sys.exit(1)


def validate_parameter(key, value):
    if key == "port":
        try:
            port = int(value)
            if 1 <= port <= 65535:
                return port
            else:
                print("Ошибка: Порт должен быть числом от 1 до 65535.")
                return None
        except ValueError:
            print("Ошибка: Порт должен быть целым числом.")
            return None

    elif key == "use_ssl":
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            if value.lower() in ("true", "1", "yes"):
                return True
            elif value.lower() in ("false", "0", "no"):
                return False
        print("Ошибка: use_ssl должен быть true/false или 1/0.")
        return None

    elif key in ("database", "host"):
        if isinstance(value, str) and len(value.strip()) > 0:
            return value.strip()
        print("Ошибка: Значение не может быть пустым.")
        return None

    else:
        print(f"Ошибка: Неизвестный параметр '{key}'.")
        return None


def show_config(config):

    print("Текущий конфиг:")

    for key, value in config.items():
        print(f"  {key}: {value}")



def update_parameter(config, key, value):

    validated_value = validate_parameter(key, value)
    if validated_value is not None:
        config[key] = validated_value
        print(f"Параметр '{key}' обновлён: {validated_value}")
        return True
    return False


def main():

    # Загрузка конфига
    config = load_config()
    show_config(config)

    while True:
        print("\nДоступные команды:")
        print("  set <параметр> <значение> - изменить параметр")
        print("  show                      - показать конфигурацию")
        print("  save                      - сохранить и выйти")
        print("  exit                      - выйти без сохранения")

        command = input("\nВведите команду: ").strip().split()

        if not command:
            continue

        cmd = command[0].lower()

        if cmd == "exit":
            print("Выход без сохранения изменений.")
            break

        elif cmd == "show":
            show_config(config)

        elif cmd == "save":
            save_config(config)
            break

        elif cmd == "set":
            if len(command) < 3:
                print("Ошибка: Используйте формат 'set <параметр> <значение>'")
                continue

            key = command[1]
            value = " ".join(command[2:])

            if key not in config:
                print(f"Ошибка: Параметр '{key}' не существует.")
                print(f"Доступные параметры: {', '.join(config.keys())}")
                continue

            if update_parameter(config, key, value):
                pass
            else:
                continue

        else:
            print("Ошибка: Неизвестная команда.")

    print("\nРабота завершена.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)