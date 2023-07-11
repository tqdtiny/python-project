import time

import pandas as pd
import numpy as np
import pymysql
from datetime import datetime
from keras.layers import Dense
from sklearn import preprocessing
import keras

def deep_model(times,longitude,latitude):
    conn = pymysql.connect(host='119.91.135.214', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
    sql = "select time,level,lot,lat,deep from china_data where time>=2020"
    # 读取mysql数据库的数据为dataframe
    data = pd.read_sql_query(sql, conn)

    # 无效的日期替换成一个合法的日期，日没有0日
    data['time'] = data['time'].str.replace('-00', '-01')
    # 将给定的日期和时间转换为以秒为单位的 Unix 时间和数字。这可以很容易地用作我们构建的网络的入口
    data['Timestamp'] = data['time'].apply(
        lambda x: (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime(1970, 1, 1)).total_seconds())

    final_data1 = data.drop(['time'], axis=1)
    # 转换数据类型并删除包含非 float 值的行
    final_data = final_data1.convert_objects(convert_numeric=True)
    final_data.dropna(inplace=True)

    # 标准化数据
    scaler = preprocessing.StandardScaler()
    scaled_features = scaler.fit_transform(final_data.drop(['deep', 'level'], axis=1))
    scaled_labels = scaler.fit_transform(final_data[['level', 'deep']])

    # 构建模型
    model = keras.Sequential()
    model.add(Dense(16, activation='relu', kernel_initializer='random_normal',kernel_regularizer=keras.regularizers.l2(0.03)))
    model.add(Dense(32, activation='relu', kernel_initializer='random_normal',kernel_regularizer=keras.regularizers.l2(0.03)))
    # model.add(Dropout(0.2))
    model.add(Dense(2))
    model.compile(optimizer='adam', loss='mse', metrics=['accuracy'])

    # 调整批次大小
    batch_size = int(len(final_data) / 10)
    model.fit(scaled_features, scaled_labels, validation_split=0.2, epochs=100, batch_size=batch_size)

    # 预测新数据
    new_data = pd.DataFrame({'lot': [longitude], 'lat': [latitude], 'Timestamp': [times]})
    # 将给定的日期和时间转换为以秒为单位的 Unix 时间和数字。这可以很容易地用作我们构建的网络的入口
    new_data['Timestamp'] = new_data['Timestamp'].apply(
        lambda x: (datetime.strptime(x, '%Y-%m-%d %H:%M:%S') - datetime(1970, 1, 1)).total_seconds())
    # print(new_data)
    features_data = np.array(new_data)
    features = final_data.drop(['deep', 'level'], axis=1)
    features = np.array(features)
    arr3 = np.vstack((features_data, features))
    result = scaler.fit_transform(arr3)
    # print(result)
    prediction = model.predict(result)
    # print(prediction[0])
    scaled_labels1 = scaler.fit_transform(final_data[['level', 'deep']])
    unscaled_data = scaler.inverse_transform(prediction)

    print('New data prediction:', unscaled_data[0])
    return unscaled_data[0]



if __name__ == '__main__':
    deep_model('2023-04-16 00:12:45', 84.67, 44.05)