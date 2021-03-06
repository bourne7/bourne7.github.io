# Git 笔记

2019-02-02

## 0. 配置 SSH

下面是配置多个账号的方法：

```
ssh-keygen -t rsa -C "aaa@gmail.com"

这里需要输入生成 的 RSA 公钥密钥对，名称叫做
aaa_id_rsa
aaa_id_rsa.pub
```
接着生成第二个账号的：

```
ssh-keygen -t rsa -C "bbb@gmail.com"

这里需要输入生成 的 RSA 公钥密钥对，名称叫做
bbb_id_rsa
bbb_id_rsa.pub
```

在 ~/.ssh 文件夹里面，现在新增了上面4个文件了，需要新建一个 config 文件，内容如下：
```
# aaa git
# 这里就是以后要匹配的git，用于命令输入，如果需要保持和github原本的一样的话，这里可以写 git@github.com
Host git_aaa
    # 真正的git远程连接
    HostName https://github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/aaa_id_rsa
 
# bbb git
Host git_bbb
    # 这里可以写任意的地址，比如公司搭建的git仓库
    HostName https://github.com
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/bbb_id_rsa
```

## 1. git reset

当前分支下, 如果编辑了文件, 但是需要撤销自己的所有编辑, 回到当前分支的状态的时候, 可以使用以下2种都可以:

```text
git reset --hard HEAD 1.txt
git reset --hard HEAD~1
git checkout 1.txt
```

reset 命令后面有几种参数如下：

* soft 将现有的改动保存到暂存区
* mix 将现有的改动保存到工作区
* hard 放弃现在的工作区和暂存区里面的所有改动

注意使用 reset 的时候，要确认好当前的HEAD指向哪里，当前是否有未commit的内容。

**关于消失的commit**

reset 到之前的某一个 commit A 以后, 如果在 commit A 这里又重新commit了其他的内容, 那么原有的 commit A 以后的那些 commit 就都会在 git log 里面消失, 但是会在 ref log 里面保留. 所以在push 到远端以后, 别人如果下载下来以后, 会见不到这部分的内容了. 如果需要做到将所有的内容都放到git里面去的话, 建议在 commit A 这里新拉出来一个分支来改动会好很多, 这样会保留所有的操作痕迹.

## 2. config

查看所有的配置: 这里建议将 list写在前面, 是为了方便改后面的这个参数

```text
git config --list
git config --list --system
git config --list --global
git config --list --local
```

## 3. git diff

直接使用 git diff 是比较当前工作区和 add 到缓存区的文件之间的区别。

## 4. git add

下面这3个命令在不同的Git里面有不同的意思，这里选用新的2.X的作为说明。

```text
git add -A（添加左右的文件，包括增加的，修改的，和删除的）
git add .（和上面的一样）
git add -u（和上面的一样，但是不包括新增的）
```

基本上使用第二条只最方便的了。

## 5. git log

```text
git log -5
```

查看最近3次的提交

## 6. git rm

```text
git rm file_name
```

从工作区和暂存区删除，这样提交以后，会彻底删除这个文件。

```text
git rm --cached file_name
```

从暂存区删除，但是工作区还是存在的，这时候还可以再用add添加回去暂存区。

## 7. git bisect

好用的二分法来查找某个特定的 commit ，比如当代码被人弄坏了以后，想找到最后一个能用的commit。

```text
git bisect start
git bisect good xxxxxx
git bisect bad xxxxxx
git bisect bad
git bisect good
git bisect good
(...)
git bisect reset
```

## 8. 本地新建分支然后推送到远程

推送本地的 new\_feature \(冒号前面的\) 分支到远程origin的 new\_feature \(冒号后面的\) 分支，如果远程没有的话会自动创建。一般来说，最好要保持这2个分支名称一样。

git checkout -b new\_feature git push origin new\_feature:new\_feature

## 9. 设置代理
```
git config --global http.proxy 'socks5://127.0.0.1:1080'
git config --global https.proxy 'socks5://127.0.0.1:1080'

git config --global --unset http.proxy
git config --global --unset https.proxy
```