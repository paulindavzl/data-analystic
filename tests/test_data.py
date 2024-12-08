import os
import pytest
from src.core import FILES
from src.core.data import Data

@pytest.fixture()
def create_test_data():
    filename = 'for_tests.xlsx'
    data = Data()
    df = data.new({
        'name': [
            'test01', 'test02', 'test03'
        ],
        'years old': [
            0, 0, 0
        ]
    }).get('data')

    data.save(filename, df, test=True)

    yield filename

    data.remove(filename)


# testa abrir um arquivo
def test_data_open(create_test_data):
    resp = Data().open('for_tests.xlsx')

    assert resp == {'result': 'Success'}


if __name__ == '__main__':
    pytest.main(['-vv', 'test_data.py'])