syntax on
:set number
set term=screen-256color
filetype plugin on
call plug#begin('~/.vim/plugged')

Plug 'crusoexia/vim-monokai'

Plug 'airblade/vim-gitgutter'

Plug 'tpope/vim-sensible'

Plug 'tpope/vim-fugitive'

Plug 'valloric/youcompleteme'

Plug 'tpope/vim-surround'

Plug 'scrooloose/syntastic'

Plug 'scrooloose/nerdcommenter'
" On-demand loading
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
call plug#end()
