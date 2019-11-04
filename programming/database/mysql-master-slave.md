# Mysql 主从备份

## 1. 准备工作:

版本一样的Mysql数据库, 这里使用的是 5.7
版本一帮的Ubuntu, 这里使用的是 18.04

## 2. 打开 Linux 上面的数据库配置文件

sudo vi /etc/mysql/my.cnf

主服务器的配置如下:
```
[mysqld]
log-bin=mysql-bin
server-id=1 #这个id用于识别, 只要是独一无二的就行
expire_logs_days = 30 #日志过期时间, 关于这个参数的说明请看下面的解释.

从服务器的配置如下:
[mysqld]
log-bin=mysql-bin
server-id=2 #这个id用于识别, 只要是独一无二的就行
expire_logs_days = 30
replicate_wild_do_table=test.% #只同步test库下的表, 我们这里不需要对整个数据库进行备份, 只需要针对特定的数据库
relay_log=mysqld-relay-bin #记录中继日志
log-slave-updates=YES #从服务器同步后记录日志
```
修改了配置一定要重启数据库，配置才能生效

## 3. 检查状态

确保1号数据库的账号, 你能从2号数据库访问到. 然后现在1号数据库里面查看当前的log状态:
```
mysql> SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+-------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000002 | 476 | | | |
+------------------+----------+--------------+------------------+-------------------+
```

我们先在2个数据里面都建立2个名字一样的空白数据库: test 这个名字必须要和上面第2步里面配置好的 replicate_wild_do_table 是一致的. 否则就是整个数据库都会监听的.

## 4. 设置初始备份

在2号数据库里面执行下面的初始备份语句:
``` SQL
CHANGE MASTER TO MASTER_HOST='172.16.1.1', MASTER_USER='root', MASTER_PASSWORD='root', MASTER_LOG_FILE='mysql-bin.000002', MASTER_LOG_POS=476;
```
注意这里的 MASTER_LOG_FILE 和 MASTER_LOG_POS 是在第3步里面读取出来的.

到这里就已经设置好了, 下面开始进行测试, 以下是在2号数据库上面执行的:

mysql> START SLAVE; #先开启第一次的复制


## 5. 不暂停数据库的方法

如果是不想让主数据库暂停, 那么可以采用下面的方法:

先暂停从数据库: STOP SLAVE;

再执行
```
mysqldump -uroot -proot -h 172.16.1.1 --master-data --lock-all-tables --net_buffer_length 20000 --default-character-set=utf8 db_name > init.sql
```
先将数据库导出, 这个时候注意, 这个 init.sql 的顶部是有上面那句 change master 的设置语句的, 这个时候里面的 position 一定是正确的

最后恢复从数据库: START SLAVE;  

实际上这种方法是最好的, 可以在不暂停主数据库的情况下时候, 所以以后优先采用这种方法.


## 6. 可以随时查看2号数据库状态
```
mysql> SHOW SLAVE STATUS\G
*************************** 1. row ***************************
Slave_IO_State: Waiting for master to send event
Master_Host: 172.16.1.122
Master_User: root
Master_Port: 3306
Connect_Retry: 60
Master_Log_File: mysql-bin.000002
Read_Master_Log_Pos: 476
Relay_Log_File: mysqld-relay-bin.000002
Relay_Log_Pos: 320
Relay_Master_Log_File: mysql-bin.000002
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
Replicate_Do_DB: 
Replicate_Ignore_DB: 
Replicate_Do_Table: 
Replicate_Ignore_Table: 
Replicate_Wild_Do_Table: test.%
Replicate_Wild_Ignore_Table: 
Last_Errno: 0
Last_Error: 
Skip_Counter: 0
Exec_Master_Log_Pos: 476
Relay_Log_Space: 528
Until_Condition: None
Until_Log_File: 
Until_Log_Pos: 0
Master_SSL_Allowed: No
Master_SSL_CA_File: 
Master_SSL_CA_Path: 
Master_SSL_Cert: 
Master_SSL_Cipher: 
Master_SSL_Key: 
Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
Last_IO_Errno: 0
Last_IO_Error: 
Last_SQL_Errno: 0
Last_SQL_Error: 
Replicate_Ignore_Server_Ids: 
Master_Server_Id: 1
Master_UUID: 5241c574-fde3-11e8-8765-000c2924d6f3
Master_Info_File: /var/lib/mysql/master.info
SQL_Delay: 0
SQL_Remaining_Delay: NULL
Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
Master_Retry_Count: 86400
Master_Bind: 
Last_IO_Error_Timestamp: 
Last_SQL_Error_Timestamp: 
Master_SSL_Crl: 
Master_SSL_Crlpath: 
Retrieved_Gtid_Set: 
Executed_Gtid_Set: 
Auto_Position: 0
Replicate_Rewrite_DB: 
Channel_Name: 
Master_TLS_Version: 
1 row in set (0.00 sec)
```

这个时候看到里面的 Slave_IO_Running Slave_SQL_Running 都是 YES, 并且 Slave_SQL_Running_State 也是正常的, Master_UUID 也没问题, 那么就代表 2号数据库已经对1号数据库进行了监听了.

## 7. 测试

