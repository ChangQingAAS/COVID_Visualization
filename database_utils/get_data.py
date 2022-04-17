from .connector import query


# 返回大屏div id = c1的数据
def get_c1_data() -> tuple:
    with open("./database_utils/sql/center1.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res[0]


# 返回各省数据
def get_c2_data() -> tuple:
    with open("./database_utils/sql/center2.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res


def get_l1_data() -> tuple:
    with open("./database_utils/sql/left1.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res


def get_l2_data() -> tuple:
    with open("./database_utils/sql/left2.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res


# 返回确诊人数前5名的city
def get_r1_data() -> tuple:
    with open("./database_utils/sql/right1.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res


# 返回最近的30条热搜
def get_r2_data() -> tuple:
    with open("./database_utils/sql/right2.sql", encoding="utf-8") as f:
        sql = f.read()
    res = query(sql)
    return res
