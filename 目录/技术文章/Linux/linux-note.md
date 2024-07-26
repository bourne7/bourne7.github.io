# Linux 笔记

2019-02-02

## 查看进程

ps -ef 是用标准的格式显示进程的，ps aux 是用BSD的格式来显示。

为了在前面加上头部，可以加上

ps -ef \| head -1

然后在加上需要查询条件。这里要注意，aux前面的横线可加可不加，不加就是BSD风格，建议不加。详情这里不多说，可以man ps 看到。

ps -ef \| grep java ps aux \| grep java


## 查询端口

netstat命令各个参数说明如下：

```bash
-n 拒绝显示别名，能显示数字的全部转化成数字。
-p 显示建立相关链接的程序名
-l 仅列出有在 Listen (监听) 的服務状态
-e 显示扩展信息，例如uid等

-t (tcp)仅显示tcp相关选项
-u (udp)仅显示udp相关选项

-a (all)显示所有选项，默认不显示LISTEN相关
-r 显示路由信息，路由表
-s 按各个协议进行统计
-c 每隔一个固定时间，执行该netstat命令。

提示：LISTEN和LISTENING的状态只有用-a或者-l才能看到

netstat -nplt   //查看当前所有tcp端口·
netstat -ntulp | grep 80   //查看所有80端口使用情况·
netstat -an | grep 3306   //查看所有3306端口使用情况·
```

## nmap 代替 telnet

可以代替 telnet 来检查端口是否开放

```
aac@myhost:/mnt/c/Users/aac$ nmap -p 80 127.0.0.1
Starting Nmap 7.80 ( https://nmap.org ) at 2023-05-05 11:09 CST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000041s latency).

PORT   STATE  SERVICE
80/tcp closed http

Nmap done: 1 IP address (1 host up) scanned in 0.02 seconds
```

## 格式压缩与解压

使用 tar
```
打包：tar -jcvf file_name target_name.tar.gz
解包：tar -jxvf target_name.tar.gz

c 代表 create（创建）
x 代表 extract（解包）
v 代表 verbose（详细信息）
f 代表 filename（文件名），所以f后必须接文件名。
z 代表用gzip算法来压缩/解压。生成 “.tar.gz”
j 代表用bzip2算法来压缩/解压。生成 “.tar.bz2”
```

7z压缩。压缩比例更高，命令更简单。
```
7z a file.7z file
7z x file.7z
```

## VIM 快捷键

```bash
ctrl+f           在文件中前移一页（相当于pagedown）；
ctrl+b           在文件中后移一页（相当于pageup）；
gg               将光标定位到文件第一行起始位置；
G                将光标定位到文件最后一行起始位置；
nG或ngg或:n      将光标定位到第N行的起始位置；

H                将光标移到屏幕上的起始行（或最上行）；
M                将光标移到屏幕中间；
L                将光标移到屏幕最后一行；

w                右移光标到下一个字的开头；
b                左移光标到前一个字的开头；
0                数字０，左移光标到本行的开始；
$                右移光标，到本行的末尾；

/str1            正向搜索字符串str1；
n                继续搜索，找出str1字符串下次出现的位置；
N                继续搜索，找出str1字符串上一次出现的位置；
?str2            反向搜索字符串str2；

x                删除（剪切）光标所指向的当前字符；
dd               删除（剪切）光标所在行，并去除空隙；
ndd              删除（剪切）n行内容，并去除空隙；

p                小写字母p，将缓冲区的内容粘贴到光标的后面；
P                大写字母P，将缓冲区的内容粘贴到光标的前面；
v                单个选择；
V                整行选择；
yw               复制当前单词；
yy               复制当前行到内存缓冲区；
"+yy             复制1行到操作系统的粘贴板；

u                撤消前一条命令的结果；
.                重复最后一条修改正文的命令；
```


## 常用命令

```bash

# 文件夹下有a、b、c三个文件，删除b和c,不删除a
rm -f !\(a\) 

# 保留a和b
rm -f !\(a\|b\)

# 查看Ubuntu所有系统服务
service --status-all


## 通过 python 快速分享文件
server.py [-h] [--cgi] [--bind ADDRESS] [--directory DIRECTORY] [port]
sudo python3 -m http.server 80
python -m http.server --bind 192.168.10.6 81

# 查看文件夹下面的所有文件个数
# 其中 R 代表递归；用正则代表筛选出来文件；wc表示统计数量，按照行。
ls -lR| grep "^-"| wc -l

# 查看文件夹大小
du -sh *

## 创建连接/命令别名 
unlink /usr/local/bin/python
ln -s /usr/local/bin/python3.3 /usr/local/bin/python
```

## SSH SCP


从 主机A 里面执行 SCP 指令，copy 主机B 的文件到 A，需要在A电脑里面执行 ssh-copy-id

