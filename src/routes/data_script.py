from flask import Blueprint, request
from src.core.script import engine

script = Blueprint('script', __name__)


# executa comandos passados pelo usuário
@script.route('/run')
def run():
    
    return '0'