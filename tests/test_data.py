import os
import pytest
from pandas import DataFrame
from src.core import FILES
from src.core.data import Data


@pytest.fixture
def data():
    return Data()


@pytest.fixture()
def create_test_data():
    # esta fixture já fica como teste para new(), save(), remove() e eventualmente remove_all()
    filename = 'for_tests.xlsx'
    data = Data()
    df = data.new({
        'name': [
            'test01', 'test02', 'test03'
        ],
        'years old': [
            0, 0, 0
        ]
    })

    data.save(filename, df, test=True)

    yield filename

    data.remove(filename)


# testa abrir um arquivo
def test_data_open(create_test_data, data):
    resp = data.open('for_tests.xlsx')

    assert resp == {'result': 'Success'}


# tenta passar valores que gerem erros em open()
def test_data_open_errors(data):
    # declara filename com um valor diferente de str
    filename = data.open(0)
    assert filename == {'err': 'type_error', 'data': 0, 'expected': 'str'}

    # declara dtype com um valor diferente de str
    dtype = data.open('filename', dtype=0)
    assert dtype == {'err': 'type_error', 'data': 0, 'expected': 'str'}

    # declara max_lines com um valor diferente de int
    max_lines = data.open('filename', max_lines='0')
    assert max_lines == {'err': 'type_error', 'data': '0', 'expected': 'int'}

    # passa um arquivo que não existe
    resp = data.open('invalid_data.xlsx')
    assert resp == {'err': 'data_not_found', 'data': 'spreadsheet', 'filename': 'invalid_data.xlsx'}

    # passa um valor para dtype que não tem suporte
    dtype_unsupported = data.open('filename', dtype='other')
    assert dtype_unsupported == {'err': 'type_not_supported', 'type': 'other'}


# obtém os valores de uma coluna
def test_data_get_column(create_test_data, data):
    data.open('for_tests.xlsx')

    column = data.get_column('name', True).get('data')

    assert column == ['test01', 'test02', 'test03']


# tenta passar valores que gerem erros em get_column()
def test_data_get_column_errors(data):
    # declara column_name com um valor diferente de str
    column_name = data.get_column(0)
    assert column_name == {'err': 'type_error', 'data': 0, 'expected': 'str'}

    # declara to_list com um valor diferente de bool
    to_list = data.get_column('column_name', to_list=0)
    assert to_list == {'err': 'type_error', 'data': 0, 'expected': 'bool'}

    # tenta obter uma coluna sem abrir a planilha antes
    data_undefined = data.get_column('column_name')
    assert data_undefined == {'err': 'data_not_defined', 'data': 'spreadsheet', 'expected': 'DataFrame'}


# obtém os valores várias colunas
def test_data_get_columns(create_test_data, data):
    data.open('for_tests.xlsx')

    column = data.get_columns('name', 'years old', to_list=True).get('data')

    assert column == [['test01', 0], ['test02', 0], ['test03', 0]]


# tenta passar valores que gerem erros em get_columns()
def test_data_get_columns_errors(data):
    # declara column_name com um valor diferente de str
    column_name = data.get_columns('column_name', 0)
    assert column_name == {'err': 'type_error', 'data': 0, 'expected': 'str'}

    # declara to_list com um valor diferente de bool
    to_list = data.get_columns('column_name', to_list=0)
    assert to_list == {'err': 'type_error', 'data': 0, 'expected': 'bool'}

    # tenta obter uma coluna sem abrir a planilha antes
    data_undefined = data.get_columns('column_name')
    assert data_undefined == {'err': 'data_not_defined', 'data': 'spreadsheet', 'expected': 'DataFrame'}


# passa valores que gerem erros em new():
def test_data_new_errors(data):
    # declara data com um valor diferente de dict
    dt = data.new(0)
    assert dt == {'err': 'type_error', 'data': 0, 'expected': 'dict'}

    # passa um dicionário vazio
    empty = data.new({})
    assert empty == {'err': 'data_empty',  'data': 'spreadsheet'}


# passa valores que gerem erros em save():
def test_data_save_errors(create_test_data, data):
    # declara filename com um valor diferente de str
    filename = data.save(0, {'data': DataFrame()})
    assert filename == {'err': 'type_error', 'data': 0, 'expected': 'str'}

    # declara data com um tipo de dado diferente de DataFrame ou dicionário sem {'data': 'DataFrame'}
    df = data.save('filename', data=[])
    assert df == {'err': 'type_error', 'data': [], 'expected': 'DataFrame'}
    
    # passa um dicionário sem {'data': 'DataFrame'}
    dt = data.save('filename', data={})
    assert dt == {'err': 'type_error', 'data': {}, 'expected': 'DataFrame'} 

    # declara index com um valor diferente de bool
    index = data.save('filename', DataFrame(), index=0)  
    assert index == {'err': 'type_error', 'data': 0, 'expected': 'bool'}

    # declara overwrite com um valor diferente de bool
    overwrite = data.save('filename', DataFrame(), overwrite=0)  
    assert overwrite == {'err': 'type_error', 'data': 0, 'expected': 'bool'}

    # tenta criar uma planilha com um nome que já existe
    exists_filename = data.save('for_tests.xlsx', DataFrame(), overwrite=False)
    assert exists_filename == {'err': 'spreadsheet_already_exists', 'filename': 'for_tests.xlsx'}

    # tenta salvar uma planiha como for_tests.xlsx sem permitir reescrever o arquivo existente
    invalid_filename = data.save('for_tests.xlsx', DataFrame())
    assert invalid_filename == {'err': 'invalid_filename', 'filename': 'for_tests.xlsx'}


# o funcionamento correto de save() assim como os seus erros provam que __file_exists() está funcionando


if __name__ == '__main__':
    pytest.main(['-vv', 'test_data.py'])