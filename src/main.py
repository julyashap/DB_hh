from src.hh import HH
from src.db_manager import DBManager
from src.utils import print_list_tuple_vacancies


def main():
    # создание экземпляров
    hh_api = HH()
    db_manager = DBManager("HH_data")

    # создание таблиц в БД
    db_manager.create_tables()

    # взятие данных с API
    employers = hh_api.load_employers(["Билайн", "Сбер", "Яндекс", "Тинькофф", "Альфа",
                                       "Татнефть", "2ГИС", "VK", "Skyeng", "Финам"])
    vacancies = hh_api.load_vacancies()

    # заполнение таблиц данными
    db_manager.fill_tables(employers, vacancies)

    # взаимодействие с данными
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
    print("Список компаний и количество вакансий:")
    for company_and_vacancy_count in companies_and_vacancies_count:
        print(f"{company_and_vacancy_count['employer_name']}: {company_and_vacancy_count['vacancies_count']}")

    all_vacancies = db_manager.get_all_vacancies()
    print("\n\nСписок всех вакансий:")
    for vacancy in all_vacancies:
        if vacancy[2] != 0:
            print(f"Название компании: {vacancy[0]}, название вакансии: {vacancy[1]}, "
                  f"зарплата: {vacancy[2]}\nСсылка: {vacancy[3]}")
        else:
            print(f"Название компании: {vacancy[0]}, название вакансии: {vacancy[1]}, "
                  f"зарплата: не указана\nСсылка: {vacancy[3]}")

    avg_salary = db_manager.get_avg_salary()
    print(f"\n\nСредняя зарплата: {avg_salary}")

    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    print("\n\nВакансии с самой высокой зарплатой:")
    print_list_tuple_vacancies(vacancies_with_higher_salary)

    keyword = input("Введите ключевое слово, которое должно быть в названии вакансии: ")
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
    print(f"Вакансии c '{keyword}':")
    print_list_tuple_vacancies(vacancies_with_keyword)

    # закрытие соединения
    db_manager.cur.close()
    db_manager.conn.close()


if __name__ == '__main__':
    main()
