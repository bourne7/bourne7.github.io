# Git 笔记

2019-02-02


## Git 工作区、暂存区和版本库

> [http://www.runoob.com/git/git-workspace-index-repo.html](http://www.runoob.com/git/git-workspace-index-repo.html)

我们先来理解下Git 工作区、暂存区和版本库概念

* 工作区：就是你在电脑里能看到的目录。
* 暂存区：英文叫stage, 或index。一般存放在 ".git目录下" 下的index文件（.git/index）中，所以我们把暂存区有时也叫作索引（index）。
* 版本库：工作区有一个隐藏目录.git，这个不算工作区，而是Git的版本库。

  下面这个图展示了工作区、版本库中的暂存区和版本库之间的关系：

![git-working-stage-repository-picture-1.jpg](git-working-stage-repository-picture-1.jpg)

图中左侧为工作区，右侧为版本库。在版本库中标记为 "index" 的区域是暂存区（stage, index），标记为 "master" 的是 master 分支所代表的目录树。

图中我们可以看出此时 "HEAD" 实际是指向 master 分支的一个"游标"。所以图示的命令中出现 HEAD 的地方可以用 master 来替换。

图中的 objects 标识的区域为 Git 的对象库，实际位于 ".git/objects" 目录下，里面包含了创建的各种对象及内容。

当对工作区修改（或新增）的文件执行 "git add" 命令时，暂存区的目录树被更新，同时工作区修改（或新增）的文件内容被写入到对象库中的一个新的对象中，而该对象的ID被记录在暂存区的文件索引中。

当执行提交操作（git commit）时，暂存区的目录树写到版本库（对象库）中，master 分支会做相应的更新。即 master 指向的目录树就是提交时暂存区的目录树。

当执行 "git reset HEAD" 命令时，暂存区的目录树会被重写，被 master 分支指向的目录树所替换，但是工作区不受影响。

当执行 "git rm --cached \" 命令时，会直接从暂存区删除文件，工作区则不做出改变。

当执行 "git checkout ." 或者 "git checkout -- \" 命令时，会用暂存区全部或指定的文件替换工作区的文件。这个操作很危险，会清除工作区中未添加到暂存区的改动。

当执行 "git checkout HEAD ." 或者 "git checkout HEAD \" 命令时，会用 HEAD 指向的 master 分支中的全部或者部分文件替换暂存区和以及工作区中的文件。这个命令也是极具危险性的，因为不但会清除工作区中未提交的改动，也会清除暂存区中未提交的改动。

## Http 协议（建议使用）

```sh
设置
git config --global http.proxy "socks5://127.0.0.1:7777"

取消设置
git config --global --unset http.proxy

只针对 github
git config --global http.https://github.com.proxy socks5://127.0.0.1:7777
取消
git config --global --unset http.https://github.com.proxy
```

针对 Http 协议，建议使用 access token 来获取访问权限，比如可以用 intellij 来生成一个 classic token，然后共享给全局用。

* Window：登录信息会储存在 Control Panel\All Control Panel Items\Credential Manager 里面。
* Intellij：储存在 ide 内部

如果在intellij 里面使用了网页登陆 github，那么保存的不是 token，而是密码。这个密码也可以选择保存的地方。不过不建议使用这种方式，以为要撤销的话，只能通过改密码来解决。

用 token 的好处就是可以方便的管理权限，比 ssh 要灵活很多。

此外，可以在 https://api.github.com/users/bourne7 看到自己的信息，里面的 id 是真实的账号 id。

## SSH 协议（不建议使用）

修改 `~/.ssh/config` 文件

在 ~/.ssh 文件夹里面新建一个 config 文件，内容如下：
```sh
# 这里只是个 alias，用于命令行
Host aaa
    User git
    Port 22
    # 真正的git远程连接
    HostName github.com
    PreferredAuthentications publickey
    TCPKeepAlive yes
    IdentityFile ~/.ssh/aaa_id_rsa

# Host github.com
#   User git
#   Port 22
#   HostName github.com
#   IdentityFile ~/.ssh/github
#   TCPKeepAlive yes
#   ProxyCommand "C:\Program Files\Git\mingw64\bin\connect" -S 127.0.0.1:7777 -a none %h %p

# Host ssh.github.com
#   User git
#   Port 443
#   Hostname ssh.github.com
#   IdentityFile ~/.ssh/github
#   TCPKeepAlive yes
#   ProxyCommand "C:\Program Files\Git\mingw64\bin\connect" -S 127.0.0.1:7777 -a none %h %p
```

## 全局配置样例 .gitconfig

```conf
[user]
	name = bourne7
	email = xxx
# 上面的配置会作为默认配置，下面的配置会只针对包含该路径的子文件夹。可以方便的配置出2套不同的用户名，而不用去修改每一个 git 目录。
[includeIf "gitdir/i:my-projects/"]
	path = .gitconfig-my-projects
[filter "lfs"]
	clean = git-lfs clean -- %f
	smudge = git-lfs smudge -- %f
	process = git-lfs filter-process
	required = true
[init]
	defaultBranch = master
[safe]
	directory = *
[http "https://github.com"]
	proxy = socks5://127.0.0.1:7777
```

## git remote

目前有3种 clone 的方式，分别是 http, ssh, git。比较方便的还是 https。

```
//查看当前的仓库连接方式
git remote -v
git remote show
git remote show origin

//然后删除当前的方式
git remote rm origin

// 然后添加新的仓库方式
git remote add origin git@github.com:myaccount/cocos2d-x.git
```

> 新仓库可能会遇到的问题：upstream到底是什么？

git中存在upstream和downstream, 简言之,当我们把仓库A中某分支x的代码push到仓库B分支y, 此时仓库B的这个分支y就叫做A中x分支的upstream, 而x则被称作y的downstream, 这是一个相对关系, 每一个本地分支都相对地可以有一个远程的upstream分支（注意这个upstream分支可以不同名, 但通常我们都会使用同名分支作为upstream）.

初次提交本地分支,例如 
```sh
git push origin develop 
```

操作, 并不会定义当前本地分支的upstream分支, 我们可以通过
```sh
git branch --set-upstream-to=origin/<branch> develop
或者
git push --set-upstream origin develop
```

关联本地develop分支的upstream分支,另一个更为简洁的方式是初次push时,加入-u参数,例如
```sh
git push -u origin develop
```

这个操作在push的同时会指定当前分支的upstream。注意：
```sh
push.default = current
```
可以在远程同名分支不存在的情况下自动创建同名分支,有些时候这也是个极其方便的模式,比如初次push你可以直接输入 git push 而不必显示指定远程分支.

## git reset git checkout 

当前分支下, 如果编辑了文件, 但是需要撤销自己的所有编辑, 回到当前分支的状态的时候, 可以使用以下2种都可以:

```sh
git reset --hard HEAD 1.txt
git reset --hard HEAD~1
git checkout 1.txt
```

reset 命令后面有几种参数如下：

* soft 将现有的改动保存到暂存区
* mix 将现有的改动保存到工作区
* hard 放弃现在的工作区和暂存区里面的所有改动

注意使用 reset 的时候，要确认好当前的HEAD指向哪里，当前是否有未commit的内容。

## config

global 是在用户目录下面，一般建议改这个。System 和 Local 的不建议修改。

```sh
git config --list
git config --list --system
git config --list --global
git config --list --local
设置参数:(也可以直接通过修改config文件来达到一样的效果.)
git config --global user.name "myname"
git config --global user.email "aaa@aaa.com"
```

## git diff

直接使用 git diff 是比较当前工作区和 add 到缓存区的文件之间的区别。

## git add

下面这3个命令在不同的Git里面有不同的意思，这里选用新的2.X的作为说明。

```sh
git add <path> 把<path>添加到索引库（<path>可以是文件也可以是目录）
git add -A 提交所有变化
git add -u 提交被修改(modified)和被删除(deleted)文件,不包括新文件(new)
git add . 提交新文件(new)和被修改(modified)文件,不包括被删除(deleted)文件
git status 可以时刻看见仓库状态,有什么文件被修改被删除等等...
```

## git rm

```sh
git rm file_name
```

从工作区和暂存区删除，这样提交以后，会彻底删除这个文件。

```sh
git rm --cached file_name
```

从暂存区删除，但是工作区还是存在的，这时候还可以再用add添加回去暂存区。

## git bisect

好用的二分法来查找某个特定的 commit ，比如当代码被人弄坏了以后，想找到最后一个能用的commit。

```sh
git bisect start
git bisect good xxxxxx
git bisect bad xxxxxx
git bisect bad
git bisect good
git bisect good
(...)
git bisect reset
```

## 本地新建分支然后推送到远程

推送本地的 new\_feature \(冒号前面的\) 分支到远程origin的 new\_feature \(冒号后面的\) 分支，如果远程没有的话会自动创建。一般来说，最好要保持这2个分支名称一样。

git checkout -b new\_feature git push origin new\_feature:new\_feature

## Git 版本问题

在 cicd 的过程中，需要获取提交的 commitID 和 branch name，搜索到的结果如下：

> https://stackoverflow.com/questions/6245570/how-to-get-the-current-branch-name-in-git

If you want to retrieve only the name of the branch you are on, you can do:
```
git rev-parse --abbrev-ref HEAD
```
or with Git 2.22 and above:
```
git branch --show-current
```

我在我本地是可以正常的跑 gradle 脚本的，也能正常获取，但就是在服务器上面不行，我看到这里的回答有说到版本22以后才有后面的指令，那么会不会上面的指令也有版本限制呢？我挖了以下cicd服务器的git，版本只有17。

实际上又遇到了其他问题：

> https://stackoverflow.com/questions/47098342/jenkinsfile-git-rev-parse-abbrev-ref-head-returns-head

这个哥们遇到了一样的问题，我想可能是git使用方式的问题，然后通过远端的 git branch 以后，发现竟然是个 detached HEAD 。在不修改 cicd 的配置和拉取方式的情况下，只能使用 branch 来获取分支号了，指令如下：

> https://stackoverflow.com/questions/13624774/how-to-i-read-the-second-line-of-the-output-of-a-command-into-a-bash-variable

```
git branch | sed -n 2p
```

后来又找到一个比较复杂的写法，但是这个提出来的人自己都觉得这么做有点过于麻烦。

> https://stackoverflow.com/questions/6059336/how-to-find-the-current-git-branch-in-detached-head-state

```
git show-ref | grep $(git log --pretty=%h -1) | sed 's|.*/\(.*\)|\1|' | sort -u | grep -v HEAD
```

所以在这个提问里面，有人提出了下面2条：

```
git log -n 1 --pretty=%d HEAD

git show -s --pretty=%d HEAD
```

然后我在这里找到了关于 pretty 的一些格式化的参数。

https://git-scm.com/docs/pretty-formats

所以我最后采用了

```
git log -n 1 --pretty='%d %ai'
```

## Oneline and pretty

git log -a --pretty=format:"%h%x09%an%x09%ad%x09%s"

## 双作者：作者后面的星号 asterisk after author

> https://stackoverflow.com/questions/44625270/intellij-idea-asterisk-after-authors-name-in-git-log

Every change in GIT (and in the most of modern VCS's) has an author and a committer. The Log shows an author because we respect authorship even if the author of changes doesn't have access to the repo or isn't able to commit code by himself.

Asterisk on the author's name in the Log means that this commit was created by the described person, but was applied by someone else.

There are some common cases when this happens:

* you cherrypicked someone else's commit
* you rebased branch with someone else's commits
* you applied .patch file mailed to you by someone else
* you merged the pull-request via GitHub UI - GitHub does it with its own user but leaves authorship to you.

Use
```
git log your_hash --pretty=full
```
to show both author names


## unsafe repository 不安全目录问题

Started from Git version: 2.35.3

```
git config --global --add safe.directory *
```

>https://git-scm.com/docs/git-config/#Documentation/git-config.txt-safedirectory
```
These config entries specify Git-tracked directories that are considered safe even if they are owned by someone other than the current user. By default, Git will refuse to even parse a Git config of a repository owned by someone else, let alone run its hooks, and this config setting allows users to specify exceptions, e.g. for intentionally shared repositories (see the --shared option in git-init[1]).
```


## Git history simplification

> https://docs.microsoft.com/en-us/azure/devops/repos/git/git-log-history-simplification?view=azure-devops

> https://stackoverflow.com/questions/56553346/git-log-missing-merge-commit-that-undid-a-change

Understand Git history simplification

The thing about history simplification is that most of the time you will never notice it. But when a merge conflict goes wrong and you want to know what happened -- you may find yourself looking at the git log history and wondering where your changes went.

Now, instead of panicking, you know that:

History simplification for files is turned on by default
The --full-history flag will give you a more comprehensive file history

## Other optional method to view modified parts

full command:
```sh
git log -p -m file.txt
```

```
--diff-merges=m
-m
```
This option makes diff output for merge commits to be shown in the default format. -m will produce the output only if -p is given as well. The default format could be changed using log.diffMerges configuration parameter, which default value is separate.


```
--diff-merges=combined
--diff-merges=c
-c
```
With this option, diff output for a merge commit shows the differences from each of the parents to the merge result simultaneously instead of showing pairwise diff between a parent and the result one at a time. Furthermore, it lists only files which were modified from all parents. -c implies -p.

```
--diff-merges=dense-combined
--diff-merges=cc
--cc
```
With this option the output produced by --diff-merges=combined is further compressed by omitting uninteresting hunks whose contents in the parents have only two variants and the merge result picks one of them without modification. --cc implies -p