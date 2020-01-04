# Linux 笔记

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