### 如何下载Youtube视频

#### 1.安装好 youtube-dl 和 ffmpeg

ffmpeg 能解决一切和多媒体有关的事情,包括播放,转换格式等等,功能强大.

youtube-dl 会调用 ffmpeg 做合并, 所以需要确保这2个都安装好了, 都能在命令行里面调用. windows的话需要加入到环境变量里面去.

https://github.com/rg3/youtube-dl

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
    

#### 3.ffmpeg 使用

文件合并
```
ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy video_with_audio.mp4

这个是视频直接复制，音频重编码。
ffmpeg -i 1.mp4 -i 1.m4a -c:v copy -map 0:v:0 -map 1:a:0 new.mp4
```

如果默认编码器有问题, 可以尝试一下手动设置编码器
```
ffmpeg -i video.mp4 -i audio.m4a -c:v libx264 copy -c:a copy video_with_audio.mp4
```

视频顺时针旋转90度
```
ffmpeg -i 1.mp4 -vf "transpose=1" 2.mp4
```

视频合并. 先建立一个叫做 file.txt 的文件,内容如下:
```
file '1.flv'
file '2.flv'
file '3.flv'
file '4.flv'
```

调用合并指令:
```
ffmpeg -f concat -i ./file.txt -c copy output.mkv 
```

下载播放列表
```
ffmpeg -i "播放列表网址" -c copy output.mp4
```

修改分辨率
```
ffmpeg -i input.mp4 -s 1280x720 -c:a copy output.mp4
```

Trim a media file using start and stop times. https://www.ostechnix.com/20-ffmpeg-commands-beginners/ ,
To trim down a video to smaller clip using start and stop times, we can use the following command.
```
ffmpeg -i input.mp4 -ss 00:00:50 -codec copy -t 50 output.mp4
```

默认确认所有选择 `-y`

修改文件里面默认的分辨率，只改配置，不改真实分辨率 `-aspect 16:9` 这样的修改是秒改完的。

合并2个webm
```
ffmpeg -i _video.webm -i _audio.webm -c:v copy -c:a copy -strict experimental output.mkv
```

合并一个音频和一个视频，选取其中比较短的一个来截取。要注意这里一定要加 shortest，否则会不一致。
```
ffmpeg -y -i "2.mp4" -i "audioFile.mp3"  -map 0:v -map 1:a -c:v copy -c:a copy -shortest outPutFile.mp4
```

替换视频中的音频

> https://superuser.com/questions/1137612/ffmpeg-replace-audio-in-video

You will want to copy the video stream without re-encoding to save a lot of time but re-encoding the audio might help to prevent incompatibilities:
```
ffmpeg -i v.mp4 -i a.wav -c:v copy -map 0:v:0 -map 1:a:0 new.mp4

-map 0:v:0 maps the first (index 0) video stream from the input to the first (index 0) video stream in the output.

-map 1:a:0 maps the second (index 1) audio stream from the input to the first (index 0) audio stream in the output.
```
If the audio is longer than the video, you will want to add -shortest before the output file name.

Not specifying an audio codec, will automatically select a working one. You can specify one by for example adding -c:a libvorbis after -c:v copy.