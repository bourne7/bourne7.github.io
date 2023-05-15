### Git 笔记

#### 1.创建SSH秘钥
```bash
ssh-keygen -t rsa -C "Work"

copy to github

ssh -T git@github.com
```

修改~/.ssh/config以添加多个ssh配置

```config
# ProxyCommand "C:\Program Files\Git\mingw64\bin\connect" -S 127.0.0.1:1080 -a none %h %p
# ProxyCommand connect -S 127.0.0.1:1080 -a none %h %p

Host github.com
  User git
  Port 22
  HostName github.com
  IdentityFile ~/.ssh/github
  TCPKeepAlive yes

Host ssh.github.com
  User git
  Port 443
  Hostname ssh.github.com
  IdentityFile ~/.ssh/github
  TCPKeepAlive yes
```

#### 2. Clone项目

目前有3种 clone 的方式，分别是 http, ssh, git。个人认为最好的应该是 ssh。gh还需要安装客户端，我认为不太方便。

其中 ssh 又分为普通的和 基于 https 的 ssh。如果你没法正常访问 22 端口，那么建议用 https

```bash
git clone git@github.com:bourne7/bourne7.github.io.git
git clone git@ssh.github.com:bourne7/bourne7.github.io.git

// 官方文档格式如下。可以看出可以省去 ssh:// 以及在 config 里面配置端口后，可以省去 443，那么和普通 ssh 链接相比，就只多了个 ssh.
git clone ssh://git@ssh.github.com:443/YOUR-USERNAME/YOUR-REPOSITORY.git

//查看当前的仓库连接方式
git remote -v
git remote show
git remote show origin

//然后删除当前的方式
git remote rm origin

// 然后添加新的仓库方式
git remote add origin git@github.com:myaccount/cocos2d-x.git
```


新仓库可能会遇到的问题：upstream到底是什么？

git中存在upstream和downstream, 简言之,当我们把仓库A中某分支x的代码push到仓库B分支y, 此时仓库B的这个分支y就叫做A中x分支的upstream, 而x则被称作y的downstream, 这是一个相对关系, 每一个本地分支都相对地可以有一个远程的upstream分支（注意这个upstream分支可以不同名, 但通常我们都会使用同名分支作为upstream）.

初次提交本地分支,例如 

git push origin develop 

操作, 并不会定义当前本地分支的upstream分支, 我们可以通过

git push --set-upstream origin develop

关联本地develop分支的upstream分支,另一个更为简洁的方式是初次push时,加入-u参数,例如

git push -u origin develop

这个操作在push的同时会指定当前分支的upstream.

注意

push.default = current

可以在远程同名分支不存在的情况下自动创建同名分支,有些时候这也是个极其方便的模式,比如初次push你可以直接输入 git push 而不必显示指定远程分支.


#### 3. 一般使用

1. 对项目文件夹里面的东西进行修改或者新增
```
`git add <path>` 把<path>添加到索引库（<path>可以是文件也可以是目录）
`git add -A` 提交所有变化
`git add -u` 提交被修改(modified)和被删除(deleted)文件,不包括新文件(new)
`git add .` 提交新文件(new)和被修改(modified)文件,不包括被删除(deleted)文件
`git status` 可以时刻看见仓库状态,有什么文件被修改被删除等等...
```

2. 代码提交
```
git commit -m "my commit message"
git push
```

3. pull和push

当我们执行 git pull 的时候, 实际上是做了 git fetch + git merge 操作, fetch 操作将会更新本地仓库的 remote tracking, 也就是 refs/remotes 中的代码, 并不会对 refs/heads 中本地当前的代码造成影响.

当我们进行 pull 的第二个行为 merge 时, 对git来说,如果我们没有设定当前分支的 upstream, 它并不知道我们要合并哪个分支到当前分支,所以我们需要通过下面的代码指定当前分支的upstream:

git branch --set-upstream-to=origin/<branch> develop

或者

git push --set-upstream origin develop


4. 其他要注意的

查看当前配置
```
git config --system --list
git config --global --list
git config --local --list
设置参数:(也可以直接通过修改config文件来达到一样的效果.)
git config --global user.name "myname"
```

global 是在用户目录下面，一般建议改这个。System 和 Local 的不建议修改。

5. 分支的使用

```
查看分支: git branch 或者 git branch -a
这个是详细版，很强大，可以查看本地和远程的关系 git branch -vv

创建分支: git branch <name>

切换分支: git checkout <name>

创建+切换分支: git checkout -b <name>

合并<name>分支到当前分支: git merge <name>

删除分支: git branch -d <name>
```

#### 4. 其他事项

- 匿名提交

提交到Github的信息里面,邮箱和用户名其实可以可以随便填写的,如果是随便填写的话,就一般匹配不上头像和相对应的连接了,不过好处就是可以匿名提交.

- Git中的工作区(Working Directory)、暂存区(Stage)和历史记录区(History)
  - 工作区：在git管理下的正常目录都算是工作区。我们平时的编辑工作都是在工作区完成。
  - 暂存区：可以理解为一个临时区域。里面存放将要提交文件的快照。
  - 历史区：commit后，记录的归档。
  
```
+-----------------+              +-----------------+               +-----------------+
| Working         |              | Staging Area    |               | Commit History  |
| Directory       |              | (Index)         |               | (Repository)    |
+-----------------+              +-----------------+               +-----------------+
| File 1          |              | File 1          |               | Commit 1        |
| File 2          |   git add    | File 2          |  git commit   | Commit 2        |
| File 3          +------------->| File 3          +-------------->| Commit 3        |
| ...             |              | ...             |               | ...             |
| ...             |<-------------+ ...             |<--------------+ ...             |
| ...             | git checkout | ...             |   git reset   | ...             |
+-----------------+              +-----------------+               +-----------------+
(Draw by ChatGPT and modified by author)

```

- 代码回滚：git reset、git checkout和git revert区别和联系

git reset 改变指针指向的位置，向历史方向。

git checkout 提取目前的 HEAD 里面的文件，如果加了 -b 就是别的分支的 HEAD。

git revert 将历史当作未来，会产生新的内容，向未来走。



#### Git代理

Http 协议

```bash
git config --global http.proxy "http://127.0.0.1:8080"
git config --global https.proxy "http://127.0.0.1:8080"

或者
git config --global http.proxy "socks5://127.0.0.1:1080"
git config --global https.proxy "socks5://127.0.0.1:1080"

取消设置

git config --global --unset http.proxy
git config --global --unset https.proxy

只针对 github
git config --global http.https://github.com.proxy socks5://127.0.0.1:1080
git config --global --unset http.https://github.com.proxy
```

SSH 协议

修改 `~/.ssh/config` 文件，可以参考顶部的 config 文件

**结论**

一般情况下，用ssh 形式，如果网络实在不好，就用 ssh over https，最后再用普通的 https


#### unsafe repository 不安全目录问题

Started from Git version: 2.35.3

```
git config --global --add safe.directory *
```

>https://git-scm.com/docs/git-config/#Documentation/git-config.txt-safedirectory
```
These config entries specify Git-tracked directories that are considered safe even if they are owned by someone other than the current user. By default, Git will refuse to even parse a Git config of a repository owned by someone else, let alone run its hooks, and this config setting allows users to specify exceptions, e.g. for intentionally shared repositories (see the --shared option in git-init[1]).
```