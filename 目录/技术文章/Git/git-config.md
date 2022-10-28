### Git 笔记

#### 1.创建SSH秘钥
` ssh-keygen -t rsa -C "test@youremail.com" `
使用
` ssh -T git@github.com `
验证一下.如果是在同一个电脑上面,同时使用多个账号的话,可以参考下面的教程:
> https://blog.csdn.net/wangpingfang/article/details/53117087

假定两个公钥创建完后为:
`    ~/.ssh/id_rsa_work`
`    ~/.ssh/id_rsa_personal`
将新建的公钥分别添加到公司github账号和个人github账号

修改~/.ssh/config以添加多个ssh配置

```config
# Work GitHub
Host github.com
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa_work

# Personal GitHub
Host personal.github.com # 这个网址是随便写的.不过要和项目的对应网址一致.
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa_personal
```

测试配置,使用如下命令,检查之前的配置是否正确:

    $ ssh -T git@github.com
    Hi pwang08! You've successfully authenticated, but GitHub does not provide shell access.
    $ ssh -T git@personal.github.com
    Hi Turalyonx! You've successfully authenticated, but GitHub does not provide shell access.

试一下不同的项目.对于公司账号的项目,git使用跟之前没有任何区别,因为公司账号是默认账号.但是对于个人账户下的项目,假设其ssh链接为:（这个是从github主页上复制的连接.）
    `git@github.com:myaccount/cocos2d-x.git`
如果我们直接执行
    `git clone git@github.com:myaccount/cocos2d-x.git`
git会根据 `~/.ssh/config` 配置下的 Host 去寻找授权信息,注意到这里的Host为 `github.com` ,所以git就会使用~/.ssh/id_rsa_work进行授权,因为匹配到了上面的 `~/.ssh/config` 里面的 Word.最终授权就会失败.那么如何才能让git去找到正确的授权信息呢?只需要把项目链接
    `git@github.com:myaccount/cocos2d-x.git`
修改成
    `git@personal.github.com:myaccount/cocos2d-x.git`
即可.现在git就会根据`personal.github.com`找到`~/.ssh/id_rsa_personal`,并使用其作为授权文件.

#### 2. Clone项目
`git clone git@github.com:myaccount/cocos2d-x.git`
`git clone https://github.com/myaccount/cocos2d-x.git`

这2条都行,但是如果使用了ssh的话,就要用第一个,这样可以不用输入账号密码,缺点是可能有些网络有限制.(比如屏蔽了22端口.)
如果本来使用的 https 的话,就要改一下远程仓库连接:
先查看当前的仓库连接方式:
`git remote -v`
然后删除当前的方式
`git remote rm origin`
然后添加新的仓库方式
`git remote add origin git@github.com:myaccount/cocos2d-x.git`
再次查看当前的仓库连接方式 
`git remote -v`

当然，也可以直接通过修改config文件来达到一样的效果。

>https://segmentfault.com/a/1190000002783245
说到这里,需要解释一下git中的upstream到底是什么:
git中存在upstream和downstream,简言之,当我们把仓库A中某分支x的代码push到仓库B分支y,此时仓库B的这个分支y就叫做A中x分支的upstream,而x则被称作y的downstream,这是一个相对关系,每一个本地分支都相对地可以有一个远程的upstream分支（注意这个upstream分支可以不同名,但通常我们都会使用同名分支作为upstream）.
初次提交本地分支,例如git push origin develop操作,并不会定义当前本地分支的upstream分支,我们可以通过
git push --set-upstream origin develop
关联本地develop分支的upstream分支,另一个更为简洁的方式是初次push时,加入-u参数,例如
git push -u origin develop
这个操作在push的同时会指定当前分支的upstream.
注意
push.default = current
可以在远程同名分支不存在的情况下自动创建同名分支,有些时候这也是个极其方便的模式,比如初次push你可以直接输入 git push 而不必显示指定远程分支.

