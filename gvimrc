" The commands in this are executed when the GUI is started.

" Make external commands work through a pipe instead of a pseudo-tty
"set noguipty

set visualbell
set number

set encoding=utf-8
set guifont=Andale\ Mono\ 12

" winpos 600 30

set lines=71
set columns=106

" Make command line two lines high
set cmdheight=3
set listchars=trail:■,extends:>,precedes:<,tab:❱➝ list

set background="dark"

  " Switch on syntax highlighting.
syntax enable

  " Switch on search pattern highlighting.
set hlsearch
:map <F7> :set hls!<CR>

  " Hide the mouse pointer while typing
set mousehide
set mousefocus

colorscheme kwdcolors

if v:progname == "Vim"
	set cursorcolumn
	map <M-Left> :bp<CR>
	map <M-Right> :bn<CR>
	map <M-Del> :bd<CR>
	map ZZ :bd<CR>
endif

if &diff
   set columns=212
   nmap ZZ :qall<CR>
endif

