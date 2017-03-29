from bs4 import BeautifulSoup
import requests
import re
import time
import pymysql
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 '
                  'Safari/537.36 ',
    'Cookie': 'bid=f6UjerZSDCw; gr_user_id=1627bd69-7b43-423f-b3b3-3759e4d400a1; ll="108258"; '
              'viewed="26899097_11523293_2152385"; ps=y; _ga=GA1.2.1021420151.1487723833; '
              'dbcl2="5802449:xe72NkODRBI"; ck=cAW9; '
              '_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1490371328%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; '
              '__utmt_douban=1; _pk_id.100001.4cf6=f7269c5891a650b0.1487752747.5.1490371350.1489851670.; '
              '_pk_ses.100001.4cf6=*; __utma=30149280.1021420151.1487723833.1489936313.1490371056.16; '
              '__utmb=30149280.12.10.1490371056; __utmc=30149280; '
              '__utmz=30149280.1490371056.16.16.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=('
              'not%20provided); __utmv=30149280.580; __utma=223695111.1401633265.1487752746.1489851641.1490371328.6; '
              '__utmb=223695111.0.10.1490371328; __utmc=223695111; '
              '__utmz=223695111.1490371328.6.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; '
              'push_noty_num=0; push_doumail_num=0; '
              '_vwo_uuid_v2=DEFC84ED10E45C09B46AB9C06810842A|db34cafdf27f614c69e0b02cc0ae02ab; ap=1 '
}
'''
def get_movies(url):
    L = []
    web_data = requests.get(url)
    # 构建一个Request对象，该对象将被发送到服务器请求或查询网页资源，Requests得到一个从服务器返回的响应并产生Response对象
    soup = BeautifulSoup(web_data.text, 'lxml')  #利用lxml解析器解析网页内容并存以text文件格式
    titles = soup.select('div.pl2 > a[class=""]')  #爬取电影的名称
    points = soup.select('div.pl2 > p[class="pl"]')  #爬取电影的产地，上映时间和演员
    grades = soup.select('div.star > span.rating_nums')  #爬取电影的评分
    views = soup.select('div.star > span.pl')
    l = [] #创建一个列表用于下面存放电影的各项信息
    for title, point, grade, view in zip(titles, points, grades, views):
        #从HTML标签中爬取相关电影信息
        title = title.get_text().split("/")[0].strip()
        point = point.get_text()
        _time = point.split("(")[0]
        address = point.split(")")[0].split("(")[-1]
        actor = point.split(") /")[-1]
        grade = grade.get_text()
        view = view.get_text()
        l.append([title, _time, address, actor, grade, view]) #把爬取的电影信息存放在创建好的空列表
    sql = "INSERT INTO movies values(%s,%s,%s,%s,%s,%s)"  #sql插入
    cur.executemany(sql, l)  ##执行sql语句，并用executemary()函数批量插入数据库中
    conn.commit()

conn = pymysql.connect(user="root", password="2190", database="python_movie", charset='utf8')
cur = conn.cursor()

# 将Python连接到MySQL中的python数据库中
cur.execute('DROP TABLE IF EXISTS movies')  #如果数据库中有的数据库则删除
sql = """CREATE TABLE movies(
        title CHAR(255) NOT NULL,
        _time CHAR(255),
        address CHAR(255),
        actor CHAR(255),
        grade CHAR(255),
        view CHAR(255),
 )"""
cur.execute(sql)  ##执行sql语句，新建一个movies的数据库

#爬取多个标签页的电影信息
urls = ['https://movie.douban.com/tag/%E7%88%B1%E6%83%85?start={}&type=T'.format(str(i)) for i in range(0, 40, 20)]
start = time.clock()  #爬虫爬取开始时间
for url in urls:
    time.sleep(2)  #设置爬虫爬取频率，避免被墙
    get_movies(url)
end = time.clock()  #爬虫爬取结束时间
print("time usage: ", end - start)  #计算爬虫运行总时间
count = cur.execute('select * from movies')  #返回爬虫爬取的总数目条数
print('has %s record' % count)
# 释放数据连接
if cur:
    cur.close()
if conn:
    conn.close()


