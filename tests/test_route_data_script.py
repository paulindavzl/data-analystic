import pytest
from src.main import app


# retorna a aplicação para testes
@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    app.config['TESTING'] = False


# retorna a url
@pytest.fixture
def url():
    return '/script/run'


# tenta executar um script válido
def test_data_script_run(client, url):
    body = {
        'script': '''
value1 = 1
value2 = 2

value3 = value1 + value2'''}

    request = client.post(url, json=body)
    response = request.json
    variables = response.get('variables')
    value3 = variables.get('value3')

    assert value3 == 3


# tenta passar um script com erro de sintaxe
def test_data_script_sintaxe_error(client, url):
    body = {
        'script': '''
value1 1
value2 = 2
'''}

    request = client.post(url, json=body)
    response = request.json
    err = response.get('err')
    line = response.get('line')

    assert err == 'sintaxe_error'
    assert line == 2


# tenta passar um script com uuma função proibida
def test_data_script_danger_func(client, url):
    body = {
        'script': '''
exec("print('Hello, World!')")
'''
    }

    request = client.post(url, json=body)
    response = request.json
    err = response.get('err')
    e_type = response.get('sus')

    assert err == 'suspect'
    assert e_type == [['exec', 'funct']]


# tenta passar um script que faz importações
def test_data_script_import_from(client, url):
    body1 = {
        'script': '''
import database
'''
    }

    body2 = {
        'script': '''
from os import system
'''
    }

    request1 = client.post(url, json=body1)
    response1 = request1.json
    err1 = response1.get('err')
    e_type1 = response1.get('sus')

    assert err1 == 'suspect'
    assert e_type1 == [['database', 'import']]

    request2 = client.post(url, json=body2)
    response2 = request2.json
    err2 = response2.get('err')
    e_type2 = response2.get('sus')

    assert err2 == 'suspect'
    assert e_type2 == [['os', 'import'], ['system', 'from']]


if __name__ == '__main__':
    pytest.main(['-vv', 'tests/test_route_data_script.py'])