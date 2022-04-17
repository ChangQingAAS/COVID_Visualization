import time
import traceback
import json
import requests
import sys
sys.path.append("..")
from database_utils.connector import get_conn, close_conn


# 返回历史数据和当日详细数据
def get_history_data():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
    }
    res = requests.get(url, headers)

    # json字符串转字典
    data_all = json.loads(json.loads(res.text)["data"])

    # 历史数据
    history = {}
    for i in data_all["chinaDayList"]:
        # 匹配时间
        tmp = time.strptime(i["y"] + "." + i["date"], "%Y.%m.%d")
        # 改变时间格式，适应数据库
        ds = time.strftime("%Y-%m-%d", tmp)
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {
            "confirm": confirm,
            "suspect": suspect,
            "heal": heal,
            "dead": dead
        }

    for i in data_all["chinaDayAddList"]:
        # 匹配时间
        tmp = time.strptime(i["y"] + "." + i["date"], "%Y.%m.%d")
        # 改变时间格式，适应数据库
        ds = time.strftime("%Y-%m-%d", tmp)
        confirm_add = i["confirm"]
        suspect_add = i["suspect"]
        heal_add = i["heal"]
        dead_add = i["dead"]
        try:
            history[ds].update({
                "confirm_add": confirm_add,
                "suspect_add": suspect_add,
                "heal_add": heal_add,
                "dead_add": dead_add
            })
        except Exception as e:
            history[ds] = {
                "confirm": None,
                "suspect": None,
                "heal": None,
                "dead": None,
                "confirm_add": confirm_add,
                "suspect_add": suspect_add,
                "heal_add": heal_add,
                "dead_add": dead_add
            }

    return history


# insert history data into table history
def insert_history():
    cursor = None
    conn = None
    try:
        dic = get_history_data()
        print(f"{time.asctime()} 开始更新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [
                    k,
                    v.get("confirm"),
                    v.get("confirm_add"),
                    v.get("suspect"),
                    v.get("suspect_add"),
                    v.get("heal"),
                    v.get("heal_add"),
                    v.get("dead"),
                    v.get("dead_add")
                ])
                conn.commit()
        print(f"{time.asctime()} 更新历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
