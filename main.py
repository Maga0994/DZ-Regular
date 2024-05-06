
import csv
import re
from pprint import pprint

# Открываем CSV файл и считываем данные
with open('C:\\Users\\user\\Desktop\\DZ Regular\\phonebook_raw.csv', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

def format_phone(phone):
    phone_pattern = r'\+?(\d{1,2})?[\s\(\-\)]*?(\d{3})[\s\(\-\)]*?(\d{3})[\s\(\-\)]*?(\d{2})[\s\(\-\)]*?(\d{2})[\s\(\-\)]*?(доб\.\s*\d{4})?'

    match = re.match(phone_pattern, phone)

    if match:
        groups = match.groups()
        formatted_phone = "+7({}){}-{}-{}".format(groups[1], groups[2], groups[3], groups[4])
        if groups[5]:
            formatted_phone += " доб." + groups[5][5:]  # Обрезаем "доб." и оставляем только номер
        return formatted_phone
    else:
        return None


def format_contacts(raw_contacts):
    formatted_contacts = []
    added_names = set()  # Для хранения добавленных имен
    added_phones = set()  # Для хранения добавленных номеров телефонов

    for contact in raw_contacts[1:]:
        lastname, firstname, surname, organization, position, phone, email = contact

        name_parts = firstname.split()
        if len(name_parts) > 1:
            firstname = name_parts[0]
            surname = " ".join(name_parts[1:])

        formatted_phone = format_phone(phone)

        # Проверка на уникальность контактов по Фамилии и Имени и номеру телефона
        if (lastname, firstname) not in added_names and formatted_phone not in added_phones:
            formatted_contacts.append([lastname, firstname, surname, organization, position, formatted_phone, email])
            added_names.add((lastname, firstname))
            added_phones.add(formatted_phone)

    return formatted_contacts

# Получаем отформатированные данные
formatted_contacts = format_contacts(contacts_list)

# Вывод отформатированных данных
for contact in formatted_contacts:
    # Преобразуем данные в красивый вид и убираем лишние пробелы
    formatted_contact = [str(item).strip() for item in contact if item]
    print(formatted_contact)

# Записываем отформатированные данные в новый CSV файл
output_file = 'formatted_phonebook.csv'
with open(output_file, mode='w', encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Фамилия', 'Имя', 'Отчество', 'Организация', 'Должность', 'Телефон', 'E-mail'])
    for contact in formatted_contacts:
        writer.writerow(contact)


print(f"Данные успешно записаны в файл: {output_file}")

