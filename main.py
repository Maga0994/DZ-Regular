
import csv
import re
from pprint import pprint

# Открываем CSV файл и считываем данные
with open('C:\\Users\\user\\Desktop\\DZ Regular\\phonebook_raw.csv', encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


def format_name(full_name):
    # Разбиваем полное имя на части по пробелам
    name_parts = full_name.split()
    # Извлекаем фамилию
    lastname = name_parts[0]
    # Извлекаем имя
    firstname = name_parts[1]
    # Если указано отчество, добавляем его
    surname = name_parts[2] if len(name_parts) > 2 else 'Владимировна'

    return lastname, firstname, surname


def unique_phone_and_email(contact, added_phones, added_emails):
    # Проверка уникальности телефона и email
    phone = contact[5]
    email = contact[6]

    return phone not in added_phones and email not in added_emails


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
    added_phones = set()  # Для хранения добавленных номеров телефонов
    contacts_dict = {}  # Словарь для хранения контактов по ключу (фамилия, имя)

    for contact in raw_contacts[1:]:
        lastname, firstname, surname = format_name(" ".join(contact[:2]))
        organization = contact[3]
        position = contact[4]
        phone = contact[5]
        email = contact[6]

        formatted_phone = format_phone(phone)
        # Проверка на уникальность по номеру телефона
        if formatted_phone not in added_phones:
            added_phones.add(formatted_phone)
        key = (lastname, firstname)

        if key in contacts_dict:
            # Объединяем контакты с одинаковой фамилией и именем
            existing_contact = contacts_dict[key]
            if not existing_contact[3]:
                existing_contact[3] = organization
            if not existing_contact[4]:
                existing_contact[4] = position
            if not existing_contact[5]:
                existing_contact[5] = phone
            if not existing_contact[6]:
                existing_contact[6] = email
        else:
            contacts_dict[key] = [lastname, firstname, surname, organization, position, phone, email]

    # Формируем список отформатированных контактов
    formatted_contacts = [contact for contact in contacts_dict.values()]

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