import requests
from requests.exceptions import RequestException
import re
import time
import csv

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
    content = re.compile('data-point="(.*?)".*?data-foreign',re.S)
    items = re.findall(content,html)
    for item in items:
        print(item)
        write_to_csv(item)

def write_to_csv(item):
    with open('datapoint.csv', 'a',newline = '',encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(items)

def main(x):   
    url='https://piao.qunar.com/ticket/list.htm?keyword=%E4%B8%8A%E6%B5%B7&region=&from=mpl_search_suggest&page='+str(x)
    html = get_one_page(url)
    parse_one_page(html)

if __name__ == '__main__':
    print("开始爬取")
    for x in range(1,108):
        main(x)
        time.sleep(0.5)
        print('爬取进度：',x/107)
