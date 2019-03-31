import requests
import json
import re
import time
from requests.exceptions import RequestException
import pymongo

'''
相对于mysql简单了很多
'''
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
        
def save_to_mongodb(item):
    client = pymongo.MongoClient(host='localhost')
    db = client.maoyan
    collection = db.movie
    try:
        if(collection.insert_one(item)):
            print('yes')
    except:
        print('no')
    

def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(i*10)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        save_to_mongodb(item)


if __name__=='__main__':
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)
