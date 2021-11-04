# Kafka 笔记

2020-12-03

## 查看版本

可以在 lib 下面看到 jar 包的版本，比如我的是 2.2.1


## 如何查看某个消费者组里面的 offset

```
./kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group wms-core-consumer-group --describe
```

如果是在 docker 里面，可以执行下面的命令

```
/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group [your-group-name] --describe
```

如果是在 docker 外面，可以执行下面的命令
```
docker exec -it kafka bash -c "/opt/bitnami/kafka/bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group [your-group-name] --describe"
```

## 参数调整

> https://www.cnblogs.com/weknow619/p/kafka.html


1. fetch.min.bytes

该属性指定了消费者从服务器获取记录的最小字节数。 broker 在收到消费者的数据请求时， 如果可用的数据量小于 fetch.min.bytes指定的大小，那么它会等到有足够的可用数据时才把它返回给消费者。这样可以降低消费者和 broker 的工作负载，因为它们在主题不是很活跃的时候(或者一天里的低谷时段)就不需要来来回回地处理消息。如果没有很多可用数据，但消费者的 CPU 使用率却很高，那么就需要把该属性的值设得比默认值大。如果消费者的数量比较多，把该属性的值设置得大一点可以降低 broker 的工作负载。

2. fetch.max.wait.ms

我们通过 fetch.min.bytes 告诉 Kafka，等到有足够的数据时才把它返回给消费者。而 fetch.max.wait.ms则用于指定 broker的等待时间，默认是 500ms。如果没有足够的数据流入 Kafka，消费者获取最小数据量的要求就得不到满足，最终导致500ms的延迟。 如果要降低潜在的延迟(为了满足 SLA)，可以把该参数值设置得小一些。如果 fetch.max.wait.ms被设 为 100ms，并且 fetch.min.bytes 被设为 1MB，那么 Kafka在收到消费者的请求后，要么返 回 1MB 数据，要么在 100ms 后返回所有可用的数据 ， 就看哪个条件先得到满足。

3. max.parition.fetch.bytes

该属性指定了服务器从每个分区里返回给消费者的最大字节数。它的默认值是 1MB，也 就是说， KafkaConsumer.poll() 方法从每个分区里返回的记录最多不超过 max.parition.fetch.bytes 指定的字节。如果一个主题有 20个分区和 5 个消费者，那么每个消费者需要至少 4MB 的可用内存来接收记录。在为消费者分配内存时，可以给它们多分配一些，因 为如果群组里有消费者发生崩溃，剩下的消费者需要处理更多的分区。 max.parition.fetch.bytes 的值必须比 broker能够接收的最大消息的字节数(通过 max.message.size属 性配置 )大， 否则消费者可能无法读取这些消息，导致消费者一直挂起重试。在设置该属性时，另一个需要考虑的因素是消费者处理数据的时间。 消费者需要频繁调用 poll() 方法来避免会话过期和发生分区再均衡，如果单次调用 poll() 返回的数据太多，消费者需要更多的时间来处理，可能无法及时进行下一个轮询来避免会话过期。如果出现这种情况， 可以把 max.parition.fetch.bytes 值改小 ，或者延长会话过期时间。

4. session.timeout.ms

该属性指定了消费者在被认为死亡之前可以与服务器断开连接的时间，默认是 3s。如果消费者没有在 session.timeout.ms 指定的时间内发送心跳给群组协调器，就被认为已经死亡，协调器就会触发再均衡，把它的分区分配给群组里的其他消费者 。该属性与 heartbeat.interval.ms紧密相关。heartbeat.interval.ms 指定了poll()方法向协调器 发送心跳的频 率， session.timeout.ms 则指定了消费者可以多久不发送心跳。所以， 一般需要同时修改这两个属性， heartbeat.interval.ms 必须比 session.timeout.ms 小， 一般是 session.timeout.ms 的三分之一。如果 session.timeout.ms 是 3s，那么 heartbeat.interval.ms 应该是 ls。 把 session.timeout.ms 值设 得比默认值小，可以更快地检测和恢 复崩溃的节点，不过长时间的轮询或垃圾收集可能导致非预期的再均衡。把该属性的值设置得大一些，可以减少意外的再均衡 ，不过检测节点崩溃需要更长的时间。

5. auto.offset.reset

该属性指定了消费者在读取一个没有偏移量的分区或者偏移量无效的情况下(因消费者长时间失效，包含偏移量的记录已经过时井被删除)该作何处理。它的默认值是latest， 意 思是说，在偏移量无效的情况下，消费者将从最新的记录开始读取数据(在消费者 启动之 后生成的记录)。另一个值是 earliest，意思是说，在偏移量无效的情况下，消费者将从 起始位置读取分区的记录。

6. enable.auto.commit

我们稍后将介绍 几种 不同的提交偏移量的方式。该属性指定了消费者是否自动提交偏移量，默认值是 true。为了尽量避免出现重复数据和数据丢失，可以把它设为 false，由自己控制何时提交偏移量。如果把它设为 true，还可以通过配置 auto.commit.interval.mls 属性来控制提交的频率。

7. partition.assignment.strategy

我们知道，分区会被分配给群组里的消费者。 PartitionAssignor 根据给定的消费者和主题，决定哪些分区应该被分配给哪个消费者。 Kafka 有两个默认的分配策略 。

- Range
该策略会把主题的若干个连续的分区分配给消费者。假设悄费者 C1 和消费者 C2 同时 订阅了主题 T1 和主题 T2，井且每个主题有 3 个分区。那么消费者 C1 有可能分配到这 两个主题的分区 0 和 分区 1，而消费者 C2 分配到这两个主题 的分区 2。因为每个主题 拥有奇数个分区，而分配是在主题内独立完成的，第一个消费者最后分配到比第二个消费者更多的分区。只要使用了 Range策略，而且分区数量无法被消费者数量整除，就会出现这种情况。

- RoundRobin
该策略把主题的所有分区逐个分配给消费者。如果使用 RoundRobin 策略来给消费者 C1 和消费者 C2分配分区，那么消费者 C1 将分到主题 T1 的分区 0和分区 2以及主题 T2 的分区 1，消费者 C2 将分配到主题 T1 的分区 l 以及主题T2 的分区 0和分区 2。一般 来说，如果所有消费者都订阅相同的主题(这种情况很常见), RoundRobin策略会给所 有消费者分配相同数量 的分区(或最多就差一个分区)。

可以通过设置 partition.assignment.strategy 来选择分区策略。默认使用的是 org. apache.kafka.clients.consumer.RangeAssignor， 这个类实现了 Range策略，不过也可以 把它改成 org.apache.kafka.clients.consumer.RoundRobinAssignor。我们还可以使用自定 义策略，在这种情况下 ， partition.assignment.strategy 属性的值就是自定义类的名字。

8. client.id

该属性可以是任意字符串 ， broker用它来标识从客户端发送过来的消息，通常被用在日志、度量指标和配额里。

9. max.poll.records

该属性用于控制单次调用 call() 方法能够返回的记录数量，可以帮你控制在轮询里需要处理的数据量。

10. receive.buffer.bytes 和 send.buffer.bytes

socket 在读写数据时用到的 TCP 缓冲区也可以设置大小。如果它们被设为-1，就使用操作系统的默认值。如果生产者或消费者与 broker处于不同的数据中心内，可以适当增大这些值，因为跨数据中心的网络一般都有 比较高的延迟和比较低的带宽 。