# SQL指令

## 1.查看数据库的一些设置:

```text
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