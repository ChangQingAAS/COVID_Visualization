from bs4 import BeautifulSoup
import requests
import time
import traceback
from selenium.webdriver import Chrome, ChromeOptions
import sys
sys.path.append("..")
from database_utils.connector import get_conn, close_conn


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
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
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
