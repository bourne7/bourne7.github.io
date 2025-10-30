# Java Thread 线程

### ThradLocal

需要注意的地方有：

* 里面的 Map 用于解决冲突用的是后向寻址，而不是桶+链表结构。
* hashcode 的计算很神奇，用的不是直接计算，而是在线程一开始就会创建，基于同步加法的斐波那契散列，看了一下相关文章，能得到比较好的分散值。
* 对于Key的引用时弱引用，主要是为了当线程结束的时候能使得变量被回收，但是有可能造成 key 为 null，但是 value 不为 null，从而导致 value 不能被回收。这个时候里面有一套复杂的清理脏数据逻辑。但是对于为什么一定要用弱引用，参考文章表示在业务代码里面强行执行 threadLocalInstance==null 的确会造成在比如线程池的情况下，永远无法回收的情况。而在弱引用的情况下，业务代码仍然这么写，就有很大概率被 ThreadLocal 的清理脏数据功能干掉。
* 在清理脏数据的时候，使用的逻辑是：从指定位置，向后最多查找 log(n) 个位置的数据，如果遇到了脏数据，会直接向后注意查询，直到一个非脏数据，接下来继续进行 log(n) 次查找。这里总结来说就是：由于放的时候，是后向寻址，一个位置塞过值，那么这个地方后面几个位置有值的概率就相对较大，但是也不是特别大，所以就折中一下决定扫描 log(n) 次。

总结就是，ThreadLocal 最好还是手动 remove。

> https://www.jianshu.com/p/dde92ec37bd1

### 关于斐波那契哈希

> https://book.huihoo.com/data-structures-and-algorithms-with-object-oriented-design-patterns-in-c++/html/page214.html#figgolden

为什么数组可以通过乘以斐波那契数，然后通过位移来得到比较好的散列？我猜测和斐波那契数的组成有关。