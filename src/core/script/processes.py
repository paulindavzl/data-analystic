import ast

class Check(ast.NodeVisitor):

    def __init__(self):
        self.black_list = [
            'import', 'open', 'from', 'exec', 'os', 'subprocess', 'eval', 'os.system', 'subprocess.run', 'globals', 'locals'
        ]


    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.black_list:
            self.err(node.func.id, 'funct')

        self.generic_visit(node)

    
    def visit_Import(self, node):
        for alias in node.names:
            self.err(alias.name, 'import')

        self.generic_visit(node)

    
    def visit_ImportFrom(self, node):
        # Verifica o módulo base
        if node.module in self.black_list:
            self.err(node.module, 'import')
        
        # Verifica os nomes importados
        for alias in node.names:
            self.err(alias.name, 'from')

        self.generic_visit(node)

    
    # marca um erro
    def err(self, err: str, e_type: str):
        self.response['result'] = False
        self.response['err'] = 'suspect'
        self.response['sus'].append([err, e_type])


    # garante que o script do usuário não prejudique o sistema
    def is_safe(self, script: str) -> dict:
        self.response = {'result': True, 'sus': []}

        try:
            tree = ast.parse(script) # obtém a árvore do script completo
        except SyntaxError as e:
            return {'result': False, 'err': 'sintaxe_error', 'line': e.lineno}

        self.visit(tree)

        if self.response.get('sus') == []:
            self.response.pop('sus')
        
        return self.response
    

