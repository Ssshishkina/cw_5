import requests
import psycopg2


def gets_jobs(employer_ids):
    """Делает запрос по API hh.ru,
    получает по 100 вакансий для каждой компании,
    загружает информации в таблицы PostgreSQL
    """

    # URL-адрес API hh.ru для поиска вакансий
    url = 'https://api.hh.ru/vacancies'

    # Параметры запроса
    params = {
        'per_page': 100
    }

    # Установка соединения с базой данных
    conn = psycopg2.connect(
        host="localhost",
        database="hh.ru",
        user="postgres",
        password="4242"
    )

    # Создание курсора
    cursor = conn.cursor()

    # Удаление старых вакансий
    cursor.execute("""
            TRUNCATE TABLE vacancies RESTART IDENTITY
        """)

    for employer_id in employer_ids:
        params['employer_id'] = employer_id

        # Отправка GET-запроса
        response = requests.get(url, params=params)

        # Проверка статуса ответа
        if response.status_code == 200:
            # Получение данных в формате JSON
            data = response.json()

            for vac in data['items']:
                company = vac['employer']['name']
                title = vac['name']
                area = vac['area']['name']
                salary_from = vac["salary"].get("from", 0) if vac["salary"] is not None else 0
                currency = vac["salary"].get("currency") if vac["salary"] is not None else None
                link = vac['alternate_url']

                # Вставка данных в таблицу компаний
                cursor.execute("""
                    INSERT INTO companies (company_id, company_name)
                    VALUES (%s, %s)
                    ON CONFLICT (company_id) DO NOTHING
                """, (employer_id, company))

                # Вставка данных в таблицу вакансий
                cursor.execute("""
                               INSERT INTO vacancies (company_id, vacancy, city, salary_from, currency, link_vacancy)
                               VALUES (%s, %s, %s, %s, %s, %s)
                           """, (employer_id, title, area, salary_from, currency, link))
        else:
            print(
                f'Ошибка при получении данных для компании с идентификатором {employer_id}. Код ошибки: {response.status_code}')

    # Закрытие курсора и сохранение изменений
    cursor.close()
    conn.commit()
    conn.close()

