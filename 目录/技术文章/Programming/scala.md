# Scala

## 安装

打开官网以后(2022-07), 发现只能通过 the Scala installer for Windows 来安装了, 没有之前的手动下载模式了. 所以先尝试用这种方式安装

* 双击 exe 开始安装的时候, 极大概率会遇到网络问题无法下载, 由于这个还不是命令行的脚本, 我就没研究加代理的方式, 重试了好几次才安装成功
* 如果安装的时候报错了, 可以将报错对应的文件夹删除掉, 然后重新安装.
* 都安装完以后可以通过控制台进行测试

idea 安装

* 先安装 scala 插件
* 新建新项目的时候, 选择 scala 和 sbt
* 会提醒下载所需要的组件, 都选上, 然后等下载完毕就行了.

## Scala REPL

Scala REPL is an interactive command line interpreter shell, where REPL stands for Read-Evaluate-Print-Loop. It works like it stands for only.

## SBT

Scala 专用的编译工具. 实际上可以不用安装别的, 只需要下载 sbt 官方的安装包, 就能完成 scala 的编译了, 换句话说, scala 只是一种开发期的SDK, 并不是必须的. (这个是我的理解, scala 官方的手动方式就是这样的)

按照下面的方式可以弄出来一个简单的 Scala 项目
>https://www.scala-sbt.org/1.x/docs/sbt-by-example.html

## 注意

* sbt 和 maven, gradle 最大的不同在于是开启了一个服务, 可以在这个服务里面执行参数. 服务本身不会停止, 除非手动退出.
* session save 指令可以保存当前 session 里面的变量到 build.sbt 文件, 如果文件不存在则会创建
* Scala 文件和 java 文件的路径不一样, 实际上是可以不对应的, 也就是可以在 A 路径下面的 scala 文件里的 package 写明是 B

一个典型的结构如下:
```
.
├── build.sbt
├── project
│   └── target
│       ├── active.json
│       └── config-classes
│           ├── $10f25d1a0540d76b1a11$.class
│           ├── $10f25d1a0540d76b1a11.cache
│           ├── $10f25d1a0540d76b1a11.class
│           ├── $d9a346d63c703f78d9df$.class
│           ├── $d9a346d63c703f78d9df.cache
│           └── $d9a346d63c703f78d9df.class
└── src
    └── main
        └── scala
            └── example
                └── Hello.scala
```

注意这个时候的 Hello.scala 的 package 和 真实路径不一致, 真实路径是 example. 我认为这种方式不太好, 不强制规定会导致项目结构混乱.
```scala
package com.example

object Hello {
  def main(args: Array[String]): Unit = {
    println("Hello")
  }
}
```

## 数据类型

> https://www.baeldung.com/scala/nil-null-nothing-unit-none
> https://www.geeksforgeeks.org/scala-null-null-nil-nothing-none-and-unit/
> https://www.runoob.com/scala/scala-data-types.html


Null - Trait，同时也是所有普通对象的子类（不包括基础类型），null 的类型，同时也是所有普通对象的子类（不包括基础类型）

None - Option 的一个子类，用于避免赋值一个 null

Nothing - Trait，同时也是任何其他类型的子类型，所以注定无法被实例化。（用于返回一个对象，但是该方法注定会抛出异常？）

Nil - 空的 List，The type of Nil is List[Nothing]

Unit – the Empty Return Type, 等于 java 的 void

Any - 所有类的父类

AnyRef - AnyRef类是Scala里所有引用类(reference class)的基类


## 杂项

* apply 约等于 c++ 里面对于 () 的重载, 可以取代构建方法

* In Java terms, Scala's Seq would be Java's List, and Scala's List would be Java's LinkedList.
  Note that Seq is a trait, which is equivalent to Java's interface, but with the equivalent of up-and-coming defender methods. Scala's List is an abstract class that is extended by Nil and ::, which are the concrete implementations of List.

