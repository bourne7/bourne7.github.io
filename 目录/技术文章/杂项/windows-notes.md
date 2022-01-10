# Windows使用笔记

2019-02-12

## 快捷键

>https://blogs.windows.com/windowsexperience/2014/10/03/keyboard-shortcuts-in-the-windows-10-technical-preview/

Snapping window: WIN + LEFT or RIGHT (can be used with UP or DOWN to get into quadrants)【这个是比较有用的。】

Switch to recent window: ALT + TAB (unchanged) – Hold shows new Task view window view, let go and switches to app.

Task view: WIN + TAB – New Task view opens up and stays open.

Create new virtual desktop: WIN + CTRL + D

Close current virtual desktop: WIN + CTRL + F4

Switch virtual desktop: WIN + CTRL + LEFT or RIGHT

## 网络指令

```
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

## windows 11

> https://winaero.com/windows-11-show-or-hide-icons-in-tray-area-taskbar-corner-overflow/

The option to Show all taskbar tray icons:

BytestormLLC
July 29, 2021 at 6:47 pm
You can still access the ability to turn them all on with the following:
```
Win+R
shell:::{05d7b0f4-2121-4eff-bf6b-ed3f69b894d9}
```
Then at the bottom of the screen, check the “Always show…” checkbox


## 不满足Win11系统需求照样升级：教你绕过TPM、内存等限制

Win11的最系统要求中，受信任的平台模块 (TPM) 2.0 版本通常是“老爷机”们难以逾越的一道坎，毕竟6代酷睿之后，该模块才普及开来。


下面分享一些绕过TPM版本验证甚至是内存验证的方法：

方法一：绕过一切硬件限制

在遇到Windows 11安装助手提示PC配置不满足时，定位到C:\$WINDOWS.~BT\Sources，找到appraiserres.dll并删除，接着回到安装助手界面，点击后退，再下一步即可。


方法二：

用记事本创建注册表文件bypass.reg，内容如下

Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\Setup\LabConfig]

"BypassTPMCheck"=dword:00000001

"BypassSecureBootCheck"=dword:00000001

"BypassRAMCheck"=dword:00000001

"BypassStorageCheck"=dword:00000001

"BypassCPUCheck"=dword:00000001

U盘启动遇到无法安装提示时，点击后退箭头，接着按下Shift+F10调出命令提示符，输入regedit打开注册表，并导入刚才保存的bypass.reg。之后关闭所有窗口，开始正常安装。


方法三：

下载Windows 11安装助手，右键选择属性——兼容性——以Windows7兼容模式运行。

方法四：开源批处理

Aveyo在Github制作了跳过TPM验证的cmd批处理，还有用户下载免验证ISO或制作启动盘的纯净版媒体介质创建工具。

# 自动显示任务栏状态栏所有图标

> https://superuser.com/questions/1680130/windows-11-taskbar-corner-overflow-show-all-tray-icons
> 
My Checkbox for show all was unusable, here's what got it for me on a Windows 10 Home > 11 Home upgrade machine.

Open Regedit, go here:
```
[HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer]
```
Look for EnableAutoTray and set the value from 0 to 1

Then run this cmd:

```
explorer shell:::{05d7b0f4-2121-4eff-bf6b-ed3f69b894d9}
```
The check box for showing all items should be interactable.

