import requests
import json
import re
import time
from requests.exceptions import RequestException
import pymysql

def get_one_page(url):#爬取一页的内容
    try:
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            }
        response = requests.get(url,headers=headers)
        if(response.status_code == 200):
            return(response.text)
        return None
    except RequestException:
        return None

def parse_one_page(html):#筛选一页的内容    
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a''.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>''.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{ #yield迭代器
            'num':item[0],
            'name':item[2].strip(),
            'actor':item[3].strip()[3:]if len(item[3])>3 else '',
            'time':item[4].strip()[5:]if len(item[4])>5 else '',
            'score':item[5].strip()+item[6].strip()
            }

class my_sql(): #定义一个mysql类，实现连接和插入数据操作
    def __init__(self,num,name,actor,time,score):
        self.num = num
        self.name = name
        self.actor = actor
        self.time = time
        self.score = score
        self.connect = pymysql.connect(
            host='localhost',
            user='yourusername', # 你的用户名
            password='yourpassword', # 你的密码
            port=3306,
            db = 'spider_maoyan'
            )
        self.cursor = self.connect.cursor()


    def save_mysql(self):
        sql = 'insert into example(num,name,actor,time,score) values(%s,%s,%s,%s,%s)'
        try:
            self.cursor.execute(sql,(self.num,self.name,self.actor,self.time,self.score))
            self.connect.commit()
            print('insert OK')
        except:
            print('insert ERROR')
            
def mysql(item): #实例化对象，传入数据
    num = int(item['num'])
    name = item['name']
    actor = item['actor']
    time = item['time']
    score = item['score']
    down = my_sql(num,name,actor,time,score)
    down.save_mysql()
    
def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(i*10)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        mysql(item)


if __name__=='__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