* 成员变量: 只有 trait 和 abstract 的 class 可以不用初始化成员变量, 其他都需要初始化, 这一点和 java 是不同的, 不过我觉得这一点其实还是可以像 java 那样好一些, 因为 对象就默认都是 null, 基本类型基本都是 0 就行了. java 这种做法唯一的问题在于 final 的又需要额外处理, 所以 scala 可能就是在这一点做到了统一吧.

* 目前处于 2 和 3 的替换期，还有很多东西不明朗，其实对这门语言来说很不利。比如这里 https://docs.scala-lang.org/cheatsheets/index.html 有说到 Define function. def f(x: Int)   { x * x } Hidden error: without = it’s a procedure returning Unit; causes havoc. Deprecated in Scala 2.13.

* zip 顾名思义，能合并2个迭代对象

## 源码阅读 scala.Option#orNull

```scala
scala.Option#orNull

@inline final def orNull[A1 >: A](implicit ev: Null <:< A1): A1 = this.getOrElse(ev(null))

@inline final def orNull[A1 >: A](implicit ev: Null <:< A1): A1 = this getOrElse ev(null)

```

### 1. implicit

有3种使用方式: 类, 方法, 参数. 效果差不多: 当缺省的时候, 编译器会寻找到最符合的 implicit 的对象来调用, 所以这里也不允许相同类型的隐式方式存在2份. 

我认为这个是一个语法糖, 有点类似于 inline 的意思. 在这个地方意思就是说 ev 这个方法的默认实现已经有了.

>https://blog.bruchez.name/posts/generalized-type-constraints-in-scala/#question-3-how-does-this-whole-thing-even-work

这个解释更加详细，这个的解释也是我认为目前最好的。

### => 参数传递：值传递或者名字传递

>https://stackoverflow.com/questions/13337338/call-by-name-vs-call-by-value-in-scala-clarification-needed

call-by-value functions compute the passed-in expression's value before calling the function, thus the same value is accessed every time. Instead, call-by-name functions recompute the passed-in expression's value every time it is accessed.

这个实在是有点隐晦。。。可以认为变量替换：provider 每次都会重新计算。

### <- 生成器，for 的新用法

>https://www.baeldung.com/scala/for-comprehension
>https://docs.scala-lang.org/tour/for-comprehensions.html

The statement result <- results represent a generator. It introduces a new variable, result, that loops over each value of the variable results. So, the type of result is TestResult.

注意这种写法是需要配合 yield 使用的

```scala
case class User(name: String, age: Int)

val userBase = List(
  User("Travis", 28),
  User("Kelly", 33),
  User("Jennifer", 44),
  User("Dennis", 23))

val twentySomethings =
  for (user <- userBase if user.age >=20 && user.age < 30)
  yield user.name  // i.e. add this to a list

twentySomethings.foreach(println)  // prints Travis Dennis
```

### 2. <:<

有点像泛型的上下界限的合体, 能指定一个范围

> https://stackoverflow.com/questions/7759361/what-does-b-a-do-in-scala
> https://stackoverflow.com/questions/3427345/what-do-and-mean-in-scala-2-8-and-where-are-they-documented

* [B >: A] is a lower type bound. It means that B is constrained to be a supertype of A.
* [B <: A] is an upper type bound, meaning that B is constrained to be a subtype of A.
* A =:= B means A must be exactly B
* A <:< B means A must be a subtype of B (analogous to the simple type constraint <:) 
* A <%< B means A must be viewable as B, possibly via implicit conversion (analogous to the simple type constraint <%) 

这里表示入参的类型, 必须要是可以 Null 类型的子类, 也就是不能是基础类型. 这里要注意只用了一半, 实际上完整用法是这样的:

```scala
def toMap[T, U](implicit ev: A <:< (T, U)): immutable.Map[T, U]

可以看出 <:< 的参数是2个, 分别是上下界. 它不是一个关键词, 而是一个类, 定义如下

sealed abstract class <:<[-From, +To] extends (From => To) with Serializable {

从这里还可以看出是一个 sealed 的类, 不过用起来的时候就感觉是个关键词了, 聪明的 idea 仍然将其染色成为了 class 的颜色
```

