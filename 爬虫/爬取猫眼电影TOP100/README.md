## 爬取猫眼电影TOP并存入数据库
requests和正则解析简单爬取猫眼电影TOP100，pymsql连接并存入MySQL，pymongo连接并存入MongoDB
## 运行环境
<ul>
<li>Python3.6</li>
<li>MySQL8.0</li>
<li>MongoDB4.0</li>
</ul>

## 简介
<ul>
<li>此代码参照崔庆才《Python3网络爬虫实战》的代码修改而成，原例子是将数据存进txt文档中，本例子改造存入数据库中</li>
<li>MySQL例子代码运行前需建立一个spider_maoyan的库，在库里生成一个example表，表的列名为num,name,actor,time,score，其中num为INT主键，其余长度VARCHAR自定义</li>
<li>MongoDB可直接运行</li>
</ul>
