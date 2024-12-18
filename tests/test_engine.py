import os
import pytest
from src.core.script  import PATH,  IMPORTS
from src.core.script.engine import Engine


# retorna o script
@pytest.fixture
def script():
    script = '''
value1 = 1
value2 = 2

value3 = value1 + value2
'''

    return script


# testa salvar um arquivo
def test_engine_save(script):
    en = Engine(script)
    en.save

    assert en.get == script

    en.delete


# testa executar o script e obter as variáveis
def test_engine_execute(script):
    en = Engine(script)
    en.save

    response = en.execute

    value3 = response.get('variables').get('value3')
    assert value3 == 3


# tenta executar um arquivo inexistente
def test_engine_err_file_not_found():
    en = Engine('')

    response = en.execute

    assert response == {'err': 'file_not_found', 'filename': 'temp_commands.py'}


if __name__ == '__main__':
    pytest.main(['tests/test_engine.py', '-vv'])