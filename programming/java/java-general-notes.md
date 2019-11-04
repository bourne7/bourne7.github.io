# Java 通用笔记

2019-02-02

### 1. Comparator 和 Comparable

>http://www.cnblogs.com/skywang12345/p/3324788.html

Comparable 是排序接口。
若一个类实现了Comparable接口，就意味着“该类支持排序”。  即然实现Comparable接口的类支持排序，假设现在存在“实现Comparable接口的类的对象的List列表(或数组)”，则该List列表(或数组)可以通过 Collections.sort（或 Arrays.sort）进行排序。
此外，“实现Comparable接口的类的对象”可以用作“有序映射(如TreeMap)”中的键或“有序集合(TreeSet)”中的元素，而不需要指定比较器。

Comparable 定义
Comparable 接口仅仅只包括一个函数，它的定义如下：

```java
package java.lang;
import java.util.*;

public interface Comparable<T> {
    public int compareTo(T o);
}
```
说明：
假设我们通过 x.compareTo(y) 来“比较x和y的大小”。若返回“负数”，意味着“x比y小”；返回“零”，意味着“x等于y”；返回“正数”，意味着“x大于y”。

```java
// 对list进行排序，即会根据“name”进行排序
Collections.sort(list);
System.out.printf("Name sort, list:%s\n", list);

// 通过“比较器(AscAgeComparator)”，对list进行排序
// AscAgeComparator的排序方式是：根据“age”的升序排序

Collections.sort(list, new AscAgeComparator());
System.out.printf("Asc(age)  sort, list:%s\n", list);

// 通过“比较器(DescAgeComparator)”，对list进行排序
// DescAgeComparator的排序方式是：根据“age”的降序排序

Collections.sort(list, new DescAgeComparator());
System.out.printf("Desc(age) sort, list:%s\n", list);
```

### 2.ReentrantLock

在 ReentrantLock 里面有用到一个 AbstractQueuedSynchronizer，这个抽象类又继承了 AbstractOwnableSynchronizer，可以看出里面有一个用 transient 修饰的对象，就是一个独占的拥有当前同步器的线程 exclusiveOwnerThread 。加上 transient 是避免将当前线程也序列化进去。
