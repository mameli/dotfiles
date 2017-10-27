#!/bin/bash

echo "Copying .config.fish"
rm  ~/.config/fish/config.fish
cp ./config.fish ~/.config/fish/config.fish 

echo "Copying .zshrc config"
rm ~/.zshrc
cp ./.zshrc ~/.zshrc

echo "Copying .vimrc config"
rm ~/.vimrc
cp ./.vimrc ~/.vimrc

echo "Copying .tmux.config"
rm ~/.tmux.conf  
cp ./.tmux.conf ~/.tmux.conf
