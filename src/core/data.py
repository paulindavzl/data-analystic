import os
import glob
import pandas as pd
from typing import Optional as Op
from src.core import FILES

# classe responsável por manipular dados
class Data:

    def __init__(self):
        self.__method = pd.read_excel
        self.__data = None
        self.__files = []


    # abre uma planilha
    def open(self, filename: str, type: Op[str]='xlsx', max_lines: Op[int]=None):
        path = FILES + filename

        # garante que a planilha já foi importada
        if not os.path.exists(path):
            return {'err': 'data_not_found', 'data': 'spreadsheet'}, path

        pd.set_option('display.max_rows', max_lines)
        self.__files.append(filename)

        # define o método mais adequado
        if type == 'xlsx':
            self.__method = pd.read_excel
        elif type == 'csv':
            self.__method = pd.read_csv
        else:
            return {'err': 'type_not_supported', 'type': type}
        
        self.__data = self.__method(path)

        return {'result': 'Success'}


    # obtém uma coluna
    def get_column(self, column_name: str):
        # garante que a planilha já foi aberta
        try:
            if not self.__data:
                return {'err': 'data_not_defined', 'data': 'spreadsheet'}
        except:
            pass
        
        data = self.__data[column_name]

        return {'data': data}
    

    # obtém várias colunas
    def get_columns(self, *columns: str):
         # garante que a planilha já foi aberta
        try:
            if not self.__data:
                return {'err': 'data_not_defined', 'data': 'spreadsheet'}
        except:
            pass

        data = self.__data[list(columns)]

        return {'data': data}
    

    # cria uma nova planilha do zero
    def new(self, data: dict):
        # garante que a planilha não será vazia
        if len(data) <= 0:
            return {'err': 'data_empty',  'data': 'spreadsheet'}

        spreadsheet = pd.DataFrame(data)
        
        return {'data': spreadsheet}
    

    # cria uma pllanilha a partir de outra
    def save(self, filename: str, data: pd.DataFrame, index: Op[bool]=True, overwrite: Op[bool]=True, test: Op[bool]=False):
        path = FILES + filename

        # garante que a planilha não está vazia
        if data.empty:
            return {'err': 'data_empty', 'data': 'spreadsheet'}
        
        # verifica se já existe uma pllanilha com esse nome
        elif self.__file_exists(path, overwrite):
            return {'err': 'spreadsheet_already_exists', 'filename': filename}
        
        # não permite salvar o arquivo como for_tests
        elif filename == 'for_tests.xlsx' and not test:
            return {'err': 'invalid_filename', 'filename': filename}
        
        self.__files.append(filename)
        
        data.to_excel(path, index=index)

        return {'result': 'Success'}
    

    # apaga todas as planilhas
    @property
    def remove_all(self):
        files = glob.glob(FILES + '*.xlsx')

        for file in files:
            os.remove(file)

    
    # apaga um ou mais arquivos específicos
    def remove(self, *files):
        files = list(files)
        print(files)
        for file in files:
            if os.path.exists(FILES + file):
                os.remove(FILES + file)
    

    # verifica se um arquivo já existe
    def __file_exists(self, path: str, overwrite: Op[bool]=False):
        return True if os.path.exists(path) and not overwrite else False


    