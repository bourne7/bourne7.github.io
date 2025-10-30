# youtube-dl

#### 1.安装好 youtube-dl 和 ffmpeg

ffmpeg 能解决一切和多媒体有关的事情,包括播放,转换格式等等,功能强大.

youtube-dl 会调用 ffmpeg 做合并, 所以需要确保这2个都安装好了, 都能在命令行里面调用. windows的话需要加入到环境变量里面去.

https://github.com/ytdl-org/youtube-dl

#### 2.下载

先查看视频拥有的格式,一般是有mp4和webm这2种,另外声音也有2种.
```
youtube-dl --proxy socks5://127.0.0.1:1080/ --list-formats https://www.youtube.com/watch?v=111
```

下载选定的文件,比如这里的 200 和 100 就是代表对应的视频和声音. 注意视频要放在前面.
```
youtube-dl --proxy socks5://127.0.0.1:1080/ -o '%(title)s.%(ext)s' -f 200+100 https://www.youtube.com/watch?v=111
```
这里会自动调用 ffmpeg 来合并, 合并以后的文件名会有点混乱. 

也可以自动下载最高品质的视频和音频
```
youtube-dl --proxy socks5://127.0.0.1:1080/ -o '%(title)s.%(ext)s' -f bestvideo+bestaudio https://www.youtube.com/watch?v=111
```