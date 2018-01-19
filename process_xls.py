#!/usr/bin/env python3
#-*- condig:utf-8 -*-

import requests
import os
import xlrd

from datetime import datetime
from utils import Utils
from adapter import Adapter

class Xls:

    utils        = None
    adapter      = None
    current_date = None
    xls_file_instance = None

    def __init__(self):
        self.utils          = Utils()
        self.adapter        = Adapter()
        self.current_date   = datetime.now().strftime("%Y-%m-%d")
        dir_name            = os.path.dirname(__file__) 
        self.files_dir_name = os.path.join(dir_name,'file')
        
        self.make_xls_file()

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
        full_dir_name     = '{}/xls_{}'.format(self.files_dir_name,self.current_date)
        self.create_directory(full_dir_name)
        file_name    = '{}/{}_{}.xls'.format(full_dir_name,file_name,self.current_date)
        
        if os.path.exists(file_name):
            os.remove(file_name)

        with open(file_name,'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)

            file.flush()

    def download_and_create_xls(self,file_name,url):
        """
        Funcao que baixa o xls e chama a funcao para criar o arquivo na maquina
        """
        try:
            print('Downloading file {}_{}.xls'.format(file_name,self.current_date))
            response = requests.get(url)
        except Exception as ex:
            self.utils.error_message_and_stop_script(
                'Erro ao baixar o arquivo {}_{}.xls'.format(file_name,self.current_date),ex
            )
        else:
            print('{}_{}.xls downloaded with success\n'.format(file_name,self.current_date))

        self.create_and_write_xls(file_name,response)

    def make_xls_file(self):
        """
        Funcao que executa a funcao de download do xls e criacao do xls
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
        '''
        Funcao que le o arquivo xls e retorna os dados. Caso o xls seja do sema sera
        retornado todos os dados em uma lista de lista dividido por folha, e caso o
        xls seja o icmbio todos os dados serao retornados em apenas uma lista de lista  
        '''
        self.xls_file_instance = xlrd.open_workbook(path_xls_file,formatting_info=True)
        sheets                 = self.xls_file_instance.sheets()
        new_row                = []
        sheet                  = []
        sheet_data_sema        = []
        cell_obj               = None
        xls_data               = []
    
        # removendo a segunda folha do xls icbio pois
        # ela contem apenas um coluna de dados
        if is_icmbio_xls:
            sheets = [sheets[0]]

        for sheet in sheets:
            
            cell_obj = None
            
            # este if serve para zerar os dados de uma folha e adicionar
            # os dados lidos de forma separada folha a folha na lista sheet_data_sema
            if is_sema_xls:
                xls_data = []

            # iterando sobre as linhas
            for row_index in range(sheet.nrows):
                new_row = []
                # iterando sobre as colunas
                for col_index in range(sheet.ncols):
                    cell_obj   = sheet.cell(row_index,col_index)
                    cell_value = self.adapter.adapter_cell_object_by_type(
                        cell_obj,self.xls_file_instance
                    )
                    new_row.append(cell_value)
                
                # este if serve para que nao seja adicionado linhas totalmente em branco
                if sheet.row_values(row_index).count('') != len(sheet.row_values(row_index)):
                    xls_data.append(new_row)

            # adicionando uma nova folha no xls sema
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
        path_xls_file = '{}/xls_{}/icmbio_{}.xls'.format(
            self.files_dir_name,self.current_date,self.current_date
        )
        xls_data = self.read_xls(path_xls_file,is_icmbio_xls=True)
        columns_name_with_index = {}

        for index in range(len(xls_data)):
            
            if xls_data[index].count('') > 5:
                xls_data.pop(index)
           
            if index == 1:
                break
        
        # obtendo o indice de cada coluna
        for index_column in range(len(xls_data[0])):
            columns_name_with_index[xls_data[0][index_column]] = index_column 
        
        # Removendo a primeira lista que contem o nome das colunas e deixando
        # apenas os dados prontos para serem processados 
        xls_data.pop(0)
        
        columns_name_with_index = self.adapter.column_name_index_icmbio(
            columns_name_with_index,os.path.basename(path_xls_file)
        )
        xls_data = self.adapter.convert_date_icmbio(
            xls_data,columns_name_with_index,self.xls_file_instance
        )

        return (columns_name_with_index,xls_data)

    def get_sema(self):
        """
        Funcao que obtem os dados dos xls sema divididos por folha.
        Esta funcao tambem pega os nomes das colunas e formata para nomes
        padronizados, tambem dividido por folha
        """
        path_xls_file    = '{}/xls_{}/sema_{}.xls'.format(
            self.files_dir_name,self.current_date,self.current_date
        )
        sheets_data_sema         = self.read_xls(path_xls_file,is_sema_xls=True)
        columns_name_with_index  = []
        sheet_index              = 0
        controller_index_removed = 0
        # a variavel "controller_index_removed" e necesaria para que seja calculado seu 
        # valor com o indice de cada linha de uma folha para manter o indice no item correto

        """
        Este loop remove as duas primeiras linhas do xls que sao apenas
        titulos irrelevantes para a carga, e este loop tambem obtem o nome
        das colunas e adiciona na variavel "columns_name_with_index" junto
        com o indice da coluna para facilitar a identificacao dos dados
        na iteracao de todos os registros
        """
        for sheet in sheets_data_sema:
            controller_index_removed = 0
            sheet_index = sheets_data_sema.index(sheet)

            for index in range(len(sheet)):
                # este calculo ocorre para manter o indice no item certo,
                # isto e necessario devido a remocao de um item na lista 
                index -= controller_index_removed

                if index < 3 and sheet[index].count('') > 6:
                    # Este if remove as primeira linhas irrelevantes para a carga
                    sheets_data_sema[sheet_index].pop(index)
                    controller_index_removed += 1
                    continue

                if index == 0:
                    # Este if obtem o nome das colunas de cada folha do xls
                    # e insere em uma lista de dicionarios e depois remove a
                    # linha dos nomes das colunas para que fique apenas os dados.
                    columns_name_with_index.append({})

                    for index_item_row in range(len(sheet[index])):
                        columns_name_with_index[sheet_index][
                            sheet[index][index_item_row]
                        ] = index_item_row

                    sheets_data_sema[sheet_index].pop(0)

                if index > 5:
                    break

        columns_name_with_index = self.adapter.column_name_index_sema(
            columns_name_with_index,os.path.basename(path_xls_file)
        )
        sheets_data_sema = self.adapter.convert_date_sema(
            sheets_data_sema,columns_name_with_index,self.xls_file_instance
        )
        return (columns_name_with_index,sheets_data_sema)
