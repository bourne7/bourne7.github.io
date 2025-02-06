# SQL指令

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