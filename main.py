"""
Address Book Assistant - v0.0.18

Author: Yury Vdovychenko

Date: 2025-03-21

Description:
This program allows users to manage a simple address book with contacts and their phone numbers.
It provides the following commands:
- hello: Greet the bot
- add <name> <phone>: Add a new contact
- change <name> <old_phone> <new_phone>: Change an existing phone number
- phone <name>: Show contact details by name
- all | a : Show all contacts
- add-birthday <name> <birthday>: Add a birthday to a contact (format: DD.MM.YYYY)
- show-birthday <name>: Show the birthday of a contact
- birthdays <days = 7>: Show contacts with birthdays in the next <days> days (default: 7)
- help | h | ? : This help
- close | exit | e | c : Exit
"""

# Imports
from collections import UserDict
from datetime import datetime, timedelta
from colorama import init, Fore, Style
import re
import pickle

# Initializing the colorama
init(autoreset=True)

# Constants
GREETING = """
                ▗▖ ▗▖▗▄▄▄▖▗▖    ▗▄▄▖ ▗▄▖ ▗▖  ▗▖▗▄▄▄▖  ▗▄▄▄▖▗▄▖                  
                ▐▌ ▐▌▐▌   ▐▌   ▐▌   ▐▌ ▐▌▐▛▚▞▜▌▐▌       █ ▐▌ ▐▌                 
                ▐▌ ▐▌▐▛▀▀▘▐▌   ▐▌   ▐▌ ▐▌▐▌  ▐▌▐▛▀▀▘    █ ▐▌ ▐▌                 
                ▐▙█▟▌▐▙▄▄▖▐▙▄▄▖▝▚▄▄▖▝▚▄▞▘▐▌  ▐▌▐▙▄▄▖    █ ▝▚▄▞▘                 
                                                                                  
▗▄▄▄▖▗▖ ▗▖▗▄▄▄▖   ▗▄▖  ▗▄▄▖ ▗▄▄▖▗▄▄▄▖ ▗▄▄▖▗▄▄▄▖▗▄▖ ▗▖  ▗▖▗▄▄▄▖  ▗▄▄▖  ▗▄▖▗▄▄▄▖
  █  ▐▌ ▐▌▐▌     ▐▌ ▐▌▐▌   ▐▌     █  ▐▌     █ ▐▌ ▐▌▐▛▚▖▐▌  █    ▐▌ ▐▌▐▌ ▐▌ █  
  █  ▐▛▀▜▌▐▛▀▀▘  ▐▛▀▜▌ ▝▀▚▖ ▝▀▚▖  █   ▝▀▚▖  █ ▐▛▀▜▌▐▌ ▝▜▌  █    ▐▛▀▚▖▐▌ ▐▌ █  
  █  ▐▌ ▐▌▐▙▄▄▖  ▐▌ ▐▌▗▄▄▞▘▗▄▄▞▘▗▄█▄▖▗▄▄▞▘  █ ▐▌ ▐▌▐▌  ▐▌  █    ▐▙▄▞▘▝▚▄▞▘ █  
                                                                                  
"""

HELP = f"""
{Fore.WHITE}Commands:\n
{Fore.YELLOW}{'hello:':35} {Fore.WHITE}Greet the bot
{Fore.YELLOW}{'add <name> <phone>:':35} {Fore.WHITE}Add new contact
{Fore.YELLOW}{'change <name> <old_phone> <new_phone>:':35} {Fore.WHITE}Change an existing phone number.
{Fore.YELLOW}{'phone <name>:':35} {Fore.WHITE}Show contact details by name
{Fore.YELLOW}{'all | a :':35} {Fore.WHITE}Show all contacts
{Fore.YELLOW}{'add-birthday <name> <birthday>:':35} {Fore.WHITE}Add a birthday to a contact (format: DD.MM.YYYY)
{Fore.YELLOW}{'show-birthday <name>:':35} {Fore.WHITE}Show the birthday of a contact.
{Fore.YELLOW}{'birthdays <days>:':35} {Fore.WHITE}Show contacts with birthdays in the next <days> days.
{Fore.YELLOW}{'help | h | ? :':35} {Fore.WHITE}This help
{Fore.YELLOW}{'close | exit | e | c :':35} {Fore.WHITE}Exit
"""


# Base class
class Field:
    """Base class for fields like Name, Phone, and Birthday."""

    def __init__(self, value) -> None:
        self.value = value

    def __str__(self):
        return str(self.value)

# Class for user name


