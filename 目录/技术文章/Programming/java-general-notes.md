# Java 通用笔记

2019-02-02

## Comparator 和 Comparable

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

## ReentrantLock

在 ReentrantLock 里面有用到一个 AbstractQueuedSynchronizer，这个抽象类又继承了 AbstractOwnableSynchronizer，可以看出里面有一个用 transient 修饰的对象，就是一个独占的拥有当前同步器的线程 exclusiveOwnerThread 。加上 transient 是避免将当前线程也序列化进去。

## 为什么匿名内部类用到的外部变量，只能是 final？

这里有个解释：
> https://www.cnblogs.com/dolphin0520/p/3811445.html

总结一下就是：外部的方法结束以后，匿名内部类生命周期还没结束，这样的话，外部的变量在内部就无法访问了。为了解决这个问题，java就将外部的变量复制了一份到内部。

但是这样会造成2份数据不一致，所以就通过 final 来进行限制。顺便说一句，Lambda使用的并不是匿名内部类，而且是：

> lambda表达式与普通的匿名内部类的实现方式不一样，在第一次编译阶段只是多增了一个lambda方法，并通过invoke dynamic 指令指明了在第二次编译（运行）的时候需要执行的额外操作——第二次编译时通过java/lang/invoke/LambdaMetafactory.metafactory 这个工厂方法来生成一个class（其中参数传入的方法就是第一次编译时生成的lambda方法。）这个操作最终还是会生成一个实现lambda表达式的内部类。
> https://www.cnblogs.com/chenjingquan/p/10574320.html

## Java 泛型 super 和 extends

看到很多例子都是拿 List 做例子，其实通配符还用在了很多地方，比如：

```java
// java.util.stream.Stream#min
Optional<T> min(Comparator<? super T> comparator);
```

可以这么思考：给泛型对象赋值，或者读取泛型对象的时候，是否可以确认此对象满足 super 或者 extends 要求。显然，当使用 extends 的时候，对象有可能是任何 T 的子类，是无法对这个对象进行赋值的，但是读取成为 T 是没问题的。而 使用 super 的时候，如果读取成为 T 的话，是不行的，因为有可能对象是 T 的父类，缺少一些属性，所以只能读取成为一定不会缺少任何属性的 Object，但是这样就会丢失几乎所有属性。而赋值给 super 的话，则是没有问题的，但是也一定要赋值 T 或者 T 的子类，这样能确保所有的对象都能满足 继承自T 的要求。

## JMC (Java Mission Control) 

高版本的的 JMC 启动会出问题, 原因是 jdk 版本太低了, 需要提高到 11 或者 17, 不能用 8. 如果这个时候我们不想修改全局的环境变量, 可以单独修改 JMC 的运行 JDK 版本.

```
jmc.ini

-vm
D:/java-17/bin/java
```

## JDK

* 上哪里下载 JDK？

目前比较好的方式是去 adoptium 官网下 

> https://adoptium.net/temurin/releases/

这个是 adopt openjdk 的继任者，我们的生产库用的 jdk 镜像也是基于 adopt 打包出来的。另外，尽量别用 oracle 的，因为从 2020 年的 8u202 版本开始，用了 Java SE OTN License，总的来说为了避免各种 License 的麻烦事，最好避免用 oracle 的 jdk。

> https://www.oracle.com/java/technologies/javase/javase8-archive-downloads.html



## JNI JNR JNA FFI

> https://developer.okta.com/blog/2022/04/08/state-of-ffi-java

简单来说，FFI 是一种调用标准 Foreign Function Interface，其他都是实现，其中 Java Native Runtime (JNR) 和 Java Native Access (JNA) 都是 Java Native Interface (JNI) 的封装。

Enter Project Panama 是 FFI 的最新的实现。具有以下功能

* Foreign-Memory Access API 是 Java 14 开始有的，能原生访问堆外内存了
* Foreign Linker API 是 Java 16 开始有的，提供了静态类型的，原生java对native的调用。原生支持 C
* Vector API which is crucial for FFI, especially in machine learning and advanced computations.
* Foreign Function & Memory API. Foreign Linker API & Foreign-Memory Access API has evolved together to become the Foreign Function & Memory API. It was first incubated in JDK 17. 是前2个和统称
* jextract. And finally, there is the fantastic jextract tool. While it’s not an API or part of the JDK itself, it is an essential tool for Project Panama. 一个工具，能生成 h 头文件，并且会成为 jdk 的一部分。

Panama 的目的就是为了取代 JNI。看了一下使用方法，新的方式有2种，分别是反射调用以及用 jextract 生成对应的类调用，后者比较好一些，速度更快，更安全。不过前者也有好处，是平台无关的，所以简单调用就用前者，复杂调用后后者。


## 取一个指定位数的最大整数

```text
long MAX = -1L ^ (-1L << BIT);
long MAX= ~(-1L << BIT);
```

上面这2句是等效的，实际上第二行是idea的代码提醒让我改的，的确更加简洁了。-1的二进制标识就是 “1111111111111111”。

## JMC

JMC可以说是非常强大的 jvm 监控工具了，除了可以分析 jmap dump 出来的内存以外，也可以直接远程到 jvm 来监测。这里给出需要添加的参数：

> https://stackoverflow.com/questions/31257968/how-to-access-jmx-interface-in-docker-from-outside

```
-Dcom.sun.management.jmxremote
-Dcom.sun.management.jmxremote.authenticate=false
-Dcom.sun.management.jmxremote.ssl=false
-Dcom.sun.management.jmxremote.port=<PORT>
-Dcom.sun.management.jmxremote.rmi.port=<PORT>
-Djava.rmi.server.hostname=<IP>

where:

<IP> is the IP address of the host that where you executed 'docker run' 如果是 docker 的话，这里的 IP 是宿主机的。
<PORT> is the port that must be published from docker where the JVM's JMX port is configured (docker run --publish 7203:7203, for example where PORT is 7203). Both `port` and `rmi.port` can be the same.
```

