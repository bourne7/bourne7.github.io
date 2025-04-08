# Python Pip代理笔记


## 配置路径

通过 `pip config -v list` 看路径
* Linux 配置路径 `~/.pip/pip.conf`
* Windows 配置路径 `~\pip\pip.ini`

## Python pip配置国内源

```
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple 
阿里云：http://mirrors.aliyun.com/pypi/simple/

[global] 
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```

## 代理

```
[global]
proxy     = http://127.0.0.1:7777
```

## 单次配置

每次下载的时候,加入 `--proxy`
`pip3 install --proxy http://127.0.0.1:7777  pillow`