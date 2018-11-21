function fishconfig
	vim ~/.config/fish/config.fish
end

function lastcommit
	git log -1
end

set PATH ~/snap/bin $PATH
set PATH ~/anaconda3/bin $PATH
set -gx TERM screen-256color-bce
