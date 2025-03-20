from collections import UserDict
from datetime import datetime, date, timedelta
from pathlib import Path
from colorama import init, Fore, Back, Style
import re
import handlers

# Initializing the colorama
init(autoreset=True)


# Класи для роботи з винятками
class PhoneNumberError(Exception):
    pass


class NameError(Exception):
    pass


class Field:
    # Базовий клас
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Клас для зберігання імені контакту. Обов'язкове поле.
    def __init__(self, value: str) -> None:
        if not value:
            raise NameError("Name is required")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value: str):
        try:
            self.birthday = datetime.strptime(value.strip(), '%d.%m.%Y')
            # ...
            # Додайте перевірку коректності даних -----------------------------
            # та перетворіть рядок на об'єкт datetime
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Phone(Field):
    # Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
    def __init__(self, value: str) -> None:
        if not self.__validate(value):
            raise PhoneNumberError(
                f"Invalid phone number '{value}'. It should be 10 digits.")
        super().__init__(value)

    @staticmethod
    def __validate(value) -> bool:
        # Перевірка формату телефону (10 цифр)
        return bool(re.match(r'^\d{10}$', value))


class Record:
    # Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.
    def __init__(self, name: str) -> None:
        self.name = Name(name)  # Ім'я контактної особи (обов'язкове)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday):
        # додати валідацію дати -----------------------------------------------
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        # Додавання телефону
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        # Видалення телефону за номером
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        # Редагування телефону
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError(f"Error: phone number '{old_phone}' not found.")

    def find_phone(self, phone_number) -> str | None:
        # Пошук телефону
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phone_numbers = "; ".join([str(phone) for phone in self.phones])
        return f"Contact name: {self.name}, phones: {phone_numbers}"


class AddressBook(UserDict):
    # Клас для зберігання та управління записами.
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name) -> str:
        # Пошук запису за ім'ям
        return self.data.get(name)

    def delete(self, name) -> None:
        # Видалення запису за ім'ям
        if name in self.data:
            del self.data[name]

    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())


def main():

    book = AddressBook()

    handlers.greeting()
    # print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = handlers.parse_input(user_input)

        if command in ["close", "exit", "e", "c"]:
            break

        elif command in ["help", "h", "?"]:
            print(handlers.HELP)
        
        elif command == "hello":
            print(f"\n{Fore.YELLOW}How can I help you?{Style.RESET_ALL}\n")

        elif command == "add":
            print(handlers.add_contact(args, book))
            # реалізація

        elif command == "change":
            ...
            print(handlers.change_contact(args, book))
            # реалізація

        elif command == "phone":
            ...
            # print(show_contact(args, contacts))
            # реалізація

        elif command == "all":
            ...
            # print(show_all_contact(contacts))
            # реалізація

        elif command == "add-birthday":

            ...
            # реалізація

        elif command == "show-birthday":
            ...
            # реалізація

        elif command == "birthdays":
            ...
            # реалізація

        else:
            print("Invalid command.")

    # print(write_db(DB_NAME, contacts))
    print(f"\n{Back.WHITE}Good bye!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
