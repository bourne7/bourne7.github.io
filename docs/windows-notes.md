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

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
```


## PowerShell 支持 ll

```powershell
New-Alias -Name ll -Value Get-ChildItem
New-Alias -Name l -Value Get-ChildItem
```



## PowerShell 代理（可迁移配置）

建议把代理配置放在用户目录，查看当前 shell 的 profile 路径：

```powershell
$PROFILE

可能上面的返回的地址是 OneDrive，但是本地版本的也会被识别。

```

配置地址 C:\Users\your_name\Documents\PowerShell\Microsoft.PowerShell_profile.ps1

```powershell
function proxy {
    $proxyHttp = 'http://127.0.0.1:7777'
    $proxySocks = 'socks5://127.0.0.1:7777'

    $env:http_proxy = $proxyHttp
    $env:https_proxy = $proxyHttp
    $env:all_proxy = $proxySocks
    $env:HTTP_PROXY = $proxyHttp
    $env:HTTPS_PROXY = $proxyHttp
    $env:ALL_PROXY = $proxySocks

    git config --global http.proxy $proxyHttp | Out-Null
    git config --global https.proxy $proxyHttp | Out-Null

    npm config set proxy $proxyHttp | Out-Null
    npm config set https-proxy $proxyHttp | Out-Null

    Write-Host '✅ 代理已开启 (127.0.0.1:7777)'
}

function unproxy {
    Remove-Item Env:http_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:https_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:all_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:ALL_PROXY -ErrorAction SilentlyContinue

    git config --global --unset http.proxy 2>$null
    git config --global --unset https.proxy 2>$null

    npm config delete proxy 2>$null
    npm config delete https-proxy 2>$null

    Write-Host '❌ 代理已关闭'
}

function testproxy {
    $curl = Get-Command curl.exe -ErrorAction SilentlyContinue

    Write-Host '正在测试连接 Google...'

    if ($null -ne $curl) {
        & $curl.Source -I -L --connect-timeout 5 https://www.google.com
        return
    }

    Invoke-WebRequest 'https://www.google.com' -Method Head -TimeoutSec 5
}
```

当前会话立即生效：

```powershell
. $PROFILE
```


## 列出目录下占用空间最大的文件夹

```powershell
Get-ChildItem -Directory | ForEach-Object {
  $size = (Get-ChildItem -LiteralPath $_.FullName -Recurse -File -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum
  if ($null -eq $size) { $size = 0 }
  [PSCustomObject]@{
    Folder = $_.Name
    SizeGB = [math]::Round($size / 1GB, 2)
    SizeMB = [math]::Round($size / 1MB, 2)
    Bytes  = $size
  }
} | Sort-Object -Property Bytes -Descending | Format-Table -AutoSize
```