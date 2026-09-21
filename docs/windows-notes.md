# Windows使用笔记

2019-02-12


## Terminal 配置

https://www.freecodecamp.org/news/windows-terminal-themes-color-schemes-powershell-customize/

`font` 在新版中改为嵌套的 `face` / `size`（旧版的 `fontFace` / `fontSize` 已废弃）：

```json
{
    "profiles": {
        "defaults": {
            "opacity": 80,
            "useAcrylic": true,
            "useAtlasEngine": true,
            "font": {
                "face": "Maple Mono NF CN",
                "size": 12
            },
            "experimental.retroTerminalEffect": false
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

scoop bucket add extras
scoop bucket add nerd-fonts


# 代理配置
scoop config proxy 127.0.0.1:7777
scoop config rm proxy

```


## PowerShell 支持 ll

```powershell
Set-Alias -Name ll -Value Get-ChildItem
Set-Alias -Name l -Value Get-ChildItem
```

`ll` 等价于 `ls`，Windows 上 `ls` 本身就是 `Get-ChildItem` 的别名，所以写成 `Set-Alias ll ls` 也可以。



## PowerShell 代理（可迁移配置）

建议把代理配置放在用户目录，查看当前 shell 的 profile 路径：

```powershell
$PROFILE
```

上面返回的地址可能在 OneDrive 下，但本地版本的也会被识别。

配置地址 `~/Documents/PowerShell/Microsoft.PowerShell_profile.ps1`

下面的写法**只改当前会话的环境变量**，不写 `git` / `npm` 的全局配置文件。
这样忘记 `unproxy` 就关掉终端时，不会留下一份永久生效的代理设置。
git 的代理交给 `~/.gitconfig` 自行管理（可以在那里针对 GitHub 单独配置）。

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

    Write-Host '✅ 代理已开启 (127.0.0.1:7777) — 仅当前会话'
}

function unproxy {
    'http_proxy', 'https_proxy', 'all_proxy',
    'HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY' | ForEach-Object {
        Remove-Item "Env:$_" -ErrorAction SilentlyContinue
    }

    Write-Host '❌ 代理已关闭 — 仅当前会话'
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

如果只想给 GitHub 走代理，在 `~/.gitconfig` 里单独配置，与上面的会话级代理互不干扰：

```ini
[http "https://github.com"]
    proxy = socks5://127.0.0.1:7777
```

当前会话立即生效：

```powershell
. $PROFILE
```


## PowerShell 7 与 Windows PowerShell 5.1

Windows 自带的是 **Windows PowerShell 5.1**（`powershell.exe`），它和 **PowerShell 7**（`pwsh.exe`）是两个不同的产品，不是同一个软件的新旧版本：

| | Windows PowerShell 5.1 | PowerShell 7 |
|---|---|---|
| 可执行文件 | `powershell.exe` | `pwsh.exe` |
| 运行时 | .NET Framework | .NET（Core） |
| PSEdition | `Desktop` | `Core` |
| 平台 | 仅 Windows | Windows / macOS / Linux |

5.1 依赖 .NET Framework，而后者是 Windows 的系统组件，因此 5.1 被固定在系统里且**不再有新功能**（版本号永远是 5.1.x）。7 是独立产品，需要单独安装，两者并存。系统自带版本号里那串大数字是 Windows 的构建号，不是 PowerShell 自身的版本。

### 用 scoop 安装（免安装器）

```powershell
scoop install pwsh
```

scoop 用的是官方 zip 包，不需要安装器，适合有软件安装策略限制的机器。

### 注意：PS7 会污染子进程的 PSModulePath

PS7 启动时会把自身的模块目录写进 `PSModulePath`，并传给所有子进程。这些目录下的 `psd1` 声明了 `CompatiblePSEditions = "Core"`，当 **5.1 作为子进程**继承该变量时，会优先命中同名模块的 PS7 清单并**静默降级**——命令凭空消失，且不报错。

典型症状：`Get-FileHash`、`Get-ExecutionPolicy` 找不到，导致 `scoop` 报 `Hash check failed`。

排查：

```powershell
# 在 5.1 里执行，若返回 False 即中招
[bool](Get-Command Get-FileHash -ErrorAction SilentlyContinue)
```

解决：在 PS7 的 profile 开头把该目录从导出给子进程的环境里摘掉（PS7 自身的模块经 `$PSHOME` 内部解析，不受影响）：

```powershell
$env:PSModulePath = (
    $env:PSModulePath -split ';' |
        Where-Object { $_ -and $_.TrimEnd('\') -ne (Join-Path $PSHOME 'Modules').TrimEnd('\') }
) -join ';'
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


## Eudic 欧路字典

可以直接修改配置来更改欧路字典的主题和字体。原本这里需要开会员才能做到。

> C:\Users\aac\AppData\Roaming\Francochinois\eudic\config.ini

```ini
ColorStyle=black
ColorStyle2=sepia 这里填写 Black 或者 Night 就行了
FontFamily=Maple Mono NF CN
```

