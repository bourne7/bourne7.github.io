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


## PowerShell 代理（可迁移配置）

目标：在新电脑上快速恢复 `proxy` / `unproxy` / `testproxy` 命令。

### 文件位置

建议把代理配置放在用户目录：

```
$HOME\.config\proxy\config.psd1
$HOME\.config\powershell\proxy.ps1
```

PowerShell 启动入口（按你实际环境）：

```
Windows PowerShell 5.1: $HOME\OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
Windows PowerShell 5.1: $HOME\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1
PowerShell 7:           $HOME\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
PowerShell 7:           $HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
```

查看当前 shell 的 profile 路径：

```powershell
$PROFILE
```

### 一次性快速初始化

在 PowerShell 里执行下面整段命令（可直接复制）：

```powershell
# 1) 创建目录
$proxyDir = Join-Path $HOME '.config\proxy'
$psDir = Join-Path $HOME '.config\powershell'
New-Item -ItemType Directory -Path $proxyDir -Force | Out-Null
New-Item -ItemType Directory -Path $psDir -Force | Out-Null

# 2) 写入代理配置
@"
@{
    HttpProxy  = 'http://127.0.0.1:7777'
    HttpsProxy = 'http://127.0.0.1:7777'
    AllProxy   = 'socks5://127.0.0.1:7777'
}
"@ | Set-Content -Encoding UTF8 (Join-Path $proxyDir 'config.psd1')

# 3) 写入函数脚本
@"
$ProxyConfigPath = Join-Path $HOME '.config\proxy\config.psd1'

function Get-ProxyConfig {
    if (-not (Test-Path $ProxyConfigPath)) {
        throw "Proxy config not found: $ProxyConfigPath"
    }

    Import-PowerShellDataFile $ProxyConfigPath
}

function proxy {
    $cfg = Get-ProxyConfig

    $env:http_proxy = $cfg.HttpProxy
    $env:https_proxy = $cfg.HttpsProxy
    $env:all_proxy = $cfg.AllProxy
    $env:HTTP_PROXY = $cfg.HttpProxy
    $env:HTTPS_PROXY = $cfg.HttpsProxy
    $env:ALL_PROXY = $cfg.AllProxy

    git config --global http.proxy $cfg.HttpProxy | Out-Null
    git config --global https.proxy $cfg.HttpsProxy | Out-Null

    npm config set proxy $cfg.HttpProxy | Out-Null
    npm config set https-proxy $cfg.HttpsProxy | Out-Null

    Write-Host "proxy on: $($cfg.HttpProxy)"
}

function unproxy {
    Remove-Item Env:http_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:https_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:all_proxy -ErrorAction SilentlyContinue
    Remove-Item Env:HTTP_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:HTTPS_PROXY -ErrorAction SilentlyContinue
    Remove-Item Env:ALL_PROXY -ErrorAction SilentlyContinue

    git config --global --unset http.proxy 2>`$null
    git config --global --unset https.proxy 2>`$null

    npm config delete proxy 2>`$null
    npm config delete https-proxy 2>`$null

    Write-Host 'proxy off'
}

function testproxy {
    $curl = Get-Command curl.exe -ErrorAction SilentlyContinue

    try {
        if ($null -ne $curl) {
            & $curl.Source -I -L --connect-timeout 5 https://www.google.com | Out-Null
            Write-Host 'proxy test ok'
            return
        }

        $cfg = Get-ProxyConfig
        Invoke-WebRequest 'https://www.google.com' -Method Head -TimeoutSec 5 -Proxy $cfg.HttpProxy | Out-Null
        Write-Host 'proxy test ok'
    }
    catch {
        Write-Host $_.Exception.Message
    }
}
"@ | Set-Content -Encoding UTF8 (Join-Path $psDir 'proxy.ps1')

# 4) 把加载逻辑写入 PowerShell 5.1 和 PowerShell 7（兼容 OneDrive / 本地 Documents）
$profileCandidates = @(
    (Join-Path $HOME 'OneDrive\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'),
    (Join-Path $HOME 'Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1'),
    (Join-Path $HOME 'OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1'),
    (Join-Path $HOME 'Documents\PowerShell\Microsoft.PowerShell_profile.ps1')
) | Select-Object -Unique

$loader = @"
$proxyScript = Join-Path $HOME '.config\powershell\proxy.ps1'
if (Test-Path $proxyScript) {
    . $proxyScript
}
"@

foreach ($profilePath in $profileCandidates) {
    $profileDir = Split-Path -Parent $profilePath
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null

    if (-not (Test-Path $profilePath)) {
        New-Item -ItemType File -Path $profilePath -Force | Out-Null
    }

    $current = Get-Content $profilePath -Raw
    if ($current -notmatch [regex]::Escape("Join-Path `$HOME '.config\\powershell\\proxy.ps1'")) {
        Add-Content -Path $profilePath -Value "`r`n$loader"
    }
}

# 5) 当前会话立即生效
. $PROFILE
```

### 日常使用

```powershell
proxy
testproxy
unproxy
```

### 说明

- `proxy` / `unproxy` 会设置或清理当前 shell 的环境变量。
- 同时会设置或清理 Git / npm 的全局代理。
- 如果你要改端口（例如 `7890`），只需要改 `config.psd1`。



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