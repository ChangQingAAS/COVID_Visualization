from .connector import query

def get_c1_data() -> tuple:
    """
    返回大屏div id = c1的数据
    """
    # because of updating data several times, get the newest data
    sql = """
    select sum(confirm),(select suspect from history order by ds desc limit 1), sum(heal), sum(dead) 
    from details 
    where update_time=(
        select update_time 
        from details 
        order by update_time desc 
        limit 1
    ) 
    """
    res = query(sql)
    return res[0]


# 返回各省数据
def get_c2_data():
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = """
    select province,sum(confirm) 
    from details 
    where update_time=(
        select update_time 
        from details
        order by update_time desc 
        limit 1
    ) 
    group by province
    """
    res = query(sql)
    return res


def get_l1_data():
    sql = """
    select ds,confirm,suspect,heal,dead 
    from history
    """
    res = query(sql)
    return res


def get_l2_data():
    # 因为会更新多次数据，取时间戳最新的那组数据
    sql = "select end_update_time,province,city,county,address,type" \
        " from risk_area " \
        "where end_update_time=(select end_update_time " \
        "from risk_area " \
        "order by end_update_time desc limit 1) "
    res = query(sql)
    return res


# 返回确诊人数前5名的city
def get_r1_data():

    sql = """
    SELECT city,confirm 
    FROM (
        select city,confirm 
        from details
        where update_time=(
            select update_time 
            from details 
            order by update_time desc 
            limit 1
        )   and  province not in ( "北京","上海","天津","重庆","香港","台湾") 
        union all 
            select province as city,sum(confirm) as confirm 
            from details  
            where update_time=(
                select update_time 
                from details 
                order by update_time desc 
                limit 1
            ) 
        and province in ("北京","上海","天津","重庆","香港","台湾") 
        group by province
        ) as a  
    ORDER BY confirm DESC 
    LIMIT 5
    """
    res = query(sql)
    return res


def get_r2_data():
    """
    :return:  返回最近的30条热搜
    """
    sql = 'select content from hotsearch order by id desc limit 30'
    res = query(sql)  # 格式 (('民警抗疫一线奋战16天牺牲 1037364',), ('四川再派两批医疗队 1537382',)
    return res