泛型约束 关于 =:= 这些。 These are called generalized type constraints. 

```scala
case class Foo[A](a:A) { // 'A' can be substituted with any type
    // getStringLength can only be used if this is a Foo[String]
    def getStringLength(implicit evidence: A =:= String) = a.length
}
```




### 3. +A

> https://stackoverflow.com/questions/4531455/whats-the-difference-between-ab-and-b-in-scala

Q[A <: B] means that class Q can take any class A that is a subclass of B.

Q[+B] means that Q can take any class, but if A is a subclass of B, then Q[A] is considered to be a subclass of Q[B].

Q[+A <: B] means that class Q can only take subclasses of B as well as propagating the subclass relationship.

The first is useful when you want to do something generic, but you need to rely upon a certain set of methods in B. For example, if you have an Output class with a toFile method, you could use that method in any class that could be passed into Q.

The second is useful when you want to make collections that behave the same way as the original classes. If you take B and you make a subclass A, then you can pass A in anywhere where B is expected. But if you take a collection of B, Q[B], is it true that you can always pass in Q[A] instead? In general, no; there are cases when this would be the wrong thing to do. But you can say that this is the right thing to do by using +B (covariance; Q covaries--follows along with--B's subclasses' inheritance relationship).

"+" 的作用可以解决 Java 里面，泛型擦除的问题。

> https://stackoverflow.com/questions/29412857/what-does-a-mean-in-scala-class-declaration
```scala
val x: Option[String] = Some("a")
val y: Option[Object] = x
```



### 协变和逆变 covariance and contravariance

Consider a Scala immutable Seq. It is defined as trait Seq[+A]. The little + says that if I require a Seq[Fruit], I can pass a Seq[Banana] just fine:

```scala
def takeFruits(fruits: Seq[Fruit]) = ...
takeFruits(Seq(new Banana))
```

可以记忆为： + 就是 extends


另外一个例子

>https://stackoverflow.com/questions/27627782/signs-in-generic-declaration-in-scala

It's covariance and contravariance. https://en.wikipedia.org/wiki/Covariance_and_contravariance_(computer_science)

Basically it says for Generic types how inheritance will work. Easy sample from Scala is - trait Seq[+A] Because of the + , the code
```scala
val s: Seq[Person] = Seq[Student]()
```
will compile because Student extends Person. Without the + it won't work

A bit more complex sample -
```scala
class C[-A, +B] {
  def foo(param: A): B = ???
}

class Person(val name: String)

class Student(name: String, val university: String) extends Person(name)

val sample: C[Student, Person] = new C[Person, Student]
```


### 对于 => 的解释

> https://stackoverflow.com/questions/6951895/what-does-and-mean-in-scala

=> has several meanings in Scala, all related to its mathematical meaning as implication.

In a value, it introduces a function literal, or lambda. e.g. the bit inside the curly braces in List(1,2,3).map { (x: Int) => x * 2 }

In a type, with symbols on both sides of the arrow (e.g. A => T, (A,B) => T, (A,B,C) => T, etc.) it's sugar for Function<n>[A[,B,...],T], that is, a function that takes parameters of type A[,B...], and returns a value of type T.

Empty parens on the left hand side (e.g. () => T) indicate that the function takes no parameters (also sometimes called a "thunk");

Empty parens on the right hand side denote that it returns ()—the sole value of type Unit, whose name can also be written ()—confused yet? :)

A function that returns Unit is also known as a procedure, normally a method that's called only for its side effect.

In the type declaration for a method or function parameter, with no symbol on the left hand side (e.g. def f(param: => T)) it's a "by-name parameter", meaning that is evaluated every time it's used within the body of the function, and not before. Ordinary "by-value" parameters are evaluated before entry into the function/method.

In a case clause, they separate the pattern (and optional guard) from the result expression, e.g. case x => y.



