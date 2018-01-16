#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
y e a longitude e x a latitude
"""
import psycopg2

from constants import HOST,PASSWD,USER,DATABASE,SCHEMA
from utils import Utils
from process_xls import Xls

class Dao:
    
    utils = None

    def __init__(self):
        self.utils = Utils()

    def connection(self):
        """
        Funcao que realiza a conexao com a base de daddos
        """
        conn = None

        try:
            conn = psycopg2.connect(
               host=HOST,
               user=USER,
               password=PASSWD,
               database=DATABASE
            )
        except Exception as ex:
            self.utils.message_and_stop_script(
                ex,'Erro na conexão'
            )
        return conn

    def insert_sema(self,cursor,columns_name,row_data):
        sql = None

        if row_data[columns_name['lat']] == ''\
          or row_data[columns_name['lat']] == None\
          or row_data[columns_name['lng']] == ''\
          or row_data[columns_name['lng']] == None:
            sql = "insert into sema(num_identificacao, dt_lavratura, desc_sucinta_fato, id_processo_administrativo, nom_propriedade, nom_proprietario, cpf, area, exploracao, desmate_app, desmate_total, queimada, classificacao_area)"\
            " values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"
            sql = sql.format(
                row_data[columns_name['num_identificacao']],row_data[columns_name['dt_lavratura']],
                row_data[columns_name['desc_sucinta_fato']],row_data[columns_name['id_proc_administrativo']],
                row_data[columns_name['nom_propriedade']],row_data[columns_name['nom_proprietario']],
                row_data[columns_name['cpf']],
                row_data[columns_name['area_15_17']],row_data[columns_name['explor_ha']],
                row_data[columns_name['desmate_app_ha']],row_data[columns_name['desmate_total']],
                row_data[columns_name['queimada']],row_data[columns_name['classific_area_15_17']]
            )
        else:
            sql = "insert into sema(num_identificacao, dt_lavratura, desc_sucinta_fato, id_processo_administrativo, nom_propriedade, nom_proprietario, cpf, geom, area, exploracao, desmate_app, desmate_total, queimada, classificacao_area)"\
            "values('{}','{}','{}','{}','{}','{}','{}',st_setsrid(ST_MakePoint({}, {}),4674),'{}','{}','{}','{}','{}','{}')"
            sql = sql.format(
                row_data[columns_name['num_identificacao']],row_data[columns_name['dt_lavratura']],
                row_data[columns_name['desc_sucinta_fato']],row_data[columns_name['id_proc_administrativo']],
                row_data[columns_name['nom_propriedade']],row_data[columns_name['nom_proprietario']],
                row_data[columns_name['cpf']],row_data[columns_name['lat']],row_data[columns_name['lng']],
                row_data[columns_name['area_15_17']],row_data[columns_name['explor_ha']],
                row_data[columns_name['desmate_app_ha']],row_data[columns_name['desmate_total']],
                row_data[columns_name['queimada']],row_data[columns_name['classific_area_15_17']]
            )
        cursor.execute(sql)

    def insert_icmbio(self,cursor,dict_column_name,xls_data):
        
        if xls_data[dict_column_name['dt_auto']] is not 'null':
            sql = "insert into icmbio (id,num_auto_infracao, serie, cpfj, autuado, desc_infracao, art_1, art_2, tipo_infracao, nome_uc, cnuc, municipio, uf, dt_auto, obs_embargo, area, num_processo)"\
            " values({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')";
        else:
            sql = "insert into icmbio (id,num_auto_infracao, serie, cpfj, autuado, desc_infracao, art_1, art_2, tipo_infracao, nome_uc, cnuc, municipio, uf, dt_auto, obs_embargo, area, num_processo)"\
            " values({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{},'{}','{}','{}')";

        sql = sql.format(
            xls_data[dict_column_name['id']],xls_data[dict_column_name['num_auto_infracao']],
            xls_data[dict_column_name['serie']],xls_data[dict_column_name['cpfj']],
            xls_data[dict_column_name['autuado']],xls_data[dict_column_name['desc_infracao']],
            xls_data[dict_column_name['art_1']],xls_data[dict_column_name['art_2']],
            xls_data[dict_column_name['tipo_infracao']],xls_data[dict_column_name['nom_uc']],
            xls_data[dict_column_name['cnuc']],xls_data[dict_column_name['municipio']],
            xls_data[dict_column_name['uf']],xls_data[dict_column_name['dt_auto']],
            xls_data[dict_column_name['obs_embargo']],xls_data[dict_column_name['area']],
            xls_data[dict_column_name['num_processo']]
        )

        cursor.execute(sql)

    def truncate_sema(self):
        pass

    def truncate_icmbio(self):
        pass

    def execute_insert_in_sema_and_icmbio(self,columns_name_sema,
        sheets_data_sema,columns_name_icmbio,xls_data_icmbio):
        conn                = self.connection()
        cursor              = conn.cursor()
        data_counter_sema   = 0
        data_counter_icmbio = 0

        try:
            for sheet in sheets_data_sema:
                sheet_index = sheets_data_sema.index(sheet)
                for row in sheet:
                    self.insert_sema(cursor,columns_name_sema[sheet_index],row)
                    data_counter_sema += 1

            for data in xls_data_icmbio:
                self.insert_icmbio(cursor,columns_name_icmbio,data)
                data_counter_icmbio += 1 
        
        except Exception as ex:
            self.utils.error_message_and_stop_script(
                'Error: erro na inserção de dados.',ex
            )
            conn.rollback()
        else:
            conn.commit()
            print('{} records inserted in the table sema.'.format(data_counter_sema))
            print('{} records inserted in the table icmbio.'.format(data_counter_icmbio))


if __name__ == '__main__':
    Dao().execute_insert_in_sema_and_icmbio()