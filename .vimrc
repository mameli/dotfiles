syntax on
colorscheme monokai
:set number

call plug#begin('~/.vim/plugged')

Plug 'crusoexia/vim-monokai'

Plug 'JuliaEditorSupport/julia-vim'

Plug 'airblade/vim-gitgutter'

Plug 'tpope/vim-sensible'

Plug 'tpope/vim-fugitive'

Plug 'valloric/youcompleteme'

Plug 'tpope/vim-surround'

Plug 'scrooloose/syntastic'
" On-demand loading
Plug 'scrooloose/nerdtree', { 'on': 'NERDTreeToggle' }
call plug#end()
