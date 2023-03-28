# Linux 指令笔记

2019-02-02

## 1.查看进程

ps -ef 是用标准的格式显示进程的，ps aux 是用BSD的格式来显示。

为了在前面加上头部，可以加上

ps -ef \| head -1

然后在加上需要查询条件。这里要注意，aux前面的横线可加可不加，不加就是BSD风格，建议不加。详情这里不多说，可以man ps 看到。

ps -ef \| grep java ps aux \| grep java

## 2.查看文件

这里建议添加一个 alias，将ll加强一点，比如添加 -h 指令。

## 3.查询端口

netstat命令各个参数说明如下：

```text
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

## 4.格式压缩与解压

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



## 5.禁止开机启动

```text
sudo update-rc.d mysql disable
```

要去掉这条的话，就用 remove。

## 6.VIM 快捷键

```text
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

## 7.删除文件指令

如文件夹下有a、b、c三个文件，如何一行命令删除b和c,不删除a。

其中rm -f !\(a\) 最为方便。如果保留a和b,可以运行rm -f !\(a\|b\)来实现。

## 8.查看Ubuntu所有系统服务

```text
service --status-all
```

## 9. 通过 python 快速分享文件

可以使用
```
server.py [-h] [--cgi] [--bind ADDRESS] [--directory DIRECTORY] [port]
sudo python3 -m http.server 80
python -m http.server --bind 192.168.10.6 81
```
来快速建立一个http服务器，这样别人可以方便的获取本目录下面的文件。有时候如果IP地址不唯一的话，需要指明绑定的 IP。

## 查看文件夹下面的所有文件个数

```
ls -lR| grep "^-"| wc -l
```
其中 R 代表递归；用正则代表筛选出来文件；wc表示统计数量，按照行。

## 查看文件夹大小

```
du -sh *
```

## SSH SCP
ssh 产生公钥密钥对，建议不要老是用同一对公钥密钥，还是稍微分类一下比较好。
注意，如果是本地电脑A想要执行 SCP 指令，copy 电脑B的内容到本地电脑的话，需要在A电脑里面执行 ssh-copy-id
```
ssh-keygen
```

部署公钥
```
ssh-copy-id -i [identity_file] user@host
```

如果不指明 identity_file 的话，就是默认的 id_rsa

如果是放到 git 上面，可以通过下面的语句检测
```
ssh -T git@github.com
```


scp [OPTION] [user@]SRC_HOST:]file1 [user@]DEST_HOST:]file2

-P - Specifies the remote host ssh port.
-p - Preserves files modification and access times.
-q - Use this option if you want to suppress the progress meter and non-error messages.
-C - This option forces scp to compresses the data as it is sent to the destination machine.
-r - This option tells scp to copy directories recursively.

scp -r user1@192.168.110.8:/data /data

## Htop showing multiple java processes with different pids

> https://stackoverflow.com/questions/11017597/htop-showing-multiple-java-processes-with-different-pids
> https://unix.stackexchange.com/questions/10362/why-does-htop-show-more-process-than-ps

By default, htop lists each thread of a process separately, while ps doesn't. To turn off the display of threads, press H, or use the "Setup / Display options" menu, "Hide userland threads". This puts the following line in your ~/.htoprc or ~/.config/htop/htoprc (you can alternatively put it there manually):

hide_userland_threads=1
(Also hide_kernel_threads=1, toggled by pressing K, but it's 1 by default.)

Another useful option is “Display threads in a different color” in the same menu (highlight_threads=1 in .htoprc), which causes threads to be shown in a different color (green in the default theme).


## ls 的改进

可以用下面的命令显示完整的，按照修改日期升序排列的文件夹

```
ls -alFhtr --time-style=long-iso
```

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