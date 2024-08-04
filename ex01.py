from datetime import datetime, timedelta
from addressbook import AddressBook
from records import Record, Birthday, Phone, Name

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Error: {e}"
    return wrapper

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add [name] [phone]"
    name, phone = args[:2]
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
    if len(args) < 3:
        return "Usage: change [name] [old_phone] [new_phone]"
    name, old_phone, new_phone = args[:3]
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: phone [name]"
    name = args[0]
    record = book.find(name)
    if record:
        return f"{name}: {', '.join(p.value for p in record.phones)}"
    else:
        return "Contact not found."

@input_error
def show_all(book: AddressBook):
    if book.data:
        return "\n".join([str(record) for record in book.data.values()])
    else:
        return "No contacts found."

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        return "Usage: add-birthday [name] [birthday]"
    name, birthday = args[:2]
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        return "Usage: show-birthday [name]"
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.date.strftime('%d.%m.%Y')}"
    else:
        return "Birthday not found."

@input_error
def birthdays(args, book: AddressBook):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "\n".join([f"{record['name']}'s birthday is on {record['birthday']} (congratulate on {record['congratulation_date']})" for record in upcoming_birthdays])
    else:
        return "No birthdays in the next week."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        
        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("""How can I help you? Possible commands are:
- add [name] [phone]
- change [name] [old_phone] [new_phone]
- phone [name]
- add-birthday [name] [DD.MM.YYYY]
- show-birthday [name]
- birthdays
- all""")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()