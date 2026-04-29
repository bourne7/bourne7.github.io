# Python Pip代理笔记


## 配置路径

通过 `pip config -v list` 看路径
* Linux 配置路径 `~/.pip/pip.conf`
* Windows 配置路径 `~\pip\pip.ini`


## 代理

```
[global]
proxy     = http://127.0.0.1:7777
```

## 单次配置

每次下载的时候,加入 `--proxy`
`pip3 install --proxy http://127.0.0.1:7777  pillow`