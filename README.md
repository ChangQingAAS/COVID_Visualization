# COVID-Visualization
基于Python+Flask+Echarts的疫情爬虫&amp;数据可视化项目

### 项目介绍

本项目基于[ Python爬取疫情实战 ](https://www.bilibili.com/video/BV177411j7qJ)开发。可点击 [此处]() 预览成功部署后的页面。本项目使用Flask作为web服务框架，提供后台数据接口，利用python实现公开数据的抓取并插入数据库，前端基于jquery使用ajax异步加载数据，echarts根据填充的数据进行可视化。

***
## 步骤
>* Python网络爬虫
>* 使用Python与MySQL数据库交互
>* 使用Flask构建web项目
>* 基于Echarts数据可视化展示
>* 在Linux上部署web项目及爬虫

## 项目环境
### windows:
>* Python 3.8.10
>* MySQL 8.0.22
>* Flask 1.1.2
### Linux: TODO

> 

## 文件说明
>* app.py是flask的运行程序，整体项目也是运行它
>* spider.py是爬取各种数据并存入数据库的，定时爬虫就是定时运行它
>* utils.py是数据库的相关操作的封装，spider.py中会调用它的函数
>* templates/中
>>* test.html是写项目过程中用于测试用的，和项目运行无关，可删
>>* main.html是前端页面

## 运行方式：

### **本地win10上:**

- 按照 create.sql 中的内容配置好mysql数据库
  - 在mysql数据库中新建cov数据库，并在其中新建4张表details,history,hotsearch,
- 打开config.py文件配置数据库账号
- 在utils.py和spider.py中更改get_conn函数中的数据库连接，host,user,password，db 
- 手动更新数据 `python spider.py`
  - 运行spider.py爬取数据写入到mysql中
- 开启服务 `python app.py`
- 项目启动前需手动更新一次数据，之后程序会每隔6小时自动更新数据，可在`config.py`中修改

### 服务器上



### 注意事项

- 项目中chromedriver适用于Google Chrome102版本，其他版本请前往 [此处](https://chromedriver.storage.googleapis.com/index.html) 下载并复制到项目所在目录。


## 各大平台疫情数据的网站
### 百度
https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1    
### 爬取百度的疫情数据平台的今日疫情热搜
https://voice.baidu.com/act/virussearch/virussearch?from=osari_map&tab=0&infomore=1 

### 腾讯
https://news.qq.com//zt2022/page/feiyan.htm   

### 爬取腾讯yq数据
https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5

https://view.inews.qq.com/g2/getOnsInfo?name=disease_other