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

git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting

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

## Font
sudo apt-get install fonts-cascadia-code

## Scrool fix
sudo apt install imwheel
bash <(curl -s http://www.nicknorton.net/mousewheel.sh)
imwheel -b "4 5"

## wsl fix cloudera
touch .wslconfig

[wsl2]
kernelCommandLine = vsyscall=emulate

wsl --shutdown

docker run --hostname=quickstart.cloudera --privileged=true -t -i -v /Users/mameli/cloudera-files:/cloudera
-files --publish-all=true -p 8888:8888 -p 80:80 cloudera/quickstart /usr/bin/docker-quickstart
