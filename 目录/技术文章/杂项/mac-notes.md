# Mac使用笔记

2019-02-02

## Python

Mac自带的 Python2，路径为 /System/Library/Frameworks/Python.framework/Versions/2.6

Brew安装的在 /usr/local/Cellar/

查看python路径的两种方法：

```text
which python3

import sys
print(sys.path)
```

建议将第三方板安装到系统全局，这样不用以后重复安装。尤其是在使用 pycharm 的时候。

## brew

Finally, I find the right way to use homebrew. 1. Let http requests of git go through a socks5 proxy

```text
git config --global http.proxy 'socks5://127.0.0.1:1081'
```

1. Since homebrew doanloads files using curl, set a socks proxy for curl: just add 

   ```text
   proxy=socks5://127.0.0.1:1081 to ~/.curlrc.
   ```

> [https://lencerf.github.io/post/2015-10-03-brew-with-a-socks5-proxy/](https://lencerf.github.io/post/2015-10-03-brew-with-a-socks5-proxy/)

brew是使用的是crul来下载的。https://www.logcg.com/archives/1617.html
所以可以指定下载的代理:
`export ALL_PROXY=socks5://127.0.0.1:1080`
如果说你想要 brew 永久如此，我们就需要将环境变量写入终端的配置当中，这取决于你的终端，如果是默认的 bash，则写入 `~/.bash_profile` ，如果是 zsh，则写在  `~/.zshrc`  里。
或者直接用如下语句来将命令直接导入到配置文件里，感谢 surveillance104 的提醒哦！
echo export ALL_PROXY=socks5://127.0.0.1:1080 >> ~/.bash_profile
//如果是zsh就下边这个
echo export ALL_PROXY=socks5://127.0.0.1:1080 >> ~/.zsh_profile

## Intellij

- 如果使用Intellij的时候,需要使用自己安装的gradle,需要在后面加一个 libexec:
`/usr/local/Cellar/gradle/4.7/libexec`

## ShadowsocksX

- `~/.ShadowsocksX-NG/` 是pac位置,适用于`ss-ng`.


## Switch SD card

```
sudo chflags -R arch /Volumes/SDCARD_NAME
```