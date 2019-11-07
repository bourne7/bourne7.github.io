# SQL笔记

2019-02-02

## 浅谈sql中的in与not in,exists与not exists的区别以及性能分析

> 引用自：[https://blog.csdn.net/baidu\_37107022/article/details/77278381](https://blog.csdn.net/baidu_37107022/article/details/77278381)

**in和exists**

in是把外表和内表作hash连接，而exists是对外表作loop循环，每次loop循环再对内表进行查询，一直以来认为exists比in效率高的说法是不准确的。如果查询的两个表大小相当，那么用in和exists差别不大；如果两个表中一个较小一个较大，则子查询表大的用exists，子查询表小的用in。

**not in 和not exists**

not in 逻辑上不完全等同于not exists，如果你误用了not in，小心你的程序存在致命的BUG。 如果查询语句使用了not in，那么对内外表都进行全表扫描，没有用到索引；而not exists的子查询依然能用到表上的索引。所以无论哪个表大，用not exists都比not in 要快。

**in 与 = 的区别**

```sql
select name from student where name in('zhang','wang','zhao');
select name from student where name='zhang' or name='wang' or name='zhao'
```

结果是相同的。

另外IN时不对NULL进行处理，NOT EXISTS 与 NOT IN 不能完全互相替换，看具体的需求。如果选择的列可以为空，则不能被替换。

我们要根据实际的情况做相应的优化，不能绝对的说谁的效率高谁的效率低，所有的事都是相对的。

## varchar存储规则：

> https://www.cnblogs.com/lbf1994/articles/5677453.html

4.0版本以下，varchar(20)，指的是20字节，如果存放UTF8汉字时，只能存6个（每个汉字3字节） 

5.0版本以上，varchar(20)，指的是20字符，无论存放的是数字、字母还是UTF8汉字（每个汉字3字节），都可以存放20个，最大大小是65532字节 