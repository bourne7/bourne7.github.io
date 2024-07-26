# Docker笔记

> 一图流说明（来自于@fntsrlike）

![Docker-Command-Diagram.png](Docker-Command-Diagram.png)

### Docker 安装

https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository

1. Add Docker's official GPG key:
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
```

注意这个步骤需要加代理 
```bash
sudo curl -x http://192.168.197.1:7777 -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

2. Add the repository to Apt sources:
```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
```

3. 正式安装组件
```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

4. 测试运行
```bash
sudo docker run hello-world
```


### Docker 拉取镜像设置代理

> 版权声明：本文为 neucrack 的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
> 原文链接：https://neucrack.com/p/286

docker pull 和 docker build/run 的方式不一样

docker pull 的代理被 systemd 接管，所以需要设置 systemd

```bash
sudo mkdir /etc/systemd/system/docker.service.d
sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf

[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7777"
Environment="HTTPS_PROXY=http://127.0.0.1:7777"
```
这里的127.0.0.1是直接用了本机的 http 代理，然后重启服务才能生效
```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```
可以通过sudo systemctl show --property=Environment docker看到设置的环境变量。


### Docker 容器内部代理

建议使用

```
docker run -p 1080:1080 .....
export ALL_PROXY='socks5://127.0.0.1:1080'
```


### Image操作

* 停止所有的container并且删除所有镜像：
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
```

* 删除指定Image
```
docker images
docker rmi image_id
```

* 如果遇到了 \<none>:\<none> 类型的 untagged images 应该如何删除
关于这种类型的镜像的产生，有2种原因，可以在这个网页上面找到解释：

> https://www.projectatomic.io/blog/2015/07/what-are-docker-none-none-images/

类型有2种，分别是旧版的 images 和 被现有自定义镜像依赖的旧版 images。都可以通过ID来删除：
```
 sudo docker rmi 8eccc77fd8d0
```

# 运行镜像

```
docker run -d -p 5000:5000 <image_name> ping www.docker.com
```
在这个命令里面
> -d: 让容器在后台运行。

* 删除所有的container，请确保所有 container 都停止的情况下才使用。
```
sudo docker rm $(sudo docker ps -a -q)

docker ps --help
Usage:  docker ps [OPTIONS]
List containers
Options:
  -a, --all             Show all containers (default shows just running)
  -f, --filter value    Filter output based on conditions provided (default [])
      --format string   Pretty-print containers using a Go template
      --help            Print usage
  -n, --last int        Show n last created containers (includes all states) (default -1)
  -l, --latest          Show the latest created container (includes all states)
      --no-trunc        Don‘t truncate output
  -q, --quiet           Only display numeric IDs
  -s, --size            Display total file sizes
```

查看当前正在运行的容器。
```
docker ps -a -q

docker rm --help
Usage:  docker rm [OPTIONS] CONTAINER [CONTAINER...]
Remove one or more containers
Options:
  -f, --force     Force the removal of a running container (uses SIGKILL)
      --help      Print usage
  -l, --link      Remove the specified link
  -v, --volumes   Remove the volumes associated with the container
```

也可使用下面的命令
> 引用自：https://www.jianshu.com/p/5e0358b77f28
```
docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm
docker ps -a | grep Exit | awk '{ print $1}'  | xargs sudo docker rm
docker rm $(docker ps --all -q -f status=exited)

```

# 运行时如何输入命令

```
docker exec --help

Usage:	docker exec [OPTIONS] CONTAINER COMMAND [ARG...]

Run a command in a running container

Options:
  -d, --detach               Detached mode: run command in the background
      --detach-keys string   Override the key sequence for detaching a container
  -e, --env list             Set environment variables
  -i, --interactive          Keep STDIN open even if not attached
      --privileged           Give extended privileges to the command
  -t, --tty                  Allocate a pseudo-TTY
  -u, --user string          Username or UID (format: <name|uid>[:<group|gid>])
  -w, --workdir string       Working directory inside the container
```

比如之前启动了
```
sudo docker run -dit --name "test-java" java
```
然后可以找到它的ID是 75b3b99d2025 ，通过
```
sudo docker exec -it 75b3b99d2025 /bin/bash
```
可以去到容器的内部，执行指令。这里要注意的是，这个容器的内部可能十分简陋，很多工具和命令都是没有的。



# 额外内容
/etc/resolv.conf是DNS客户机配置文件，用于设置DNS服务器的IP地址及DNS域名，还包含了主机的域名搜索顺序。

该文件是由域名解析 器（resolver，一个根据主机名解析IP地址的库）使用的配置文件。它的格式很简单，每行以一个关键字开头，后接一个或多个由空格隔开的参数。

cat /etc/resolv.conf  
nameserver 8.8.8.8      //google服务器
nameserver 8.8.4.4      //google备用服务器



## docker in windows wsl ubuntu

按照官方教程安装好以后发现无法启动，其实是由于 wsl 本身不是管理员权限，可以在windows 里面用管理员权限启动 docker 就行了

在开始菜单里面找到 ubuntu 图标，右键管理员运行，然后启动 docker
```
sudo service docker start
```


## docker top

可以用于寻找 容器 对应的系统 PID

docker top container_name

## docker mount 和 docker volume

Differences between -v and --mount behavior
Because the -v and --volume flags have been a part of Docker for a long time, their behavior cannot be changed. This means that there is one behavior that is different between -v and --mount.

If you use -v or --volume to bind-mount a file or directory that does not yet exist on the Docker host, -v creates the endpoint for you. It is always created as a directory.

If you use --mount to bind-mount a file or directory that does not yet exist on the Docker host, Docker does not automatically create it for you, but generates an error.

You cannot mount root in container to host. 

经过测试：无法将容器的根目录映射到外面。

猜测原因：
* 在创建容器的时候，目录映射会将容器内部的某个目录映射到外部，并且采用外部的值。
* 如果映射文件的话，则是会单向的在创建容器的时候，将外面的文件映射到容器里面。

我认为为了容器的映射方便，最好将所有的非基础镜像的内容，都放到非根目录里面，比如可以放到 /data 里面去，然后映射出来，这样就方便许多了。

> https://forums.docker.com/t/mount-container-volume-root-folder/38265/3
If you could successfully run docker run -v /host/path:/ image then it would cause the contents of /host/path to be the only thing visible in the container; it would be the container’s root. That is, you can mount things into the container but not out.

## ports and volumes

内外映射问题。 都是由外到内，即左外右内。

The following command will create a directory called nginxlogs in your current user’s home directory and bindmount it to /var/log/nginx in the container:

docker run --name=nginx -d -v ~/nginxlogs:/var/log/nginx -p 5000:80 nginx

端口也是一样的：外-内

```
services:
  myapp1:
    ...
    ports:
    - "3000"                             # container port (3000), assigned to random host port
    - "3001-3005"                        # container port range (3001-3005), assigned to random host ports
    - "8000:8000"                        # container port (8000), assigned to given host port (8000)
    - "9090-9091:8080-8081"              # container port range (8080-8081), assigned to given host port range (9090-9091)
    - "127.0.0.1:8002:8002"              # container port (8002), assigned to given host port (8002) and bind to 127.0.0.1
    - "6060:6060/udp"                    # container port (6060) restricted to UDP protocol, assigned to given host (6060)
```

## Ubuntu docker

如果是通过 ubuntu server 自带的 snap 安装的 docker，有几个主意的点：

* sevice name

sudo systemctl restart snap.docker.dockerd.service

* add permission

sudo chmod 666 /var/run/docker.sock

* check all service

sudo systemctl list-units --type=service