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

```sh
proxy=socks5://127.0.0.1:1080 to ~/.curlrc
```

> [https://lencerf.github.io/post/2015-10-03-brew-with-a-socks5-proxy/]


## proxy and unproxy 命令

zsh 和 bash 的切换
```conf
# =================================================================
# Mac 代理自动化配置
# =================================================================

proxy() {
    # 1. 直接使用本机回环地址
    local host_ip="127.0.0.1"

    # 2. 设置环境变量 (端口 7777)
    export http_proxy="http://${host_ip}:7777"
    export https_proxy="http://${host_ip}:7777"
    export all_proxy="socks5://${host_ip}:7777"

    # 3. 同时配置 Git 代理 (如果你需要 Git 也走代理)
    git config --global http.proxy "http://${host_ip}:7777"
    git config --global https.proxy "http://${host_ip}:7777"

    # 4. 设置 NPM 代理配置 (持久化到 .npmrc)
    npm config set proxy "http://${host_ip}:7777"
    npm config set https-proxy "http://${host_ip}:7777"

    echo "✅ 代理已开启"
    echo "地址: ${host_ip}:7777"
}

unproxy() {
    # 1. 清除环境变量
    unset http_proxy
    unset https_proxy
    unset all_proxy

    # 2. 清除 Git 代理
    git config --global --unset http.proxy
    git config --global --unset https.proxy

    echo "❌ 代理已关闭"
}

# 测试代理状态的便捷命令
testproxy() {
    echo "正在测试连接 Google..."
    curl -I -L --connect-timeout 5 https://www.google.com
}
```

# fish shell 版本（将下面内容粘到 ~/.config/fish/config.fish 或单独的脚本中）

```shell
# =================================================================
# Mac 代理自动化配置
# =================================================================
function proxy
    # 1. 直接使用本机回环地址
    set -l host_ip "127.0.0.1"

    # 2. 设置环境变量（端口 7777）
    set -gx http_proxy "http://$host_ip:7777"
    set -gx https_proxy "http://$host_ip:7777"
    set -gx all_proxy "socks5://$host_ip:7777"

    # 3. 同时配置 Git 代理
    git config --global http.proxy "http://$host_ip:7777"
    git config --global https.proxy "http://$host_ip:7777"

    # 4. NPM 代理配置
    npm config set proxy "http://$host_ip:7777"
    npm config set https-proxy "http://$host_ip:7777"

    echo "✅ 代理已开启"
    echo "地址: $host_ip:7777"
end

function unproxy
    # 清除环境变量
    set -e http_proxy
    set -e https_proxy
    set -e all_proxy

    # 清除 Git 代理（忽略错误并静默输出）
    git config --global --unset http.proxy >/dev/null 2>&1; or true
    git config --global --unset https.proxy >/dev/null 2>&1; or true

    # 清除 NPM 代理（如果需要）
    npm config delete proxy 2>/dev/null; or true
    npm config delete https-proxy 2>/dev/null; or true

    echo "❌ 代理已关闭"
end

function testproxy
    echo "正在测试连接 Google..."
    curl -I -L --connect-timeout 5 https://www.google.com
end
```


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

```sh
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


## 手动下载和安装 iOS app

从 iTunes 12.7 开始已经将 app 从资料库里面去掉了，所以我们只能使用最后的能下载 app 的版本 12.6.5.3

这个版本的 iTunes 可以从 苹果的官网下载：
> https://support.apple.com/en-us/HT208079

苹果竟然将这个网页删除了，这个页面是给企业用户部署用的，这样都能删除。。。真实丧病。。。不过好在下面的链接还是能继续使用的。并且我还找到了一个新的网址用于下载历史版本的

https://www.theiphonewiki.com/wiki/ITunes

提取出来下载连接
> https://secure-appldnld.apple.com/itunes12/091-87819-20180912-69177170-B085-11E8-B6AB-C1D03409AD2A6/iTunes64Setup.exe
>
> 大小: 277744968 字节 (264 MiB)
>
> SHA256: 666DCC84D26EA7BA79228F744F9CAEAC1192A9F274A5E795CC9E9352D41D80F3
>
> SHA1: 7B317DA13C3D0E463F73C27123A69379C4DBFD9D


苹果其实提供了 mac 的，但是 mac 的没啥用，因为不支持最新的 mac os。所以使用 windows 的就行了。

安装好了以后，可以和以前的 iTunes 一样下载 ipa 文件。但是后来我发现这个版本的 iTunes 不能同步了，所以从 2020-01 开始的最新方法是这样的：

* 使用原生的 windows 或者在虚拟机里面安装好 windows
* 在 windows 里面安装 iTunes 12.6.5.3
* 登录账号并且下载 ipa
* 如果能直接同步的话最好，如果不能的话，用 win10 的宿主机，或者另外一个虚拟机，或者 mac 最新版。连接 ios 设备，然后将下载的 ipa 拖到展开 **设备** 后的左边栏里面，ipa 就自动安装好了。
* 也可以通过 xcode 安装。在 window -> Device and Simulators -> Devices -> Installed apps 这里，直接拖到这里就行。
  
之前没这么麻烦的，只不过现在苹果对于手动管理 app 支持度越来越低，高的越来越麻烦。而且随着时间推移，一旦 12.6.5.3 这个版本的也打不开 app 商店的话，就没有任何官方办法了。非官方的软件倒是有的，只不过我不太愿意使用，并且目前 iMazing 和 iTools 用起来也不方便。

Apple Configurator 2 也可以，不过我还没探索。
