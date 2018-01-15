#!/usr/bin/env python3
#-*- coding:utf-8 -*-


"""
y e a longitude e x a latitude
"""
import psycopg2

from constants import HOST,PASSWD,USER,DATABASE,SCHEMA
from utils import Utils

class dao:
	
	utils = None

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

