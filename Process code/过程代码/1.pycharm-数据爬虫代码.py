import requests
import re
from bs4 import BeautifulSoup
import threading
import time
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.63'
}
# url = 'http://ditu.92cha.com/dizhen.php?dizhen_ly=china'
# resp = requests.get(url, headers=headers)
# print(resp)
# html = resp.text
# soup = BeautifulSoup(html, 'lxml')
def Crawl_data(url, csv_file):
    resp = requests.get(url, headers=headers)
    # 获取总页数
    r = re.compile('查询到 (\d+) 条记录，分 (\d+) 页显示')
    pcount = int(r.findall(resp.text)[0][1])
    print(pcount)
    # 爬取内容
    with open(csv_file, 'a', encoding='utf-8') as fp:
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
                place = tds[2].text
                # print(place)
                # 爬取经度
                longitude = tds[3].text
                # print(longitude)
                # 爬起维度
                latitude = tds[4].text
                # print(latitude)
                # 爬取深度
                deep = tds[5].text
                # print(deep)
                fp.write('%s, %s, %s, %s, %s, %s\n' % (times, level, place, longitude, latitude, deep))
            print('Done')


if __name__ == '__main__':
    # Crawl_data('http://ditu.92cha.com/dizhen.php?dizhen_ly=china', 'earthQuake_china.csv')
    Crawl_data('http://ditu.92cha.com/dizhen.php?dizhen_ly=usa&dizhen_zjs=1&dizhen_zje=10&dizhen_riqis=&dizhen_riqie=&ckwz=', 'earthQuake_usa.csv')





