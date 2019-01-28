function fishconfig
	vim ~/.config/fish/config.fish
end

function lastcommit
	git log -1
end

set PATH /opt/miniconda3/bin $PATH 
# Virtual env
source /opt/miniconda3/etc/fish/conf.d/conda.fish

set -gx TERM screen-256color-bce
