import time
import pymysql
import traceback
import requests
import re
from bs4 import BeautifulSoup
import updata_cityname
import pandas as pd
from sqlalchemy import create_engine

import plotly.express as px
import plotly.io as pio
import numpy as np


# 获取服务器时间戳
def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年","月","日")

# 爬虫
def get_china_data(pcount,url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
    }

    # url = 'http://ditu.92cha.com/dizhen.php?dizhen_ly=china'
    # resp = requests.get(url, headers=headers)
    # print(resp)
    # html = resp.text
    # soup = BeautifulSoup(html, 'lxml')
    csv_file = 'earthQuake_china.csv'
    resp = requests.get(url, headers=headers)
    # 获取总页数
    r = re.compile('查询到 (\d+) 条记录，分 (\d+) 页显示')
    # pcount = int(r.findall(resp.text)[0][1])

    # print(pcount)
    # 爬取内容
    china_data = []
    # fp.write('times, level, place, longitude, latitude, deep \n')
    for page in range(1, pcount + 1):
        print('第%d页/共%d页' % (page, pcount), '...', end='')
        # 获取全部页面网址
        all_url = (url + '&page=%d' % page)
        # print(all_url)
        resp = requests.get(all_url, headers=headers)
        soup = BeautifulSoup(resp.text, 'lxml')
        # 获取当前网页中所有地震数目（tr）
        for tr in soup.find_all('tr')[1:]:
            # 获得当前页面所有页面的地震数据：发震时刻、震级、参考位置、经度、维度、深度（td）
            tds = tr.find_all('td')
            # 爬取发震时刻
            times = tds[0].text
            # print(times)
            # 爬取震级
            level = tds[1].text
            # print(level)
            # 爬取参考位置
            places = tds[2].text
            place = places.replace("（显示地图）","") #删除位置中的（显示地图）
            # print(place)

            # print(place)
            # 爬取经度
            longitude = tds[3].text
            # print(longitude)
            # 爬起维度
            latitude = tds[4].text
            # print(latitude)
            # 爬取深度
            deep = tds[5].text
            china_data.append([times, level, place, longitude, latitude, deep])
            # print(china_data)
        print('Done')

    return china_data

