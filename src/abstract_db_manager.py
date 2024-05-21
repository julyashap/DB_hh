from abc import ABC, abstractmethod


class AbstractDBManager(ABC):
    """Абстрактный класс для соединения с базой данных с компаниями и вакансиями"""

    @abstractmethod
    def __init__(self, db_name: str):
        """Конструктор класса"""
        pass

    @abstractmethod
    def create_tables(self) -> None:
        """Создает таблицы в базе данных"""
        pass

    @abstractmethod
    def fill_tables(self, employers: list, vacancies: list) -> None:
        """Заполняет базу данных переданными значениями"""
        pass

    @abstractmethod
    def get_companies_and_vacancies_count(self) -> list[dict]:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        pass

    @abstractmethod
    def get_all_vacancies(self) -> list[tuple]:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    @abstractmethod
    def get_avg_salary(self) -> int:
        """Получает среднюю зарплату по вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        pass
