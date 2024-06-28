# Windows使用笔记

2019-02-12

## 快捷键

建议安装 PowerToys 进行辅助，这个是一个官方的工具集，github 和 windows store 上面都有。

## 网络指令

```
netsh winsock reset
netsh int ip reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

## Terminal 配置

https://www.freecodecamp.org/news/windows-terminal-themes-color-schemes-powershell-customize/

```json
{
    "profiles": {
        "defaults": {
            "opacity": 60,
            "useAcrylic": true,
            "useAtlasEngine": true,
            "font": {
                "fontFace": "PxPlus IBM VGA8",
                "fontSize": 16
            },
            "experimental.retroTerminalEffect": true
        }
    },
    "schemes": [
        {
            "name": "Duotone Dark",
            "background": "#1F1D27",
            "black": "#1F1D27",
            "blue": "#2488FF",
            "brightBlack": "#353147",
            "brightBlue": "#2488FF",
            "brightCyan": "#6AD7D9",
            "brightGreen": "#2DCD73",
            "brightPurple": "#DE8D40",
            "brightRed": "#D9393E",
            "brightWhite": "#DFD1ED",
            "brightYellow": "#D9B76E",
            "cursorColor": "#FFFFFF",
            "cyan": "#6AD7D9",
            "foreground": "#B7A1FF",
            "green": "#2DCD73",
            "purple": "#DE8D40",
            "red": "#D9393E",
            "selectionBackground": "#FFFFFF",
            "white": "#B7A1FF",
            "yellow": "#D9B76E"
        }
    ]
}
```


## Chrome

开启额外的分身浏览器

"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --user-data-dir="d:\_chrome_user_data"


## Altas OS

https://github.com/Atlas-OS/atlas-releases/releases/download/20H2-v0.5.2/Atlas_v0.5.2_21H2.iso

```
Name: Atlas_v0.5.2.iso
Size: 1595277312 bytes (1521 MiB)
CRC32: 0B5937A3
CRC64: C4FEAC7A971F75EB
SHA256: c0c90fb4ff7c4122d03658fa42a1367fce99f81cfdaa7637360b94a7bf661d9f
SHA1: 5de11d95ec67b6c080b80e161a43a52d5064ced3
BLAKE2sp: 48fa88d4f7108eb3d81a50658cb8fca0b81f10f316d1c15e966fc42b308e6c53
```