from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.validate_phone(value)
        super().__init__(value)

    def validate_phone(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити 10 цифр")

class Birthday(Field):
    def __init__(self, value):
        self.validate_birthday(value)
        self.value = datetime.strptime(value, "%d.%m.%Y")

    def validate_birthday(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Дата народження повинна бути у форматі DD.MM.YYYY")

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        found = False
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                found = True
                break
        if not found:
            raise ValueError(f"Телефон {old_phone} не знайдено")

    def add_birthday(self, birthday):
        if not self.birthday:
            self.birthday = Birthday(birthday)
        else:
            raise ValueError("Цей контакт вже має день народження.")

    def __str__(self):
        phones_str = ', '.join(p.value for p in self.phones)
        birthday_str = f", День народження: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Ім'я контакту: {self.name.value}, Телефони: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def get_birthdays_per_week(self):
        today = datetime.now()
        one_week_ahead = today + timedelta(days=7)
        birthdays_this_week = {}
        for record in self.data.values():
            if record.birthday:
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year <= one_week_ahead:
                    day_of_week = birthday_this_year.strftime("%A")
                    if day_of_week in ["Saturday", "Sunday"]:
                        day_of_week = "Monday"
                    if day_of_week not in birthdays_this_week:
                        birthdays_this_week[day_of_week] = []
                    birthdays_this_week[day_of_week].append(record.name.value)
        for day, names in sorted(birthdays_this_week.items()):
            print(f"{day}: {', '.join(names)}")

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)
    return inner

@input_error
def add_contact(book, name, phone, birthday=None):
    if name in book:
        book[name].add_phone(Phone(phone).value)
        if birthday:
            book[name].add_birthday(birthday)
    else:
        record = Record(name)
        record.add_phone(phone)
        if birthday:
            record.add_birthday(birthday)
        book.add_record(record)
    return "Контакт успішно додано."

@input_error
def change_phone(book, name, new_phone):
    if name in book:
        book[name].edit_phone(Phone(phone).value, new_phone)
    else:
        raise ValueError(f"Контакт з іменем {name} не знайдено.")

@input_error
def show_phone(book, name):
    if name in book:
        return ", ".join(book[name].phones)
    else:
        raise ValueError(f"Контакт з іменем {name} не знайдено.")

@input_error
def show_all_contacts(book):
    if book:
        return "\n".join(str(record) for record in book.values())
    else:
        return "Контактів не знайдено."

@input_error
def add_birthday(book, name, birthday):
    if name in book:
        book[name].add_birthday(birthday)
    else:
        raise ValueError(f"Контакт з іменем {name} не знайдено.")

@input_error
def show_birthday(book, name):
    if name in book:
        if book[name].birthday:
            return book[name].birthday.value.strftime("%d.%m.%Y")
        else:
            return "Дата народження не вказана."
    else:
        raise ValueError(f"Контакт з іменем {name} не знайдено.")

def main():
    book = AddressBook()
    while True:
        command = input("Введіть команду: ").lower()
        if command in ["close", "exit"]:
            print("До побачення!")
            break
        elif command == "hello":
            print("Як я можу вам допомогти?")
        elif command.startswith("add "):
            _, name, phone, *birthday = command.split()
            birthday = birthday[0] if birthday else None
            print(add_contact(book, name, phone, birthday))
        elif command.startswith("change "):
            _, name, new_phone = command.split()
            print(change_phone(book, name, new_phone))
        elif command.startswith("phone "):
            _, name = command.split()
            print(show_phone(book, name))
        elif command == "all":
            print(show_all_contacts(book))
        elif command.startswith("add-birthday "):
            _, name, birthday = command.split()
            print(add_birthday(book, name, birthday))
        elif command.startswith("show-birthday "):
            _, name = command.split()
            print(show_birthday(book, name))
        elif command == "birthdays":
            book.get_birthdays_per_week()
        else:
            print("Невідома команда.")

if __name__ == "__main__":
    main()
