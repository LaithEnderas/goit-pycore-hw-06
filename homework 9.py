from collections import UserDict

class Field: #створюємо клас для збереження даних та їх форматування у str
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field): #клас для імені, який видаляє пробіли
    def __init__(self, value):
        super().__init__(value.strip())

class Phone(Field): #клас для фільтрації номеру телефону
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Телефон має містити 10 цифр")
        super().__init__(value)

class Record: #основний клас
    def __init__(self, name):
        self.name = Name(name) 
        self.phones = []  #словник для номерів телефону

    def add_phone(self, phone): #використовуємо клас Phone для додавання номеру у список
        try:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        except ValueError as e:
            print(f"Не вдалося додати номер: '{phone}'. {e}")

    def edit_phone(self, old_phone, new_phone): #метод для редагування номеру
        for phone in self.phones:
            if phone.value == old_phone: #перевіряємо, чи інує цей номер у списку
                try:
                    phone.value = Phone(new_phone).value #за допомогою класу Phone замінюємо значення номеру 
                    print(f"Телефон '{old_phone}' змінено на '{new_phone}'")
                    return
                except ValueError as e:
                    print(f"Помилка зміни номера: {e}")
                    return
        print(f"Телефон '{old_phone}' не знайдено у записі {self.name.value}")

    def find_phone(self, phone): #метод для пошуку номера
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def delete_phone(self, phone): #метод для видалення номеру
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                print(f"Телефон '{phone}' видалено")
                return
        print(f"Телефон '{phone}' не знайдено")

    def __str__(self): #повернення данних у читабельному вигляді
        phones_str = "; ".join(str(p) for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"

class AddressBook(UserDict): #наш "словник" із контактами
    def __init__(self):
        super().__init__()

    def add_record(self, record): #вносимо інформацію до книги
        self.data[record.name.value] = record

    def find(self, name): #метод для пошуку імені у книзі
        return self.data.get(name, None)

    def delete(self, name): #метод для видалення записів
        if name in self.data:
            del self.data[name]
            print(f"Запис '{name}' видалено")
        else:
            print(f"Запис '{name}' не знайдено")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
    
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

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

# Знаходження та редагування телефону для John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# Видалення запису Jane
book.delete("Jane")

