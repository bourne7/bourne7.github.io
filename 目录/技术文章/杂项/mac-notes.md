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

```bash
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

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Python

Mac自带的 Python3 路径在 /usr/bin/python3

Brew安装的在 /usr/local/Cellar/

查看python路径的两种方法：

```bash
whereis python3
python3: /usr/bin/python3

where python3
/usr/bin/python3

which -a python3 
/usr/bin/python3

which python3
/usr/bin/python3

import sys
print(sys.path)
```


## Switch SD card

```
sudo chflags -R arch /Volumes/SDCARD_NAME
```

## Xcode
xcode-select --install


## java jdk


1. brew 安装（这个主要用于环境变量）
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

然后可以在系统里面找到多个JDK
```
aac@MacBook-Pro ~/L/J/JavaVirtualMachines> /usr/libexec/java_home -V
Matching Java Virtual Machines (4):
    21.0.3 (arm64) "Amazon.com Inc." - "Amazon Corretto 21" /Users/aac/Library/Java/JavaVirtualMachines/21/Contents/Home
    21.0.3 (arm64) "Amazon.com Inc." - "Amazon Corretto 21" /Users/aac/Library/Java/JavaVirtualMachines/corretto-21.0.3/Contents/Home
    17.0.11 (arm64) "Homebrew" - "OpenJDK 17.0.11" /opt/homebrew/Cellar/openjdk@17/17.0.11/libexec/openjdk.jdk/Contents/Home
    1.8.0_402 (arm64) "Amazon" - "Amazon Corretto 8" /Users/aac/Library/Java/JavaVirtualMachines/corretto-1.8.0_402/Contents/Home
/Users/aac/Library/Java/JavaVirtualMachines/21/Contents/Home
```


2. intellij 安装（这个主要用于开发）

直接使用 ide 来下载，默认路径是

/Users/aac/Library/Java/JavaVirtualMachines/

3. 手动下载（不建议）

如果需要手动安装的话，可以下载 zip 包，然后解压到

/Library/Java/JavaVirtualMachines

就可以被 ide 自动识别了。PATH 也可以设置一下 alias
