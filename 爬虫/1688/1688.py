from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup
import time

browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)

'''
参考https://blog.csdn.net/Fan_shui/article/details/81516645#commentsedit
'''
def crawle():
    url='https://www.1688.com/'
    browser.get(url=url)
    # 叉掉首页弹出大框
    button1=browser.find_element_by_class_name('identity-close')
    button1.click()
    # 定位搜索框
    info=browser.find_element_by_id('alisearch-keywords')
    info.send_keys('手机')
    # 定位搜索按钮
    sea_button=browser.find_element_by_id('alisearch-submit')
    sea_button.click()
    # 叉掉弹出第二个大框
    button2=browser.find_element_by_class_name('s-overlay-close-l')
    button2.click()
    # 定位成交量
    button_deal=browser.find_elements_by_css_selector('.sm-widget-sort.fd-clr.s-widget-sortfilt li')[1]
    button_deal.click()         # 中间无空格表示同时拥有class1和class2

    # 滚动至底部加载全部数据
    try:
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(3) # 延时等待，避免还未加载又往下滑
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#offer60')))
    except :
        print('*'*30,'超时加载','*'*30,'\n\n\n')

    get_products()

  
def get_products():
    html=browser.page_source
    doc=pq(html)
    items=doc('.sm-offer .fd-clr .sm-offer-item').items()
    index=0
    for item in items:
        index+=1
        print('*'*50)
        title=item.find('.s-widget-offershopwindowtitle').text().split('\n')
        title=' '.join(title)
        price_a=item.find('.s-widget-offershopwindowprice').text().split('\n')
        price=''.join(price_a[:2])
        deal=''.join(price_a[2:])
        #产品网址
        text=item.find('.s-widget-offershopwindowtitle')
        soup=BeautifulSoup(str(text),'lxml')
        a=soup.select('.s-widget-offershopwindowtitle a')[0]
        url=a['href']
        print(title)
        print(price)
        print(deal)
        print(url)


    print(' (●ˇ∀ˇ●) '*5)
    print('一共%d条数据'%index)


crawle()
