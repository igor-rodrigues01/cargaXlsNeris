#!/usr/bin/env python3
#-*-coding:utf-8-*-

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
        
        self.dao.execute_insert_in_sema_and_icmbio(
            columns_name_sema,sheets_data_sema,
            columns_name_icmbio,xls_data_icmbio
        )

if __name__ == '__main__':
    Main().main()
