" The commands in this are executed when the GUI is started.

" Make external commands work through a pipe instead of a pseudo-tty
"set noguipty

set visualbell
set number

set encoding=utf-8

" Make command line two lines high
set cmdheight=3
set listchars=trail:■,extends:>,precedes:<,tab:❱➝ list

set background="dark"

  " Switch on syntax highlighting.
syntax enable

set colorcolumn=+1

  " Switch on search pattern highlighting.
set hlsearch
:map <F7> :set hls!<CR>

  " Hide the mouse pointer while typing
set mousehide
set mousefocus

colorscheme kwdcolors

" mvim is a symlink to gvim that's short for multi-buffer gvim. Vim is MacVim
if v:progname == "Vim" || v:progname == "mvim"
	set cursorcolumn
	map <M-Left> :bp<CR>
	map <M-Right> :bn<CR>
	map <M-Del> :bd<CR>
	map ZZ :bd<CR>
endif

runtime gvimrc.local

if &diff
   set columns=212
   nmap ZZ :qall<CR>
endif