查看远程仓库信息. 我们可以通过命令 
`git remote show [remote-name] `
查看某个远程仓库的详细信息，比如要看所克隆的 origin 仓库，可以运行：
`git remote show origin`

#### 3.正常使用
1. 对项目文件夹里面的东西进行修改或者新增
`git add <path>` 把<path>添加到索引库（<path>可以是文件也可以是目录）
`git add -A` 提交所有变化
`git add -u` 提交被修改(modified)和被删除(deleted)文件,不包括新文件(new)
`git add .` 提交新文件(new)和被修改(modified)文件,不包括被删除(deleted)文件
`git status` 可以时刻看见仓库状态,有什么文件被修改被删除等等...

2. 代码提交
`git commit -m "my commit message"`

3. pull和push
`pull = fetch + merge`
>详解git pull.
当我们未指定当前分支的upstream时,通常git pull操作会得到如下的提示:
There is no tracking information for the current branch.
Please specify which branch you want to merge with.
See git-pull(1) for details
git pull <remote> <branch>
If you wish to set tracking information for this branch you can do so with:
git branch --set-upstream-to=origin/<branch> new1
git pull的默认行为和git push完全不同.当我们执行git pull的时候,实际上是做了git fetch + git merge操作,fetch操作将会更新本地仓库的remote tracking,也就是refs/remotes中的代码,并不会对refs/heads中本地当前的代码造成影响.
当我们进行pull的第二个行为merge时,对git来说,如果我们没有设定当前分支的upstream,它并不知道我们要合并哪个分支到当前分支,所以我们需要通过下面的代码指定当前分支的upstream:
git branch --set-upstream-to=origin/<branch> develop
// 或者git push --set-upstream origin develop
实际上,如果我们没有指定upstream,git在merge时会访问git config中当前分支(develop)merge的默认配置,我们可以通过配置下面的内容指定某个分支的默认merge操作
[branch "develop"]
remote = origin
merge = refs/heads/develop // [1]为什么不是refs/remotes/develop?
或者通过command-line直接设置:
git config branch.develop.merge refs/heads/develop
这样当我们在develop分支git pull时,如果没有指定upstream分支,git将根据我们的config文件去merge origin/develop；如果指定了upstream分支,则会忽略config中的merge默认配置.
以上就是git push和git pull操作的全部默认行为,如有错误,欢迎斧正


#### 4.其他要注意的

- **查看当前配置**
`git config --system --list`
`git config --global --list`
`git config --local --list`
设置参数:(也可以直接通过修改config文件来达到一样的效果.)
`git config --global user.name "myname"`

- **分支的使用**
  `https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001375840038939c291467cc7c747b1810aab2fb8863508000`
Git鼓励大量使用分支:
查看分支:git branch 或者 git branch -a
创建分支:git branch <name>
切换分支:git checkout <name>
创建+切换分支:git checkout -b <name>
合并<name>分支到当前分支:git merge <name>
删除分支:git branch -d <name>
git branch -vv 查看设置的所有跟踪分支，可以使用 git branch 的 -vv 选项。 这会将所有的本地分支列出来并且包含更多的信息，如每一个分支正在跟踪哪个远程分支与本地分支是否是领先、落后或是都有。https://blog.csdn.net/kjunchen/article/details/52155055

- **匿名提交**
    提交到Github的信息里面,邮箱和用户名其实可以可以随便填写的,如果是随便填写的话,就一般匹配不上头像和相对应的连接了,不过好处就是可以匿名提交.

- **Git中的工作区(Working Directory)、暂存区(stage)和历史记录区(history)**
  https://www.cnblogs.com/Phantom01/p/6295060.html
    - 工作区：在git管理下的正常目录都算是工作区。我们平时的编辑工作都是在工作区完成。
    - 暂存区：可以理解为一个临时区域。里面存放将要提交文件的快照。
    - 历史区：commit后，记录的归档。
  简单来说,就是完全新建的文件就是放在 工作区 的. Add以后就去到了 暂存区. Commit以后就是历史区.

