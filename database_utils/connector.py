import pymysql
from .config import *


def get_conn():
    # 建立连接
    conn = pymysql.connect(host=HOST,
                           user=USER,
                           password=PASSWORD,
                           db=DATABASE,
                           charset=CHARSET)
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


# 封装通用查询
def query(sql: str, *args) -> tuple:
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res
