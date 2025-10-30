# SQL 笔记

## Windows 安装 MySQL

如果是用 Mac 或者 Linux，强烈推荐用 Docker。如果是 Windows，那么可以考虑免安装的方式。

这里需要注意的是，安装分为2个部分：
1. 将免安装 zip 包解压到适当的程序目录
2. 执行初始化
3. 安装 Service 方便开机自动启动

这种方式也符合“干净，绿色，无污染”的程序使用方式。尽量不要用 exe/msi 的形式安装。

```sh
"D:\Program Files\MySQL Server 9\bin\mysqld.exe" --install MySQL9 --defaults-file="D:\Program Files\MySQL Server 9\my.ini"

"D:\Program Files\MySQL Server 9\bin\mysqld" --defaults-file="D:\Program Files\MySQL Server 9\my.ini" --initialize --console

C:\Users\aac>"D:\Program Files\MySQL Server 9\bin\mysqld" --defaults-file="D:\Program Files\MySQL Server 9\my.ini" --initialize --console
2025-08-13T05:52:27.658938Z 0 [System] [MY-015017] [Server] MySQL Server Initialization - start.
2025-08-13T05:52:27.663765Z 0 [System] [MY-013169] [Server] D:\Program Files\MySQL Server 9\bin\mysqld (mysqld 9.4.0) initializing of server in progress as process 38684
2025-08-13T05:52:27.682420Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
2025-08-13T05:52:27.879502Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
2025-08-13T05:52:28.800999Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: y<F+-t&(O2!Z
2025-08-13T05:52:30.319063Z 0 [System] [MY-015018] [Server] MySQL Server Initialization - end.


"D:\Program Files\MySQL Server 9\bin\mysqld" --console
```

## 1.查看数据库的一些设置:

```sh
SHOW VARIABLES WHERE Variable_Name LIKE "%dir"
```

## 2.mysqldump 参数问题
```
mysqldump -uroot -proot -h 172.16.1.1 --master-data --lock-all-tables --net_buffer_length 20000 --default-character-set=utf8 db_name > init.sql
```

net_buffer_length 这个参数可以让一行数据不至于太大。否则读入的时候会有麻烦。

master-data 可以加上主数据库的bin位置。


## 3. 修改密码
```sql
set password for root@localhost = password('123');
或者
update mysql.user set password=password('123') where user='root' and host='localhost';  
```

## 查看数据库大小

1.查看所有数据库容量大小

```sql
SELECT
	table_schema AS '数据库',
	sum( table_rows ) AS '记录数',
	sum(
	TRUNCATE ( data_length / 1024 / 1024, 2 )) AS '数据容量(MB)',
	sum(
	TRUNCATE ( index_length / 1024 / 1024, 2 )) AS '索引容量(MB)' 
FROM
	information_schema.TABLES 
GROUP BY
	table_schema 
ORDER BY
	sum( data_length ) DESC,
	sum( index_length ) DESC;
```
　　

2.查看所有数据库各表容量大小
```sql
SELECT
	table_schema AS '数据库',
	table_name AS '表名',
	table_rows AS '记录数',
	TRUNCATE ( data_length / 1024 / 1024, 2 ) AS '数据容量(MB)',
	TRUNCATE ( index_length / 1024 / 1024, 2 ) AS '索引容量(MB)' 
FROM
	information_schema.TABLES 
ORDER BY
	data_length DESC,
	index_length DESC;
```　

3.查看指定数据库容量大小
例：查看mysql库容量大小

```sql
SELECT
	table_schema AS '数据库',
	sum( table_rows ) AS '记录数',
	sum(
	TRUNCATE ( data_length / 1024 / 1024, 2 )) AS '数据容量(MB)',
	sum(
	TRUNCATE ( index_length / 1024 / 1024, 2 )) AS '索引容量(MB)' 
FROM
	information_schema.TABLES 
WHERE
	table_schema = 'mysql';
```　　

4.查看指定数据库各表容量大小
例：查看mysql库各表容量大小

```sql
SELECT
	table_schema AS '数据库',
	table_name AS '表名',
	table_rows AS '记录数',
	TRUNCATE ( data_length / 1024 / 1024, 2 ) AS '数据容量(MB)',
	TRUNCATE ( index_length / 1024 / 1024, 2 ) AS '索引容量(MB)' 
FROM
	information_schema.TABLES 
WHERE
	table_schema = 'mysql' 
ORDER BY
	data_length DESC,
	index_length DESC;
```


# Mysql Workbench

在使用数据库建模的时候，我只用过 Mysql Workbench 和 SAP 的 PowerDesigner。这2个工具都不好用，不过由于考虑到跨平台和授权的因素，我还是优先选择了 MW（Mysql Workbench）。

以下是使用的一些笔记：

## 关系连接线的标识

分别是：

1. 双平行线：表示1个且一定要有一个
2. 单线条+小圆圈：表示一个或0个。
3. 线条+三分叉：表示多个，至少有1个。
4. 小圆圈+三分叉：表示多个，可以是0个。

其中一对多或者一对一是由 Cardinality 这个选项决定的（在关系线上面双击就能修改。）

是否允许为0个是由 Mandatory 这个选项决定的。

线条是实线还是虚线是由 Identifying Relationship 来决定的。

但是实际在导出成为建表语句的时候，可以选择不将外键约束导出。
