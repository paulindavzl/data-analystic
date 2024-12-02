import time

# executa scripts
def execute(script: str):
    save(script) # salva o script em um arquivo

    with open('script.da', 'r') as file:
        script_line = 1
        transalated_script = '' # armazena um script python traduzido
        condition = False # controla condições

        for line in file.readlines():
            response = check_script(line, condition)
            
            # verifica se houve erro
            if response.get('err'):
                response['line'] = script_line
                return response
            script_line += 1

            transalated_script += response.get('script')
            condition = response.get('condition')

        # executa o arquivo .py
        execute_py(transalated_script)


# executa um arquivo python
def execute_py(script):
    print(script)
    # exec(script)


# salva o script para análise e execução
def save(script: str):
    with open('./script.da', 'w') as file:
        file.write(script)
        


# verifica o script
def check_script(script: str, condition: bool):
    script = script.strip()
    char = 1 # conta o número do caractére para identificar erros
    funct = [False, ''] # define se há uma função ativa
    special_chars = ['$', '=', '>', '<', '!']
    content = '' # conteúdo da função
    translate = '' # script tranduzido para Python
    receive = False # analisa se uma variável está recebendo algum valor

    for i in script:
        # se o script não iniciar com $ (erro)
        if i != '$' and i != ' ' and char == 1 and not condition:
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 0}
        
        # se tentar chamar uma função com um já ativa
        elif i == '$' and funct[0]:
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 1}
        
        # nomeclatura errada
        elif not i.isupper() and funct[0] and i != ' ':
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 2}
        
        elif not funct[0] and content == '' and i.isdigit():
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 3}
        
        # tenta iniciar uma função sem finalizar outra
        elif i == '$' and funct[1] != '':
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 4}
        
        # receber valor já estando recebendo um
        elif i == '=' and receive:
            return {'err': 'invalid_sintaxe', 'char': char, 'verify': 5}
        
        # inicia uma função
        elif i == '$':
            funct = [True, i]
        
        # adiciona conteúdo para um recebedor de dados
        elif receive and i != ' ':
            if i != ':':
                content = content[: len(content) - 1]
                content += i + '"'
                continue
            content += i
        
        # finalisa uma função
        elif i == ' ' and funct[0]:
            funct[0] = False

        # monta o nome da função
        elif not receive and funct[0]:
            funct[1] += i

        # finaliza o conteúdo
        elif i == ' ' and content != '':
            if not receive:
                response = parser(funct[1], content)
                translate += response[0]
                condition = response[1]
                content = ''
                continue

            response = parser(funct, content)
            content += response[0]
            condition = response[1]

        # recebe dados
        elif i == '=' and funct[1] != '':
            funct = [False, '']
            receive = True
            content = ' == "' if condition else ' = "'
        
        # adiciona conteúdo da função
        elif not funct[0] and funct[1] != '' and not receive:
            content += i
            
        char += 1

    translate += content

    return {'script': translate, 'condition': condition}


# traduz comandos para script python
def parser(funct: str, content: str):
    # declara uma variável
    if funct == '$VAR':
        return content, False
    
     # adiciona uma condição if
    elif funct == '$IF':
        return f'if {content}', True

    return content
    
   

x = execute('''$IF variable = value:
    condition''')

print(x)