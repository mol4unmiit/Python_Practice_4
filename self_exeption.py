#Создание собственных исключений
class NegativeAgeError(Exception):
    """Исключение для отрицательного возраста"""
    pass

class TooYoungError(Exception):
    """Исключение для слишком молодого возраста"""
    pass

def check_age(age):
    if age < 0:
        raise NegativeAgeError("Возраст не может быть отрицательным!")
    if age < 18:
        raise TooYoungError("Возраст меньше 18 лет!")
    return "Возраст корректен"

# Тестирование собственных исключений
ages_to_test = [25, -5, 16]

for age in ages_to_test:
    try:
        result = check_age(age)
        print(f"Возраст {age}: {result}")
    except NegativeAgeError as e:
        print(f"Возраст {age}: Ошибка — {e}")
    except TooYoungError as e:
        print(f"Возраст {age}: Ошибка — {e}")