class Name(Field):
    """Class for storing and validating a contact's name."""

    def __init__(self, value: str) -> None:
        if not value:
            raise ValueError(
                f"\n{Fore.RED}Name is required{Style.RESET_ALL}\n")
        super().__init__(value)

# Class for user's birthday


class Birthday(Field):
    """Class for storing and validating a contact's birthday."""

    def __init__(self, value: str):
        try:
            datetime.strptime(value.strip(), '%d.%m.%Y')
        except ValueError:
            raise ValueError(
                f"{Fore.RED}Invalid date format. Use 'DD.MM.YYYY'{Style.RESET_ALL}")
        else:
            super().__init__(value.strip())


# Class for user's phone number
class Phone(Field):
    """Class for storing and validating a contact's phone number."""

    def __init__(self, value: str) -> None:
        if not bool(re.match(r'^\d{10}$', value)):
            raise ValueError(
                f"{Fore.RED}Invalid phone number '{value}'. It should be 10 digits.{Style.RESET_ALL}")
        super().__init__(value)


# Record class
class Record:
    """Class for storing a contact's details."""

    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_birthday(self, birthday: str) -> None:
        """Add a birthday to the contact."""
        self.birthday = Birthday(birthday)

    def add_phone(self, phone_number: str) -> None:
        """Add a phone number to the contact."""
        self.phones.append(Phone(phone_number))

    def remove_phone(self, phone_number: str) -> None:
        """Remove a phone number from the contact."""
        self.phones = [p for p in self.phones if p.value != phone_number]

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Edit an existing phone number."""
        if self.find_phone(old_phone):
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError(
                f"\n{Fore.RED}Error: phone number '{old_phone}' not found.{Style.RESET_ALL}\n")

    def find_phone(self, phone_number: str) -> str | None:
        """Find a phone number in the contact."""
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def __str__(self):
        phone_numbers = "; ".join([str(phone) for phone in self.phones])
        return f"{Fore.WHITE}Contact name: {Fore.GREEN}{self.name}, {Fore.WHITE}phones: {Fore.YELLOW}{phone_numbers}{Style.RESET_ALL}"

# AddressBook class


class AddressBook(UserDict):
    """Class for storing and managing multiple contacts."""

    def add_record(self, record: Record) -> None:
        """Add a new contact to the address book."""
        self.data[record.name.value] = record

    def find(self, name: str) -> str:
        """Find a contact by name."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Delete a contact by name."""
        if name in self.data:
            del self.data[name]

    def shift_if_weekend(self, date: datetime) -> timedelta:
        """Shift the date if it falls on a weekend."""
        return timedelta(days=(0 if date.weekday() < 5 else 7 - date.weekday()))

# работаю над включением этого метода в класс AddressBook
    def get_upcoming_birthdays(self, days=7):
        """Get contacts with birthdays in the next <days> days."""
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(
                    record.birthday.value, '%d.%m.%Y').replace(year=today.year)
                if (birthday - today).days < 0:
                    birthday = birthday.replace(year=today.year + 1)
                birthday += self.shift_if_weekend(birthday)
                if 0 <= (birthday - today).days <= days:
                    upcoming_birthdays.append(
                        {"name": str(record.name.value), "birthday": birthday.strftime('%d.%m.%Y')})
        return upcoming_birthdays

    def __str__(self):
        return f'\n{Fore.WHITE}' + '\n'.join(str(record) for record in self.data.values()) + f'{Style.RESET_ALL}\n'


# Decorator for error handling
def input_error(func):
    """Decorator to handle errors in user input."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"\n{Fore.RED}{e}{Style.RESET_ALL}\n"
    return wrapper


# Handlers
def greeting():
    """Show a greeting message."""
    print(f"{Fore.GREEN}{GREETING}{Style.RESET_ALL}")
    print(HELP, "\n")


@input_error
def parse_input(user_input):
    """Parse user input into a command and arguments."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args


@input_error
def add_contact(args, book):
    """Add a new contact to the address book."""
    if len(args) < 2:
        raise ValueError(
            f"{Fore.RED}Error: Provide a name and phone number.{Style.RESET_ALL}")
    name, phone = args[0], args[1]
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return f"\n{Fore.GREEN}Contact added successfully!{Style.RESET_ALL}\n"


@input_error
def change_contact(args, book):
    """Change an existing phone number for a contact."""
    if len(args) < 3:
        return f"\n{Fore.RED}Error: Provide a name, old phone, and new phone.{Style.RESET_ALL}\n"
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f"\n{Fore.GREEN}Phone number updated successfully!{Style.RESET_ALL}\n"
    raise ValueError(
        f"\n{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}\n")


