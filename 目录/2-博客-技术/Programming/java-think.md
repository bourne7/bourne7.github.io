# Java 思考

## Vavr

从 https://mincong.io/en/my-hackathon-projects-at-datadog/ 这里看到一个有意思的项目。看黄明聪的说法，这个引入最终被拒绝了，但是我挖了一下这个项目的官网还是挺有意思的。

主要是针对函数式编程做了一些优化，比如下面这种

```java
Tuple2<String, Integer> java8 = Tuple.of("Java", 8); 

// (vavr, 1)
Tuple2<String, Integer> that = java8.map(
        s -> s.substring(2) + "vr",
        i -> i / 8
);

// (vavr, 1)
Tuple2<String, Integer> that = java8.map(
        (s, i) -> Tuple.of(s.substring(2) + "vr", i / 8)
);

```

可以看出上面这2种写法是现有的java 不具备的，因为 tuple 实际上是对多重结果的包装，一个函数可以返回多个结果了。在我自己的代码里面，我弄过 TupleThree 这个数量的，但是我在一些中间件里面发现过 Tuple8 这样的东西，这意味着对于业务系统来说，存在这需要返回大量不同值的情况。

### 柯里化

```java
Function2<Integer, Integer, Integer> sum = (a, b) -> a + b;
Function1<Integer, Integer> add2 = sum.curried().apply(2); 

then(add2.apply(4)).isEqualTo(6);


Function3<Integer, Integer, Integer, Integer> sum = (a, b, c) -> a + b + c;
final Function1<Integer, Function1<Integer, Integer>> add2 = sum.curried().apply(2);

then(add2.apply(4).apply(3)).isEqualTo(9);
```

### 总结

Vavr 是对 java8 的函数式编程的一种补充，总的来说还是挺科学的，但是会有一些缺点，比如团队不是所有人都愿意用这种思想来干活；里面的大部分特性我觉得很有可能是以后的java会自带的，也用不着现在着急引入。不过作为个人项目的话，还是可以研究和学习一下的。
