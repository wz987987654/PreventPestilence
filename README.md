# HYTC -- 传染病预警系统 (python)

#### 介绍

   项目介绍等等。。。。。。


#### 安装工具说明和介绍
> 主题：如何从0开始搭建可运行的平台。

1 安装python。
    python的安装十分的简单。

    1.从官网拉取最新的版本，[Python官网](https://www.python.org/)点击即可。需要注意的是，现在下载的本本推荐是3.0以上的版本。本工程推荐使用的版本是python3.7，但是如果你想使用python3.8（最新版本也是可以的）。
       
    2.安装根据自己的操作系统，进行操作。参照：[安装教程地址，菜鸟教程](https://www.runoob.com/python/python-install.html)。

2.安装mysql

    1.mysql的安装也非常的简单，此处久不多讲。

3.安装Django框架和mysql依赖
    
    首先安装pip工具。shell下执行一下命令（linux命令）。

> sudo easy_install pip

   输入用户名和密码，即可安装。
    
  1.安装Django框架

> pip install Django (option version)

  2.安装pymysql包

> pip install pymysql

可能会遇到的问题：
 
    1. pip版本不对

* pip install --upgrade pip  更新pip版本
* 将pip命令换成pip3命令

>  pip命令是基于python2.x版本的，pip3是基于python3.x版本因此可以强制使用最新版本。       

    2. 声称数据库镜像。
*创建数据库。

> settings.py 里面的DATABASES


* 执行以下命令：
> python manage.py makemigrations

    'NAME': "kaishen" 是数据库的名字。
    创建数据库：create database kaishen;

> python manage.py migrate

    ----生成镜像命令


> 运行  python3  manage.py runserver

    3. 管理段地址

> http://127.0.0.1:8000/admin/login/?next=/admin/

#### 数据库设计



#### 



#### 


#### 如何提交代码

1. Fork 本仓库
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


