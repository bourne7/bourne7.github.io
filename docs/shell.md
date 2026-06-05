# Shell 配置指南


## oh-my-zsh

### 安装 oh-my-zsh 插件

```bash
# 1. 创建 custom 插件目录（如果不存在）
mkdir -p ~/.oh-my-zsh/custom/plugins

# 2. 克隆三个插件（只克隆最新提交）
git clone --depth 1 https://github.com/zsh-users/zsh-autosuggestions ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions
git clone --depth 1 https://github.com/zsh-users/zsh-syntax-highlighting ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting
git clone --depth 1 https://github.com/marlonrichert/zsh-autocomplete ~/.oh-my-zsh/custom/plugins/zsh-autocomplete
# 更新这三个插件
git -C ~/.oh-my-zsh/custom/plugins/zsh-autosuggestions pull --ff-only
git -C ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting pull --ff-only
git -C ~/.oh-my-zsh/custom/plugins/zsh-autocomplete pull --ff-only

# 3. 验证插件已安装
ls -la ~/.oh-my-zsh/custom/plugins/
```

### 添加插件到 .zshrc

```bash
nano ~/.zshrc
```

找到 `plugins=(...)` 这一行，改成：

```bash
plugins=(
  git
  zsh-autosuggestions
  zsh-syntax-highlighting
  zsh-autocomplete
)
```

保存退出（`nano`: `Ctrl+X -> Y -> Enter`），然后执行：

```bash
source ~/.zshrc
```

### 注意事项

- 插件顺序很重要：`zsh-syntax-highlighting` 必须放在最后。
- `zsh-autocomplete` 默认启用：因为它可能与前面两个插件有交互问题，建议先稳定运行后再启用。
- 如果启用 `zsh-autocomplete`：删除 `#` 注释符号，然后重新执行 `source ~/.zshrc`。

### 测试是否成功

```bash
# 检查插件是否加载成功
echo $ZSH_CUSTOM/plugins/
ls ~/.oh-my-zsh/custom/plugins/

# 测试自动提示：输入 "git ch" 应该会灰显 "git checkout"
# 测试语法高亮：输入错误的命令应该显示红色
```

## starship

Starship 是一个跨平台、速度很快的终端提示符（prompt），可以在 bash、zsh、fish、powershell 等 shell 中统一显示 Git 分支、语言版本、目录状态等信息。

建议终端字体使用 Nerd Font，否则部分图标可能显示为方块。

```bash
brew install starship

# 然后把初始化命令写入 zsh 配置：
echo 'eval "$(starship init zsh)"' >> ~/.zshrc
source ~/.zshrc
```

生成默认配置文件

```bash
mkdir -p ~/.config
starship preset nerd-font-symbols -o ~/.config/starship.toml
```

常用命令

```bash
# 查看 starship 完整配置说明
starship explain

# 打印当前生效配置
starship print-config

# 检查配置是否可用
starship module character
```
建议终端字体使用 Nerd Font，否则部分图标可能显示为方块。