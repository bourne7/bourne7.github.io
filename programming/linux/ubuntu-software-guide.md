# Ubuntu 安装常用软件

以下操作都是基于 Ubuntu 18.04 

## 1. 系统环境设置：

Ubuntu 的软件源配置文件是 /etc/apt/sources.list, 打开这个文件并且添加一下清华大学源:
```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
#deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
#deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
#deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
#deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-security main restricted universe multiverse
# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ bionic-proposed main restricted universe multiverse
```
## 2. 安装 Oracle Java：
添加 ppa
sudo add-apt-repository ppa:webupd8team/java

安装 oracle-java-installer
sudo apt install oracle-java8-installer

## 3. 安装 MySQL 5.7

先通过 apt-show-versions -a -p mysql-server

查看是否有需要的版本, 这里我们需要的是 5.7 版本.

sudo apt install mysql-server-5.7

安装完以后，默认的root密码是不知道的。所以先重置密码。
前往

sudo vi /etc/mysql/my.cnf（ps: 如果是用的mariadb，则执行语句为 sudo vi /etc/mysql/mariadb.cnf）

加上下面这几行：
```
[mysqld]
skip-grant-tables
bind-address = 0.0.0.0
port = 3306
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO ,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```
上面一共有3个设置，分别是：
1. 登录时跳过权限检查。（这个在设置完root密码以后，记得关闭。）
2. 允许远程登录。
3. 数据库模式。

Note: In MySQL 5.7, default sql_mode additionally includes ONLY_FULL_GROUP_BY, which will break WMS queries, that's why we reset sql_mode in the conf file

在修改过设置以后，重启mysql：

sudo /etc/init.d/mysql restart

或者使用

sudo service mysql restart

然后可以直接使用 mysql; 来登录了。登录以后，前往mysql数据库，修改root限制。

update mysql.user set authentication_string = password('root'), plugin="mysql_native_password", password_expired = 'n',host = '%' where user = 'root';
flush privileges;

然后退出数据库, 再将上面添加的:
```
[mysqld]
# skip-grant-tables
bind-address = 0.0.0.0
port = 3306
sql_mode = STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO ,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
```
这堆东西里面的 skip-grant-tables 注释掉. 然后再重启一次. 就可以使用 root/root 从任意IP访问这个服务器了

## 4. 安装 redis
```
sudo apt install redis-server
设置远程访问（如果需要的话）
cd /etc/redis
sudo cp redis.conf redis.conf.backup
sudo vi redis.conf
将 bind 127.0.0.1 这行注释掉。
将下面一点的保护模式关闭，可以搜索 protect
```
重启 redis

sudo /etc/init.d/redis-server restart


## 5.新建一个用户 new_user

sudo adduser new_user

修改文件夹 new_folder 的权限。

sudo chmod -R 755 /new_folder

修改文件夹 new_folder 的拥有者。

sudo chown -R new_user:new_user /new_folder

最后在目录里面应该看到

drwxr-xr-x 4 new_user new_user 4096 Aug 2 20:13 new_folder/

 
## 6. VIM

vim 默认显示行号: 先安装好 vim, 然后建立文件:

$vi ~/.vimrc

往文件里面添加内容： set number , 保存退出。


## 7. 设置时区

sudo tzselect

这里选择好需要的城市

sudo ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

这个指令的作用是强制创建一个软连接, 将上一个步骤选中的城市所在的配置连接到本地使用的时间上面. 在18.04 里面, 也可以通过UI去设置.

## 8. crontab 克隆表达式
```
sudo vi /etc/crontab

在最后面添加一行:

* * * * * /bin/ls 代表每分钟执行一次
* * * * * root /work/my_task > /dev/null 2>&1

重启一次 crontab:

sudo /etc/init.d/cron start (或者: sudo service cron start )
sudo /etc/init.d/cron stop (或者: sudo service cron stop )
sudo /etc/init.d/cron restart (或者: sudo service cron restart )
```