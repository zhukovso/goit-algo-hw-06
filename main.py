from collections import UserDict
import re

# Decorator with error handler
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PhoneNumberValidationError as e:
            print(e)
        except PhoneNumberNotFound as e:
            print(e)
    return inner

class PhoneNumberValidationError(Exception):
    pass

class PhoneNumberNotFound(Exception):
    pass


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate_phone_number(value):
            raise PhoneNumberValidationError(f"Phone number {value} should contain exactly 10 digits..")
        super().__init__(value)

    # TODO: validate_phone_number make static
    def validate_phone_number(self, phone_number: str) -> bool:
        cleaned_number = re.sub(r'\D', '', phone_number)
        return len(cleaned_number) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    @input_error
    def add_phone(self, phone_number: str):
        self.phones.append(Phone(phone_number))
        return self

    @input_error
    def remove_phone(self, phone_number: str) -> None:
        if not self.find_phone(phone_number):
            raise PhoneNumberNotFound(f"While remove, phone number {phone_number} was not found in {self.name.value} numbers..")
        if Phone(phone_number):
            self.phones = [phone for phone in self.phones if phone.value != phone_number]

    @input_error
    def edit_phone(self, old_phone_number: str, new_phone_number: str) -> None:
        found_phone = next((phone for phone in self.phones if phone.value == old_phone_number), None)
        if not found_phone:
            raise PhoneNumberNotFound(f"While edit, phone number {old_phone_number} was not found in {self.name.value} numbers..")
        if Phone(new_phone_number):
            found_phone.value = new_phone_number

    def find_phone(self, phone: str) -> Phone:
        return next((item for item in self.phones if item.value == phone), None)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record
        return self
    
    def find(self, name: str) -> Record:
        return next((value for key, value in self.data.items() if key.value == name), None)

    def delete(self, name):
        self.data = {key: value for key, value in self.data.items() if key.value != name}


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")


    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Додавання запису Bill до адресної книги
    # book.add_record(Record("Bill").add_phone("3333333333").add_phone("2222222222"))

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    # john.edit_phone("1234567890", "1112223333")
    # john.edit_phone("1112223333", "123456789")
    # john.remove_phone("1234567890")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

    # Видалення запису Jane
    book.delete("Jane")
