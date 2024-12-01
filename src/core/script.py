import time
from typing import Optional as Op

# executa scripts
def execute(script: str):
    save(script) # salva o script em um arquivo

    with open('script.da', 'r') as file:
        script_line = 1
        transalated_script = '' # armazena um script python traduzido

        for line in file.readlines():
            response = check_script(line)
            
            # verifica se houve erro
            if response.get('err'):
                response['line'] = script_line
                return response
            script_line += 1

            transalated_script += response.get('script')

        # cria um arquivo .py
        save(transalated_script, type='py')

        # executa o arquivo .py
        execute_py()


# executa um arquivo python
def execute_py():
    import translated_script


# salva o script para análise e execução
def save(script: str, type: Op['str']='da'):
    if type == 'da':
        with open('./script.da', 'w') as file:
            file.write(script)
        
        return 0
    
    with open('translated_script.py', 'w') as file:
        file.write(script)


# verifica o script
def check_script(script: str):
    char = 1
    funct = [False, ''] # define se há uma função ativa
    special_chars = ['$', '=', '>', '<', '!']
    content = '' # conteúdo da função
    translate = '' # script tranduzido para Python
    receive = False

    for i in script:
        # se o primeiro caractére não for $ e não for uma função (erro)
        if char == 1 and not i == '$' and not funct[0] and funct[1] == '':
            return {'err': 'invalid_sintaxe', 'char': char}
        
        # se i for $ mas uma função já estiver ativa (erro)
        elif i == '$' and funct[0]:
            return {'err': 'invalid_sintaxe', 'char': char}
        
        # se o primeiro caractére do conteúdo de uma função for um número (erro)
        elif not i in special_chars and not funct[0] and content == '' and i.isdigit():
            return {'err': 'invalid_sintaxe', 'char': char}
        
        # se i $ inicia uma função
        elif i == '$':
            funct = [True, i]

        # se i é ' ' e tem função ativa então adiciona conteúdo
        elif i == ' ' and funct[0]:
            funct[0] = False
        
        # se uma função está ativa e i é válido (insere no conteúdo)
        elif not i in special_chars and funct[0]:
            funct[1] += i

        # verifica se está recebendo um valor
        elif not i == ' ' and receive:
            translate = translate[:len(translate)-1]
            translate += i + '"'

        # se i é ' ' e tem função ativa
        elif i == ' ' and content != '':
            translate += parser(funct[1], content) + ' '
            funct = [False, '']
            content = ''
        
        # adiciona conteúdo
        elif not funct[0] and funct[1] != '':
            content += i

        # verifica se i está indicando =
        elif i == '=':
            translate += '= ""'
            receive = True

        char += 1
    
    return {'script': translate}


# traduz comandos para script python
def parser(funct: str, content: str):
    print(funct, 0)
    if funct == '$VAR':
        return content
    return content




x = execute('''$VAR variable = value''')