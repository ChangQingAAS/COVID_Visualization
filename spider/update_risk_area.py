import time
import hashlib
import json
import requests
import traceback
import sys
sys.path.append("..")
from database_utils.connector import get_conn, close_conn


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
        str(e + 'fTN2pfuisxTavbTuYVSsNJHetwq5bJvCQkjjtiLM2dCratiA' +
            e).encode("utf8"))
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
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
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
