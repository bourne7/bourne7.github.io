# Docker笔记

## docker 登录 于 token

To use the access token from your Docker CLI client:

这里登录的时候，需要设置代理

```sh
export HTTP_PROXY=http://127.0.0.1:7777 
export HTTPS_PROXY=http://127.0.0.1:7777
```

1. Run
```bash
docker login -u bourne7
```

2. At the password prompt, enter the personal access token.
```bash
Your Token
```

位置在 `cat ~/.docker/config.json` 的 auths 下面。用了 Base64 加密。


## Docker 拉取镜像设置代理

docker pull 和 docker build/run 的方式不一样

docker pull 的代理被 systemd 接管，所以需要设置 systemd

```sh
sudo mkdir /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf

[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7777"
Environment="HTTPS_PROXY=http://127.0.0.1:7777"

# 然后运行
sudo systemctl daemon-reload
sudo systemctl restart docker
```


可以通过`sudo systemctl show --property=Environment docker`看到设置的环境变量。

## Docker 容器内部代理

建议使用

```
docker run -p 1080:1080 .....
export ALL_PROXY='socks5://127.0.0.1:1080'
```

如果遇到了基础镜像引入的外部的一些找不到来源的环境变量，就可以手动覆盖

```yml
version: '3'

services:
  open-webui:
    image: ghcr.io/open-webui/open-webui:main
    container_name: open-webui
    restart: always
    ports:
      - "3000:8080"
    environment:
      - HF_HUB_OFFLINE=1
      - OLLAMA_BASE_URL=http://127.0.0.1:11434
      - http_proxy=
      - HTTP_PROXY=
      - https_proxy=
      - HTTPS_PROXY=
      - no_proxy=
      - NO_PROXY=
    volumes:
      - ./data:/app/backend/data
```

后来找到了是这个引起的。这个是在每次容器被构建的时候被注入的。不建议使用这个设定，比较隐蔽。

```json
// cat ~/.docker/config.json
{
    "proxies": {
        "default": {
            "httpProxy": "http://127.0.0.1:7777",
            "httpsProxy": "http://127.0.0.1:7777",
            "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
        }
    }
}
```

