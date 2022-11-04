# from flask_mysqldb import MySQL

# mysql = MySQL()
# -*- coding: utf8 -*-
from os import getenv
import pymysql
from pymysql.err import OperationalError
mysql_conn = None

if not mysql_conn:
    mysql_conn = pymysql.connect(
      host        = getenv('DB_HOST', '43.143.90.80'),
      user        = getenv('DB_USER','share'),
      password    = getenv('DB_PASSWORD','Take@@2022Xie'),
      db          = getenv('DB_DATABASE','lims-meinv'),
      port        = int(getenv('DB_PORT','33307')),
      charset     = 'utf8mb4',
      autocommit  = True
    )


def __get_cursor():
    mysql_conn.ping(reconnect=True)
    return mysql_conn.cursor(pymysql.cursors.DictCursor)
    # try:
    #     return mysql_conn.cursor(pymysql.cursors.DictCursor)
    # except OperationalError:
    #     mysql_conn.ping(reconnect=True)
    #     return mysql_conn.cursor(pymysql.cursors.DictCursor)