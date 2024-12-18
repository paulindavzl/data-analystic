import pytest
from src.core.script.processes import Check


# cria uma instância para Check():
@pytest.fixture
def ch():
    return Check()


# testa passar um script válido
def test_check_valid_script(ch):
    script = '''
value1 = 1
value2 = 2

value3 = value1 + value2
'''

    response = ch.is_safe(script)

    assert response == {'result': True}


# testa passar um script com erro de sintaxe
def test_check_invalid_sintaxe(ch):
    script = '''
value1 _ 1
value2 = 2

value3 = value1 + value2
'''

    response = ch.is_safe(script)
    
    assert response == {'result': False, 'err': 'sintaxe_error', 'line': 2}


# testa passar uma função proibida
def test_check_danger_func(ch):
    script = '''
exec(print("Hello, World!"))
'''

    response = ch.is_safe(script)

    assert response == {'result': False, 'err': 'suspect', 'sus': [['exec', 'funct']]}


# tenta importar alguma biblioteca externa
def test_check_danger_import_from(ch):
    script_import = '''
import os

os.system("clear")
'''

    script_from = '''
from subprocess import run

run(['cmd', '/c', 'dir'])
'''

    resp_import = ch.is_safe(script_import)
    resp_from = ch.is_safe(script_from)

    assert resp_import == {'result': False, 'err': 'suspect', 'sus': [['os', 'import']]}

    assert resp_from == {'result': False, 'err': 'suspect', 'sus': [['subprocess', 'import'], ['run', 'from']]}



if __name__ == '__main__':
    pytest.main(['-vv', 'tests/test_processes.py'])