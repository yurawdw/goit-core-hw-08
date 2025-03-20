import re
import sys
from collections import UserDict
from datetime import datetime
from colorama import init, Fore, Style

# Ініціалізація colorama для кросплатформенності
init(autoreset=True)

def parse_log_line(line: str):
    """
    Парсить рядок логу, повертаючи рівень логування та повідомлення.
    """
    match = re.match(r'\[(INFO|ERROR|DEBUG|WARNING)\] (.+)', line)
    return {"level": match.group(1), "message": match.group(2)} if match else {}

def load_logs(file_path: str):
    """
    Завантажує логи з файлу та повертає список словників.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [parse_log_line(line.strip()) for line in file if parse_log_line(line.strip())]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found.{Style.RESET_ALL}")
        sys.exit(1)

def filter_logs_by_level(logs, level):
    """
    Фільтрує логи за рівнем логування.
    """
    return [log for log in logs if log["level"] == level.upper()]

def count_logs_by_level(logs):
    """
    Підраховує кількість логів за рівнями.
    """
    levels = {"INFO": 0, "ERROR": 0, "DEBUG": 0, "WARNING": 0}
    for log in logs:
        levels[log["level"]] += 1
    return levels

def display_log_counts(counts):
    """
    Виводить статистику логів у форматі таблиці.
    """
    print(f"{Fore.WHITE}Log Level | Count")
    print("-----------------")
    for level, count in counts.items():
        print(f"{Fore.YELLOW}{level:<9} | {count}{Style.RESET_ALL}")

def main():
    """
    Основна функція для запуску скрипта.
    """
    if len(sys.argv) < 2:
        print(f"{Fore.RED}Usage: python script.py <log_file> [log_level]{Style.RESET_ALL}")
        sys.exit(1)
    
    log_file = sys.argv[1]
    logs = load_logs(log_file)
    
    if len(sys.argv) == 3:
        level = sys.argv[2]
        filtered_logs = filter_logs_by_level(logs, level)
        for log in filtered_logs:
            print(f"{Fore.GREEN}[{log['level']}] {log['message']}{Style.RESET_ALL}")
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

if __name__ == "__main__":
    main()
