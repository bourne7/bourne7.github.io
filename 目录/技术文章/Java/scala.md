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
> https://www.runoob.com/scala/scala-data-types.html
* Null - 是个类型, 这个java 里面没有类似的概念, scala 的 null 等于 java 的 null, 但是多了一个形容 null 的类型的类 Null, 这一点是和 java 不同的
* Nil - 空的 List
* None - None is a subtype of Option type
* Unit – the Empty Return Type, 等于 java 的 void
* Nothing - Nothing is the absolute “no value” type in Scala. It doesn’t have any methods or values. Therefore, we can use Nothing in place of any Scala type both reference types and value types. Nothing类型在Scala的类层级的最底端；它是任何其他类型的子类型。一个是任何类子类的类, 注定无法被实例化.
* Any - Any type is the root of the entire Scala type system, and Nothing extends the Any type. Any 是所有类的父类
* AnyRef - AnyRef类是Scala里所有引用类(reference class)的基类



> https://www.geeksforgeeks.org/scala-null-null-nil-nothing-none-and-unit/

* null:

The reference types such as Objects, and Strings can be nulland the value types such as Int, Double, Long, etc, cannot be null, the null in Scala is analogous to the null in Java.

* Null:

It is a Trait, which is a subset of each of the reference types but is not at all a sub-type of value types and a single instance of Null is null. The reference types can be assigned null but the value types cannot be assigned null.

```scala
// Scala program using Null and null
  
// Creating object
object GfG
{
  
    // Main method
    def main(args: Array[String]) 
    {
        // Method that takes a parameter of type Null
        def usingnull(thing: Null): Unit = 
        { 
            println("GeeksForGeeks"); 
        }
  
        /*error: type mismatch;
  
        found   : java.lang.String("hey")
  
        required: Null*/
        //usingnull("hey")
  
        // passing null itself
        usingnull(null)
    }
}
```


* Nothing:

Nothing is also a Trait, which has no instances. It is a subset of each of the distinct types. The major motive of this Trait is to supply a return type for the methods which consistently throws an exception i.e, not even a single time returns generally. It is also helpful in providing a type for Nil.

* Unit:

The Unit is Scala is analogous to the void in Java, which is utilized as a return type of a functions that is used with a function when the stated function does not returns anything.

```scala
// Scala program using Unit type
  
// Creating object
object GfG
{
  
    // Main method
    def main(args: Array[String]) 
    {
        // Method return type is unit
        def printNumber(num: (Int) => Unit) = 
        {
  
            num(1); 
            num(2); 
            num(3);
        }
          
        printNumber(println)
    }
}
```
Here, method printNumber takes a parameter called num, which has a type of (Int) => Unit. This means that num is a method that consists a single parameter of type Int. method printNumber return type of Unit, which means num isn’t supposed to return a value.



* Nil:

Nil is Considered as a List which has zero elements in it. The type of Nil is List[Nothing] and as stated above, that Nothing has no instances, we can have a List which is confirmed to be desolated.

```scala
// Scala program to show that
// Nil is an empty list
  
// Creating object
object GfG
{
  
    // Main method
    def main(args: Array[String]) 
    {
  
        // Displays empty list
        println(Nil)
    }
}
```


* None:

It is one of the children of Scala’s Option class which is utilized to avoid assignment of null to the reference types. lets see some examples.

```scala
// Scala program to convert
// None to empty list
  
// Creating object
object GfG
{
  
    // Main method
    def main(args: Array[String]) 
    {
  
        // Displays empty list
        println(None.toList)
    }
}
```


## 一些总结

* apply 约等于 c++ 里面对于 () 的重载, 可以取代构建方法

* In Java terms, Scala's Seq would be Java's List, and Scala's List would be Java's LinkedList.
  Note that Seq is a trait, which is equivalent to Java's interface, but with the equivalent of up-and-coming defender methods. Scala's List is an abstract class that is extended by Nil and ::, which are the concrete implementations of List.

* 成员变量: 只有 trait 和 abstract 的 class 可以不用初始化成员变量, 其他都需要初始化, 这一点和 java 是不同的, 不过我觉得这一点其实还是可以像 java 那样好一些, 因为 对象就默认都是 null, 基本类型基本都是 0 就行了. java 这种做法唯一的问题在于 final 的又需要额外处理, 所以 scala 可能就是在这一点做到了统一吧.

## 源码阅读 scala.Option#orNull

```scala
scala.Option#orNull

@inline final def orNull[A1 >: A](implicit ev: Null <:< A1): A1 = this getOrElse ev(null)
```

### 1. implicit

有3种使用方式, 类, 方法, 参数. 效果差不多: 当缺省的时候, 编译器会寻找到最符合的 implicit 的对象来调用, 所以这里也不允许相同类型的隐式方式存在2份. 

我认为这个是一个语法糖, 有点类似于 inline 的意思. 在这个地方意思就是说 ev 这个方法的默认实现已经有了.

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



