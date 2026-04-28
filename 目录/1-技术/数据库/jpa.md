# JPA

## @Modifying 的使用

主要是讨论 clearAutomatically 和 flushAutomatically 的使用.

现在在 Springboot 里面有下面的代码
```java
// Repository
@Repository
public interface MysqlFruitRepository extends JpaRepository<MysqlFruit, Long>,
        JpaSpecificationExecutor<MysqlFruit> {
    void deleteByName(String name);

    List<MysqlFruit> findAllByName(String name);

    @Modifying(clearAutomatically = false, flushAutomatically = false)
    @Query("update MysqlFruit set size = :size, updateTime = :updateTime where name = :name")
    int updateFruit(Integer size, Date updateTime, String name);

}

// Service
@Transactional(transactionManager = "mysqlTransactionManager", timeout = 36000, rollbackFor = Exception.class)
@Override
public void updateFruit(String name) {

	if (!TransactionSynchronizationManager.isActualTransactionActive()) {
		throw new RuntimeException("No transaction!");
	}

	MysqlFruit fruit = mysqlFruitRepository.findAllByName(name);

	log.info("before update: fruit {}", JsonUtils.obj2String(fruit));

	mysqlFruitRepository.updateFruit(atomInteger.getAndIncrement(), new Date(), name);

	log.info("after update: fruit {}", JsonUtils.obj2String(fruit));

	MysqlFruit fruit2 = mysqlFruitRepository.findAllByName(name);

	log.info("after update and select again: fruit {}", JsonUtils.obj2String(fruit));

	log.info("after update and select again: fruit2 {}", JsonUtils.obj2String(fruit2));

//        fruit.setName("a1");

	fruit2.setName("a2");

}

// Entity
@Data
@EqualsAndHashCode(callSuper = false)
@Entity
@EntityListeners(AuditingEntityListener.class)
@Table
@DynamicUpdate
public class MysqlFruit {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private Integer size;

    @LastModifiedDate
    private Date updateTime;
}
```

对应的数据库如下
```sql
show create table mysql_fruit;

CREATE TABLE `mysql_fruit` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT 'Fruit name.',
  `size` int DEFAULT NULL,
  `update_time` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_k9oym0pnlq6pbnhh0a1aheivt` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
-- update mysql_fruit set size = -1, update_time = now();

truncate mysql_fruit;

INSERT INTO `demo_spring`.`mysql_fruit` (`id`, `name`, `size`, `update_time`) VALUES (1, 'a', -1, now());
INSERT INTO `demo_spring`.`mysql_fruit` (`id`, `name`, `size`, `update_time`) VALUES (2, 'b', -1, now());

select * from mysql_fruit;
```

现有如下的数据
```
id	name	size	update_time
5	a		-1		2022-06-09 10:41:32.697000
```

执行一次服务以后, 日志如下
```
before update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit2 {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
```

#### 如果改为 @Modifying(clearAutomatically = false, flushAutomatically = true) 

可以看出, 在没有使用 @Modifying 的任何参数的时候, 这次的修改是不会对缓存数据有任何影响的. 这个时候虽然已经往数据库刷了数据, 但是 select 仍然没有进行原生查找, 仍然走的是缓存, 所以结果不会有任何改变. 日志同上.

#### 再改为 @Modifying(clearAutomatically = true, flushAutomatically = false) 

这个时候的结果是 
```
before update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit2 {"id":1,"name":"a","size":0,"updateTime":"2022-06-09 12:06:39"}
```

这里只有 fruits2 的 size 被更新成为了0, 也就是说, 这次的查找是原生查找. 这里看上去有点诡异, 因为同一行数据, 已经发生了不一致了, 那么这里测试一下各自有没有被 entityManager 管理. 

#### 测试是否被 entityManager 管理

```
fruit.setName("a1");
fruit2.setName("a2");
```
尝试将 上面这2行分开执行, 发现这2个都仍然被 entityManager 管控, 也就是这里还是没有发生被动的 detach 行为. 目前我只能说所有的 detach 都只能手动进行.


#### 再改为 @Modifying(clearAutomatically = true, flushAutomatically = true) 

这个时候的结果仍然是 
```
before update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit {"id":1,"name":"a","size":-1,"updateTime":"2022-06-09 12:06:39"}
after update and select again: fruit2 {"id":1,"name":"a","size":0,"updateTime":"2022-06-09 12:06:39"}
```
也就是说, flushAutomatically 对于 RR 级别的事务来说, 没有太大区别, 只是相当于提前发送了命令给数据库执行


## 探索 entity 和 entityManager 的绑定

先看下面这段代码

```java
@Transactional(transactionManager = "mysqlTransactionManager", timeout = 36000, rollbackFor = Exception.class)
@Override
public void updateFruitEntity(MysqlFruit mysqlFruit) {

	mysqlFruitRepository.save(mysqlFruit);

	// 如果没有这一句的话, 则不会即时刷新到 数据库, 那么报错只会发生在事务提交的一瞬间. 如果加了这一句, 那么就会在过程中报错.
	// entityManager.flush();

	log.info("mysqlFruit {}", JsonUtils.obj2String(mysqlFruit));

	// 注意这里不会自动让 mysqlFruit 被 entityManager 管理
	mysqlFruit.setName("after saving");

}
```

这里的结论如下:
* save 不会自动刷新到数据库
* save 不会让外部实体自动绑定


## in 被改为 = 的问题

> https://stackoverflow.com/questions/47992165/jpa-jpql-in-clause-how-to-use-in-clause-in-jpa

Not directly related to OP's specific query, but relevant to JPA IN clause in general:

Contrary to pvpkiran's answer, if you are doing anything other than SELECT queries (e.g. DELETE, UPDATE), it may be much more efficient to use @Query:

```java
@Modifying
@Query("DELETE from Customer al where al.fileCode in :groups")
deleteByFileCodeIn(@Param("groups") List<String> groups)
instead of relying on Spring JPA's query method:

deleteByFileCodeIn(List<String> groups) // avoid this
```
Reason:

Spring JPA query method's default implementation of the IN clause is inefficient. Underneath the hood, it will 1. first select all records that match the IN criteria, then 2. execute a DELETE statement for each record found.

```sql
select customer.id as id,... from customer where customer.file_code in (?,?,?,...)
delete from customer where id=?
delete from customer where id=?
delete from customer where id=?
...
```

This means that if there are 1000 matching records, it will generate and execute 1000 delete statements -- instead of a single DELETE...IN statement which is what's usually intended.

By using @Query for IN clauses, you can override Spring JPA's default implementation and dictate a more efficient query to use instead. In my own testing this has resulted in 10x improvement in response time for large (>3K) datasets.

One caveat is that depending on the database, there may be limitations in the number of parameters that can be used in the IN clause. This can be overcome by partitioning the List.

结论: 不要用 repository 的 jpa 方法进行非 select 操作, 不然就会单个执行.