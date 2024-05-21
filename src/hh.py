from src.api_employers import APIEmployers
import requests


class HH(APIEmployers):
    """Класс для работы с API сайта hh.ru"""

    def __init__(self):
        """Конструктор класса HHCompanies"""

        self.url = 'https://api.hh.ru/employers'
        self.headers = {'User-Agent': 'HH-User-Agent'}
        self.params = {'text': '', 'area': 1, 'page': 0, 'per_page': 100}  # area = 1 - область поиска = Россия
        self.employers = []

    def load_employers(self, keywords: list) -> list:
        """Метод для получения списка работодателей по запросу"""

        for keyword in keywords:
            self.params['text'] = keyword
            self.params['page'] = 0

            while self.params.get('page') != 20:
                response = requests.get(self.url, headers=self.headers, params=self.params)
                employers = response.json()['items']
                self.employers.extend(employers)
                self.params['page'] += 1

        return self.employers

    def load_vacancies(self) -> list:
        """Метод для получения списка вакансий работодателя"""
        all_vacancies = []

        for employer in self.employers:
            url = employer.get('vacancies_url')
            response = requests.get(url)
            vacancies = response.json()['items']
            all_vacancies.extend(vacancies)

        return all_vacancies
