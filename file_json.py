import json

# Создание и запись JSON-данных
person = {
    "name": "Алексей",
    "age": 35,
    "city": "Екатеринбург",
    "hobbies": ["программирование", "шахматы", "плавание"]
}

with open("person.json", "w", encoding="utf-8") as jsonfile:
    json.dump(person, jsonfile, ensure_ascii=False, indent=4)

# Чтение JSON-файла
with open("person.json", "r", encoding="utf-8") as jsonfile:
    loaded_person = json.load(jsonfile)
    print("Загруженные данные:")
    print(loaded_person)