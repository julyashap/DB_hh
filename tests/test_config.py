import pytest
from src.config import config
import os.path


def test_config_with_section():
    path_to_file = os.path.join("..", "src", "database.ini")
    params = config(path_to_file)

    assert type(params) == dict
    assert params['host'] == 'localhost'
    assert params['user'] == 'postgres'
    assert params['port'] == '5432'


def test_config_without_section():
    with pytest.raises(Exception, match='Section postgresql is not found in the database_without_section.ini file.'):
        config("database_without_section.ini")
