from function import gets_jobs
from src.cls_DBManager import DBManager

# Список идентификаторов работодателей Яндекс, МТС, СБЕР, Tinkoff, Аэрофлот, Озон, Магнит, РЖД, Альфа-банк, Пятерочка
employer_ids = [1740, 3776, 3529, 78638, 1373, 2180, 49357, 23427, 80, 1942330]

gets_jobs(employer_ids)

db_manager = DBManager("localhost", "hh.ru", "postgres", "4242")
db_manager.connect()

print('Привет!')
print('')
print('Нажмите 1 если хотите получить список всех доступных компаний и количества вакансий')
print('Нажмите 2 если хотите получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию')
print('Нажмите 3 если хотите получить среднюю зарплату по всем вакансиям')
print('Нажмите 4 если хотите получить список вакансий с зарплатой выше средней')
print('Нажмите 5 если хотите получить список вакансий по Вашему запросу')
print('Ни в коем случае не жмите 6 !')

while True:
    user_input = input()
    if user_input == '1':
        print("Хорошо, вы выбрали '1' ")
        print("Вот список всех доступных компаний и количества вакансий: ")
        companies_with_vacancies  = db_manager.get_companies_and_vacancies_count()
        for company, vacancies_count in companies_with_vacancies:
            print(f"Компания: {company}, Количество вакансий: {vacancies_count}")
        db_manager.disconnect()
        break
    elif user_input == '2':
        print("Хорошо, вы выбрали '2' ")
        print("Вот список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию: ")
        all_vacancies = db_manager.get_all_vacancies()
        for company, vacancy, salary_from, link in all_vacancies:
            if salary_from == 0 or None:
                salary_from = 'Нет данных по зарплате'
                print(f"Компания: {company}, Вакансия: {vacancy}, Зарплата: {salary_from}, Ссылка: {link}")
        db_manager.disconnect()
        break
    elif user_input == '3':
        print("Хорошо, вы выбрали '3' ")
        print("Вот средняя зарплата по всем вакансиям: ")
        avg_salary = db_manager.get_avg_salary()
        print(f'{round(avg_salary)} руб')
        db_manager.disconnect()
        break
    elif user_input == '4':
        print("Хорошо, вы выбрали '4' ")
        print("Вот список вакансий с зарплатой выше средней: ")
        vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
        for vacancy, salary, link in vacancies_with_higher_salary:
            print(f"Вакансия: {vacancy}, Зарплата: {salary}, Ссылка: {link}")
        db_manager.disconnect()
        break
    elif user_input == '5':
        print("Хорошо, вы выбрали '5', введите данные для поиска ")
        user_keyword = input()
        print(f"Вот список вакансий по Вашему запросу - '{user_keyword}': ")
        vacancies_with_keyword = db_manager.get_vacancies_with_keyword(user_keyword)
        for vacancy, salary_from, link in vacancies_with_keyword:
            if salary_from == 0 or None:
                salary_from = 'Нет данных'
                print(f"Вакансия: {vacancy}, Зарплата: {salary_from}, Ссылка: {link}")
        db_manager.disconnect()
        break
    elif user_input == '6':
        print("Поздравляю, ты люпопытный человек, тебе ж сказали не нажимать, давай ка заново! ")
    else:
        print("Введите корректные данные - числа 1, 2, 3, 4, 5")