我们之前已经在2个数据库里面都建立了一个叫做 test 的数据库, 我们先将建表语句 ddl.sql 在1号数据库里面执行一次, 然后看一下1号的日志状态:
mysql> SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+-------------------+
| File | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql-bin.000002 | 46826 | | | |
+------------------+----------+--------------+------------------+-------------------+

发现已经前进了, 此时我们再打开2号数据库里面的 test库, 发现里面已经有了刚刚在1号数据库里面 执行的 ddl.sql 了, 2个test库保持了一样了.


## 8. 可能遇到的问题:

在第4步里面的 查看2号数据库状态 的时候, 如果看到有 Slave_IO_Running: No, 并且 Last_IO_Error: Fatal error: The slave I/O thread stops because master and slave have equal MySQL server UUIDs; these UUIDs must be different for replication to work. 那么是因为2个数据库的UUID是一样的, 这个时候我们需要修改一下其中一个数据库的UUID, 这里我们选择修改2号数据库的UUID.

先找到data所在的目录 SHOW VARIABLES WHERE Variable_Name LIKE "%dir"

然后删除 auto.cnf, 这个文件里面记录了 UUID , 并且重启的时候可以自动生成.

重启 mysql

完成上面3个步骤以后, 需要再一次从第3步开始进行, 因为此时的日志文件已经向前走了几个位置了.

## 9. 关于 expire_logs_days 参数的解释:
Deprecate expire_logs_days https://dev.mysql.com/worklog/task/?id=10924
```
Executive Summary
-----------------
This worklog adds a deprecation warning when users try to set expire_logs_days
either alone or along with binlog_expire_logs_seconds.

Background
----------
expire_logs_days is the number of days for automatic binary log file removal.
The default is 30, which means that the binary logs files will be purged after
30 days, if no other value is specified. Possible purge happens at start up and
when binary log is flushed.

Rationale
---------
In 8.0 a new variable binlog_expire_log_seconds was introduced. This allowed
users to set expire time which need not be integral multiple of days. This is
the better way to set the expiration time and also more flexible, it will make
the system variable expire_logs_days unneeded, so that should be deprecated in
8.0 and may be removed in later version.
```

查看是否配置好:
show binary logs;
show variables like '%log%';

## 9. 常用binlog日志操作命令

查看所有binlog
show master logs;

查看master状态
show master status;

刷新log日志, 立刻新开一个日志
flush logs;

重置(清空)所有binlog日志
reset master;

位置在 /var/lib/mysql

**binlog 查看**

可以使用 mysqlbinlog mysql-bin.000001 直接查看, 但是这种办法读取出binlog日志的全文内容较多，不容易分辨查看pos点信息，这里介绍一种更为方便的查询命令：
mysql> show binlog events [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count];

选项解析：
IN 'log_name' 指定要查询的binlog文件名(不指定就是第一个binlog文件)
FROM pos 指定从哪个pos起始点开始查起(不指定就是从整个文件首个pos点开始算)
LIMIT [offset,] 偏移量(不指定就是0)
row_count 查询总条数(不指定就是所有行)
截取部分查询结果：
```
*************************** 20. row ***************************
Log_name: mysql-bin.000021 ----------------------------------------------> 查询的binlog日志文件名
Pos: 11197 ----------------------------------------------------------> pos起始点:
Event_type: Query ----------------------------------------------------------> 事件类型：Query
Server_id: 1 --------------------------------------------------------------> 标识是由哪台服务器执行的
End_log_pos: 11308 ----------------------------------------------------------> pos结束点:11308(即：下行的pos起始点)
Info: use `zyyshop`; INSERT INTO `team2` VALUES (0,345,'asdf8er5') ---> 执行的sql语句
*************************** 21. row ***************************
Log_name: mysql-bin.000021
Pos: 11308 ----------------------------------------------------------> pos起始点:11308(即：上行的pos结束点)
Event_type: Query
Server_id: 1
End_log_pos: 11417
Info: use `zyyshop`; /*!40000 ALTER TABLE `team2` ENABLE KEYS */
*************************** 22. row ***************************
Log_name: mysql-bin.000021
Pos: 11417
Event_type: Query
Server_id: 1
End_log_pos: 11510
Info: use `zyyshop`; DROP TABLE IF EXISTS `type`
```

这条语句可以将指定的binlog日志文件，分成有效事件行的方式返回，并可使用limit指定pos点的起始偏移，查询条数；

A.查询第一个(最早)的binlog日志：
mysql> show binlog events\G; 

B.指定查询 mysql-bin.000021 这个文件：
mysql> show binlog events in 'mysql-bin.000021'\G;

C.指定查询 mysql-bin.000021 这个文件，从pos点:8224开始查起：
mysql> show binlog events in 'mysql-bin.000021' from 8224\G;

D.指定查询 mysql-bin.000021 这个文件，从pos点:8224开始查起，查询10条
mysql> show binlog events in 'mysql-bin.000021' from 8224 limit 10\G;

E.指定查询 mysql-bin.000021 这个文件，从pos点:8224开始查起，偏移2行，查询10条
mysql> show binlog events in 'mysql-bin.000021' from 8224 limit 2,10\G;

## 10. 引用: 
https://www.jianshu.com/p/2347b1a9eacd
https://www.opsdash.com/blog/mysql-replication-howto.html
https://www.cnblogs.com/martinzhang/p/3454358.html
https://www.cnblogs.com/phpstudy2015-6/p/6485819.html