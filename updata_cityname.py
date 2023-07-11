import pymysql
import utlis
def upcity():
    sql0 = "update china_data set provinces = '北京' where provinces like '%北京%'"
    sql1 = "update china_data set provinces = '天津' where provinces like '%天津%'"
    sql2 = "update china_data set provinces = '河北' where provinces like '%河北%'"
    sql3 = "update china_data set provinces = '山西' where provinces like '%山西%'"
    sql4 = "update china_data set provinces = '内蒙古' where provinces like '%内蒙古%'"
    sql5 = "update china_data set provinces = '黑龙江' where provinces like '%黑龙江%'"
    sql6 = "update china_data set provinces = '上海' where provinces like '%上海%'"
    sql7 = "update china_data set provinces = '江苏' where provinces like '%江苏%'"
    sql8 = "update china_data set provinces = '浙江' where provinces like '%浙江%'"
    sql9 = "update china_data set provinces = '安徽' where provinces like '%安徽%'"
    sql10 = "update china_data set provinces = '福建' where provinces like '%福建%'"
    sql11 = "update china_data set provinces = '山东' where provinces like '%山东%'"
    sql12 = "update china_data set provinces = '河南' where provinces like '%河南%'"
    sql13 = "update china_data set provinces = '湖北' where provinces like '%湖北%'"
    sql14 = "update china_data set provinces = '湖南' where provinces like '%湖南%'"
    sql15 = "update china_data set provinces = '广东' where provinces like '%广东%'"
    sql16 = "update china_data set provinces = '广西' where provinces like '%广西%'"
    sql17 = "update china_data set provinces = '海南' where provinces like '%海南%'"
    sql18 = "update china_data set provinces = '重庆' where provinces like '%重庆%'"
    sql19 = "update china_data set provinces = '四川' where provinces like '%四川%'"
    sql20 = "update china_data set provinces = '贵州' where provinces like '%贵州%'"
    sql21 = "update china_data set provinces = '云南' where provinces like '%云南%'"
    sql22 = "update china_data set provinces = '西藏' where provinces like '%西藏%'"
    sql23 = "update china_data set provinces = '陕西' where provinces like '%陕西%'"
    sql24 = "update china_data set provinces = '甘肃' where provinces like '%甘肃%'"
    sql25 = "update china_data set provinces = '青海' where provinces like '%青海%'"
    sql26 = "update china_data set provinces = '宁夏' where provinces like '%宁夏%'"
    sql27 = "update china_data set provinces = '新疆' where provinces like '%新疆%'"
    sql28 = "update china_data set provinces = '香港' where provinces like '%香港%'"
    sql29 = "update china_data set provinces = '澳门' where provinces like '%澳门%'"
    sql30 = "update china_data set provinces = '台湾' where provinces like '%台湾%'"
    sql31 = "update china_data set provinces = '南海诸岛' where provinces like '%南海%'"
    sql32 = "update china_data set provinces = '江西' where provinces like '%江西%'"
    sql33 = "update china_data set provinces = '辽宁' where provinces like '%辽宁%'"
    sql34 = "update china_data set provinces = '吉林' where provinces like '%吉林%'"
    sql35 = "update china_data set provinces = place where provinces is null or provinces = ''"
    sql36 = "update china_data set citys = place where citys is null or citys = ''"
    sql37 = "update china_data set citys = REPLACE(citys, '市', '') where citys like '%市%'"
    sql38 = "update china_data set citys = REPLACE(citys, '地区', '') where citys like '%地区%'"
    sql39 = "update china_data set citys = REPLACE(citys, '自治州', '') where citys like '%自治州%'"
    sql40 = "update china_data set citys = REPLACE(citys, '省', '') where citys like '%省%'"
    sql = [sql0, sql1, sql2, sql3, sql4, sql5, sql6, sql7, sql8, sql9, sql10, sql11, sql12, sql13, sql14, sql15, sql16,
           sql17, sql18, sql19, sql20, sql21, sql22, sql23, sql24, sql25, sql26, sql27, sql28, sql29, sql30, sql31, sql32, sql33,sql34]
    # city = ["北京","天津","河北","山西","内蒙古","辽宁","吉林","黑龙江","上海","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","广西","海南","重庆","四川","贵州","云南","西藏","陕西","甘肃","青海","宁夏","新疆","香港","澳门","台湾"]
    conn = pymysql.connect(host='你的服务器IP地址', port=3306, user='earthquake', password='123456',
                           database='earthquake', charset='utf8')
    # 创建游标
    cursor = conn.cursor()

    # 填充provinces和citys中的空值
    cursor.execute(sql35)
    cursor.execute(sql36)
    conn.commit()

    # 删除 citys中的“市”，“地区”，“自治州”，“省”等字符
    cursor.execute(sql37)
    cursor.execute(sql38)
    cursor.execute(sql39)
    cursor.execute(sql40)
    conn.commit()

    for i in sql:
        cursor.execute(i)
        conn.commit()
    sql_ = "select provinces,count(*) from china_data group by provinces having count(provinces)>1"
    res = utlis.query(sql_)
    # 关闭游标与连接
    cursor.close()
    conn.close()
    # print(res)
    return res

if __name__ == '__main__':
    upcity()
