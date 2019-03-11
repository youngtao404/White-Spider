import requests
import re
import json
from requests.exceptions import RequestException
import time

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

#解析源码
def parse_one_page(html):
    pattern = re.compile('<tr.*?><td>(.*?)</td><td><div.*?>(.*?)</div></td><td>(.*?)</td><td>(.*?)</td><td.*?indicator5.*?>(.*?)</td>.*?</tr>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield{
            '排名':item[0],
            '学校名称':item[1],
            '省份':item[2],
            '总分':item[3]
            }

#写入数据在文档
def write_to_file(item):
    with open('爬取中国大学排名.txt','a',encoding='utf-8')as f:
        f.write(json.dumps(item,ensure_ascii=False)+'\n')
    
#主函数
def main():
    url = 'http://www.zuihaodaxue.com/zuihaodaxuepaiming2019.html'
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
        print(item)

main()
