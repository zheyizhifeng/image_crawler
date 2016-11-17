* 安装必要软件包：

* 安装python的安装包管理程序 pip及其他必要软件包

sudo apt-get install python-pip
sudo pip install Django
sudo pip install tagging
sudo apt-get install apache2 libapache2-mod-wsgi python-twisted python-cairo python-django-tagging

* 用pip安装以下三个graphite组件
* whisper (简单的存放和操作数据的库), carbon (监控数据的 Twisted 守护进程) 和 graphite-web (Django webapp)

pip install carbon
pip install whisper
pip install graphite-web

* 初始化配置，直接用 example 文件里的默认配置就可以：

$ cd /opt/graphite/conf/

$ sudo cp carbon.conf.example carbon.conf
$ sudo cp storage-schemas.conf.example storage-schemas.conf
$ sudo cp graphite.wsgi.example graphite.wsgi

* 修改 apache 配置，增加一个 vhost 或者偷懒下载一个配置文件覆盖 000-default.conf，覆盖后需要重新 reload 配置：

$ wget http://launchpad.net/graphite/0.9/0.9.9/+download/graphite-web-0.9.9.tar.gz
$ tar -zxvf graphite-web-0.9.9.tar.gz
$ cd graphite-web-0.9.9
$ sudo cp examples/example-graphite-vhost.conf /etc/apache2/sites-available/000-default.conf

###### 这里注意与Ubuntu12.04的配置不同，Ubuntu12.04修改如下
$ sudo cp examples/example-graphite-vhost.conf /etc/apache2/sites-available/default

* sockets 最好不要放在 /etc/httpd/ 下面（不同 Linux 发行版本对不同目录的权限问题很混淆人），ubuntu 版本可以放在 /var/run/apache2 下，所以修改 000-default 文件里的 WSGISocketPrefix 部分：

$ sudo vi /etc/apache2/sites-available/000-default
...
WSGISocketPrefix /var/run/apache2/wsgi
...

$ sudo /etc/init.d/apache2 reload



## pip install parse_lookup ==>
如果出现提示No distributions at all found for parse-lookup,则是因为django最新的改动，django.db.models.query包中已不含parse_lookup方法，

I believe the error is due to the django-tagging package missing. Even so, Django 1.4 was just released two weeks ago and Graphite hasn’t yet made the changes yet to be compatible with it (see https://bugs.launchpad.net/graphite/+bug/963684) so I’d suggest starting with Django 1.3 as you’ll run into other issues otherwise.

解决方法：不要使用项目组提供的打包文件，用源码安装：
先卸载之前安装的djongo-tagging：pip uninstall tagging
从 https://code.google.com/p/django-tagging/downloads/list 下载最新的django-tagging安装，安装命令：进入解压目录， python setup.py install

* 初始化 graphite 需要的数据库，修改 storage 的权限，用拷贝的方式创建 local_settings.py 文件：

$ cd /opt/graphite/webapp/graphite/

$ sudo python manage.py syncdb
$ sudo chown -R www-data:www-data /opt/graphite/storage/
$ sudo cp local_settings.py.example local_settings.py

### $ sudo /etc/init.d/apache2 restart

* 启动 carbon：

$ cd /opt/graphite/

$ sudo ./bin/carbon-cache.py start

* 浏览器访问 IP 地址（127.0.0.1）后就可以看到 graphite web 界面：


* 要启用一个爬虫的持久化，运行以下命令:

scrapy crawl image -s JOBDIR = crawls/image-1
然后，你就能在任何时候安全地停止爬虫(按Ctrl-C或者发送一个信号)。恢复这个爬虫也是同样的命令:
scrapy crawl image -s JOBDIR = crawls/image-1

##################################################
* 避免爬虫被禁的策略：
  * 禁用cookie[default enable]
  * 实现了一个download middleware，不停的变user-aget
  * 实现了一个可以访问google cache中的数据的download middleware(默认禁用)

* 调试策略的实现：
  * 将系统log信息写到文件中
  * 对重要的log信息(eg:drop item,success)采用彩色样式终端打印

* 访问速度动态控制:
  * 跟据网络延迟，分析出scrapy服务器和网站的响应速度，动态改变网站下载延迟
  * 配置最大并行requests个数，每个域名最大并行请求个数和并行处理items个数

* 爬虫状态查看：
  * 将爬虫stats信息(请求个数，文件下载个数，图片下载个数等)保存到redis中
  * 实现了一个针对分布式的stats collector，并将其结果用graphite以图表形式动态实时显示

#### 注意

每次运行完之后都要执行commands/clear_stats.py文件来清除redis中的stats信息
     python clear_stats.py