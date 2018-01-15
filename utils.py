import sys

class Utils:

    def message_and_stop_script(self,exception_msg,custom_msg):
        print('\nError: {}\n\n{}\n'.format(exception_msg,custom_msg))
        sys.exit()


class Adapter:

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

        return dict_column_name_index

