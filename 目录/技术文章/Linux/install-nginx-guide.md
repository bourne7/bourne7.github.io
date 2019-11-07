# 快速安装 Nginx 用于分享文件

2019-02-02

首先在 Ubuntu 18.04 上面安装好 Nginx，我这里装好后的版本是 1.14.0。 默认的配置在 /etc/nginx/nginx.conf，可以看到里面包含了

```text
include /etc/nginx/conf.d/*.conf
include /etc/nginx/sites-enabled/*
```

然后我们打开这2个目录，发现 conf.d 里面是空的，而在 sites-enabled 里面有一个指向 /etc/nginx/sites-available/default 的连接，所以我们打开这个连接所在的目录。

这个目录里面只有一个 default 文件，这个就是我们要改的了，下面我要改这个文件了，不过修改前先备份好，复制一份叫做 default.bak 的文件。 default 里面有指明 root 是 root /var/www/html，并且默认的 index 是 index.nginx-debian.html，我们在这个目录里面也的确找到了这文件，然后将 default 改为下面的样子:

```text
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    charset utf-8;
    root /var/www;
    index html/index.nginx-debian.html;
    server_name _;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

这里要注意的是，一定要指明编码是 utf-8，否则就会出现中文文件名乱码. 当然，如果所有路径和文件名都是英文的话，可以不用加这句了。

改完以后要重启 nginx，这个时候我们的默认页面还是能够打开，但是我们能用这个 download 做一个文件目录了. 加上下面这段，然后在 /var/www 下面建立一个 download 文件夹。

```text
location /download {
    include mime.types;
    default_type application/octet-stream;
    autoindex on;
    autoindex_exact_size off;
    autoindex_localtime on;
}
```

还可以在默认的 index.nginx-debian.html 里面加入去到下载目录的连接:

```markup
<p><a href="/download">点击这里去到下载目录: /download</a></p>
```

这样的话，用户可以直接访问 IP 地址就能看到这个连接了，当然，直接通过 IP/download 也能看到这个目录。

使用这种方式在局域网里面分享文件，最大的好处是用户可以使用浏览器就能看到共享目录的东西，也能使用filezilla通过sftp往上面放东西。

