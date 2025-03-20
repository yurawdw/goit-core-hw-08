'''
Personal helper menu module
version: pre-alfa 0.0.4 
'''
import sys
from re import search
from pathlib import Path
from colorama import init, Fore, Back, Style

# Initializing the colorama
init(autoreset=True)

# constants
DB_NAME = './contacts.db'
GREATING = '''
   ____  ____  ____  ____   __   __ _   __   __        
  (  _ \(  __)(  _ \/ ___) /  \ (  ( \ / _\ (  )       
   ) __/ ) _)  )   /\___ \(  O )/    //    \/ (_/\     
  (__)  (____)(__\_)(____/ \__/ \_)__)\_/\_/\____/     
 _  _  ____  __    ____  ____  ____    ____   __  ____ 
/ )( \(  __)(  )  (  _ \(  __)(  _ \  (  _ \ /  \(_  _)
) __ ( ) _) / (_/\ ) __/ ) _)  )   /   ) _ ((  O ) )(  
\_)(_/(____)\____/(__)  (____)(__\_)  (____/ \__/ (__)                                      
'''

HELP = '''
commands:
\thelp | h | ? : this help
\thello : print greetings
\tadd | ad <name> <phone> : add new contact
\tchange | ch <name> <phone> : change contact's phone
\tphone | ph <name> : show phone number of <name>
\tall | a : show all contacts
\tremove | rm <name> : remove contact
\tclear : clear database
\tclose | exit | e : exit
'''


def greatting():
    print(f"{Fore.GREEN}{GREATING}{Style.RESET_ALL}")
    print(HELP, "\n")


def max_field_length(data: dict):
    """
    Calculating the maximum length among dictionary fields. Preparing for future use
    """
    if not data:
        return 0
    return max(len(str(key)) for key in data.keys())


def normalize_phone(phone_number: str) -> str:
    '''
    Clear the phone number
    '''
    return search(r'-?\d+(\.\d+)?', phone_number).group()


def parse_input(user_input: str):
    '''
    User input processing
    '''
    cmd, *args = user_input.strip().split()
    return cmd.lower(), *args


def add_contact(args, contacts: dict):
    '''
    Adding user's information
    '''
    if len(args) < 2:
        return f"\n{Fore.RED}Enter the correct information: <name> <phone>{Style.RESET_ALL}\n"

    *name_parts, phone = args
    name = " ".join(name_parts).strip()
    phone = normalize_phone(args.pop())

    if name in contacts:
        return f"'{name}' {Fore.GREEN}already exists. Rejected{Style.RESET_ALL}\n"

    contacts[name] = phone
    return f"{Fore.GREEN}Contact added.{Style.RESET_ALL}\n"


def change_contact(args, contacts: dict):
    '''
    Changing user's information
    '''
    if len(args) < 2:
        return f"\n{Fore.YELLOW}Enter correct information: <name> <phone>{Style.RESET_ALL}\n"

    *name_parts, phone = args
    name = " ".join(name_parts).strip()
    phone = normalize_phone(phone)

    if not (name in contacts):
        return f"'{name}' {Fore.YELLOW}does not exists. Add it first{Style.RESET_ALL}\n"

    contacts[name] = phone
    return f"{Fore.GREEN}Contact changed.{Style.RESET_ALL}\n"


def show_contact(args, contacts: dict):
    '''
    Show information about user
    '''
    if not args:
        return f"\n{Fore.YELLOW}Enter correct information: show <name>{Style.RESET_ALL}\n"

    name = " ".join(args).strip()

    return f"\n{name}'s {Fore.WHITE}phone number is {contacts.get(name)}\n" if contacts.get(name) else f"\n'{name}' {Fore.RED}does not exist.{Style.RESET_ALL}\n"


def show_all_contact(contacts: dict):
    '''
    Show all information
    '''
    column_one = 15
    column_two = 20
    l = column_one + column_two + 3

    if not contacts:
        return f"{Fore.YELLOW}Phone book is empty.{Style.RESET_ALL}"

    result = "\n" + "-" * l + "\n"
    result += "|" + "Name".center(column_one) + \
        "|" + "Phone".center(column_two) + "|\n"
    result += "-" * l + "\n"

    for name, phone in contacts.items():
        result += "|" + name.center(column_one) + \
            "|" + phone.center(column_two) + "|\n"
        result += "-" * l + "\n"

    return result


def remove_contact(args, contacts: dict):
    '''
    Removing information about user
    '''
    if not args:
        return f"\n{Fore.YELLOW}Enter correct information: remove <name>{Style.RESET_ALL}\n"

    # *name_parts, phone = args
    name = " ".join(args).strip()

    if not (name in contacts):
        return f"'{name}' {Fore.YELLOW}does not exists. Add it first{Style.RESET_ALL}\n"

    del contacts[name]

    return f"{Fore.GREEN}Contact removed.{Style.RESET_ALL}\n"


def clear_contact(contacts: dict):
    '''
    Delete all information from the database
    '''
    contacts.clear()
    return f"{Fore.YELLOW}Phone book is empty.{Style.RESET_ALL}\n"


def read_db(db_name, contacts: dict):
    '''
    Reading information from the database
    '''
    with open(db_name, 'r') as db:
        contacts_data = db.readlines()

    for st in contacts_data:
        add_contact(st.split(';'), contacts)


def write_db(db_name, contacts: dict):
    '''
    Writing information to the database
    '''
    if db_is_exist(db_name):
        answer = input(
            f"{Fore.RED}The database exists. Do you want to rewrite all the data? (y/N):{Style.RESET_ALL} ").lower().strip()
        if answer != 'y':
            return f"{Fore.YELLOW}The database was not updated.{Style.RESET_ALL}\n"

    with open(db_name, 'w') as db:
        for name, phone in contacts.items():
            db.writelines(f"{name};{phone}\n")
    return f"{Fore.GREEN}The database was updated.{Style.RESET_ALL}\n"


def db_is_exist(path) -> bool:
    '''
    Checking the existence of a database file
    '''
    return (True if Path(path).exists() else False)


def main():
    """
    Main function to execute the script.
    """

    greatting()

    contacts = {}

    if db_is_exist(DB_NAME):
        read_db(DB_NAME, contacts)

    while True:
        user_input = input(
            f"{Fore.WHITE}Enter a command or 'h' for help:{Style.RESET_ALL} ")
        if user_input:
            command, *args = parse_input(user_input)
            command = command.lower().strip()
        else:
            command = "help"

        if command in ["close", "exit", "e"]:
            break
        # elif command in ["help", "h", "?"]:
        #     print(HELP)
        # elif command in ["hello", "h"]:
        #     print(f"\n{Fore.YELLOW}How can I help you?{Style.RESET_ALL}\n")
        # elif command in ["add", "ad"]:
        #     print(add_contact(args, contacts))
        # elif command in ["change", "ch"]:
        #     print(change_contact(args, contacts))
        # elif command in ["phone", "ph"]:
        #     print(show_contact(args, contacts))
        # elif command in ["all", "a"]:
        #     print(show_all_contact(contacts))
        elif command in ["remove", "rm"]:
            print(remove_contact(args, contacts))
        elif command == "clear":
            answer = input(
                f"{Fore.RED}Are you sure to clear all data? (y/N):{Style.RESET_ALL} ").lower().strip()
            if answer == "y":
                print(clear_contact(contacts))
                print("\n")
            else:
                print("\n")
        else:
            print(f"{Fore.YELLOW}Invalid command.{Style.RESET_ALL}\n")

    print(write_db(DB_NAME, contacts))
    print(f"\n{Back.WHITE}Good bye!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
