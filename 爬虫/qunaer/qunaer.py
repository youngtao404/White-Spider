import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
import re
import csv
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
            }
        response = requests.get(url,headers = headers)
        response.encoding = 'utf-8'# 将编码转为utf-8，否则中文会显示乱码
        if (response.status_code == 200):
            return response.text
        return None
    except RequestException:
        print('Error')
        return None

def parse_one_page(html):
    
    soup = bs(html,'lxml')
    for info1 in soup.find_all(class_='sight_item_about'):
        
        name = info1.h3.string
        names.append(name)
        
        if(info1.select('.sight_item_info .clrfix .level')): #部分景区不存在景区等级
            level = info1.select('.sight_item_info .clrfix .level')[0].string
        else:
            level = None
        levels.append(level)
            
        area = info1.select('.sight_item_info .clrfix .area')[0].a.string
        areas.append(area)
        
        hot =info1.select('.sight_item_info .clrfix .sight_item_hot .product_star_level')[0].string.split()[1]
        if(hot=='0.0'):
            hot='0.70'
        hots.append(hot)
            
    for info2 in soup.find_all(class_='sight_item_pop'):
        
        if(info2.find(class_='sight_item_price')):
            price = info2.find(class_='sight_item_price').em.string
        else:
            price = '无或者免费'
        prices.append(price)

        if(info2.find(class_='sight_item_sold-num').find(class_='hot_num')):
            sold = info2.find(class_='sight_item_sold-num').span.string
        else:
            sold = None
        solds.append(sold)

def write_to_csv(items):
    with open('qunaer.csv', 'a',newline = '',encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(items)
    
def main(x):   
    url='https://piao.qunar.com/ticket/list.htm?keyword=%E4%B8%8A%E6%B5%B7&region=&from=mpl_search_suggest&page='+str(x)
    html = get_one_page(url)
    parse_one_page(html)

if __name__ == '__main__':

    names = [] # 地点名
    levels = [] # 景区等级
    areas = [] # 景区地点
    hots = [] # 景区热度
    prices = [] # 景区价格
    solds = [] # 景区销量
    
    print("开始爬取")
    for x in range(1,108):
        main(x)
        time.sleep(0.5)
        print('爬取进度：',x/107)
    print("爬取结束，开始存入")
    
    write_to_csv(['地点名','景区等级','景区地点','景区热度','景区价格','景区销量'])
    for i in range(len(names)):
        flag = [names[i],levels[i],areas[i],hots[i],prices[i],solds[i]]
        write_to_csv(flag)
        

