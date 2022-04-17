from flask import Flask, render_template, jsonify
from jieba.analyse import extract_tags
from time import strftime
import string
import random

from config import *
import database_utils.get_data as get_data

app = Flask(__name__)


@app.route('/')
def handle():
    return render_template('main.html')


@app.route("/c1")
def c1_handle():
    data = get_data.get_c1_data()
    return jsonify({
        'confirm': int(data[0]),
        "suspect": int(data[1]),
        "heal": int(data[2]),
        "dead": int(data[3])
    })


@app.route("/c2")
def c2_handle():
    res = []
    for tup in get_data.get_c2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({'data': res})


@app.route("/l1")
def l1_handle():
    data = get_data.get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    # 很多卫健委网站前7天都是没有数据的，所以把前7天砍掉了
    for da, co, su, he, de in data:
        day.append(da.strftime("%m-%d"))
        confirm.append(co)
        suspect.append(su)
        heal.append(he)
        dead.append(de)
    return jsonify({
        "day": day,
        "confirm": confirm,
        "suspect": suspect,
        "heal": heal,
        "dead": dead
    })


@app.route("/l2")
def get_l2_data():
    data = get_data.get_l2_data()
    # end_update_time, province, city, county, address, type
    details = []
    risk = []
    end_update_time = data[0][0]
    for a, b, c, d, e, f in data:
        risk.append(f)
        details.append(f"{b}\t{c}\t{d}\t{e}")
    return jsonify({
        "update_time": end_update_time,
        "details": details,
        "risk": risk
    })


@app.route("/r1")
def r1_handle():
    data = get_data.get_r1_data()
    city, confirm = [], []
    for ci, con in data:
        city.append(ci)
        confirm.append(int(con))
    return jsonify({"city": city, "confirm": confirm})


@app.route('/r2')
def r2_handle():
    # 格式 (('民警抗疫一线奋战16天牺牲1037364',), ('四川再派两批医疗队1537382',)
    data = get_data.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)  # 移除热搜数字
        v = i[0][len(k):]  # 获取热搜数字
        ks = extract_tags(k)  # 使用jieba 提取关键字
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": v})
    return jsonify({"kws": d})


if __name__ == "__main__":
    app.run(host=HOST,
            port=PORT + int(random.random() * random.random() * 10000))
