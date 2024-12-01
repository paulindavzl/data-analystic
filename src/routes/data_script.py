from flask import Blueprint, request, jsonify
from src.core.script import execute

script = Blueprint('script', __name__)

# rota usada para executar um script
@script.route('/run', methods=['POST'])
def run():
    data = request.json
    script = data.get('script')
    section = data.get('section')

    # verifica se o usuário passou um script
    if not script:
        return jsonify({'err': 'script_empty'}), 400
    elif not section:
        return jsonify({'err': 'section_empty'}), 400
    elif not section.idigit():
        return jsonify({'err': 'invalid_section_value'}), 400

    response = execute(script) # executa o script do usuário
    
    # verifica se houve um erro na execução
    if response.get('err'):
        err = response.get('err')

        if err == 'invalid_sintaxe':
            return jsonify(response), 422
        elif err == 'not_found':
            return jsonify(response), 404

    return jsonify(response), 200