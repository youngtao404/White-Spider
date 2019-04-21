from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq
import sys
import csv
import pymongo
import sys
import time


headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E5%A4%8D%E4%BB%87%E8%80%85%E8%81%94%E7%9B%9F',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_page(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')[0].get('card_group')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            if not item: #返回的数据中有的不包含下面的内容
                continue
            
            weibo['name'] = item.get('user').get('screen_name') #用户昵称
            weibo['gender'] = item.get('user').get('gender') #用户性别
            weibo['text'] = pq(item.get('text')).text() #微博内容
            weibo['time'] = item.get('created_at') #时间
            weibo['attitudes'] = item.get('attitudes_count') #点赞数
            weibo['comments'] = item.get('comments_count') #评论数
            weibo['reposts'] = item.get('reposts_count') #转发数
            yield weibo

def save_to_mongodb(item):
    client = pymongo.MongoClient(host='localhost')
    db = client.weibo
    collection = db.weibo
    try:
        if(collection.insert_one(item)):
            return
    except:
        return None

if __name__ == '__main__':
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D61%26q%3D%E5%A4%8D%E4%BB%87%E8%80%85%E8%81%94%E7%9B%9F%26t%3D0&page_type=searchall&page='
    print('开始爬取')
    for x in range(110):
        json = get_page(url+str(x))
        results = parse_page(json)
        for result in results:
            save_to_mongodb(result)
            print("已下载:%.3f%%" %  float(x/110),end='\r')
            sys.stdout.flush() # 刷新缓存
            time.sleep(0.5)
    print('下载完成！')
