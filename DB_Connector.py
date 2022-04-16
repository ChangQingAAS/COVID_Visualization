import pymysql
from config import *


def get_conn():
    # 建立连接
    conn = pymysql.connect(host=HOST,
                           user=USER,
                           password=PASSWORD,
                           db=DATABASE,
                           charset=CHARSET)
    # 创建游标
    cursor = conn.cursor()
    # 执行完毕返回的结果集默认以元组显示
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql: str, *args) -> tuple:
    """封装通用查询

    Args:
        sql (_type_): _description_
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res