```bash
# 在 A 里面生成文件
ssh-keygen [-f identity_file]

# Copy 到 B
ssh-copy-id -i [identity_file.pub] user@host
```

有个更方便的方式是直接去被 ssh 的主机上面的 authorized_keys 里面粘贴 pub

```bash
scp [OPTION] [user@]SRC_HOST:]file1 [user@]DEST_HOST:]file2

# OPTION
-P - Specifies the remote host ssh port.
-p - Preserves files modification and access times.
-q - Use this option if you want to suppress the progress meter and non-error messages.
-C - This option forces scp to compresses the data as it is sent to the destination machine.
-r - This option tells scp to copy directories recursively.

# 复制目录要加 -r
scp -r user1@192.168.110.8:/data /data
```

## Htop showing multiple java processes with different pids

> https://stackoverflow.com/questions/11017597/htop-showing-multiple-java-processes-with-different-pids
> https://unix.stackexchange.com/questions/10362/why-does-htop-show-more-process-than-ps

By default, htop lists each thread of a process separately, while ps doesn't. To turn off the display of threads, press H, or use the "Setup / Display options" menu, "Hide userland threads". This puts the following line in your ~/.htoprc or ~/.config/htop/htoprc (you can alternatively put it there manually):

hide_userland_threads=1
(Also hide_kernel_threads=1, toggled by pressing K, but it's 1 by default.)

Another useful option is “Display threads in a different color” in the same menu (highlight_threads=1 in .htoprc), which causes threads to be shown in a different color (green in the default theme).

## neofetch

通常我会用 lsb_release -a 看系统发行版，但是看到的信息不够多，这个命令的好处是默认都有。 但是 neofetch 这个就华丽多了，可以看到如下的内容

```
            .-/+oossssoo+/-.               aac@aaa
        `:+ssssssssssssssssss+:`           ----------------
      -+ssssssssssssssssssyyssss+-         OS: Ubuntu 22.04.1 LTS on Windows 10 x86_64
    .ossssssssssssssssssdMMMNysssso.       Kernel: 5.10.102.1-microsoft-standard-WSL2
   /ssssssssssshdmmNNmmyNMMMMhssssss/      Uptime: 7 secs
  +ssssssssshmydMMMMMMMNddddyssssssss+     Packages: 773 (dpkg)
 /sssssssshNMMMyhhyyyyhmNMMMNhssssssss/    Shell: bash 5.1.16
.ssssssssdMMMNhsssssssssshNMMMdssssssss.   Terminal: Windows Terminal
+sssshhhyNMMNyssssssssssssyNMMMysssssss+   CPU: Intel i7-8700 (12) @ 3.192GHz
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   GPU: c658:00:00.0 Microsoft Corporation Device 008e
ossyNMMMNyMMhsssssssssssssshmmmhssssssso   Memory: 266MiB / 15920MiB
+sssshhhyNMMNyssssssssssssyNMMMysssssss+
.ssssssssdMMMNhsssssssssshNMMMdssssssss.
 /sssssssshNMMMyhhyyyyhdNMMMNhssssssss/
  +sssssssssdmydMMMMMMMMddddyssssssss+
   /ssssssssssshdmNNNNmyNMMMMhssssss/
    .ossssssssssssssssssdMMMNysssso.
      -+sssssssssssssssssyyyssss+-
        `:+ssssssssssssssssss+:`
            .-/+oossssoo+/-.
```


## 当指令的以 sudo 开头的时候，&& 后面的指令仍然是 sudo 权限吗？

> https://askubuntu.com/questions/634620/when-using-and-sudo-on-the-first-command-is-the-second-command-run-as-sudo-t

答案是后面的指令不是 sudo

```bash
$ sudo whoami && whoami
root
username
```

## 单引号和双引号的区别

> https://stackoverflow.com/questions/6697753/difference-between-single-and-double-quotes-in-bash

Single quotes won't interpolate anything, but double quotes will. For example: variables, backticks, certain \ escapes, etc.

单引号不会改变任何引号里面的东西，引号里面的内容被视为文本。但是双引号会进行语义分析。

## shell中>/dev/null 2>&1

> https://www.cnblogs.com/520playboy/p/6275022.html
> https://www.cnblogs.com/chengmo/archive/2010/10/20/1855805.html
> https://blog.csdn.net/reyleon/article/details/11595985


shell重定向介绍
就像我们平时写的程序一样，一段程序会处理外部的输入，然后将运算结果输出到指定的位置。在交互式的程序中，输入来自用户的键盘和鼠标，结果输出到用户的屏幕，甚至播放设备中。而对于某些后台运行的程序，输入可能来自于外部的一些文件，运算的结果通常又写到其他的文件中。而且程序在运行的过程中，会有一些关键性的信息，比如异常堆栈，外部接口调用情况等，这些都会统统写到日志文件里。

  | 类型                        | 文件描述符 | 默认情况               | 对应文件句柄位置 |
  | --------------------------- | ---------- | ---------------------- | ---------------- |
  | 标准输入（standard input）  | 0          | 从键盘获得输入         | /proc/slef/fd/0  |
  | 标准输出（standard output） | 1          | 输出到屏幕（即控制台） | /proc/slef/fd/1  |
  | 错误输出（error output）    | 2          | 输出到屏幕（即控制台） | /proc/slef/fd/2  |


输出重定向

| 命令                | 介绍                       |
| ------------------- | -------------------------- |
| command >filename   | 把标准输出重定向到新文件中 |
| command 1>filename  | 同上                       |
| command >>filename  | 把标准输出追加到文件中     |
| command 1>>filename | 同上                       |
| command 2>filename  | 把标准错误重定向到新文件中 |
| command 2>>filename | 把标准错误追加到新文件中   |

我们使用>或者>>对输出进行重定向。符号的左边表示文件描述符，如果没有的话表示1，也就是标准输出，符号的右边可以是一个文件，也可以是一个输出设备。当使用>时，会判断右边的文件存不存在，如果存在的话就先删除，然后创建一个新的文件，不存在的话则直接创建。但是当使用>>进行追加时，则不会删除原来已经存在的文件。


输入重定向
在理解了输出重定向之后，理解输入重定向就会容易得多。对输入重定向的基本命令如下：

| 命令                 | 介绍                                      |
| -------------------- | ----------------------------------------- |
| command < filename   | 以filename文件作为标准输入                |
| command 0< filename  | 同上                                      |
| command << delimiter | 从标准输入中读入，直到遇到delimiter分隔符 |

我们使用 < 对输入做重定向，如果符号左边没有写值，那么默认就是0。

高级用法
重定向绑定
```
command >/dev/null
```
这条命令的作用是将标准输出1重定向到/dev/null中。/dev/null代表linux的空设备文件，所有往这个文件里面写入的内容都会丢失，俗称“黑洞”。那么执行了>/dev/null之后，标准输出就会不再存在，没有任何地方能够找到输出的内容。
```
command 2>&1
```
这条命令用到了重定向绑定，采用&可以将两个输出绑定在一起。这条命令的作用是错误输出将和标准输出同用一个文件描述符，说人话就是错误输出将会和标准输出输出到同一个地方。

linux在执行shell命令之前，就会确定好所有的输入输出位置，并且从左到右依次执行重定向的命令，所以>/dev/null 2>&1的作用就是让标准输出重定向到/dev/null中（丢弃标准输出），然后错误输出由于重用了标准输出的描述符，所以错误输出也被定向到了/dev/null中，错误输出同样也被丢弃了。执行了这条命令之后，该条shell命令将不会输出任何信息到控制台，也不会有任何信息输出到文件中。
```
>/dev/null 2>&1 VS 2>&1 >/dev/null
```
再回到文章的开头，我说我弄反了>/dev/null和2>&1拼装的顺序，导致出了一点小问题。乍眼看这两条命令貌似是等同的，但其实大为不同。刚才提到了，linux在执行shell命令之前，就会确定好所有的输入输出位置，并且从左到右依次执行重定向的命令。

| 命令            | 标准输出 | 错误输出 |
| --------------- | -------- | -------- |
| >/dev/null 2>&1 | 丢弃     | 丢弃     |
| 2>&1 >/dev/null | 丢弃     | 屏幕     |

```
>/dev/null 2>&1 VS >/dev/null 2>/dev/null
```
那么可能会有些同学会疑问，为什么要用重定向绑定，而不是像>/dev/null 2>/dev/null这样子重复一遍呢。

这是因为采用这种写法，标准输出和错误输出会抢占往out文件的管道，所以可能会导致输出内容的时候出现缺失、覆盖等情况。现在是出现了乱码，有时候也有可能出现只有error信息或者只有正常信息的情况。不管怎么说，采用这种写法，最后的情况是无法预估的。

而且，由于out文件被打开了两次，两个文件描述符会抢占性的往文件中输出内容，所以整体IO效率不如>/dev/null 2>&1来得高。

#### nohup结合

我们经常使用nohup command &命令形式来启动一些后台程序，比如一些java服务：

```
# nohup java -jar xxxx.jar &
```
为了不让一些执行信息输出到前台（控制台），我们还会加上刚才提到的>/dev/null 2>&1命令来丢弃所有的输出：

```
# nohup java -jar xxxx.jar >/dev/null 2>&1 &
```


## find 命令

- `find` 这个用于查找文件,比较好用.http://man.linuxde.net/find
`find /home -path "*local*"` **匹配文件路径或者文件[建议使用这个]**
`find /home -name "*.txt"` 在/home目录下查找以.txt结尾的文件名
`find /home -iname "*.txt"` 同上，但忽略大小写
`find /home -iregex ".*\(\.txt\|\.pdf\)$"` 基于正则表达式匹配文件路径,忽略大小写
`find /home -maxdepth 3 -type f` 向下最大深度限制为3
`find /home -type f -atime -7` 搜索最近七天内被访问过的所有文件
`find /home -type f -atime 7` 搜索恰好在七天前被访问过的所有文件
`find /home -type f -atime +7` 搜索超过七天内被访问过的所有文件

> UNIX/Linux文件系统每个文件都有三种时间戳：
访问时间（-atime/天，-amin/分钟）：用户最近一次访问时间。
修改时间（-mtime/天，-mmin/分钟）：文件最后一次修改时间。
变化时间（-ctime/天，-cmin/分钟）：文件数据元（例如权限等）最后一次修改时间。



## fish

```
sudo apt install fish
```

发现一点，fish 使用 and 来连接2个指令的。所以fish最好还是自己登录的时候用一下，默认的shell还是使用 bash 吧，避免一些命令用不了。

```bash
vim ~/.config/fish/config.fish

set fish_prompt_pwd_dir_length 0

alias dockerf='docker compose down ; docker compose pull ; docker compose up -d'
alias ll='ls -alFhtr --time-style=long-iso'

# {{.State}} 在老版本是没有的 这个能兼容老版本 Docker
# alias dps='docker ps --format "table {{.ID}} \t {{.Names}} \t {{.Status}} \t {{.Ports}}"'
alias dps='docker ps --format "table {{.ID}} \t {{.Names}} \t {{.State}} \t {{.Status}} \t {{.Ports}}"'

alias proxy='export http_proxy=http://127.0.0.1:7777 ; export https_proxy=http://127.0.0.1:7777'
alias unproxy='set -e http_proxy ; set -e https_proxy'
```

## bash 代理 proxy and unproxy

```bash
vim ~/.bashrc

alias proxy="
 export http_proxy=http://127.0.0.1:7777;
 export https_proxy=http://127.0.0.1:7777;"

alias unproxy="
 unset http_proxy;
 unset https_proxy;"
```

## ssh config

这样可以做到在登陆 ssh 之后，预执行一些命令。

```
Host aaa
    User your_linux_user_name
    HostName 172.18.81.111
    PreferredAuthentications publickey
    IdentityFile ~/.ssh/personal_server
    Port 22
    RemoteCommand neofetch;fish
    RequestTTY yes
```


## apt 源配置

Ubuntu 的软件源配置文件是 /etc/apt/sources.list, 打开这个文件并且添加一下清华大学源:
```
# https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/

# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse

# 以下安全更新软件源包含了官方源与镜像站配置，如有需要可自行修改注释切换
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-proposed main restricted universe multiverse
# # deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-proposed main restricted universe multiverse
```

## apt 代理

/etc/apt/apt.conf.d/proxy.conf
```
Acquire::http::Proxy "http://127.0.0.1:7777";
Acquire::https::Proxy "http://127.0.0.1:7777";
Acquire::socks::Proxy "socks5h://127.0.0.1:1080";
```


## 快速设置桌面背景

```bash
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

## vmware

1. How do I mount shared folders in Ubuntu using VMware tools?
> https://askubuntu.com/questions/29284/how-do-i-mount-shared-folders-in-ubuntu-using-vmware-tools

Most other answers are outdated. For Ubuntu 18.04 (or recent Debian distros), try:
```
sudo vmhgfs-fuse .host:/ /mnt/hgfs/ -o allow_other -o uid=1000
```
If you use ubuntu 24+
```
sudo vmhgfs-fuse .host:/ /mnt/ -o allow_other -o uid=1000
```

2. 安装 vm tools
```
sudo apt install open-vm-tools-desktop

or

sudo apt install open-vm-tools
```

3. Enable drag and drop

> https://docs.vmware.com/en/VMware-Workstation-Player-for-Linux/17.0/com.vmware.player.linux.using.doc/GUID-5FC42BAD-0AAC-4EAF-8AD9-A41408ECF9BC.html
The drag-and-drop feature requires Linux hosts and guests to run X Windows and Solaris 10 guests to run an Xorg X server and JDS/Gnome.

```
sudo vim /etc/gdm3/custom.conf

# Uncomment the line below to force the login screen to use Xorg
WaylandEnable=false
```


## 统计代码行数

需要在干净的 git 仓库里面执行：

```bash
# https://stackoverflow.com/questions/3435581/how-to-count-lines-of-java-code-using-intellij-idea
find . -type f -name '*.java' | xargs cat | wc -l

# ignore blank lines: 
find . -type f -name '*.java' | xargs cat | grep -ve '^\s*$' | wc -l
```

