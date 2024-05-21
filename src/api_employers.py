from abc import ABC, abstractmethod


class APIEmployers(ABC):
    """Абстрактный класс для работы с API сайтов с вакансиями"""

    @abstractmethod
    def __init__(self):
        """Конструктор класса"""
        pass

    @abstractmethod
    def load_employers(self, keywords: list) -> list:
        """Метод для получения списка работодателей по запросу"""
        pass

    @abstractmethod
    def load_vacancies(self):
        """Метод для получения списка вакансий работодателя"""
        pass
