import psycopg2


class DBManager:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Подключает к БД PostgreSQL"""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Успешное подключение к базе данных")
        except psycopg2.Error as e:
            print(f"Ошибка подключения к базе данных: {e}")

    def disconnect(self):
        """Отключает от БД PostgreSQL"""
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("Отключение от базы данных")

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        query = """
            SELECT companies.company_name, COUNT(vacancies.vacancies_id) AS vacancies_count
            FROM companies
            LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
            GROUP BY companies.company_name
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        query = """
            SELECT companies.company_name, vacancies.vacancy, vacancies.salary_from, vacancies.link_vacancy
            FROM vacancies
            INNER JOIN companies ON vacancies.company_id = companies.company_id
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        query = "SELECT AVG(salary_from) FROM vacancies"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()
        query = f"SELECT vacancy, salary_from, link_vacancy FROM vacancies WHERE salary_from > {avg_salary}"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        query = f"SELECT vacancy, salary_from, link_vacancy FROM vacancies WHERE vacancy ILIKE '%{keyword}%'"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

