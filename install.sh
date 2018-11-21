#!/bin/bash
apt-get install git

apt-get install vim

sudo apt-get install fish

apt-get install htop

apt-get install lm-sensors

echo "Copying .config.fish"
cp ./config.fish ~/.config/fish/config.fish 

echo "Copying .vimrc config"
cp ./vimrc ~/.vim/vimrc