# Shell

## 1. zsh

```
sudo apt install zsh

sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

zsh

cd "$ZSH_CUSTOM/plugins"

git clone https://github.com/zsh-users/zsh-syntax-highlighting.git

git clone https://github.com/zsh-users/zsh-autosuggestions.git

zsh
```

切换 bash 和 zsh

```
chsh -s /bin/bash
chsh -s /bin/zsh
```

## 2. fish

```
sudo apt-get install fish
```

目前看来，有了 fish 以后，zsh 可以不用了。

发现一点，fish 使用 and 来连接2个指令的。所以fish最好还是自己登录的时候用一下，默认的shell还是使用 bash 吧，避免一些命令用不了。

一些设置
```bash
echo "set fish_prompt_pwd_dir_length 0" >> ~/.config/fish/config.fish
echo "alias dockerf='docker-compose down ; docker-compose pull ; docker-compose up -d'" >> ~/.config/fish/config.fish
alias ll="ls -alFh"
```

浏览器设置
```
fish_config
```