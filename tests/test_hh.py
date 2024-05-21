import pytest
from src.hh import HH


@pytest.fixture()
def hh():
    return HH()


def test_init(hh):
    assert hh.url == 'https://api.hh.ru/employers'
    assert str(hh.headers) == "{'User-Agent': 'HH-User-Agent'}"
    assert str(hh.params) == "{'text': '', 'area': 1, 'page': 0, 'per_page': 100}"
    assert str(hh.employers) == '[]'


def test_load_employers(hh):
    keywords = ['Яндекс', 'Сбер']
    employers = hh.load_employers(keywords)

    assert type(employers) == list
    for employer in employers:
        assert type(employer) == dict


def test_load_vacancies(hh):
    vacancies = hh.load_vacancies()

    assert type(vacancies) == list
    for vacancy in vacancies:
        assert type(vacancy) == dict
