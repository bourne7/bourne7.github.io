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

