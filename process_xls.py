#!/usr/bin/env python3
#-*- condig:utf-8 -*-

import requests
import os
import xlrd

from datetime import datetime
from utils import Utils,Adapter

"""
http://www.sema.mt.gov.br/attachments/article/3318/Embargos%20CFF%202010_2017_1.xls
http://www.icmbio.gov.br/portal/images/stories/areas_embargadas/Embargos_ICMBio.xlsx
"""
class Xls:

    utils        = None
    adapter      = None
    current_date = None

    def __init__(self):
        self.utils        = Utils()
        self.adapter      = Adapter()
        self.current_date = datetime.now().strftime("%Y-%m-%d")

        self.create_directory('file')
        self.get_xls()

    def create_directory(self,dir_name):
        """
        Funcao que verifica se o diretorio file existe, caso existe nada acontecera
        se nao sera criado o diretorio file.
        """
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

    def create_and_write_xls(self,file_name,response):
        """
        Funcao que veririca se o xls existe, caso nao existir sera criado o xls
        e sera escrito o conteudo da requisicao. 
        """
        dir_name     = 'file/xls_{}'.format(self.current_date)
        self.create_directory(dir_name)
        file_name    = '{}/{}_{}.xls'.format(dir_name,file_name,self.current_date)
        
        if os.path.exists(file_name):
            os.remove(file_name)

        with open(file_name,'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

            file.flush()

    def download_and_create_xls(self,file_name,url):
        """
        Funcao que baixa o xls no site www.sema.mt.gov.br
        """
        try:
            response = requests.get(url)
        except Exception as ex:
            self.utils.message_and_stop_script(
                ex,'Erro ao baixar o arquivo {}.xls'.format(file_name)
            )

        self.create_and_write_xls(file_name,response)

    def get_xls(self):
        """
        Funcao que executa a funcao de download do xls e criacao do mesmo
        """
        url_sema   = 'http://www.sema.mt.gov.br/'\
        'attachments/article/3318/Embargos%20CFF%202010_2017_1.xls'
        url_icmbio = 'http://www.icmbio.gov.br/'\
        'portal/images/stories/areas_embargadas/Embargos_ICMBio.xlsx'
        # download xls sema
        self.download_and_create_xls('sema',url_sema)
        # download xls icmbio
        self.download_and_create_xls('icmbio',url_icmbio)

    def read_xls(self,path_xls_file,is_icmbio_xls=False,is_sema_xls=False):
        xls_file_instance = xlrd.open_workbook(path_xls_file)
        sheets            = xls_file_instance.sheets()
        xls_data          = []
        sheet_data_sema   = []
        # removendo a segunda folha do xls icbio pois
        # ela contem apenas um coluna de dados
        if is_icmbio_xls:
            sheets = [sheets[0]]
        
        for sheet in sheets:
            # este if serve para zerar os dados de uma folha e adicionar
            # os dados lidos de forma separada folha a folha na lista sheet_data_sema
            if is_sema_xls:
                xls_data = []
            
            for row_number in range(sheet.nrows):
                xls_data.append(
                    sheet.row_values(row_number)                    
                )
            # adicionando uma folha
            if is_sema_xls and not xls_data == []:
                sheet_data_sema.append(xls_data)

        if is_icmbio_xls:
            return xls_data
        else:
            return sheet_data_sema
            

    def get_icmbio(self):
        """
        Funcao que obtem os dados do xls icmbio e chama a funcao que
        formata o nome das colunas com nomes padronizados
        """
        path_xls_file = 'file/xls_{}/icmbio_{}.xls'.format(
            self.current_date,self.current_date
        )
        xls_data = self.read_xls(path_xls_file,is_icmbio_xls=True)
        columns_name_with_index = {}

        if xls_data[0].count('') > 5:
            xls_data.pop(0)

        # obtendo o indice de cada coluna
        for index_column in range(len(xls_data[0])):
            columns_name_with_index[xls_data[0][index_column]] = index_column 
        
        xls_data.pop(0)
        columns_name_with_index = self.adapter.column_name_index(
            columns_name_with_index
        )
        return (columns_name_with_index,xls_data)

    def get_sema(self):
        path_xls_file = 'file/xls_{}/sema_{}.xls'.format(
            self.current_date,self.current_date
        )
        sheet_data_sema = self.read_xls(path_xls_file,is_sema_xls=True)
        
        """
        Tratar os dados da folha de dados sema
        """
        return sheet_data_sema


if __name__ == '__main__':
    print(Xls().get_sema())
