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


    # abre uma planilha
    def open(self, filename: str, dtype: Op[str]='xlsx', max_lines: Op[int]=None) -> dict:
        path = FILES + str(filename)

        # garante que filename seja str
        if not isinstance(filename, str):
            return {'err': 'type_error', 'data': filename, 'expected': 'str'}
        
        # garante que type seja str
        elif not isinstance(dtype, str):
            return {'err': 'type_error', 'data': dtype, 'expected': 'str'}
        
        # garante que max_lines seja int
        elif max_lines and not isinstance(max_lines, int):
            return {'err': 'type_error', 'data': max_lines, 'expected': 'int'}

        pd.set_option('display.max_rows', max_lines)

        # define o método mais adequado
        if dtype == 'xlsx':
            self.__method = pd.read_excel
        elif dtype == 'csv':
            self.__method = pd.read_csv
        else:
            return {'err': 'type_not_supported', 'type': dtype}
        
        # garante que a planilha já foi importada
        if not os.path.exists(path):
            return {'err': 'data_not_found', 'data': 'spreadsheet', 'filename': filename}
        
        self.__data = self.__method(path)

        return {'result': 'Success'}


    # obtém uma coluna
    def get_column(self, column_name: str, to_list: Op[bool]=False) -> dict:
        # garante que column_name seja str
        if not isinstance(column_name, str):
            return {'err': 'type_error', 'data': column_name, 'expected': 'str'}
        
        # garante que to_list seja bool
        elif not isinstance(to_list, bool):
            return {'err': 'type_error', 'data': to_list, 'expected': 'bool'}

        # garante que a planilha já foi aberta
        elif not isinstance(self.__data, pd.DataFrame):
            return {'err': 'data_not_defined', 'data': 'spreadsheet', 'expected': 'DataFrame'}
        
        data = self.__data[column_name] if not to_list else self.__data[column_name].tolist()

        return {'data': data}
    

    # obtém várias colunas
    def get_columns(self, *columns: str, to_list: Op[bool]=False) -> dict:
        columns = list(columns)

        # garante que os nomes das colunas sejam str
        for column in columns:
            if not isinstance(column, str):
                return {'err': 'type_error', 'data': column, 'expected': 'str'}
            
        # garante que to_list seja bool
        if not isinstance(to_list, bool):
            return {'err': 'type_error', 'data': to_list, 'expected': 'bool'}

        # garante que a planilha já foi aberta
        elif not isinstance(self.__data, pd.DataFrame):
            return {'err': 'data_not_defined', 'data': 'spreadsheet', 'expected': 'DataFrame'}

        data = self.__data[columns] if not to_list else self.__data[columns].values.tolist()

        return {'data': data}
    

    # cria uma nova planilha do zero
    def new(self, data: dict) -> dict:
        # garante que data seja dict
        if not isinstance(data, dict):
            return {'err': 'type_error', 'data': data, 'expected': 'dict'}

        # garante que a planilha não será vazia
        elif len(data) <= 0:
            return {'err': 'data_empty',  'data': 'spreadsheet'}

        spreadsheet = pd.DataFrame(data)
        
        return {'data': spreadsheet}
    

    # cria uma pllanilha a partir de outra
    def save(self, filename: str, data: pd.DataFrame, index: Op[bool]=True, overwrite: Op[bool]=True, test: Op[bool]=False) -> dict:
        path = FILES + str(filename)

        # garante que filename seja str
        if not isinstance(filename, str):
            return {'err': 'type_error', 'data': filename, 'expected': 'str'}
        
        # garante que data seja DataFrame
        elif not isinstance(data, pd.DataFrame) and (not isinstance(data, dict) or not isinstance(data.get('data'), pd.DataFrame)):
            return {'err': 'type_error', 'data': data, 'expected': 'DataFrame'}
        
        # garante que index seja bool
        elif not isinstance(index, bool):
            return {'err': 'type_error', 'data': index, 'expected': 'bool'}
        
        # garante que overwrite seja bool
        elif not isinstance(overwrite, bool):
            return {'err': 'type_error', 'data': overwrite, 'expected': 'bool'}
        
        # garante que test seja bool
        elif not isinstance(test, bool):
            return {'err': 'type_error', 'data': test, 'expected': 'bool'}

        # verifica se já existe uma planilha com esse nome
        elif self.__file_exists(path, overwrite):
            return {'err': 'spreadsheet_already_exists', 'filename': filename}
        
        # não permite salvar o arquivo como for_tests
        elif filename == 'for_tests.xlsx' and not test:
            return {'err': 'invalid_filename', 'filename': filename}
        
        # transforma data em DataFrame caso seja dict
        data = data.get('data') if isinstance(data, dict) else data
                
        data.to_excel(path, index=index)

        return {'result': 'Success'}
    

    # apaga todas as planilhas
    @property
    def remove_all(self):
        files = glob.glob(FILES + '*.xlsx')

        for file in files:
            os.remove(file)

    
    # apaga um ou mais arquivos específicos
    def remove(self, *files: str):
        files = list(files)
        for file in files:
            if os.path.exists(FILES + str(file)):
                os.remove(FILES + str(file))
    

    # verifica se um arquivo já existe
    def __file_exists(self, path: str, overwrite: Op[bool]=False) -> bool:
        # garante que path seja str
        if not isinstance(path, str):
            return {'err': 'type_error', 'data': path, 'expected': 'str'}
        
        # garante que overwrite seja str
        if not isinstance(overwrite, bool):
            return {'err': 'type_error', 'data': overwrite, 'expected': 'bool'}

        return True if os.path.exists(path) and not overwrite else False


    