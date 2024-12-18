import os
import json
from src.core.script import PATH, IMPORTS
from src.core.script.processes import Check

# realiza processos para análise e execução de comandos
class Engine:

    def __init__(self, commands: str):
        self.commands = commands
        

    @property
    def save(self):
        with open(PATH + '/temp_commands.py', 'w') as file:
            file.write(self.commands)

    
    @property
    def get(self):
        if os.path.exists(PATH + '/temp_commands.py'):
            with open(PATH + '/temp_commands.py', 'r') as file:
                return file.read()

        return False

    
    @property
    def execute(self):
        commands = self.get

        # garante que o usuário definiu comandos antes de tentar executar
        if not commands:
            return {'err': 'file_not_found', 'filename': 'temp_commands.py'}

        is_safe = Check().is_safe(commands)
        if not is_safe.get('result'):
            return is_safe
            
        try:
            variables = {}
            exec(IMPORTS + commands, {}, variables)

            self.delete

            serializable = {
                str(key): value for key, value in variables.items()
                if self.is_serializable(value) and key != 'Data'
            }
            return {'result': 'Success', 'variables': serializable}
        except Exception as err:
            return {'err': str(err)}


    # verifica se o valor pode ser serializado para ser json
    def is_serializable(self, value):
        try:
            json.dumps(value)
            return True
        except:
            return False

    
    @property
    def delete(self):
        if os.path.exists(PATH + '/temp_commands.py'):
            os.remove(PATH + '/temp_commands.py')
