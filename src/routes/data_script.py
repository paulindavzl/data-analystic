from flask import Blueprint, request, jsonify
from src.core.script.engine import Engine

script = Blueprint('script', __name__)


# executa comandos passados pelo usuário
@script.route('/run', methods=['POST'])
def run():
    body = request.json
    script = body.get('script')
    if not script:
        return jsonify({'err': 'empty_script'}), 400

    en = Engine(script)
    en.save

    response = en.execute

    if response.get('err'):
        return jsonify(response), 400
    
    return jsonify(response)
    