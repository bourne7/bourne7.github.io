# Other DBs

2020-11-28

## GraphQL is the better REST

> https://www.howtographql.com/basics/1-graphql-is-the-better-rest/

作者：Cat Chen
链接：https://www.zhihu.com/question/264629587/answer/949588861
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

第一，Facebook 从来没有公开自己的 GraphQL 后端设计，使得大家必需要用第三方的，但体验显然不如我们在 Facebook 内部使用 GraphQL 好。我上面说了，数据必需已经以图的数据结构进行存储才有优势。Facebook 内部有非常好的后端做好了这件事情，而且还内置了基于隐私设置的访问控制。例如说你发的帖子有些是所有人可见的、有些是好友可见的、有些是仅同事可见的，我在打开你的页面时 Facebook 有一个中间层保证了根据我和你的关系我只能看到我该看到的帖子。GraphQL 在这一层之上，所以无论 GraphQL 怎么写我都不可能看到我不该看到的信息。

第二，并不是所有场景都适用于 GraphQL 的，有些很简单的事情就应该用 RESTful API 来实现。Facebook 内部用户增长部门的很多 API 都还不是 GraphQL，因为没必要迁移到 GraphQL。用户增长部门的 API 处理新用户注册、填写短信验证码之类的事情，这些事情都是围绕着一个用户的具体某项或多项信息发生的，根本没有任何图的概念。可以强行写作 GraphQL，但得不到显著的好处。既然老的 API 早就写好了，需要的时候做一些小改动，但没必要重写。

第三，GraphQL 尽管查询的数据是图状数据结构，但实际获得的数据视图是树状数据结构。每一个 GraphQL 查询或更新都有自己的根节点，然后所有的数据都是从根结点展开出去的。查询后获得的数据如果要在前端重新变回图的状态，那前端就不能简单地缓存查询得到的数据，必须用对用的 GraphQL 存储库，然后通过顶点的 ID 把不同节点之间的某些边重新连接起来。

## mongodb

要注意新版的mongo客户端已经不是 mongo 而是 mongosh 了，安装方法在这里

> https://www.mongodb.com/docs/mongodb-shell/install/#std-label-mdb-shell-install

