#!/usr/bin/env python3
#-*-coding:utf-8-*-

"""
Para que este escript funcionasse de forma precisa, na lib xlrd para corrigir
um problema de obtencao de formatacao das celulas na linha 793 do arquvivo
/home/<user>/.virtualenvs/<EnvironmentName>/lib/python3.5/site-packages/xlrd/xlsx.py
(ou um path equivalente que chegue no source code das lib's python) 
foi alterado: "if formatting_info:" para "if not formatting_info:"

"""
from process_xls import Xls
from dao import Dao

class Main:
    
    xls = None
    dao = None

    def __init__(self):
        self.xls = Xls()
        self.dao = Dao()
        
    def main(self):
        columns_name_sema,sheets_data_sema  = self.xls.get_sema()
        columns_name_icmbio,xls_data_icmbio = self.xls.get_icmbio()
        
        self.dao.truncate_sema()
        self.dao.truncate_icmbio()
        self.dao.execute_insert_in_sema_and_icmbio(
            columns_name_sema,sheets_data_sema,
            columns_name_icmbio,xls_data_icmbio
        )
        self.dao.close_connection()

if __name__ == '__main__':
    Main().main()
