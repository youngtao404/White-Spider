import pandas as pd # 数据框操作
import numpy as np
import matplotlib.pyplot as plt # 绘图
import jieba # 分词
from wordcloud import WordCloud # 词云
import matplotlib as mpl # 配置字体
from pyecharts import Geo # 地理图

# 字体
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 配置绘图风格
plt.rcParams['axes.labelsize'] = 16
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14
plt.rcParams['legend.fontsize'] = 12
plt.rcParams['figure.figsize'] = [15,9]

# 导入数据
data = pd.read_excel(r'shixiseng_work_clean2.xlsx',encoding = 'gbk')


# 全国实习职位分布热力图
mylist1=[]
for i in range(len(data)):
    mylist1.append((data['工作地点'][i],data['出现次数'][i]))

geo = Geo("全国实习职位分布热力图", "data from youngtao", title_color="#fff",title_pos="center", width=1000,height=600, background_color='#404a59')
attr, value = geo.cast(mylist1)
geo.add("", attr, value, visual_range=[20, 500], maptype='china',visual_text_color="#fff",symbol_size=10, is_visualmap=True)
geo.render("全国实习职位分布热力图.html")#生成html文件

# 全国实习薪资分布热力图
mylist2=[]
for i in range(len(data)):
    mylist2.append((data['工作地点'][i],data['平均薪资'][i]))

geo = Geo("全国实习薪资分布热力图", "data from youngtao", title_color="#fff",title_pos="center", width=1000,height=600, background_color='#404a59')
attr, value = geo.cast(mylist2)
geo.add("", attr, value, visual_range=[100, 150], maptype='china',visual_text_color="#fff",symbol_size=10, is_visualmap=True)
geo.render("全国实习薪资分布热力图.html")#生成html文件
