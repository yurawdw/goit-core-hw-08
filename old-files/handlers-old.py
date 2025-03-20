'''
Personal helper menu module
version: pre-alfa 0.0.4
'''
import sys
from re import search
from pathlib import Path
from colorama import init, Fore, Back, Style
from datetime import datetime, date, timedelta

# Initializing the colorama
init(autoreset=True)

# constants
DB_NAME = './contacts.db'
GREETING = '''
                   _  _  ____  __     ___  __   _  _  ____    ____  __
                  / )( \(  __)(  )   / __)/  \ ( \/ )(  __)  (_  _)/  \
                  \ /\ / ) _) / (_/\( (__(  O )/ \/ \ ) _)     )( (  O )
                  (_/\_)(____)\____/ \___)\__/ \_)(_/(____)   (__) \__/
 ____  _  _  ____     __   ____  ____  __  ____  ____  __   __ _  ____    ____   __  ____  _
(_  _)/ )( \(  __)   / _\ / ___)/ ___)(  )/ ___)(_  _)/ _\ (  ( \(_  _)  (  _ \ /  \(_  _)/ \
  )(  ) __ ( ) _)   /    \\___ \\___ \ )( \___ \  )( /    \/    /  )(     ) _ ((  O ) )(  \_/
 (__) \_)(_/(____)  \_/\_/(____/(____/(__)(____/ (__)\_/\_/\_)__) (__)   (____/ \__/ (__) (_)
'''

HELP = '''
commands:
# \thelp | h | ? : this help
# \thello : print greetings
# \tadd | ad <name> <phone> : add new contact
# \tchange | ch <name> <phone> : change contact's phone
# \tphone | ph <name> : show phone number of <name>
# \tall | a : show all contacts
\tremove | rm <name> : remove contact
\tclear : clear database
# \tclose | exit | e | c : exit
'''

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return f"\nGive me {Fore.YELLOW}name{Style.RESET_ALL} and {Fore.YELLOW}phone{Style.RESET_ALL} please.\n"
        except KeyError:
            return f"\n{Fore.YELLOW}Give me name please.{Style.RESET_ALL}\n"
        except IndexError:
            pass
        except AttributeError:
            return f"\nGive me {Fore.YELLOW}phone{Style.RESET_ALL} please.\n"

    return inner


def greeting():
    print(f"{Fore.GREEN}{GREETING}{Style.RESET_ALL}")
    print(HELP, "\n")

# ----------------------------------------------------------------


def string_to_date(date_string):
    return datetime.strptime(date_string, "%d.%m.%Y").date()


def date_to_string(date_for_string):
    return date_for_string.strftime("%d.%m.%Y")


def find_next_weekday(start_date, weekday):
    days_ahead = weekday - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def adjust_for_weekend(birthday):
    if birthday.weekday() >= 5:
        return find_next_weekday(birthday, 0)
    return birthday


@input_error
def get_upcoming_birthdays(args, book: AddressBook, days=7):
    upcoming_birthdays = []
    today = date.today()
    name, phone, *_ = args
    users_list = book
    
    for user in users_list:
        birthday_this_year = user["birthday"].replace(year=today.year)

        if 0 <= (birthday_this_year.replace(year=today.year + 1) - today).days <= days:
            birthday_this_year = user["birthday"].replace(year=today.year + 1)

        if 0 <= (birthday_this_year - today).days <= days:

            congrat_date = date_to_string(
                adjust_for_weekend(birthday_this_year))

            upcoming_birthdays.append(
                {"name": user["name"], "birthday": congrat_date})
    return upcoming_birthdays


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = f"{Fore.WHITE}Contact updated.{Style.RESET_ALL}"    
    if record:
        if phone:
            record.add_phone(phone)
        else:
            raise AttributeError
    else:
        message = f"Contact {Fore.YELLOW}{name}{Style.RESET_ALL} not found."
    return message
