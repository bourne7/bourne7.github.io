# Docker笔记

> 一图流说明（来自于@fntsrlike）

![Docker-Command-Diagram.png](Docker-Command-Diagram.png)

### 拉取镜像

先试一下拉取一个很小的 docker：
```
docker pull hello-world
```

如果出现了 
>docker: Error response from daemon: Get https://registry-1.docker.io/v2/: dial tcp: lookup registry-1.docker.io: Temporary failure in name resolution.

那么证明域名解析有问题。可以通过：
```
curl https://registry-1.docker.io/v2/ && echo Works || echo Problem
```
来判断具体的问题。

修改docker默认仓库镜像路径： 
```
sudo vi /etc/docker/daemon.json
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

