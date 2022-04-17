import traceback
import time
import json
import requests
import sys
sys.path.append("..")
from database_utils.connector import get_conn, close_conn


# 当日详细数据
def get_detailed_data():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    res = requests.get(url, headers)

    # json字符串转字典
    data_all = json.loads(json.loads(res.text)["data"])

    # 当日详细数据
    details = []
    update_time = data_all["lastUpdateTime"]
    data_province = data_all["areaTree"][0]["children"]
    for pro_infos in data_province:
        province_name = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city_name = city_infos['name']
            confirm = city_infos['total']['confirm']
            confirm_add = city_infos['today']['confirm']
            heal = city_infos['total']['heal']
            dead = city_infos['total']['dead']
            details.append([
                update_time, province_name, city_name, confirm, confirm_add,
                heal, dead
            ])

    return details


# insert data into table details
# TODO： 这种方式可能会添加当天的重复数据
def update_details():
    cursor = None
    conn = None
    try:
        li = get_detailed_data()
        conn, cursor = get_conn()
        sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        # 对比当前最大时间戳
        sql_query = "select %s=(select update_time from details order by id desc limit 1)"
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f'{time.asctime()} 开始更新数据')
            for item in li:
                cursor.execute(sql, item)
            conn.commit()
            print(f"{time.asctime()} 更新到最新数据")
        else:
            print(f"{time.asctime()} 当前数据已经是最新数据")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