# 创建数据库连接
def get_conn():
    # 建立连接
    conn = pymysql.connect(host='你的服务器IP地址',port=3306,user='earthquake',password='123456',database='earthquake',charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor

# 关闭服务器连接
def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# mysql通用查询,return返回查询到的结果是((),())的元组形式
def query(sql,*args):
    conn, cursor = get_conn()
    cursor.execute(sql,args)
    res = cursor.fetchall()
    close_conn(conn,cursor)
    return res
# 返回大屏div id=c1的数据，因为会更新多次数据，所以取时间戳最新的数据
#(select place, count(*) as frequency from china_data group by place order by frequency desc limit 1)

def get_all():
    conn = pymysql.connect(host='你的服务器IP地址', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
    sql = "select time,place,level from china_data limit 10"
    # 创建游标
    cursor = conn.cursor()
    data1 = cursor.execute(sql)
    result = cursor.fetchall()
    datalist = []
    for item in result:
        datalist.append(item)
    cursor.close()
    conn.close()
    return datalist

#获取发生地震的次数，传给c2
def get_c2_data():
    res = updata_cityname.upcity()
    # print(res)
    return res


def get_l1_data():
    sql = 'select time,level from china_data where time=2023 order by time asc'
    res = query(sql)
    return res

def get_l2_data():
    conn = pymysql.connect(host='你的服务器IP地址', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    sql = 'select deep, level from china_data where deep != 0'
    df = pd.read_sql(sql, conn)
    result = df.values.tolist()
    cursor.close()
    conn.close()
    # print(result)
    return result

def get_r1_data():
    engine = create_engine('mysql+pymysql://earthquake:123456@你的服务器IP地址/earthquake')
    df_china = pd.read_sql(sql='select * from china_data', con=engine)  # 读取中国地震局数据
    level_count_list =df_china['level'].values.tolist()
    # 设置分段
    bins = [0, 1, 2, 3, 5, 7, 15]
    # 设置标签
    labels = ['0-1', '1-2', '2-3', '3-5', '5-7', '7-15']
    # 按分段离散化数据
    segments = pd.cut(level_count_list, bins, labels=labels)  # 按分段切割数据
    counts = pd.value_counts(segments, sort=False).values.tolist()  # 统计个数
    # print(counts)
    return counts

def search_earthquake(keyword):
    conn = pymysql.connect(host='你的服务器IP地址', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
    # 创建游标
    cursor = conn.cursor()
    sql = 'select time,place,level,deep,citys,provinces from china_data'
    earthquake_df = pd.read_sql(sql, conn)
    # 首先在provinces列中搜索关键字
    result = earthquake_df[earthquake_df['provinces'].str.contains(keyword)]

    # 如果在provinces列中没有找到，则在city列中搜索关键字
    if result.empty:
        result = earthquake_df[earthquake_df['citys'].str.contains(keyword)]

    result.to_dict('records')
    earthquake_data = []
    for index, row in result.iterrows():
        data = (row['time'], row['place'], row['level'], row['deep'])
        earthquake_data.append(data)
    print(earthquake_data)

    return earthquake_data

#更新中国数据细节函数
def update_details():
    cursor = None
    conn = None
    url = 'http://ditu.92cha.com/dizhen.php?dizhen_ly=china'
    try:
        li = get_china_data(1,url)
        print(li)

        conn, cursor = get_conn()
        sql = "INSERT INTO china_data(time, level, place, lot, lat, deep, citys, provinces) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        order_sql = "ALTER TABLE china_data ORDER BY time DESC"  # 按时间戳从大到小重新排列表格
        max_timestamp_query = "SELECT MAX(time) FROM china_data"
        sql_query = 'SELECT %s = (SELECT time FROM china_data ORDER BY time DESC LIMIT 1)'

        # 获取数据库中最新数据的时间戳
        cursor.execute(max_timestamp_query)
        max_timestamp = cursor.fetchone()[0]

        # 对比当前最大时间戳
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新数据")

            # 转为dataframe
            columns = ['time', 'level', 'place', 'lot', 'lat', 'deep']
            china_data = pd.DataFrame(li, columns=columns)
            # 中国地震局数据中地震所在地（省市）
            # 由于在原始数据中参考位置无法便捷的解析出省和市，我这边打算用经纬度信息通过百度的API来进行获取
            citys = []
            provinces = []
            for i, location in enumerate(china_data[['lot', 'lat']].values):
                location = str(location[1]) + ',' + str(location[0])
                # 删除lot数据前面的空格
                location1 = location.lstrip()
                url = 'https://api.map.baidu.com/reverse_geocoding/v3/?'
                params = {
                    'location': location,
                    'ak': 'yFOGwrppvTFaSoeN2cdqr9cDU5aBwp0e',
                    'output': 'json',
                }

                r = requests.get(url, params)
                data = r.json()['result']
                city = data['addressComponent']['city']
                province = data['addressComponent']['province']
                if len(city) == 0:
                    city = province
                citys.append(city)
                provinces.append(province)
                print(f'\r{i + 1}', end='')
            china_data['citys'] = citys
            china_data['provinces'] = provinces
            # 将DataFrame转换为列表格式
            li = china_data.values.tolist()
            # 根据原来的数据格式进行处理
            for i, item in enumerate(li):
                li[i][3] = float(item[3])
                li[i][4] = float(item[4])
                li[i][5] = float(item[5])

            print(li)
            # 更新数据库内容
            for item in li:
                if item[0] > max_timestamp:  # 比较时间戳
                    cursor.execute(sql, item)
                else:
                    continue  # 忽略旧数据

            cursor.execute(order_sql)
            conn.commit()

            print(f"{time.asctime()}更新到中国最新数据")
        else:
            print(f"{time.asctime()}已是中国最新数据！")
    except:
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
# 更新美国数据
def usa_update_details():
    cursor = None
    conn = None
    url = 'http://ditu.92cha.com/dizhen.php?dizhen_ly=usa'
    try:
        li = get_china_data(1,url)
        print(li)

        conn, cursor = get_conn()
        sql = "INSERT INTO usa_data(time, level, place, lot, lat, deep) VALUES(%s, %s, %s, %s, %s, %s)"
        order_sql = "ALTER TABLE usa_data ORDER BY time DESC"  # 按时间戳从大到小重新排列表格
        max_timestamp_query = "SELECT MAX(time) FROM usa_data"
        sql_query = 'SELECT %s = (SELECT time FROM usa_data ORDER BY time DESC LIMIT 1)'

        # 获取数据库中最新数据的时间戳
        cursor.execute(max_timestamp_query)
        max_timestamp = cursor.fetchone()[0]

        # 对比当前最大时间戳
        cursor.execute(sql_query, li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新数据")

            # 更新数据库内容
            for item in li:
                if item[0] > max_timestamp:  # 比较时间戳
                    cursor.execute(sql, item)
                else:
                    continue  # 忽略旧数据

            cursor.execute(order_sql)
            conn.commit()

            print(f"{time.asctime()}更新到美国最新数据")
        else:
            print(f"{time.asctime()}已是美国最新数据！")
    except:
        traceback.print_exc()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



if __name__ == '__main__':
    # print(get_l1_data())
    # update_details()
    # print(get_c2_data())
    # a = get_all()
    # print(search_earthquake('黑龙江'))
    # get_r1_data()
    # print(get_all())
    usa_update_details()
    # update_details()
