# 手动下载和安装 iOS app

从 iTunes 12.7 开始已经将 app 从资料库里面去掉了，所以我们只能使用最后的能下载 app 的版本 12.6.5.3

这个版本的 iTunes 可以从 苹果的官网下载：
> https://support.apple.com/en-us/HT208079

提取出来下载连接
> https://secure-appldnld.apple.com/itunes12/091-87819-20180912-69177170-B085-11E8-B6AB-C1D03409AD2A6/iTunes64Setup.exe
>
> 大小: 277744968 字节 (264 MiB)
>
> SHA256: 666DCC84D26EA7BA79228F744F9CAEAC1192A9F274A5E795CC9E9352D41D80F3
>
> SHA1: 7B317DA13C3D0E463F73C27123A69379C4DBFD9D


苹果其实提供了 mac 的，但是 mac 的没啥用，因为不支持最新的 mac os。所以使用 windows 的就行了。

安装好了以后，可以和以前的 iTunes 一样下载 ipa 文件。但是后来我发现这个版本的 iTunes 不能同步了，所以从 2020-01 开始的最新方法是这样的：

* 使用原生的 windows 或者在虚拟机里面安装好 windows
* 在 windows 里面安装 iTunes 12.6.5.3
* 登录账号并且下载 ipa
* 如果能直接同步的话最好，如果不能的话，用 win10 的宿主机，或者另外一个虚拟机，或者 mac 最新版。连接 ios 设备，然后将下载的 ipa 拖到展开 **设备** 后的左边栏里面，ipa 就自动安装好了。
* 也可以通过 xcode 安装。在 window -> Device and Simulators -> Devices -> Installed apps 这里，直接拖到这里就行。
  
之前没这么麻烦的，只不过现在苹果对于手动管理 app 支持度越来越低，高的越来越麻烦。而且随着时间推移，一旦 12.6.5.3 这个版本的也打不开 app 商店的话，就没有任何官方办法了。非官方的软件倒是有的，只不过我不太愿意使用，并且目前 iMazing 和 iTools 用起来也不方便。

Apple Configurator 2 也可以，不过我还没探索。
