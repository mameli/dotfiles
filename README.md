# dotfiles
vim, zsh config files

## Vim Plugins
`
:PlugInstall 
`

```
cd ~/.vim/plugged/youcompleteme/
sudo apt install build-essential cmake python3-dev
python install.py
```


## Theme
```
sudo add-apt-repository ppa:papirus/papirus
sudo apt-get update
sudo apt-get install papirus-icon-theme
```

## Zsh shell
```
sudo apt install zsh
chsh -s $(which zsh)
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

cd .oh-my-zsh/themes
wget https://gist.githubusercontent.com/xfanwu/18fd7c24360c68bab884/raw/f09340ac2b0ca790b6059695de0873da8ca0c5e5/xxf.zsh-theme

source ~/.zshrc
```

## Fish shell
```
sudo apt-get install fish
chsh -s /usr/local/bin/fish
[oh my fish](https://github.com/oh-my-fish/oh-my-fish)
```
## Neofetch
```
sudo apt install neofetch
```
## tlp
```
sudo add-apt-repository ppa:linrunner/tlp
sudo apt-get update
sudo apt-get install tlp
```
## Htop
```
sudo apt-get install htop
```
## lm-sensors
```
sudo apt-get install lm-sensors
```
## Vim e git
```
sudo apt-get install vim

sudo apt-get install git
```

## Matlab

conda activate jmatlab

## Power saver audio
sudo vim /etc/default/tlp
SOUND_POWER_SAVE_ON_BAT=0