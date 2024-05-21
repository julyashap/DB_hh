import pytest
from src.db_manager import DBManager
import os.path


@pytest.fixture()
def db_manager():
    path_to_file = os.path.join("..", "src", "database.ini")

    return DBManager('HH_data_test', path_to_file)


@pytest.fixture()
def employers():
    return [
        {
            'id': 1,
            'name': 'Яндекс',
            'open_vacancies': 23
        },
        {
            'id': 2,
            'name': 'Яндекс.Такси',
            'open_vacancies': 0
        },
        {
            'id': 3,
            'name': 'Сбер',
            'open_vacancies': 3
        }
    ]


@pytest.fixture()
def vacancies():
    return [
        {
            'id': 1,
            'name': 'Python-разработчик',
            'salary': 50000,
            'url': 'https://...',
            'employer': {
                'id': 1
            }
        },
        {
            'id': 2,
            'name': 'Java-разработчик',
            'salary': None,
            'url': 'https://...',
            'employer': {
                'id': 3
            }
        },
        {
            'id': 3,
            'name': 'Тестировщик',
            'salary': {
                'from': 30000
            },
            'url': 'https://...',
            'employer': {
                'id': 3
            }
        },
        {
            'id': 4,
            'name': 'UI-дизайнер',
            'salary': {
                'from': None
            },
            'url': 'https://...',
            'employer': {
                'id': 3
            }
        }
    ]


def test_init(db_manager):
    assert db_manager.conn is not None
    assert db_manager.cur is not None


def test_fill_tables(db_manager, employers, vacancies):
    db_manager.create_tables()

    db_manager.fill_tables(employers, vacancies)

    with db_manager.conn:
        db_manager.cur.execute("select * from employers")
        employers_db = db_manager.cur.fetchall()

        db_manager.cur.execute("select * from vacancies")
        vacancies_db = db_manager.cur.fetchall()

        db_manager.cur.execute("select salary from vacancies where vacancy_id in (2, 4)")
        null_salaries = db_manager.cur.fetchall()

    assert employers_db is not None
    assert len(employers_db) == 2

    assert vacancies_db is not None
    assert len(vacancies_db) == 4

    assert null_salaries[0][0] == 0
    assert null_salaries[1][0] == 0


def test_get_companies_and_vacancies_count(db_manager):
    companies_and_vacancies_count = db_manager.get_companies_and_vacancies_count()

    assert type(companies_and_vacancies_count) == list

    for company_and_vacancy_count in companies_and_vacancies_count:
        assert type(company_and_vacancy_count) == dict

        if company_and_vacancy_count['employer_name'] == 'Сбер':
            assert company_and_vacancy_count['vacancies_count'] == 3


def test_get_all_vacancies(db_manager):
    all_vacancies = db_manager.get_all_vacancies()

    assert type(all_vacancies) == list

    for vacancy in all_vacancies:
        assert type(vacancy) == tuple

    assert all_vacancies[0][0] == 'Яндекс'
    assert all_vacancies[0][1] == 'Python-разработчик'
    assert all_vacancies[0][2] == 50000
    assert all_vacancies[0][3] == 'https://...'


def test_get_avg_salary(db_manager):
    avg_salary = db_manager.get_avg_salary()

    assert avg_salary == 20000


def test_get_vacancies_with_higher_salary(db_manager):
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()

    assert type(vacancies_with_higher_salary) == list

    for vacancy in vacancies_with_higher_salary:
        assert type(vacancy) == tuple

        assert vacancy[1] > 20000


def test_get_vacancies_with_keyword(db_manager):
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword("Python")

    assert type(vacancies_with_keyword) == list

    for vacancy in vacancies_with_keyword:
        assert type(vacancy) == tuple

        assert "Python" in vacancy[0]
