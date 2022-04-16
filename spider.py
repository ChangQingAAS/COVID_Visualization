import requests
import json
import time
from selenium.webdriver import Chrome, ChromeOptions
import traceback
import sys
from DB_Connector import get_conn, close_conn
import hashlib
import sys
from bs4 import BeautifulSoup


# 返回历史数据和当日详细数据
def get_history_data():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
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
        history[ds] = {"confirm": confirm,
                       "suspect": suspect, "heal": heal, "dead": dead}

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
            history[ds].update({"confirm_add": confirm_add, "suspect_add": suspect_add,
                                "heal_add": heal_add, "dead_add": dead_add})
        except Exception as e:
            history[ds] = {"confirm": None,
                           "suspect": None, "heal": None, "dead": None, "confirm_add": confirm_add, "suspect_add": suspect_add,
                           "heal_add": heal_add, "dead_add": dead_add}

    return history


# 当日详细数据
def get_detailed_data():
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'
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
            details.append([update_time, province_name,
                            city_name, confirm, confirm_add, heal, dead])

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


# insert history data into table history
def insert_history():
    cursor = None
    con = None
    try:
        dic = get_history_data()
        print(f"{time.asctime()} 开始插入数据")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        for k, v in dic.items():
            cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                 v.get("suspect_add"), v.get(
                                     "heal"), v.get("heal_add"),
                                 v.get("dead"), v.get("dead_add")])
            conn.commit()
        print(f"{time.asctime()} 插入历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 更新历史数据
def update_history():
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
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get(
                                     "heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
                conn.commit()
        print(f"{time.asctime()} 更新历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 返回百度疫情热搜
def get_baidu_hot():
    # # url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
    # # headers = {
    # #     'User-Agent':
    # #     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    # # }
    # # res = requests.get(url=url, headers=headers)
    # # print(res.text)
    # option = ChromeOptions()  # 创建谷歌浏览器实例
    # option.add_argument("--headless")  # 隐藏浏览器
    # # option.add_argument("--no-sandbox")  # 禁用沙盘    部署在linux上访问chrome要求这样
    # # 指定用户客户端-模拟手机浏览
    # option.add_argument(
    #     'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"')

    # url = 'https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1'
    # brower = Chrome(options=option)
    # brower.get(url)
    # # 找到展开按钮
    # # but = brower.find_element_by_css_selector(
    # # '#ptab-0 > div > div.VirusHot_1-5-5_32AY4F.VirusHot_1-5-5_2RnRvg > section > div')  # 定位到点击展开按钮
    # but = brower.find_element_by_css_selector(
    #     '#ptab-1 > div.Virus_1-1-344_2SKAfr > div.Common_1-1-344_3lDRV2')

    # but.click()  # 点击展开

    # time.sleep(1)  # 爬虫与反爬，模拟人等待1秒

    # c = brower.find_elements_by_xpath(
    #     '//*[@id="ptab-0"]/div/div[2]/section/a/div/span[2]')
    # context = [i.text for i in c]  # 获取标签内容
    # print(context)
    # return context
    url = "https://top.baidu.com/board?tab=realtime"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    }
    res = requests.get(url, headers=headers)
    # res.encoding = "gb2312"
    html = res.text
    soup = BeautifulSoup(html, features="html.parser")
    kw = soup.select("div.c-single-text-ellipsis")
    count = soup.select("div.hot-index_1Bl1a")
    context = []
    for i in range(len(kw)):
        k = kw[i].text.strip()  # 移除左右空格
        v = count[i].text.strip()
        #         print(f"{k}{v}".replace('\n',''))
        context.append(f"{k}{v}".replace('\n', ''))
    return context


# 将疫情热搜插入数据库
def update_hotsearch():
    cursor = None
    conn = None
    try:
        context = get_baidu_hot()
        print(f"{time.asctime()}开始更新热搜数据")
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            cursor.execute(sql, (ts, i))  # 插入数据
        conn.commit()  # 提交事务保存数据
        print(f"{time.asctime()}数据更新完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def get_risk_area():
    """
    :return: risk_h,risk_m 中高风险地区详细数据
    """
    # 当前时间戳
    o = '%.3f' % (time.time() / 1e3)
    e = o.replace('.', '')
    i = "23y0ufFl5YxIyGrI8hWRUZmKkvtSjLQA"
    a = "123456789abcdefg"
    # 签名1
    s1 = hashlib.sha256()
    s1.update(str(e + i + a + e).encode("utf8"))
    s1 = s1.hexdigest().upper()
    # 签名2
    s2 = hashlib.sha256()
    s2.update(
        str(e + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA' + e).encode("utf8"))
    s2 = s2.hexdigest().upper()
    # post请求数据
    post_dict = {
        'appId': 'NcApplication',
        'key': '3C502C97ABDA40D0A60FBEE50FAAD1DA',
        'nonceHeader': '123456789abcdefg',
        'paasHeader': 'zdww',
        'signatureHeader': s1,
        'timestampHeader': e
    }
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'Referer': 'http://bmfw.www.gov.cn/',
        'Origin': 'http://bmfw.www.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'x-wif-nonce': 'QkjjtiLM2dCratiA',
        'x-wif-paasid': 'smt-application',
        'x-wif-signature': s2,
        'x-wif-timestamp': e,
    }
    url = "http://103.66.32.242:8005/zwfwMovePortal/interface/interfaceJson"
    req = requests.post(url=url, data=json.dumps(post_dict), headers=headers)
    resp = req.text
    res = json.loads(resp)
    # print(res)
    utime = res['data']['end_update_time']  # 更新时间
    hcount = res['data'].get('hcount', 0)  # 高风险地区个数
    mcount = res['data'].get('mcount', 0)  # 低风险地区个数
    # 具体数据
    hlist = res['data']['highlist']
    mlist = res['data']['middlelist']

    risk_h = []
    risk_m = []

    for hd in hlist:
        type = "高风险"
        province = hd['province']
        city = hd['city']
        county = hd['county']
        area_name = hd['area_name']
        communitys = hd['communitys']
        for x in communitys:
            risk_h.append([utime, province, city, county, x, type])

    for md in mlist:
        type = "中风险"
        province = md['province']
        city = md['city']
        county = md['county']
        area_name = md['area_name']
        communitys = md['communitys']
        for x in communitys:
            risk_m.append([utime, province, city, county, x, type])

    return risk_h, risk_m


def update_risk_area():
    """
        更新 risk_area 表
        :return:
        """
    cursor = None
    conn = None
    try:
        risk_h, risk_m = get_risk_area()
        conn, cursor = get_conn()
        sql = "insert into risk_area(end_update_time,province,city,county,address,type) values(%s,%s,%s,%s,%s,%s)"
        # 对比当前最大时间戳
        sql_query = 'select %s=(select end_update_time from risk_area order by id desc limit 1)'
        cursor.execute(sql_query, risk_h[0][0])  # 传入最新时间戳
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新最新数据")
            for item in risk_h:
                cursor.execute(sql, item)
            for item in risk_m:
                cursor.execute(sql, item)
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        s = """参数说明：
        0 update_history 
        1 update_details
        3 update_risk
        others update_hotsearch
        """
        print(s)
    else:
        _choice = sys.argv[1]
        if _choice == "0":
            update_history()
        elif _choice == "1":
            update_details()
        elif _choice == "2":
            update_risk_area()
        else:
            update_hotsearch()
