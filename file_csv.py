import csv

# Запись данных в CSV
data = [
    ["Имя", "Возраст", "Город"],
    ["Анна", "25", "Москва"],
    ["Иван", "30", "СПб"],
    ["Мария", "28", "Казань"]
]

with open("people.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

# Чтение CSV-файла
with open("people.csv", "r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)