from src.abstract_db_manager import AbstractDBManager
import psycopg2
from src.config import config


class DBManager(AbstractDBManager):
    def __init__(self, db_name: str):
        """Конструктор класса"""
        params = config()

        self.conn = psycopg2.connect(dbname=db_name, **params)
        self.cur = self.conn.cursor()

    def create_tables(self):
        """Создает таблицы в базе данных"""
        self.conn.autocommit = True

        self.cur.execute("drop table if exists vacancies")
        self.cur.execute("drop table if exists employers")

        self.cur.execute("create table employers ("
                         "employer_id int primary key, "
                         "employer_name varchar not null, "
                         "open_vacancies int not null, "
                         "constraint chk_employers_open_vacancies check (open_vacancies >= 0))")

        self.cur.execute("create table vacancies ("
                         "vacancy_id int primary key, "
                         "vacancy_name varchar not null, "
                         "salary int default 0, "
                         "vacancy_url varchar, "
                         "employer_id int, "
                         "constraint chk_vacancies_salary check (salary >= 0), "
                         "constraint chk_vacancies_vacancy_url check (vacancy_url like 'https://%'), "
                         "foreign key (employer_id) references employers(employer_id))")

    def fill_tables(self, employers: list, vacancies: list) -> None:
        """Заполняет базу данных переданными значениями"""

        self.conn.autocommit = True

        for employer in employers:
            if employer['open_vacancies'] == 0:
                continue

            self.cur.execute("insert into employers (employer_id, employer_name, open_vacancies) "
                             "values (%s, %s, %s)", (employer['id'], employer['name'], employer['open_vacancies']))

        for vacancy in vacancies:
            if not vacancy.get('salary') or vacancy.get('salary').get('from') is None:
                vacancy_salary = 0
            elif vacancy.get('salary').get('from'):
                vacancy_salary = vacancy['salary']['from']
            else:
                vacancy_salary = vacancy['salary']

            self.cur.execute("insert into vacancies (vacancy_id, vacancy_name, salary, vacancy_url, "
                             "employer_id) values (%s, %s, %s, %s, %s)",
                             (vacancy['id'], vacancy['name'], vacancy_salary,
                              vacancy['url'], vacancy['employer']['id']))

    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        with self.conn:
            self.cur.execute("select employer_name, count(*) from employers "
                             "join vacancies using(employer_id) "
                             "group by employer_name")
            companies_and_vacancies_count = self.cur.fetchall()

        companies_and_vacancies_count_result = []
        for company_and_vacancy_count in companies_and_vacancies_count:
            companies_and_vacancies_count_result.append({'employer_name': company_and_vacancy_count[0],
                                                         'vacancies_count': company_and_vacancy_count[1]})

        return companies_and_vacancies_count_result

    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        with self.conn:
            self.cur.execute("select employer_name, vacancy_name, salary, vacancy_url "
                             "from vacancies join employers using(employer_id)")
            all_vacancies = self.cur.fetchall()

        return all_vacancies

    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям"""
        with self.conn:
            self.cur.execute("select avg(salary) from vacancies")
            avg_salary = self.cur.fetchone()

        avg_salary_result = avg_salary[0]

        return avg_salary_result

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        avg_salary = self.get_avg_salary()

        with self.conn:
            self.cur.execute(f"select vacancy_name, salary, vacancy_url "
                             f"from vacancies where salary > {avg_salary}")
            vacancies_with_higher_salary = self.cur.fetchall()

        return vacancies_with_higher_salary

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        with self.conn:
            self.cur.execute(f"select vacancy_name, salary, vacancy_url "
                             f"from vacancies where vacancy_name like '%{keyword}%'")
            vacancies_with_keyword = self.cur.fetchall()

        return vacancies_with_keyword
