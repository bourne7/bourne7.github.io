# Windows使用笔记

2019-02-12


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


## Scoop

```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```


## 快速切换 JDK

Windows

可以将本地一个目录添加到 Path，然后编写2个 bat: java8.bat 和 java21.bat

```bat
@echo off
set JAVA_HOME=C:\Users\aac\.jdks\temurin-1.8.0_392
set PATH=%JAVA_HOME%\bin;%PATH%
echo.
echo "%JAVA_HOME%" is now set as the default JDK.
```

以后就可以通过 java8 和 java21 来切换了。