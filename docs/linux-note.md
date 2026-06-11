# Linux 笔记

2019-02-02

## nmap 代替 telnet

可以代替 telnet 来检查端口是否开放

```sh
aac@myhost:/mnt/c/Users/aac$ nmap -p 80 127.0.0.1
Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-05 11:09 CST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000041s latency).

PORT   STATE  SERVICE
80/tcp closed http

Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds
```


## SSH SCP

从 主机A 里面执行 SCP 指令，copy 主机B 的文件到 A

```sh
# 在 A 里面生成文件
ssh-keygen -t rsa [-f identity_file]
ssh-copy-id -i [identity_file.pub] user@host

scp -r user1@192.168.110.8:/data /data
```


## fish 配置

> vim ~/.config/fish/config.fish


```sh

set fish_prompt_pwd_dir_length 0

alias dockerf='docker compose down ; docker compose pull ; docker compose up -d'
alias ll='ls -alFhtr --time-style=long-iso'

# {{.State}} 在老版本是没有的 这个能兼容老版本 Docker
# alias dps='docker ps --format "table {{.ID}} \t {{.Names}} \t {{.Status}} \t {{.Ports}}"'
alias dps='docker ps --format "table {{.ID}} \t {{.Names}} \t {{.State}} \t {{.Status}} \t {{.Ports}}"'

alias proxy='export http_proxy=http://127.0.0.1:7777 ; export https_proxy=http://127.0.0.1:7777'
alias unproxy='set -e http_proxy ; set -e https_proxy'
```

## 普通情况下的 proxy and unproxy 快捷指令

适用于直接在 Linux 物理机/虚拟机/容器中使用，代理地址固定为 `127.0.0.1:7777`。

### zsh 和 bash

```conf
proxy() {
    export http_proxy=http://127.0.0.1:7777
    export https_proxy=http://127.0.0.1:7777
    export all_proxy=socks5://127.0.0.1:7777
    echo "✅ 代理已开启 (127.0.0.1:7777)"
}

unproxy() {
    unset http_proxy https_proxy all_proxy
    echo "❌ 代理已关闭"
}

# 测试代理状态的便捷命令
testproxy() {
    echo "正在测试连接 Google..."
    curl -I -L --connect-timeout 5 https://www.google.com
}
```

## WSL 情况下的 proxy and unproxy 快捷指令


### zsh 和 bash

```conf
# =================================================================
# WSL2 代理自动化配置 (兼容镜像模式与网桥模式)
# =================================================================

proxy() {
    # 1. 自动获取宿主机 IP
    # 优先从 ip route 获取默认网关，这是 WSL2 最准确的宿主机地址
    local host_ip=$(ip route show | grep default | awk '{print $3}' | head -n 1)

    # 2. 健壮性检查：如果获取的 IP 包含虚拟地址 (如 10.255.x.x)，则回退尝试
    if [[ -z "$host_ip" || "$host_ip" == "10.255.255.254" ]]; then
        # 尝试从 resolv.conf 获取，但排除掉虚拟 DNS 地址
        host_ip=$(grep nameserver /etc/resolv.conf | awk '{print $2}' | grep -v '10.255.255.254' | head -n 1)
    fi

    # 3. 最终确认
    if [ -z "$host_ip" ]; then
        echo "❌ 错误: 无法自动获取宿主机 IP，请检查网络设置。"
        return 1
    fi

    # 4. 设置环境变量 (端口 7777)
    export http_proxy="http://${host_ip}:7777"
    export https_proxy="http://${host_ip}:7777"
    export all_proxy="socks5://${host_ip}:7777"

    # 5. 同时配置 Git 代理 (如果你需要 Git 也走代理)
    git config --global http.proxy "http://${host_ip}:7777"
    git config --global https.proxy "http://${host_ip}:7777"

    # 6. 设置 NPM 代理配置 (持久化到 .npmrc)
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

### fish

将下面内容粘到 ~/.config/fish/config.fish 或单独的脚本中

```shell
function proxy
    # 1. 自动获取宿主机 IP（与 Bash 版本相同的策略）
    set -l host_ip (ip route show | grep default | awk '{print $3}' | head -n 1)

    # 2. 健壮性检查：如果获取的 IP 为空或为虚拟地址，则回退尝试
    if test -z "$host_ip" -o "$host_ip" = "10.255.255.254"
        set host_ip (grep nameserver /etc/resolv.conf | awk '{print $2}' | grep -v '10.255.255.254' | head -n 1)
    end

    # 3. 最终确认
    if test -z "$host_ip"
        echo "❌ 错误: 无法自动获取宿主机 IP，请检查网络设置。"
        return 1
    end

    # 4. 设置环境变量（端口 7777）
    set -gx http_proxy "http://$host_ip:7777"
    set -gx https_proxy "http://$host_ip:7777"
    set -gx all_proxy "socks5://$host_ip:7777"

    # 5. 同时配置 Git 代理
    git config --global http.proxy "http://$host_ip:7777"
    git config --global https.proxy "http://$host_ip:7777"

    # 6. NPM 代理配置
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




## ssh config

这样可以做到在登陆 ssh 之后，预执行一些命令。

```sh
Host aaa
    User your_linux_user_name
    HostName 172.18.81.111
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/personal_server
    Port 22
    RemoteCommand neofetch;fish
    RequestTTY yes
```

## apt 代理

/etc/apt/apt.conf.d/proxy.conf

```sh
Acquire::http::Proxy "http://127.0.0.1:7777";
Acquire::https::Proxy "http://127.0.0.1:7777";
Acquire::socks::Proxy "socks5h://127.0.0.1:1080";
```

## 快速设置桌面背景

```sh
gsettings set org.gnome.desktop.background picture-options 'none'
gsettings set org.gnome.desktop.background primary-color '#000000'
```

## 给控制台加上颜色
> https://askubuntu.com/questions/517677/how-do-i-get-a-colored-bash

Open ~/.bashrc in text editor and uncomment line:
```
force_color_prompt=yes
```
copy this and add it at the end of .bashrc file:
```
PS1='\[\033[1;36m\]\u\[\033[1;31m\]@\[\033[1;32m\]\h:\[\033[1;35m\]\w\[\033[1;31m\]\$\[\033[0m\]'
```
save then execute 
```
source ~/.bashrc
```
