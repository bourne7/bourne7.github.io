# Actor

## 概念

> https://en.wikipedia.org/wiki/Actor_model

Actor 模型的基本概念:

The actor model adopts the philosophy that everything is an actor. This is similar to the everything is an object philosophy used by some object-oriented programming languages.

An actor is a computational entity that, in response to a message it receives, can concurrently:

* create a finite number of new actors;
* designate the behavior to be used for the next message it receives.
* send a finite number of messages to other actors;

这3者的顺序我调换了一下, 我觉得原本的顺序不是时序的.

## 其他特性

* 消息无序. 虽然也可以做到有序, 但是代价太大, 且不划算.
* 本地化处理. 单个的 actor 处理只会影响到本地状态, 没有关联影响
* Computational Representation Theorem. 计算表达理论. 看上去是说有限的actor可以非决定性的产生无穷多结果. 这里没太清楚, 是有随机的原因还是因为输入本身可以是无穷多的呢? 如果将随机本身视为输入的话, 那么唯一能解释的就是输入是无穷多的了.


## Erlang

作者：布丁

链接：https://www.zhihu.com/question/38032439/answer/84176970

来源：知乎

著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

Worse is Better (http://dreamsongs.com/RiseOfWorseIsBetter.html) 能比较好地解释题主的「为什么」。注意这篇文章的写作背景，这是一位 LISP 大佬在九十年代初反思为什么 LISP 这么牛的语言日渐式微，C 和 UNIX 这么烂的东西却起来了。概括下来大概是这样的：

软件设计有以下四大目标：简单、正确、一致、完整，但两大流派 MIT Style (MIT AI Lab 是 LISP 重镇) 和 New Jersey Style (C 和 UNIX 的老家贝尔实验室所在地) 对这些目标的优先级排序不同。MIT Style 认为软件正确性要绝对保证，然后优先级 正确 ~= 一致 > 完整 > 简单，简单这一条还得分，为了接口简单，可以忍受实现复杂。而 New Jersey Style 是正好反过来：首先软件实现得简单，做不到宁愿让接口复杂点，为了简单显然可以牺牲完整性，而正确、一致，那就尽力吧…… 反正得简单。Worse is Better 前面的 Worse 指的就是像 UNIX 这样为简单甚至能放弃「正确」这种有绝对标准的好的东西，后面的 Better, 指的是更好的生存适应性，这里面不带价值判断，文章作者也为 "Worse Is Better Is Worse" or "Worse is Better is Still Better" 一直在纠结，但这是一个能解释很多现象的准确观察。

没错，Erlang 就是 MIT Style, do the right thing 那个。它跟 LISP 一样产生深远的影响，会被无数后世语言技术借鉴 —— 即使不用 Erlang 开发我还是会对每个新人都会高度推荐 Erlang paper (http://erlang.org/download/armstrong_thesis_2003.pdf) —— 可是能火起来的，还会是那帮新泽西佬做出来的敢连 generics 都没有的烂货。

一个东西火起来的关键在于传播。文章把 C 和 UNIX 比作病毒：它实现（而不是接口）很简单，所以能很容易移植（感染）到别的平台，迅速跟原有平台的东西整合，因为它东西少，不拘泥于「正确」、「本质」之类的东西，能根据平台和需求快速演化，也能不断吸(chao)收(xi) 别人的东西让自己变得更强大。

但是 Erlang 不行，阻碍 Erlang 传播的除了爱立信作死，还有它自己的特性。A History of Erlang 里数次提到，Erlang 很难移植到别的语言/运行平台，因为 Erlang 的运行模型太特别了（真可惜只有Erlang是对的），所以一切都只能自己搞，同样原因要调用宿主平台的原有模块也很困难。Erlang 有一个简单、正确、不妥协的接口，但是底层实现就不得不非常复杂精巧，当底层实现的优化都不能满足你的特定需求时，你很难绕过统一美好的模型做case by case, quick and dirty的优化。某个算法 Erlang 跑太慢了你要引入 C 模块，难（望向 PHP & Python），复制消息传递通常不是瓶颈但如果变成瓶颈能传指针么？NO, YOU'RE DOING IT WRONG! 当然实际上 Erlang 内部对这个是有优化的，大的 binary 会自动变一个引用计数 buffer 放共享堆然后就只用传引用啦，但是这马上导致一个问题，因为 Erlang 没有（不需要有）全局 GC, 如果有进程已经不引用这个 binary, 但因为各种原因触发 GC 迟了，共享 heap 里引用计数一直不清零这段 binary 就僵在那流量冲击大你就等OOM吧，这是实际线上系统会碰到的问题，Binary是不是refc又不是你说了算，所以还是时不时自己强行 GC 一下…… 这其实就是一个接口简单导致实现复杂优化困难并且难以做对结果还是要用户自己动手的例子。Go 的 STW GC 虽然简陋，但它不限模型，鼓励复制但不禁止传指针，对这种少数的 case 很容易解决，再拿个 pool 来对付一下蠢萌的 GC 就可以了。模型不纯粹，实现极简陋，但解决问题。

Worse is Better 也能解释别的语言或技术的崛起。你不用很优秀但要有一个点做得好打到痛点，你不用设计完美但至少别犯大错，然后保持简单，保证好上手易移植易与现有系统整合，就可以了。包括 PHP（别打我），它架构上首先基于 CGI: 每个请求一个独立进程，share nothing，只用管道跟 httpd 通信，这天然保证错误隔离，也让 CGI 应用完全不需要管网络交互问题，短连接模型处理完请求就进程结束所以 PHP 甚至不需要 GC, memory pool 就行，更重要的是它也天然支持了热替换。你可以说这些全部是 Erlang 的设计点，也完全符合 Erlang paper 提倡的把困难问题（HTTP server）做成框架让业务写得简单轻松的思路，同时这也是传统的 UNIX 编程方式 —— 这就是所谓设计上别犯大错。然后再做一个亮点：直接 HTML 代码里嵌入脚本，现在你觉得这很傻，但当时互联网刚起来，HTML 还是新鲜事物，更没有什么 AJAX, 不用你自己组装字符串直接把代码嵌到 HTML 里太打动人心了。是，这没什么难的，但别人没有，PHP 有。至于一台机撑多少连接？速度怎么样？当时有个人访问你网页你都兴奋半天了，谁跟你研究这种吃撑了怎么办的问题？

如果 Worse is Better 作为一个定律是正确的，这听起来很可悲，我们就活该没有好东西用了。我感觉可以稍微修正一下：对于开发技术这种存在网络效应的东西，除非一个方案有革命性的优势，否则都会服从 worse is better 定律。

在电信行业，Erlang 可能真的拥有革命性的优势，我不熟悉的领域不评论，可惜电信行业本身相对狭窄封闭再加上爱立信作死，没网络效应可言。而在其他地方，革命性的优势，它没有。