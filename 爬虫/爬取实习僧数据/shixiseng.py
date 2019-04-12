import requests
import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as bs
import base64
from fontTools.ttLib import TTFont
import csv
import json
import time
import sys

#爬取一页的HTML源码
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
        print(None)
        return None

#font文件解密后转存到本地
def parse_fontface(html):
    pattern = re.compile('base64,(.*?)\"',re.S)
    items = re.findall(pattern,html)
    b=base64.b64decode(items[0])
    with open('shixi.ttf','wb')as f:
        f.write(b)

#建立映射
def font_dict():
    font = TTFont('shixi.ttf')
    font.saveXML('shixi.xml')
    ccmap = font['cmap'].getBestCmap()
    #print("ccmap:\n",ccmap)
    newmap = {}
    for key,value in ccmap.items():
        #转换成十六进制
        key = hex(key)
        value = value.replace('uni','')
        a = 'u'+'0' * (4-len(value))+value
        newmap[key] = a
    #print("newmap:\n",newmap)
    #删除第一个没用的元素
    newmap.pop('0x78')
    #加上前缀u变成unicode....
    for i,j in newmap.items():
        newmap[i] = eval("u" + "\'\\" + j + "\'")
    #print("newmap:\n",newmap)
    new_dict = {}
    #根据网页上显示的字符样式改变键值对的显示
    for key, value in newmap.items():
        key_ = key.replace('0x', '&#x')
        new_dict[key_] = value
    return new_dict

#替换清洗html
def decode(html,new_dict):
    for key,value in new_dict.items():
        if(key in html):
            html = html.replace(key,value)
        else:
            pass
    return html

#解析页面1
def parse_one_page1(html):
    soup = bs(html,'lxml')
    for li in soup.find_all(class_='position-item clearfix font'):
        info1 = li.find(class_='info1 clearfix')
        job = info1.find(class_='position-name fl').string
        money = info1.find(class_='position-salary fl').string
        info2 = li.find(class_='info2 clearfix')
        location = info2.select('span')[0].string
        atleastday = info2.select('span')[1].string
        workday = info2.select('span')[2].string
        yield[
            job, # 实习职位
            money, # 实习薪资
            location, # 工作地点
            atleastday, # 实习天数
            workday # 实习月份
            ]


#解析页面2
def parse_one_page2(html):
    pattern = re.compile('<span class="type">(.*?)</span>.*?<span>(.*?)</span>',re.S)
    temp = re.findall(pattern,html)
    for i in temp:
        yield[
           i[0], # 实习种类
           i[1] # 实习薪水
            ]
        
#列表写进csv文档
def write_to_csv(name,content):
    with open(name, 'a',newline = '') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(content)

#主函数
def main(x):
    url = 'https://www.shixiseng.com/it/'+str(x)
    html = get_one_page(url) # 原始版本html
    parse_fontface(html) # font文件解密转存本地
    new_dict = font_dict() # 建立映射关系
    html = decode(html,new_dict) # #替换清洗html

    for i in parse_one_page1(html):
        write_to_csv('实习僧IT实习岗位汇总.csv',i)
    for i in parse_one_page2(html):
        write_to_csv('实习僧IT实习种类汇总.csv',i)
    
if __name__ == '__main__':
    write_to_csv('实习僧IT实习岗位汇总.csv',['实习职位','实习薪资','工作地点','实习天数','实习月份'])
    write_to_csv('实习僧IT实习种类汇总.csv',['实习种类','实习薪水'])
    print('开始爬取')
    for i in range(500):
        main(x=i)
        print("已下载:%.3f%%" %  float(i/500),end='\r')
        sys.stdout.flush() # 刷新缓存
        time.sleep(0.5)
    print('下载完成！')
