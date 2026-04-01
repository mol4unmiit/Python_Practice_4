import re
import os
from datetime import datetime
from collections import Counter


def parse_log_line(line):
    pattern = r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\S+)\s+(\S+)\s+[^"]*"\s+(\d+)\s+(\d+|-)'

    match = re.match(pattern, line.strip())
    if not match:
        return None

    ip, date_str, method, url, status, size = match.groups()

    try:
        size = int(size) if size != '-' else 0
    except ValueError:
        size = 0

    try:
        date = datetime.strptime(date_str.split()[0], '%d/%b/%Y:%H:%M:%S')
    except ValueError:
        date = None

    return {
        'ip': ip,
        'date': date,
        'date_str': date_str,
        'method': method,
        'url': url,
        'status': int(status),
        'size': size
    }


def read_log_file(filepath):
    records = []
    errors = 0

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                if not line.strip():
                    continue
                record = parse_log_line(line)
                if record:
                    records.append(record)
                else:
                    errors += 1
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {filepath}")
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения файла: {e}")

    return records, errors


def analyze_logs(records):
    if not records:
        return {}

    ip_counter = Counter(r['ip'] for r in records)
    status_counter = Counter(r['status'] for r in records)
    method_counter = Counter(r['method'] for r in records)
    unique_urls = set(r['url'] for r in records)
    total_bytes = sum(r['size'] for r in records)

    date_counter = Counter()
    for r in records:
        if r['date']:
            day = r['date'].strftime('%Y-%m-%d')
            date_counter[day] += 1

    url_counter = Counter(r['url'] for r in records)

    return {
        'total_requests': len(records),
        'unique_ips': len(ip_counter),
        'unique_urls': len(unique_urls),
        'total_bytes': total_bytes,
        'ip_stats': ip_counter,
        'status_stats': status_counter,
        'method_stats': method_counter,
        'date_stats': date_counter,
        'url_stats': url_counter
    }


def format_size(bytes_count):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def generate_report(stats, errors_count, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(" ")
            f.write("ОТЧЁТ ПО АНАЛИЗУ ЛОГОВ ВЕБ-СЕРВЕРА (Apache)\n")
            f.write(" ")
            f.write(f"Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Обработано строк с ошибками: {errors_count}\n\n")

            f.write(" ")
            f.write("ОБЩАЯ СТАТИСТИКА\n")
            f.write(" ")
            f.write(f"Всего запросов:        {stats.get('total_requests', 0):,}\n")
            f.write(f"Уникальных IP:         {stats.get('unique_ips', 0):,}\n")
            f.write(f"Уникальных URL:        {stats.get('unique_urls', 0):,}\n")
            f.write(f"Общий объём данных:    {format_size(stats.get('total_bytes', 0))}\n\n")

            f.write("-" * 70 + "\n")
            f.write("ЗАПРОСЫ ПО КОДАМ ОТВЕТА\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Код':<10} {'Количество':<15} {'Процент':<10}\n")
            f.write("-" * 35 + "\n")
            total = stats.get('total_requests', 1)
            for code, count in sorted(stats.get('status_stats', {}).items()):
                percent = (count / total) * 100
                f.write(f"{code:<10} {count:<15,} {percent:>6.2f}%\n")
            f.write("\n")

            f.write("-" * 70 + "\n")
            f.write("ЗАПРОСЫ ПО МЕТОДАМ\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'Метод':<10} {'Количество':<15} {'Процент':<10}\n")
            f.write("-" * 35 + "\n")
            for method, count in stats.get('method_stats', {}).items():
                percent = (count / total) * 100
                f.write(f"{method:<10} {count:<15,} {percent:>6.2f}%\n")
            f.write("\n")

            f.write("-" * 70 + "\n")
            f.write("ТОП-10 ПО КОЛИЧЕСТВУ ЗАПРОСОВ (IP-адреса)\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'IP-адрес':<20} {'Запросы':<15}\n")
            f.write("-" * 35 + "\n")
            for ip, count in stats.get('ip_stats', {}).most_common(10):
                f.write(f"{ip:<20} {count:,}\n")
            f.write("\n")

            f.write("-" * 70 + "\n")
            f.write("ТОП-10 ПО КОЛИЧЕСТВУ ЗАПРОСОВ (URL)\n")
            f.write("-" * 70 + "\n")
            f.write(f"{'URL':<50} {'Запросы':<10}\n")
            f.write("-" * 60 + "\n")
            for url, count in stats.get('url_stats', {}).most_common(10):
                url_display = url[:47] + "..." if len(url) > 50 else url
                f.write(f"{url_display:<50} {count:,}\n")
            f.write("\n")

            if stats.get('date_stats'):
                f.write("-" * 70 + "\n")
                f.write("ЗАПРОСЫ ПО ДНЯМ\n")
                f.write("-" * 70 + "\n")
                f.write(f"{'Дата':<15} {'Запросы':<15}\n")
                f.write("-" * 30 + "\n")
                for date, count in sorted(stats['date_stats'].items()):
                    f.write(f"{date:<15} {count:,}\n")
                f.write("\n")


            f.write("КОНЕЦ ОТЧЁТА\n")


        print(f"Отчёт сохранён в файл: {output_file}")
        return True

    except PermissionError:
        print(f"Ошибка: Нет прав на запись в файл {output_file}")
        return False
    except Exception as e:
        print(f"Ошибка при создании отчёта: {e}")
        return False


def print_summary(stats, errors_count):

    print("СТАТИСТИКА АНАЛИЗА ЛОГОВ")

    print(f"Всего запросов:     {stats.get('total_requests', 0):,}")
    print(f"Уникальных IP:      {stats.get('unique_ips', 0):,}")
    print(f"Уникальных URL:     {stats.get('unique_urls', 0):,}")
    print(f"Объём данных:       {format_size(stats.get('total_bytes', 0))}")
    print(f"Ошибок парсинга:    {errors_count}")

    print("\nКоды ответов:")
    for code, count in sorted(stats.get('status_stats', {}).items()):
        print(f"  {code}: {count:,}")

    print("\nТоп-3 по IP:")
    for ip, count in stats.get('ip_stats', {}).most_common(3):
        print(f"  {ip}: {count:,}")



def main():
    print("АНАЛИЗАТОР ЛОГОВ ВЕБ-СЕРВЕРА (Apache)")
    print("-" * 50)

    log_file = input("Введите путь к файлу лога: ").strip()

    if not log_file:
        log_file = "access.log"
        print(f"Используется файл по умолчанию: {log_file}")

    report_file = input("Введите имя файла отчёта (или Enter для default): ").strip()
    if not report_file:
        report_file = "log_analysis_report.txt"

    try:
        print(f"\nЧтение файла: {log_file}...")
        records, errors = read_log_file(log_file)
        print(f"Обработано записей: {len(records)}, ошибок: {errors}")

        if not records:
            print("Нет данных для анализа.")
            return

        print("Анализ данных...")
        stats = analyze_logs(records)

        print_summary(stats, errors)

        print(f"\nГенерация отчёта: {report_file}...")
        generate_report(stats, errors, report_file)

        print("\nАнализ завершён.")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except PermissionError as e:
        print(f"Ошибка прав доступа: {e}")
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")