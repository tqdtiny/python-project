from flask import Flask, redirect, url_for, render_template, send_file
from flask import jsonify
import utlis
import re
import numpy as np
from flask import request
import testbp
# 解决中文乱码
class Config(object):
    DEBUG=True
    JSON_AS_ASCII=False

app = Flask(__name__)

# 获取时间
@app.route("/time")
def get_time():
    # print(utlis.get_time())
    return utlis.get_time()

# 主页
@app.route('/')
def hello_world():
    return render_template("home.html")
# 获取最近地震数据
@app.route("/get_all")
def get_all():
    # 实时更新中国数据
    utlis.update_details()
    # 实时更新美国数据
    utlis.usa_update_details()
    data = utlis.get_all()
    return jsonify(data)

# 获取中国各省份地震次数
@app.route("/c2")
def get_c2_data():
    res = []
    for tup in utlis.get_c2_data():
        # print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    # print(res)
    return jsonify({"data":res})

# 获取中国地震累计震级
@app.route("/l1")
def get_l1_data():
    data = utlis.get_l1_data()
    time,level = [],[]
    for a,b in data:
        # 使用正则只提取时间中的年份
        c = re.findall('^.*?(?= )', a)
        # print(c)
        time.append(c)
        level.append(b)
    # print(time)
    return jsonify({"level":level,"time":time})


app.config.from_object(Config)
@app.route("/l2")
def get_l2_data():
    data = utlis.get_l2_data()
    level_deep = []
    for i in data:
        level_deep.append(i)
    return jsonify({"data":level_deep})

@app.route("/r1")
def get_r1_data():
    data = utlis.get_r1_data()
    return jsonify({"data":data})

@app.route("/r2")
def get_r2_data():
    res = []
    for tup in utlis.get_c2_data():
        # print(tup)
        res.append({"name":tup[0],"value":int(tup[1])})
    print(res)
    return jsonify({"data":res})

@app.route('/predict', methods=['POST'])
def predict():
    time = request.form['time']
    longitude = float(request.form['longitude'])
    latitude = float(request.form['latitude'])
    data = testbp.deep_model(time, longitude, latitude)
    data_float = data.astype(np.float)
    result = np.round(data_float, decimals=2)
    return jsonify({'magnitude': result[0],'deep' : result[1]})

@app.route('/embed_html')
def embed_html():
    html_file_path = './fig1.html'  # 嵌入的 HTML 文件路径
    return send_file(html_file_path, mimetype='text/html')

@app.route('/embed1_html')
def embed1_html():
    html_file_path = './fig2.html'  # 嵌入的 HTML 文件路径
    return send_file(html_file_path, mimetype='text/html')

@app.route('/embed2_html')
def embed2_html():
    html_file_path = './fig3.html'  # 嵌入的 HTML 文件路径
    return send_file(html_file_path, mimetype='text/html')


@app.route("/search", methods=["POST"])
def search():
    place = request.form["place"]
    data = utlis.search_earthquake(place)
    print(data)
    results = [{"description": f"{row[0]} {row[1]} {row[2]} {row[3]}"} for row in data]
    print(results)
    return jsonify(results)


if __name__ == '__main__':
    app.run()
