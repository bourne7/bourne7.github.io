# 使用电脑的一些技巧

### 如何快速稳定下载比较大的Podcast视频，比如每年的苹果发布会1080P原版？

苹果的Podcast是个很好用的平台，是一个免费的播客。平时我除了在上面听一些节目以外，每年的苹果发布会都会在里面下载高清版的视频内容。因为是官方出的，制作十分精良。但是因为1080p的一个m4v的发布会，时间如果在2小时左右的话，大约是7-8G的大小，如果使用iPhone或者iTunes来下载的话，可能遇到断网冲下的问题。所以这里提供一个使用第三方工具下载，比如使用迅雷来下载的方式。（可以看看我写的另外一篇关于如何下载到好一点版本的迅雷的文章。）

1. 使用iTunes先点击下载，等到开始下载的时候暂停。
2. 关闭iTunes并且找到下载的临时文件。
3. 使用任意文本编辑器打开这个plist文件。可以找到里面有个http链接。从名字也可以判断出这是苹果官方的下载链接。（竟然不是https）
4. 将上面得到的链接复制到迅雷里面直接下载就行。可以看到速度是很稳定，而且支持断点继续下载。

每年的苹果发布会以及WWDC我都会看，里面很多特性或者功能，都很有可能作为未来一段时间内科技界的风向标。

### Windows 图标的右下角的状态图标显示不对

最近在自己弄了一个SVN客户端，但是在我在win7上面拉下SVN上面的文件的时候，发现原本应该在文件的左下角显示的状态小图标没有显示出来。后来查了一下原因是有其他程序霸占了状态图标使用权，比如 Dropbox。所以我们可以人工修改成为我们需要的顺序。需要修改注册表：
```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\explorer\ShellIconOverlayIdentifiers
```

可以看出现在的软件为了让自己的状态不被别人覆盖，就在前面加了空格。。比如 Dropbox 就加了2个空格。这种取巧的方式真是太无语了。我的解决办法是在 SVN 的状态显示前面加了 4 个空格。

### iTunes 禁止本地备份

> https://www.technipages.com/disable-itunes-backup-process

Command should only be executed once and in admin terminal

```
Windows
Close out of the iTunes application.
Hold the Windows Key and press “R” to bring up the Run dialog box.
Type the following depending on whether you have 32 or 64 it Windows:
64-bit:
"C:\Program Files\iTunes\iTunes.exe" /setPrefInt DeviceBackupsDisabled 1
32-bit:
"C:\Program Files (x86)\iTunes\iTunes.exe" /setPrefInt DeviceBackupsDisabled 1
Press “Enter” or select “OK“.
When you launch iTunes again, backups for iPhone, iPad and iPod Touch devices will be disabled. If you wish to enable backups again, use the same command as above, but replace the “1” with a “0”.

Note: If you copy and paste this command, you may need to retype the quotes.

FYI, if you’re using the Windows Store version of iTunes, it will be at a different path but the command appears to work (at least it doesn’t kick back an error).

cd "C:\Program Files\WindowsApps\AppleInc.iTunes_12123.5.56009.0_x64__nzyj5cx40ttqa\"
.\iTunes.exe /setPrefInt DeviceBackupsDisabled 1

-----
MacOS
Close iTunes.
Open the “Utilities” folder and launch “Terminal“.
Type:
defaults write com.apple.iTunes DeviceBackupsDisabled -bool true
Press “Enter“.
If you wish to enable backups again, use the terminal command defaults write com.apple.iTunes DeviceBackupsDisabled -bool false to turn backups back on.

Note: If you’re using Apple Music, replace “iTunes” with “Music” in the command.

```


