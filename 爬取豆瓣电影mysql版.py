import pymysql
from bs4 import BeautifulSoup
import requests
import re
import time
import pymysql
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
def conn_db():
   conn = pymysql.connect(
       host='127.0.0.1',
       port=3306,
       user="root",
       password="123123",
       charset='utf8'
   )
   cur = conn.cursor()
   return conn, cur
def exe_query(cur, sql):
   cur.execute(sql)
   return cur

if __name__ == '__main__':
    conn, cur = conn_db()
    cur.execute('CREATE DATABASE python_movie')
    sql = """CREATE TABLE `python_movie`.`movies`(
           title CHAR(255) NOT NULL,
           TIME DATETIME,
           address CHAR(255) NOT NULL,
           actor CHAR(255) NOT NULL,
           grade FLOAT NOT NULL,
           view CHAR(255) NOT NULL
    )"""
    cur.execute(sql)  ##执行sql语句，新建一个movies的数据库
    urls = ['https://movie.douban.com/tag/%E7%88%B1%E6%83%85?start={}&type=T'.format(str(i)) for i in range(0, 40, 20)]
    start = time.clock()  #爬虫爬取开始时间
    for url in urls:
       List = []
       time.sleep(3)
       List = get_movies(url)
       for lv1 in List:
           cur.execute('insert into `python_movie`.`movies`VALUE (%s,%s,%s,%s,%s,%s)', lv1)
    end = time.clock()  #爬虫爬取结束时间
    print("time usage: ", end - start)  #计算爬虫运行总时间
    conn.commit()
    conn.close()
    cur.close()
