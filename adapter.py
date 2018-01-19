#!/usr/bin/env python3
#-*-coding:utf-8-*-

from utils import Utils
import xlrd

class Adapter:

    utils = None

    def __init__(self):
        self.utils = Utils()

    def get_cell_value_with_formatter(self,cell_obj,xls_file_instance):
        """
        Funcao que obtem uma celula com um valor numerico com o 0 a esquerda
        e mantem este numero com esse 0 a esquerda
        """
        cell_with_formatter = None
        xls_formatter_obj   = xls_file_instance.xf_list[cell_obj.xf_index]
        formatter_str       = None

        if xls_formatter_obj.format_key in xls_file_instance.format_map.keys():
            formatter_str = xls_file_instance.format_map[xls_formatter_obj.format_key].format_str
        
            if cell_obj.ctype == xlrd.XL_CELL_NUMBER and all(x == '0' for x in formatter_str):
                cell_with_formatter = '%0*d' % (len(formatter_str), int(cell_obj.value))
                return cell_with_formatter
            
            else:
                return cell_obj.value
        else:
            return cell_obj.value

    def remove_last_zero_in_int(self,cell):
        """
        Funcao que remove o ".0" no final dos numeros inteiros lidos pela
        lib xrld 
        """
        if isinstance(cell,float):
            cell = str(cell)
            
            if cell.endswith('.0'):
                cell = cell[:-1]
                cell = cell[:-1]
                
            if not cell.startswith('0') and cell.find('.') == -1:
                cell = int(cell)
                
        return cell

    def remove_simple_quotes(self,cell):
        """
        Funcao que troca 1 aspas simples por 2 aspas simples para que o dado
        seja aceito na base de dados 
        """
        if isinstance(cell,str):
            if cell.find("'") != -1:
                cell = cell.replace("'","''")

        return cell

    def adapter_cell_object_by_type(self,cell_obj,xls_file_instance):
        """
        Funcao que chava as funcoes de conversao de dados para cada celula
        """
        cell = self.get_cell_value_with_formatter(cell_obj,xls_file_instance)
        cell = self.remove_simple_quotes(cell)
        cell = self.remove_last_zero_in_int(cell)
        return cell
    
    def convert_date_sema(self,sheets,columns_name_index,xls_file_instance): 
        """
        Convertendo a data lida no xls sema em objeto datetime 
        e pegando apenas a data
        """
        index_sheet = 0
        date_obj    = None

        for sheet in sheets:
            index_sheet = sheets.index(sheet)
            index_date  = columns_name_index[index_sheet]['dt_lavratura'] 
            
            for index_row in range(len(sheet)):
                date_obj = xlrd.xldate_as_datetime(
                    sheet[index_row][index_date],xls_file_instance.datemode
                )  
                sheet[index_row][index_date] = date_obj.date()

        return sheets

    def convert_date_icmbio(self,xls_data,columns_name_index,xls_file_instance):
        """
        Convertendo a data lida no xls icmbio em objeto datetime
        e pegando apenas a data
        """
        index_date = columns_name_index['dt_auto']
        date_obj   = None
        
        for index in range(len(xls_data)):
            if xls_data[index][index_date] != ''\
              and xls_data[index][index_date] != None: 
                date_obj = xlrd.xldate_as_datetime(
                    xls_data[index][index_date],xls_file_instance.datemode
                )
                xls_data[index][index_date] = date_obj.date()
            
            else:  
                xls_data[index][index_date] = 'null'  

        return xls_data

    def column_name_index_icmbio(self,dict_column_name_index,file_name):
        """
        Funcao que ira verificar a nomenclatura das colunas no
        xls icmbio e adaptalos em um nome padrao. Esta funcao e util caso
        ocorra alguma mudanca no nome das colunas do xls.
        """
        new_key              = None
        new_dict_with_column = {}

        for key,value in dict_column_name_index.items():
            new_key = None
            
            if key.lower() == 'id':
                new_key = 'id'
                new_dict_with_column[new_key] = value                

            elif key.lower() == 'n° do auto de infração'\
              or key.lower() == 'num do auto de infração'\
              or key.lower() == 'número do auto de infração'\
              or key.lower() == 'n do auto de infração'\
              or key.lower() == 'num do auto de infracao'\
              or key.lower() == 'numero do auto de infracao'\
              or key.lower() == 'n do auto de infracao':
                new_key = 'num_auto_infracao'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'série' or key.lower() == 'serie':
                new_key = 'serie'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'cpf/cnpj'\
              or key.lower() == 'cpfcnpj'\
              or key.lower() == 'cpfj':
                new_key = 'cpfj'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'autuado' or key.lower() == 'aut':
                new_key = 'autuado'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'descrição da infração'\
              or key.lower() == 'descricao da infracao'\
              or key.lower() == 'desc da infração'\
              or key.lower() == 'desc da infracao':
                new_key = 'desc_infracao'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'art 1 (dec n° 6.514/08)'\
              or key.lower() == 'art 1 (dec n 6.514/08)'\
              or key.lower() == 'art 1':
                new_key = 'art_1'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'art 2 (dec n° 6.514/08)'\
              or key.lower() == 'art 2 (dec n 6.514/08)'\
              or key.lower() == 'art 2':
                new_key = 'art_2'
                new_dict_with_column[new_key] = value 

            elif key.lower() == 'tipo de infração'\
              or key.lower() == 'tipo de infracao':
                new_key = 'tipo_infracao'
                new_dict_with_column[new_key] = value 

            elif key.lower() == 'nome uc'\
              or key.lower() == 'nome_uc'\
              or key.lower() == 'nom_uc':
                new_key = 'nom_uc'
                new_dict_with_column[new_key] = value
              
            elif key.lower() == 'cnuc':
                new_key = 'cnuc'
                new_dict_with_column[new_key] = value 

            elif key.lower() == 'município'\
              or key.lower() == 'municipio':
                new_key = 'municipio'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'uf':
                new_key = 'uf'
                new_dict_with_column[new_key] = value 

            elif key.lower() == 'data do auto'\
              or key.lower() == 'data auto':
                new_key = 'dt_auto'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'observação - embargo'\
              or key.lower() == 'observação embargo'\
              or key.lower() == 'observacao - embargo'\
              or key.lower() == 'observacao embargo'\
              or key.lower() == 'obs - embargo'\
              or key.lower() == 'obs embargo':
                new_key = 'obs_embargo'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'área'\
              or key.lower() == 'area':
                new_key = 'area'
                new_dict_with_column[new_key] = value

            elif key.lower() == 'n° do processo'\
              or key.lower() == 'número do processo'\
              or key.lower() == 'numero do processo'\
              or key.lower() == 'num processo'\
              or key.lower() == 'n do processo':
                new_key = 'num_processo'
                new_dict_with_column[new_key] = value
        
            else:
                self.utils.error_message_and_stop_script(
                    'Error: A coluna com o nome "{}" é nova e não consta nos'\
                    ' padrões de nome de coluna do script.\n Verifique o nome'\
                    ' das colunas no arquivo {}'.format(key,file_name)
                )
        
        return new_dict_with_column

    def column_name_index_sema(self,list_dict_column_name_index,file_name):
        """
        Funcao que ira verificar a nomenclatura das colunas no xls sema e 
        adaptalos em um nome padrao. Esta funcao e util caso ocorra alguma
        mudanca no nome das colunas do xls.
        """
        new_key              = None
        index_dict           = 0
        new_list_dict_with_column = []  

        for dict_column_name_index in list_dict_column_name_index:
            index_dict = list_dict_column_name_index.index(dict_column_name_index)
            new_list_dict_with_column.append({})

            for key,value in dict_column_name_index.items():
                
                if key.lower() == 'numero de identificação'\
                  or key.lower() == 'numero de identificacao'\
                  or key.lower() == 'número de identificação'\
                  or key.lower() == 'num de identificação'\
                  or key.lower() == 'num de identificacao'\
                  or key.lower() == 'n de identificação'\
                  or key.lower() == 'n de identificacao':
                    new_key = 'num_identificacao'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'data de lavratura'\
                  or key.lower() == 'dt de lavratura'\
                  or key.lower() == 'data lavratura':
                    new_key = 'dt_lavratura'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'descrição sucinta do fato'\
                  or key.lower() =='descricao sucinta do fato'\
                  or key.lower() =='desc sucinta do fato':
                    new_key = 'desc_sucinta_fato'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'identificação do processo administrativo'\
                  or key.lower() == 'identificacao do processo administrativo'\
                  or key.lower() == 'identificação processo administrativo'\
                  or key.lower() == 'identificacao processo administrativo'\
                  or key.lower() == 'id do processo administrativo'\
                  or key.lower() == 'id processo administrativo':
                    new_key = 'id_proc_administrativo'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'nome da propriedade'\
                  or key.lower() == 'nome propriedade'\
                  or key.lower() == 'nom propriedade':
                    new_key = 'nom_propriedade'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'nome do possuidor/proprietário da área'\
                  or key.lower() == 'nome do possuidor/proprietario da area'\
                  or key.lower() == 'nome possuidor/proprietario da area'\
                  or key.lower() == 'nome possuidor/proprietario area'\
                  or key.lower() == 'nom do possuidor/proprietário da área'\
                  or key.lower() == 'nom do possuidor/proprietario da area'\
                  or key.lower() == 'nom possuidor/proprietario da area'\
                  or key.lower() == 'nom possuidor/proprietario area':
                    new_key = 'nom_proprietario'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'cpf':
                    new_key = 'cpf'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'x'\
                  or key.lower() == 'lat'\
                  or key.lower() == 'latitude':
                    new_key = 'lat'
                    # list_dict_column_name_index[index_dict].pop(key)
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'y'\
                  or key.lower() == 'lng'\
                  or key.lower() == 'long'\
                  or key.lower() == 'longitude':
                    new_key = 'lng'
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'área (15-17)'\
                  or key.lower() == 'area (15-17)':
                    new_key = 'area_15_17'
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'exploração (ha)'\
                  or key.lower() == 'exploracao (ha)':
                    new_key = 'explor_ha'
                    new_list_dict_with_column[index_dict][new_key] = value
                
                elif key.lower() == 'desmate app (ha)':
                    new_key = 'desmate_app_ha'
                    new_list_dict_with_column[index_dict][new_key] = value
                
                elif key.lower() == 'desmate total':
                    new_key = 'desmate_total'
                    new_list_dict_with_column[index_dict][new_key] = value

                elif key.lower() == 'queimada':
                    new_key = 'queimada'
                    new_list_dict_with_column[index_dict][new_key] = value
                    
                elif key.lower() == 'classificação da área (15-17)'\
                  or key.lower() == 'classificacao da area (15-17)'\
                  or key.lower() == 'classific da área (15-17)'\
                  or key.lower() == 'classific da area (15-17)'\
                  or key.lower() == 'classificação área (15-17)'\
                  or key.lower() == 'classificacao area (15-17)'\
                  or key.lower() == 'classific área (15-17)'\
                  or key.lower() == 'classific area (15-17)':
                    new_key = 'classific_area_15_17'
                    new_list_dict_with_column[index_dict][new_key] = value

                else:
                    self.utils.error_message_and_stop_script(
                        'Error: A coluna com o nome "{}" é nova e não consta nos'\
                        ' padrões de nome de coluna do script.\n Verifique o nome'\
                        ' das colunas no arquivo {}'.format(key,file_name)
                    )
                    
        return new_list_dict_with_column


