# ffmpeg notes

## 文件合并

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

```
ffmpeg -i video.mp4 -i audio.m4a -c:v copy -c:a copy video_with_audio.mp4

这个是视频直接复制，音频重编码。
ffmpeg -i 1.mp4 -i 1.m4a -c:v copy -map 0:v:0 -map 1:a:0 new.mp4
```

如果默认编码器有问题, 可以尝试一下手动设置编码器
```
ffmpeg -i video.mp4 -i audio.m4a -c:v libx264 copy -c:a copy video_with_audio.mp4
```

## 参数

顺时针转90度
```
ffmpeg -i 1.mp4 -vf "transpose=1" 2.mp4
```

## 下载播放列表
```
ffmpeg -i "播放列表网址" -c copy output.mp4
```

## 修改分辨率
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

## 合并2个webm
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

## 截短视频
```
ffmpeg -ss 600 -t 60 -i 1.mp4 -vf transpose=1 1.out.mp4
```

这里需要注意的是，分辨率和比例都需要修改。scale 和 setsar 是要同时设置，否则根据下面的公式，会被隐含的弄成不显示1：1像素
```
ffmpeg -y -ss 600 -t 10 -i 1.mp4 -vf "transpose=1,scale=1200:1920,setsar=1:1" 2.mp4
```

The setdar filter sets the Display Aspect Ratio for the filter output video.

This is done by changing the specified Sample (aka Pixel) Aspect Ratio, according to the following equation:

DAR = HORIZONTAL_RESOLUTION / VERTICAL_RESOLUTION * SAR

Keep in mind that the setdar filter does not modify the pixel dimensions of the video frame. Also, the display aspect ratio set by this filter may be changed by later filters in the filterchain, e.g. in case of scaling or if another "setdar" or a "setsar" filter is applied.

The setsar filter sets the Sample (aka Pixel) Aspect Ratio for the filter output video.

## 读取文件信息
```
ffmpeg -i 2.mp4 -f null -
```