@input_error
def show_contact(args, book):
    """Show contact details by name."""
    if len(args) < 1:
        raise ValueError(
            f"{Fore.RED}Error: Provide a name to search for.{Style.RESET_ALL}")
    name = args[0]
    record = book.find(name)
    if record:
        return f"\n{Fore.GREEN}{record}{Style.RESET_ALL}\n"
    raise ValueError(
        f"\n{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}\n")


@input_error
def show_all_contacts(book):
    """Show all contacts in the address book."""
    if len(book.data) == 0:
        raise ValueError(f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}")
    return f"\n{Fore.YELLOW}All contacts:{Style.RESET_ALL}\n{book}"


@input_error
def add_birthday(args, book):
    """Add a birthday to a contact."""
    if len(args) < 2:
        raise ValueError(
            f"{Fore.RED}Error: Provide a name and birthday (DD.MM.YYYY).{Style.RESET_ALL}")
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"\n{Fore.GREEN}Birthday added successfully!{Style.RESET_ALL}\n"
    raise ValueError(
        f"\n{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}\n")


@input_error
def show_birthday(args, book):
    """Show the birthday of a contact."""
    if len(args) < 1:
        raise ValueError(
            f"{Fore.RED}Error: Provide a name to search for.{Style.RESET_ALL}")
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"\n{Fore.WHITE}Birthday: {Fore.GREEN}{record.birthday.value}{Style.RESET_ALL}\n"
    raise ValueError(
        f"{Fore.RED}Error: Birthday for '{name}' not found.{Style.RESET_ALL}")


@input_error
def shift_if_weekend(date):
    """Shift the date if it falls on a weekend."""
    return timedelta(days=(0 if date.weekday() < 5 else 7 - date.weekday()))


@input_error
def get_upcoming_birthdays(args, book):
    """Show contacts with birthdays in the next <days> days."""
    if len(args) < 1:
        args = [7]  # Default to 7 days
    message = ""

    try:
        days = int(args[0])
    except ValueError or TypeError:
        message = f"\n{Fore.RED}Error: Days must be a valid integer number (birthdays <days>).{Style.RESET_ALL}\n"
    else:
        upcoming_birthdays = book.get_upcoming_birthdays(days)
        if upcoming_birthdays == []:
            message = f"\n{Fore.YELLOW}No upcoming birthdays in the next {days} days.{Style.RESET_ALL}\n"
        else:
            message = f"\n{Fore.YELLOW}Upcoming birthdays in the next {days} days:{Style.RESET_ALL}\n"
            for record in upcoming_birthdays:
                message += f"\n{Fore.WHITE}Contact: {Fore.GREEN}{record['name']}, {Fore.WHITE}Birthday: {Fore.YELLOW}{record['birthday']}{Style.RESET_ALL}"
            message += "\n"
    return message


def save_data(book, filename="addressbook.pkl"):
    """Save the address book data to a file."""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Load the address book data from a file or return a new address book if the file is not found."""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# Main function
def main():
    """Main function to run the Address Book Assistant."""
    # book = AddressBook()
    book = load_data()

    greeting()
    while True:
        user_input = input(f"Enter a command: {Fore.WHITE}")
        Style.RESET_ALL

        command, args = parse_input(user_input)

        if command in ["close", "exit", "e", "c"]:
            break

        elif command in ["help", "h", "?"]:
            print(HELP)

        elif command == "hello":
            print(f"\n{Fore.YELLOW}How can I help you?{Style.RESET_ALL}\n")

        elif command in ["add", "ad"]:
            print(add_contact(args, book))

        elif command in ["change", "ch"]:
            print(change_contact(args, book))

        elif command in ["phone", "ph"]:
            print(show_contact(args, book))

        elif command in ["all", "a"]:
            print(show_all_contacts(book))

        elif command in ["add-birthday", "ad-br"]:
            print(add_birthday(args, book))

        elif command in ["show-birthday", "sh-br"]:
            print(show_birthday(args, book))

        elif command in ["birthdays", "br"]:
            print(get_upcoming_birthdays(args, book))

        else:
            print(f"\n{Fore.RED}Invalid command.{Style.RESET_ALL}\n")

    print(f"\n{Fore.WHITE}Goodbye!{Style.RESET_ALL}\n")

    save_data(book)


if __name__ == "__main__":
    main()
