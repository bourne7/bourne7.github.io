# Akka 入门与实践【知乎书店】

> https://www.zhihu.com/pub/reader/119583518/chapter/1057336567902851072

## Actor 和消息传递

* Actor ：一个表示工作节点的并发原语，同步处理接收到的消息。Actor 可
以保存并修改内部状态。
* 消息 ：用于跨进程（比如多个 Actor 之间）通信的数据。
* 消息传递 ：一种软件开发范式，通过传递消息来触发各种行为，而不是直接
触发行为。
* 邮箱地址 ：消息传递的目标地址，当 Actor 空闲时会从该地址获取消息进
行处理。
* 邮箱 ：在 Actor 处理消息前具体存储消息的地方。可以将其看作是一个消
息队列。
* Actor 系统 ：多个 Actor 的集合以及这些 Actor 的邮箱地址、邮箱和配置
等。

我认为这里的邮箱非常关键，也是 Akka 的重点。Actor 本身可以认为是无状态方法，符合 lambda 编程的那一套。

## akka.actor.typed.javadsl.ActorContext

Source Code could be accessed in my repo: learn_scala

An Actor is given by the combination of a Behavior and a context in which this behavior is executed. As per the Actor Model an Actor can perform the following actions when processing a message:

* send a finite number of messages to other Actors it knows
* create a finite number of Actors
* designate the behavior for the next message

In Akka the first capability is accessed by using the tell method on an ActorRef, the second is provided by #spawn and the third is implicit in the signature of Behavior in that the next behavior is always returned from the message processing logic.

An ActorContext in addition provides access to the Actor’s own identity (“getSelf”), the ActorSystem it is part of, methods for querying the list of child Actors it created, access to Terminated and timed message scheduling.

## AbstractBehavior and AbstractActor

> https://stackoverflow.com/questions/59263528/whats-the-difference-between-using-abstractbehavior-and-abstractactor-to-define

* AbstractBehavior Is Akka Typed, which is the way to define Actor Behavior from Akka 2.6. It is in 2.5 but as experimental.
* AbstractActor Is for untyped Actors, named classic Actors as of Akka 2.6.

If you're on Akka 2.6 I'd suggest using AbstractBehavior and following the try-akka guide: https://developer.lightbend.com/guides/akka-quickstart-java/

## AbstractBehavior 执行顺序

详情可以参考 repo 里面的例子

#### 通过 ActorSystem.create 和 getContext().spawn 这2种方式创建有啥区别呢？

通过 create 创建的，只是注入了创建方式到工厂，实例化是在收到消息以后；而通过 spawn 创建的就会立刻实例化。

#### createReceive() 是否只再创建的时候调用？

调用了 tell 以后才会调用 message.fromActorRef.tell(new Greet(message.whom, getContext().getSelf()));

## 并发

共享状态是不安全的。是竞态条件，也是使用共享状态的并发模型存在的最基本的问题之一。

## 响应式四准则

* 灵敏性
* 伸缩性
* 容错性
* 事件驱动设计

