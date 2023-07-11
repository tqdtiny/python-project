import plotly.express as px
import plotly.io as pio
import pandas as pd
import numpy as np
import pymysql
import datetime
import folium.plugins as plugins
import folium
import requests

conn = pymysql.connect(host='你的服务器IP地址', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
sql = "select * from usa_data where time>=2010"

# 读取mysql数据库的数据为dataframe
data = pd.read_sql_query(sql, conn)

# 无效的日期替换成一个合法的日期,日没有0日
data['time'] = data['time'].str.replace('-00', '-01')
# 需要先将Series类型的数据转换成字符串类型，然后再调用strptime()函数进行处理。
data['time_str'] = data['time'].apply(lambda x: str(x))
data['year'] = data['time_str'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S').year)
# 数据按year列升序
data = data.sort_values(by=['year'], ascending=True)

fig1 = px.scatter_geo(data,
                      color=data.level,
                      color_continuous_scale=px.colors.sequential.Inferno,
                      lon=data.lot,
                      lat=data.lat,
                      hover_name=data.place,
                      hover_data=["lot",
                                  "lat",
                                  "time",
                                  "level",
                                  "deep"
                                  ],
                      size=np.exp(data.level) / 100,
                      projection="equirectangular",
                      title='地震频发地带'
                      )
# fig1.show()
pio.write_html(fig1, 'fig1.html')

fig2 = px.scatter_geo(data,
                      color = data.level,
                      color_continuous_scale = px.colors.sequential.Inferno,
                      lon = data.lot,
                      lat = data.lat,
                      animation_frame = data.year,
                      hover_name = data.place,
                      hover_data = ["lot",
                                    "lat",
                                    "time",
                                    "level",
                                    "deep"
                                   ],
                      size = np.exp(data.level)/100,
                      projection = "equirectangular",
                      title = '2010-2022年全球重大地震'
                      )

pio.write_html(fig2, 'fig2.html')

# 找到需要删除的行
index_to_drop = data[data['lot'] == '西藏自治区那曲地区安多县交界'].index

# 使用drop()方法删除行
df = data.drop(index_to_drop)

data_all = df[['lat', 'lot', 'level']].values.tolist()
m = folium.Map(location=[39.904989, 116.405285],
               tiles='OpenStreetMap',
               zoom_start=4)

plugins.HeatMap(data_all,
                radius=10,
                min_opacity=0.5,
                max_val=max(data['level']),
                gradient={.1: 'green', .6: 'yellow', 1: 'red'},
               ).add_to(m)

m.save('fig3.html')