- 代码回滚：git reset、git checkout和git revert区别和联系
  https://www.cnblogs.com/houpeiyong/p/5890748.html
  这个网页总结的很好.

| 命令         | 作用域   | 常用情景                           |
| ------------ | -------- | ---------------------------------- |
| git reset    | 提交层面 | 在私有分支上舍弃一些没有提交的更改 |
| git reset    | 文件层面 | 将文件从缓存区中移除               |
| git checkout | 提交层面 | 切换分支或查看旧版本               |
| git checkout | 文件层面 | 舍弃工作目录中的更改               |
| git revert   | 提交层面 | 在公共分支上回滚更改               |
| git revert   | 文件层面 | （然而并没有）                     |


#### 5.设置代理

#只对github.com
git config --global http.https://github.com.proxy socks5://127.0.0.1:1080

#取消代理
git config --global --unset http.https://github.com.proxy



# Git代理设置


### 走 HTTP 代理

```bash
git config --global http.proxy "http://127.0.0.1:8080"
git config --global https.proxy "http://127.0.0.1:8080"
```

### 走 socks5 代理（如 Shadowsocks）

```bash
git config --global http.proxy "socks5://127.0.0.1:1080"
git config --global https.proxy "socks5://127.0.0.1:1080"
```

只针对 github
```bash
git config --global http.https://github.com.proxy socks5://127.0.0.1:1080
```

### 取消设置

```bash
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## 二、SSH 形式

修改 `~/.ssh/config` 文件（不存在则新建）：

```
# 必须是 github.com
Host github.com
   HostName github.com
   User git
   # 走 HTTP 代理
   # ProxyCommand socat - PROXY:127.0.0.1:%h:%p,proxyport=8080
   # 走 socks5 代理（如 Shadowsocks）
   # ProxyCommand nc -v -x 127.0.0.1:1080 %h %p
```

.ssh/config 配置模板
```yml
# gitlab
Host gitlab.test.com
    HostName 172.16.1.13
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/gitlab_rsa
    Port 2222
 
# github
Host github.com
	# ProxyCommand "C:/Program Files/Git/mingw64/bin/connect.exe" -S 127.0.0.1:1080 -a none %h %p
    HostName github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa
    # 这里的 -a none 是 NO-AUTH 模式，参见 https://bitbucket.org/gotoh/connect/wiki/Home 中的 More detail 一节
    # 首先明确一点：connect.exe 已经在 Git 中预置了，无需再次下载安装。https://upupming.site/2019/05/09/git-ssh-socks-proxy/
    # ProxyCommand "C:/Program Files/Git/mingw64/bin/connect.exe" -S 127.0.0.1:1080 -a none %h %p
    ProxyCommand connect -S 127.0.0.1:1080 -a none %h %p

Host aa
    # bash <(curl -s -L https://git.io/ss.sh)
    HostName 157.245.227.212
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/id_rsa
```

下面是另外一种配置
```yml
# ProxyCommand "C:\Program Files\Git\mingw64\bin\connect" -S 127.0.0.1:1080 -a none %h %p

Host github.com
  User git
  Port 22
  Hostname github.com
  IdentityFile ~/.ssh/github
  TCPKeepAlive yes

Host ssh.github.com
  User git
  Port 443
  Hostname ssh.github.com
  IdentityFile ~/.ssh/github
  TCPKeepAlive yes
```

#### unsafe repository 不安全目录问题

Started from Git version: 2.35.3

```
git config --global --add safe.directory *
```
or config in ~/.gitconfig

>https://git-scm.com/docs/git-config/#Documentation/git-config.txt-safedirectory
```
These config entries specify Git-tracked directories that are considered safe even if they are owned by someone other than the current user. By default, Git will refuse to even parse a Git config of a repository owned by someone else, let alone run its hooks, and this config setting allows users to specify exceptions, e.g. for intentionally shared repositories (see the --shared option in git-init[1]).
```