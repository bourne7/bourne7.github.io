# Mac使用笔记

2019-02-02

## brew 和 代理

在 .zshrc 里面添加如下内容：

```
alias proxy='export http_proxy=127.0.0.1:1080;export https_proxy=$http_proxy;export all_proxy=$http_proxy'

alias unproxy='unset http_proxy;unset https_proxy;unset all_proxy'

# 安装好以后，会提醒 brew 没有加入 Path，同样加入这句

export PATH=/opt/homebrew/bin:$PATH 
```

如果需要养 curl 走代理，可以用这个：

```text
proxy=socks5://127.0.0.1:1080 to ~/.curlrc
```

> [https://lencerf.github.io/post/2015-10-03-brew-with-a-socks5-proxy/]

## Brew 笔记

https://cloud.tencent.com/developer/article/1867824
```
brew update               自动升级homebrew（从github下载最新版本）
brew outdated             检测已经过时的软件
brew upgrade              升级所有已过时的软件，即列出的以过时软件
brew upgrade <formula>    升级指定的软件
brew pin <formula>        禁止指定软件升级
brew unpin <formula>      解锁禁止升级
brew upgrade --all        升级所有的软件包，包括未清理干净的旧版本的包
brew cleanup -n           列出需要清理的内容
brew cleanup <formula>    清理指定的软件过时包
brew cleanup              清理所有的过时软件
brew uninstall <formula>    卸载指定软件
brew uninstall <fromula> --force 彻底卸载指定软件，包括旧版本
brew list                 显示所有的已安装的软件
brew search text          搜索本地远程仓库的软件，已安装会显示绿色的勾
brew search /text/        使用正则表达式搜软件

安装homebrew
打开终端，复制以下代码到终端，按回车即可：

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

homebrew可以安装很多类型的软件：

 终端使用的软件，比如oh my zsh等；
 
 编程使用的各种依赖环境，比如python 3.6,java1.8，mysql等；
 
 带有GUI的软件，比如wechat，vs code等。
 
对于第1和第2类软件，安装命令为： brew install app_name，卸载命令为：brew uninstall app_name,

对于第3类软件，安装命令为： brew install --cask app_name，卸载命令为：brew uninstall --cask app_name,

比如想安装atom怎么办？一行命令：

brew install --cask atom

如果想卸载了呢？一行命令：

brew uninstall --cask atom

通过看brew的帮助手册可以得知，uninstall、rm、remove三者的作用都是一样的。
 
 再次试一试。比如安装chrome：

首先搜索chrome：

brew search chrome
 
 这时候会看到有很多的与chrome相关的程序。比如chrome-devtools，epichrome，google-chrome等。


这时候下载并安装chrome：

brew install --cask google-chrome

等待安装成功即可！

Cask
到此为止学会了 Homebrew Cask 的一些基本用法，但你可能会奇怪：不是叫 Homebrew 吗，Cask 是什么？

其实 Homebrew Cask 是 Homebrew 附带的、用来安装和管理 GUI 应用软件的工具，也就是通常有一个窗口、一些按钮的这样的应用。而 Homebrew 是用于和它本身一样在终端使用的命令行软件的。我们只需要知道，除了在终端使用的软件，其他的软件都用 Cask 来管理就对了。
```

## Python

Mac自带的 Python3 路径在 /usr/bin/python3

Brew安装的在 /usr/local/Cellar/

查看python路径的两种方法：

```text
which python3

import sys
print(sys.path)
```

## Intellij

- 如果使用Intellij的时候,需要使用自己安装的gradle,需要在后面加一个 libexec:
`/usr/local/Cellar/gradle/4.7/libexec`


## Switch SD card

```
sudo chflags -R arch /Volumes/SDCARD_NAME
```

## Xcode
xcode-select --install


## java jdk

M系列芯片可以原生安装 open jdk 17，可以使用 brew 安装，安装好了以后，可以看到下面的提示

```
For the system Java wrappers to find this JDK, symlink it with
  sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-17.jdk

openjdk@17 is keg-only, which means it was not symlinked into /opt/homebrew,
because this is an alternate version of another formula.

If you need to have openjdk@17 first in your PATH, run:
  echo 'export PATH="/opt/homebrew/opt/openjdk@17/bin:$PATH"' >> ~/.zshrc

For compilers to find openjdk@17 you may need to set:
  export CPPFLAGS="-I/opt/homebrew/opt/openjdk@17/include"
```

然后可以在系统里面找到2个JDK
```
aac@Lawrences-MacBook-Pro bin % /usr/libexec/java_home -V
Matching Java Virtual Machines (2):
    21 (arm64) "JetBrains s.r.o." - "JBR-21+9-126.4-nomod 21" /Users/aac/Library/Java/JavaVirtualMachines/jbr-21/Contents/Home
    17.0.7 (arm64) "Homebrew" - "OpenJDK 17.0.7" /opt/homebrew/Cellar/openjdk@17/17.0.7/libexec/openjdk.jdk/Contents/Home
/Users/aac/Library/Java/JavaVirtualMachines/jbr-21/Contents/Home
```

如果需要手动安装的话，可以下载 zip 包，然后解压到

/Library/Java/JavaVirtualMachines

就可以被 ide 自动识别了。PATH 也可以设置一下 alias

到 2023-07-15 为止， termurin（openjdk）8 不支持 M系列芯片，支持的主要有 amazon 和 zulu，所以我选择了都用 zulu 的，但是我发现 brew 里面没有 zulu 的cmd 版本的，只有 Cask 的，所以我选择了手动安装 zulu 的 8 和 17 版本的 jdk。

