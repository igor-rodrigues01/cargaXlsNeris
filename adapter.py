#!/usr/bin/env python3
#-*-coding:utf-8-*-

from utils import Utils
import xlrd

class Adapter:

    utils = None

    def __init__(self):
        self.utils = Utils()

    def convert_date_sema(self,sheets,columns_name_index,xls_file_instance): 
        """ Convertendo a data lida em objeto datetime"""
        
        index_sheet = 0

        for sheet in sheets:
            index_sheet = sheets.index(sheet)
            index_date  = columns_name_index[index_sheet]['data_lavratura'] 
            
            for index_row in range(len(sheet)):
                sheet[index_row][index_date] = xlrd.xldate_as_datetime(
                    sheet[index_row][index_date],xls_file_instance.datemode
                )

        return sheets 

    def column_name_index(self,dict_column_name_index):
        """
        Funcao que ira verificar a nomenclatura dos
        nomes das colunas e adaptalos em um nome padrao.
        Esta funcao e util caso ocorra alguma mudanca no
        nome das colunas do xls
        """
        new_key = None
        
        # for index in range(len(dict_column_name_index))
        for key,value in dict_column_name_index.items():
            new_key = None
            
            if key.lower() == 'id':
                new_key = 'id'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'n° do auto de infração'\
              or key.lower() == 'num do auto de infração'\
              or key.lower() == 'número do auto de infração'\
              or key.lower() == 'n do auto de infração'\
              or key.lower() == 'num do auto de infracao'\
              or key.lower() == 'numero do auto de infracao'\
              or key.lower() == 'n do auto de infracao':
                new_key = 'num_auto_infracao'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'série' or key.lower() == 'serie':
                new_key = 'serie'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'cpf/cnpj'\
              or key.lower() == 'cpfcnpj'\
              or key.lower() == 'cpfj':
                new_key = 'cpfj'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'autuado' or key.lower() == 'aut':
                new_key = 'autuado'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'descrição da infração'\
              or key.lower() == 'descricao da infracao'\
              or key.lower() == 'desc da infração'\
              or key.lower() == 'desc da infracao':
                new_key = 'desc_infracao'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'art 1 (dec n° 6.514/08)'\
              or key.lower() == 'art 1 (dec n 6.514/08)'\
              or key.lower() == 'art 1':
                new_key = 'art_1'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'art 2 (dec n° 6.514/08)'\
              or key.lower() == 'art 2 (dec n 6.514/08)'\
              or key.lower() == 'art 2':
                new_key = 'art_2'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value 

            elif key.lower() == 'tipo de infração'\
              or key.lower() == 'tipo de infracao':
                new_key = 'tipo_infracao'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value 

            elif key.lower() == 'nome uc'\
              or key.lower() == 'nome_uc'\
              or key.lower() == 'nom_uc':
                new_key = 'nom_uc'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value
              
            elif key.lower() == 'cnuc':
                new_key = 'cnuc'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value 

            elif key.lower() == 'município'\
              or key.lower() == 'municipio':
                new_key = 'municipio'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'uf':
                new_key = 'uf'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value 

            elif key.lower() == 'data do auto'\
              or key.lower() == 'data auto':
                new_key = 'data_auto'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'observação - embargo'\
              or key.lower() == 'observação embargo'\
              or key.lower() == 'observacao - embargo'\
              or key.lower() == 'observacao embargo'\
              or key.lower() == 'obs - embargo'\
              or key.lower() == 'obs embargo':
                new_key = 'obs_embargo'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'área'\
              or key.lower() == 'area':
                new_key = 'area'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'área'\
              or key.lower() == 'area':
                new_key = 'area'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value

            elif key.lower() == 'n° do processo'\
              or key.lower() == 'número do processo'\
              or key.lower() == 'numero do processo'\
              or key.lower() == 'num processo'\
              or key.lower() == 'n do processo':
                new_key = 'num_processo'
                dict_column_name_index.pop(key)
                dict_column_name_index[new_key] = value
            else:
                print('else - ',key)

        return dict_column_name_index

    def column_name_index_sema(self,list_dict_column_name_index,xls_file_name):

        new_key = None
        index_dict = 0 

        for dict_column_name_index in list_dict_column_name_index:
            index_dict = list_dict_column_name_index.index(dict_column_name_index)
            for key,value in dict_column_name_index.items():
                
                if key.lower() == 'numero de identificação'\
                  or key.lower() == 'numero de identificacao'\
                  or key.lower() == 'número de identificação'\
                  or key.lower() == 'num de identificação'\
                  or key.lower() == 'num de identificacao'\
                  or key.lower() == 'n de identificação'\
                  or key.lower() == 'n de identificacao':
                    new_key = 'num_identificacao'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'data de lavratura'\
                  or key.lower() == 'dt de lavratura'\
                  or key.lower() == 'data lavratura':
                    new_key = 'data_lavratura'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'descrição sucinta do fato'\
                  or key.lower() =='descricao sucinta do fato'\
                  or key.lower() =='desc sucinta do fato':
                    new_key = 'desc_sucinta'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'identificação do processo administrativo'\
                  or key.lower() == 'identificacao do processo administrativo'\
                  or key.lower() == 'identificação processo administrativo'\
                  or key.lower() == 'identificacao processo administrativo'\
                  or key.lower() == 'id do processo administrativo'\
                  or key.lower() == 'id processo administrativo':
                    new_key = 'id_proc_administrativo'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'nome da propriedade'\
                  or key.lower() == 'nome propriedade'\
                  or key.lower() == 'nom propriedade':
                    new_key = 'nom_propriedade'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'nome do possuidor/proprietário da área'\
                  or key.lower() == 'nome do possuidor/proprietario da area'\
                  or key.lower() == 'nome possuidor/proprietario da area'\
                  or key.lower() == 'nome possuidor/proprietario area'\
                  or key.lower() == 'nom do possuidor/proprietário da área'\
                  or key.lower() == 'nom do possuidor/proprietario da area'\
                  or key.lower() == 'nom possuidor/proprietario da area'\
                  or key.lower() == 'nom possuidor/proprietario area':
                    new_key = 'nom_possuidor'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'cpf':
                    new_key = 'cpf'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'x'\
                  or key.lower() == 'lat'\
                  or key.lower() == 'latitude':
                    new_key = 'lat'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'y'\
                  or key.lower() == 'lng'\
                  or key.lower() == 'long'\
                  or key.lower() == 'longitude':
                    new_key = 'lng'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'área (15-17)'\
                  or key.lower() == 'area (15-17)':
                    new_key = 'area_15_17'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'exploração (ha)'\
                  or key.lower() == 'exploracao (ha)':
                    new_key = 'explor_ha'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value
                
                elif key.lower() == 'desmate app (ha)':
                    new_key = 'desmate_app_ha'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value
                
                elif key.lower() == 'desmate total':
                    new_key = 'desmate_total'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'queimada':
                    new_key = 'queimada'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value

                elif key.lower() == 'classificação da área (15-17)'\
                  or key.lower() == 'classificacao da area (15-17)'\
                  or key.lower() == 'classific da área (15-17)'\
                  or key.lower() == 'classific da area (15-17)'\
                  or key.lower() == 'classificação área (15-17)'\
                  or key.lower() == 'classificacao area (15-17)'\
                  or key.lower() == 'classific área (15-17)'\
                  or key.lower() == 'classific area (15-17)':
                    new_key = 'classific_area_15_17'
                    list_dict_column_name_index[index_dict].pop(key)
                    list_dict_column_name_index[index_dict][new_key] = value
                # A razao pela qual esta sendo utilizado es
                # elif key.lower() != 'numero de identificação'\
                #   or key.lower() != 'numero de identificacao'\
                #   or key.lower() != 'número de identificação'\
                #   or key.lower() != 'num de identificação'\
                #   or key.lower() != 'num de identificacao'\
                #   or key.lower() != 'n de identificação'\
                #   or key.lower() != 'n de identificacao'\
                #   or key.lower() != 'data de lavratura'\
                #   or key.lower() != 'dt de lavratura'\
                #   or key.lower() != 'data lavratura'\
                #   or key.lower() != 'descrição sucinta do fato'\
                #   or key.lower() != 'descricao sucinta do fato'\
                #   or key.lower() != 'desc sucinta do fato'\
                #   or key.lower() != 'identificação do processo administrativo'\
                #   or key.lower() != 'identificacao do processo administrativo'\
                #   or key.lower() != 'identificação processo administrativo'\
                #   or key.lower() != 'identificacao processo administrativo'\
                #   or key.lower() != 'id do processo administrativo'\
                #   or key.lower() != 'id processo administrativo'\
                #   or key.lower() != 'nome da propriedade'\
                #   or key.lower() != 'nome propriedade'\
                #   or key.lower() != 'nom propriedade'\
                #   or key.lower() != 'nome do possuidor/proprietário da área'\
                #   or key.lower() != 'nome do possuidor/proprietario da area'\
                #   or key.lower() != 'nome possuidor/proprietario da area'\
                #   or key.lower() != 'nome possuidor/proprietario area'\
                #   or key.lower() != 'nom do possuidor/proprietário da área'\
                #   or key.lower() != 'nom do possuidor/proprietario da area'\
                #   or key.lower() != 'nom possuidor/proprietario da area'\
                #   or key.lower() != 'nom possuidor/proprietario area'\
                #   or key.lower() != 'cpf'\
                #   or key.lower() != 'x'\
                #   or key.lower() != 'lat'\
                #   or key.lower() != 'latitude'\
                #   or key.lower() != 'y'\
                #   or key.lower() != 'lng'\
                #   or key.lower() != 'long'\
                #   or key.lower() != 'longitude'\
                #   or key.lower() != 'área (15-17)'\
                #   or key.lower() != 'area (15-17)'\
                #   or key.lower() != 'exploração (ha)'\
                #   or key.lower() != 'exploracao (ha)'\
                #   or key.lower() != 'desmate app (ha)'\
                #   or key.lower() != 'desmate total'\
                #   or key.lower() != 'queimada'\
                #   or key.lower() != 'classificação da área (15-17)'\
                #   or key.lower() != 'classificacao da area (15-17)'\
                #   or key.lower() != 'classific da área (15-17)'\
                #   or key.lower() != 'classific da area (15-17)'\
                #   or key.lower() != 'classificação área (15-17)'\
                #   or key.lower() != 'classificacao area (15-17)'\
                #   or key.lower() != 'classific área (15-17)'\
                #   or key.lower() != 'classific area (15-17)':
                # else:
                #     import pdb; pdb.set_trace()
                    
                    # self.error_message_and_stop_script(
                    #     'O nome {} está fora dos padrões de nomes da tabela e do script.'
                    # )

        return list_dict_column_name_index

