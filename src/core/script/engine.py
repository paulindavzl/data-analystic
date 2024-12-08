import os
from src.core.script import PATH, IMPORTS

# realiza processos para análise e execução de comandos
class Engine:

    @property
    def save(self):
        with open(f'{PATH}/temp_commands.py', 'w') as file:
            file.write(IMPORTS + self.commands)

    
    @property
    def execute(self):
        # garante que o usuário definiu comandos antes de tentar executar
        if not os.path.exists(PATH + '/temp_commands.py'):
            return {'err': 'file_not_found', 'filename': 'temp_commands.py'}

        # executa os comandos do usuário
        from src.core.script import temp_commands