### Play Framework

```scala
305 final def apply(block: R[B] => Result): Action[B] = async(block.andThen(Future.successful))
321 final def apply(block: => Result): Action[AnyContent] =
    apply(BodyParsers.utils.ignore(AnyContentAsEmpty: AnyContent))(_ => block)
```

block: => Result 为 by-name paramaters, 作用是延时调用。

一个普通的接口来说，这里的调用顺序为从左到右，最后的 (_ => block) 调用的实际上是 

final def apply(block: R[B] => Result): Action[B] = async(block.andThen(Future.successful))

从 ActionBuilder 过来的。要注意，第一次进入 321 的时候，入参是一个普通类型。第二次从 (_ => block) 进入 305 行的时候，入参时机上是一个 Function1 .


> 这里似乎隐含着 object 可以直接当对象来引用？



### case class

> https://docs.scala-lang.org/tour/case-classes.html

相当于所有成员变量都是 final 的普通类。所有的参数是 val。和 Java 最大的不同在于 == 的运算是会被判断等于的。也就是按照官网的例子，2次调用 apply 方法返回的对象，概念上是2个对象，实际上可能是2个对象？

这里的思考是：即使返回的是2个对象，也没有意义了，因为外界已经无法分辨出这2个对象的区别了。

从 Java 14 开始，多了个 record class 预览版, 作用和这个一样。这个特性从 Java 16开始，正式可以用了。


### difference between scala extension and implicit [from GPT-4]


Scala has two main mechanisms to extend existing types or provide additional functionality: extension methods and implicit conversions. Although they have similar goals, they have different ways of achieving them.

Extension methods (Scala 3):
Extension methods allow you to add new methods to existing types without modifying their source code. In Scala 3, extension methods are defined using the extension keyword. They enable you to call the new method as if it were a member of the original type. This is sometimes called "ad-hoc polymorphism."

Example:

```scala
implicit class RichString(val s: String) extends AnyVal {
  def isPalindrome: Boolean = s == s.reverse
}

val palindrome = "racecar"
val isPalindrome = palindrome.isPalindrome // true
```

In this example, an isPalindrome method is added to the String type using an extension method.

Implicit conversions (Scala 2):
Implicit conversions allow you to automatically convert one type to another using an implicit function. This is often used to extend existing types with new functionality or to provide a more natural interface between different types. Implicit conversions have been used in Scala 2, but they are discouraged in Scala 3 due to their potential for creating confusing and hard-to-understand code.

Example:

```scala
implicit class RichString(val s: String) extends AnyVal {
  def isPalindrome: Boolean = s == s.reverse
}

val palindrome = "racecar"
val isPalindrome = palindrome.isPalindrome // true
```

In this example, an isPalindrome method is added to the String type using an implicit conversion from String to a new RichString class.

Summary:

Extension methods (Scala 3) provide a more straightforward and less error-prone way to extend existing types with new methods. They make it easier to understand which methods are being added to a type and avoid the need for implicit conversions.
Implicit conversions (Scala 2) can be powerful but can lead to confusing and hard-to-understand code. They are being replaced by extension methods in Scala 3 to provide a more intuitive mechanism for extending types.

总结：截至 2023-03-30， GPT-4 的语法解释，已经比较完善了。比大部分的搜索结果完善。本来 Scala 的社区就不太活跃，语法又多变，与其自己查阅大量资料，不如一开始就问 GPT 【手动狗头】。


### force cast object

Like java casting, scala also has a force cast method. But it's not a method, it's a function.

| Scala               | Java             |
| ------------------- | ---------------- |
| obj.isInstanceOf[C] | obj instanceof C |
| obj.asInstanceOf[C] | (C)obj           |
| classOf[C]          | C.class          |

In Map.scala

```scala
def empty[K, V]: Map[K, V] = EmptyMap.asInstanceOf[Map[K, V]]
```

shows that an object could be cast as a instance. I have tested that an instance could not be cast to an object.