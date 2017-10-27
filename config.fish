function hdfix
	sudo ntfsfix /dev/sdb1
end

function fishconfig
	vim ~/.config/fish/config.fish
end

function lastcommit
	git log -1
end

set PATH /home/mameli/.anaconda3/bin $PATH
set -gx TERM screen-256color-bce
