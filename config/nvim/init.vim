"|=================|
"|  P L U G I N S  |
"|=================|

call plug#begin('~/.local/share/nvim/autoload/plugged')
  " UI
  Plug 'shaunsingh/nord.nvim'
  Plug 'ap/vim-css-color'
  Plug 'sheerun/vim-polyglot'
  Plug 'kyazdani42/nvim-tree.lua'
  Plug 'kyazdani42/nvim-web-devicons'
  Plug 'bling/vim-airline'
  Plug 'vim-airline/vim-airline-themes'

  " IDE
  Plug 'easymotion/vim-easymotion'
  Plug 'christoomey/vim-tmux-navigator'
  Plug 'neoclide/coc.nvim', {'branch': 'release'}
  Plug 'lukas-reineke/indent-blankline.nvim'
  Plug 'jiangmiao/auto-pairs' 
  Plug 'mattn/emmet-vim'
call plug#end()


" Indent blankline
let g:indent_blankline_show_first_indent_level = v:false
" " let g:indentLine_char_list = ['▏', '│', '|', '¦', '┆', '┊']
let g:indentLine_char = '│'


" Colorscheme
if has('termguicolors')
  set termguicolors
endif
let g:nord_contrast = v:true
let g:nord_borders = v:false
let g:nord_disable_background = v:true
let g:nord_italic = v:true
colorscheme nord
" Airline Theme
let g:airline_theme='base16_nord'


" Nvim Tree
let g:nvim_tree_auto_close = 1
let g:nvim_tree_quit_on_open = 1
let g:nvim_tree_symlink_arrow = ' -> '


" Easymotion
let mapleader=" "


"|=========================|
"|  N V I M   C O N F I G  |
"|=========================|

syntax enable
set nocompatible
set mouse=a 
set encoding=utf-8
set clipboard=unnamedplus

" Indentation 
set tabstop=2 
set shiftwidth=2
set softtabstop=2
set expandtab
set autoindent

" UI 
set number 
set showcmd
set ruler
set cmdheight=1
set cursorline
set wildmenu
set showmatch
set confirm
set laststatus=1
set cc=80         " set an 80 column border for good coding style
set splitbelow    " when splitting horizontally, show split window on bottom
set splitright
"set noshowmode

" Searching
set incsearch
set hlsearch
set ignorecase
set smartcase


"|=========================|
"|  K E Y B I N D I N G S  |
"|=========================|

" Move cursor in input mode
imap <A-h> <left>
imap <A-j> <down>
imap <A-k> <up>
imap <A-l> <right>

nmap <Leader>f  <Plug>(easymotion-s2)
nmap <Leader>s  :split 
nmap <Leader>v  :vsplit 
nmap <Leader>q  :q<CR> 
nmap <Leader>w  :w<CR> 
nmap <Leader>t  :NvimTreeToggle<CR>

" Toggle terminal on/off (neovim)
nnoremap <A-CR> :call TermToggle(12)<CR>
inoremap <A-CR> <Esc>:call TermToggle(12)<CR>
tnoremap <A-CR> <C-\><C-n>:call TermToggle(12)<CR>

" Terminal go back to normal mode
tnoremap <Esc> <C-\><C-n>
tnoremap :q! <C-\><C-n>:q!<CR>


"|=====================|
"|  F U N C T I O N S  |
"|=====================|

" Footer Terminal 
let g:term_buf = 0
let g:term_win = 0
function! TermToggle(height)
  if win_gotoid(g:term_win)
    hide
  else
    botright new
    exec "resize " . a:height
    try
      exec "buffer " . g:term_buf
    catch
      call termopen($SHELL, {"detach": 0})
      let g:term_buf = bufnr("")
      set nonumber
      set norelativenumber
      set signcolumn=no
    endtry
    startinsert!
    let g:term_win = win_getid()
  endif
endfunction

