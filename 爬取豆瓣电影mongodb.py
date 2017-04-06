from bs4 import BeautifulSoup
import requests
import re
import time
import pymongo
def get_movies(url):
    web_data = requests.get(url)
    # 构建一个Request对象，该对象将被发送到服务器请求或查询网页资源，Requests得到一个从服务器返回的响应并产生Response对象
    soup = BeautifulSoup(web_data.text, 'lxml')  #利用lxml解析器解析网页内容并存以text文件格式
    titles = soup.select('div.pl2 > a[class=""]')  #爬取电影的名称
    points = soup.select('div.pl2 > p[class="pl"]')  #爬取电影的产地，上映时间和演员
    views = soup.select('div.star > span.pl')
    grades = soup.select('div.star > span.rating_nums')  # 爬取电影的评分
    title_list = []
    movies_list = []  # 创建一个列表用于下面存放电影的各项信息
    for title in titles:
        title = str(title)
        res = r'<a .*?>(.*?)/ <'
        mm = re.findall(res, title, re.S | re.M)
        for value in mm:
            _title = value.strip()
            title_list.append(_title)
    for title, point, grade, view in zip(title_list, points, grades, views):
        #从HTML标签中爬取相关电影信息
        title = title
        point = point.get_text()
        times = point.split("(")[0]
        address = point.split(")")[0].split("(")[-1]
        actor = point.split(") /")[-1]
        view = view.get_text()
        grade = grade.get_text()
        movies_list.append([title, times, address, actor, grade, view]) #把爬取的电影信息存放在创建好的空列表
    return movies_list
if __name__ == '__main__':
    url = 'https://movie.douban.com/tag/%E7%88%B1%E6%83%85?start=20&type=T'
    movies_l = get_movies(url)
    client = pymongo.MongoClient('localhost', 27017)
    douban = client['douban']
    movies = douban['movies']
    index = 1
    for item in movies_l:
        data = {
            'index': index,
            'title': item[0],
            'times': item[1],
            'address': item[2],
            'actor': item[3],
            'grade': item[4],
            'view': item[5]
        }
        movies.insert(data)
        index += 1
    for item in movies.find({'grade': {'$gte': str(8)}}):
        print(item)