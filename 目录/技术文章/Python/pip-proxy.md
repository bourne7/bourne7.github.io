# Pip代理笔记

## Python pip配置国内源

```
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple 
阿里云：http://mirrors.aliyun.com/pypi/simple/
```

```
vi ~/.pip/pip.conf

[global] 
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host = https://pypi.tuna.tsinghua.edu.cn
```


如果实在 windows 上面的话，文件是:
```
%HOMEPATH%\pip\pip.ini
```

## 单次配置

每次下载的时候,加入 `--proxy`
`pip3 install --proxy http://127.0.0.1:1080  pillow`