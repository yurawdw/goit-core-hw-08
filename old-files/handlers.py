"""
Assistant helper handlers module
version: pre-alfa 0.0.4
"""
from colorama import Fore, Style
from datetime import datetime

# constants
GREETING = """
                   _  _  ____  __     ___  __   _  _  ____    ____  __
                  / )( \(  __)(  )   / __)/  \ ( \/ )(  __)  (_  _)/  \
                  \ /\ / ) _) / (_/\( (__(  O )/ \/ \ ) _)     )( (  O )
                  (_/\_)(____)\____/ \___)\__/ \_)(_/(____)   (__) \__/
 ____  _  _  ____     __   ____  ____  __  ____  ____  __   __ _  ____    ____   __  ____  _
(_  _)/ )( \(  __)   / _\ / ___)/ ___)(  )/ ___)(_  _)/ _\ (  ( \(_  _)  (  _ \ /  \(_  _)/ \
  )(  ) __ ( ) _)   /    \\___ \\___ \ )( \___ \  )( /    \/    /  )(     ) _ ((  O ) )(  \_/
 (__) \_)(_/(____)  \_/\_/(____/(____/(__)(____/ (__)\_/\_/\_)__) (__)   (____/ \__/ (__) (_)
"""

HELP = """
Available commands:
# \thello : Greet the bot
# \tadd | ad <name> <phone> : Add new contact
# \tchange | ch <name> <old_phone> <new_phone>: Change an existing phone number.
# \tphone | ph <name>: Show contact details by name
# \tall | a : Show all contacts
# \tadd-birthday | ad-br <name> <birthday> : Add a birthday to a contact (format: DD.MM.YYYY)
# \tshow-birthday | sh-br <name>: Show the birthday of a contact.
# \tbirthdays | br <days>: Show contacts with birthdays in the next <days> days.
# \thelp | h | ? : This help
# \tclose | exit | e | c : Exit
"""

def greeting():
    print(f"{Fore.GREEN}{GREETING}{Style.RESET_ALL}")
    print(HELP, "\n")

def parse_input(user_input):
    """Parse user input into a command and arguments."""
    parts = user_input.strip().split()
    command = parts[0].lower() if parts else ""
    args = parts[1:]
    return command, args

def add_contact(args, book):
    """Add a new contact to the address book."""
    if len(args) < 2:
        return f"{Fore.RED}Error: Provide a name and phone number.{Style.RESET_ALL}"
    name, phone = args[0], args[1]
    try:
        record = book.find(name)
        if record:
            record.add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
        return f"{Fore.GREEN}Contact added successfully!{Style.RESET_ALL}"
    except Exception as e:
        return f"{Fore.RED}{e}{Style.RESET_ALL}"

def change_contact(args, book):
    """Change an existing phone number for a contact."""
    if len(args) < 3:
        return f"{Fore.RED}Error: Provide a name, old phone, and new phone.{Style.RESET_ALL}"
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    if record:
        try:
            record.edit_phone(old_phone, new_phone)
            return f"{Fore.GREEN}Phone number updated successfully!{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}{e}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}"

def show_contact(args, book):
    """Show contact details by name."""
    if len(args) < 1:
        return f"{Fore.RED}Error: Provide a name to search for.{Style.RESET_ALL}"
    name = args[0]
    record = book.find(name)
    if record:
        return f"{Fore.GREEN}{record}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}"

def show_all_contacts(book):
    """Show all contacts in the address book."""
    if len(book.data) == 0:
        return f"{Fore.YELLOW}No contacts found.{Style.RESET_ALL}"
    return f"{Fore.GREEN}All contacts:{Style.RESET_ALL}\n{book}"

def add_birthday(args, book):
    """Add a birthday to a contact."""
    if len(args) < 2:
        return f"{Fore.RED}Error: Provide a name and birthday (DD.MM.YYYY).{Style.RESET_ALL}"
    name, birthday = args[0], args[1]
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
            return f"{Fore.GREEN}Birthday added successfully!{Style.RESET_ALL}"
        except Exception as e:
            return f"{Fore.RED}{e}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Error: Contact '{name}' not found.{Style.RESET_ALL}"

def show_birthday(args, book):
    """Show the birthday of a contact."""
    if len(args) < 1:
        return f"{Fore.RED}Error: Provide a name to search for.{Style.RESET_ALL}"
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{Fore.GREEN}Birthday: {record.birthday.birthday.strftime('%d.%m.%Y')}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}Error: Birthday for '{name}' not found.{Style.RESET_ALL}"

def upcoming_birthdays(args, book):
    """Show contacts with birthdays in the next <days> days."""
    if len(args) < 1:
        return f"{Fore.RED}Error: Provide the number of days to search for upcoming birthdays.{Style.RESET_ALL}"
    try:
        days = int(args[0])
        today = datetime.now()
        upcoming_birthdays = []
        for record in book.data.values():
            if record.birthday:
                birthday = record.birthday.birthday.replace(year=today.year)
                if 0 <= (birthday - today).days <= days:
                    upcoming_birthdays.append(record)
        if upcoming_birthdays:
            result = f"{Fore.GREEN}Upcoming birthdays:{Style.RESET_ALL}\n"
            result += "\n".join(str(record) for record in upcoming_birthdays)
            return result
        else:
            return f"{Fore.YELLOW}No upcoming birthdays in the next {days} days.{Style.RESET_ALL}"
    except ValueError:
        return f"{Fore.RED}Error: Days must be a number.{Style.RESET_ALL}"