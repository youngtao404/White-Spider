# -*- coding:UTF-8 -*-
import requests
from bs4 import BeautifulSoup as bs
from requests.exceptions import RequestException
import sys
import time


class downloader():
    def __init__(self):
        self.server = 'http://www.biqukan.com/'
        self.catalog = 'http://www.biqukan.com/1_1094/'
        self.names = [] #章节名
        self.urls = [] #章节链接
        self.nums = 0 #章节数


    def get_download_url(self): #获取章节信息
        response = requests.get(url = self.catalog).text
        soup = bs(response)
        div = soup.find_all('div',class_ = 'listmain')
        a_soup = bs(str(div[0]))
        a = a_soup.find_all('a')
        self.nums = len(a[16:])
        for i in a[16:]:
            self.names.append(i.string)
            self.urls.append(self.server + i.get('href'))


    def get_one_page(self,catalog): #获取一页信息
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36'
                  }
        response = requests.get(catalog,headers = headers).text
        soup = bs(response)
        texts = soup.find_all('div', class_ = 'showtxt')
        texts = texts[0].text.replace('\xa0'*8,'\n\n')
        return texts


    def writer(self,name,text):
        with open(name,'a',encoding = 'utf-8')as f:
            f.writelines(text)


if __name__ == '__main__':
    dl = downloader()
    dl.get_download_url()
    print("《一念永恒》开始下载：")
    for i in range(dl.nums):
        name=dl.names[i]+'.txt'
        dl.writer(name,dl.get_one_page(dl.urls[i]))
        print("已下载:%.3f%%" %  float(i/dl.nums),end='\r')
        sys.stdout.flush() # 刷新缓存
        time.sleep(0.1)
    print("下载完成")
