if ! has("python")
  echomsg "*** no Python 2!"
  finish
endif

if exists("g:Python_loaded")
  finish
endif
let g:Python_loaded = 1
let g:pyindent_nested_paren = '&sw' * 2
let g:pylint_onwrite = 0

" set Vim parameters that suite python best
set tm=2000

set foldmethod=indent
set foldlevel=99

set omnifunc=pythoncomplete#Complete
let g:SuperTabDefaultCompletionType = "context"
set completeopt=menuone,longest,preview

set formatoptions=crql cino=(8#1 ai smartindent nowrap comments=:#
set cinwords=if,elif,else,for,while,try,except,finally,def,class,with

" set up 4 space spacing, flag in red bad whitespace.
function PyUseSpaces()
    hi SpecialKey guifg=Red
    :set ts=4 sw=4 tw=79
    :set expandtab softtabstop=4 smarttab
    :set listchars=trail:■,extends:>,precedes:<,tab:❱➝ list
endfunction

" set up 2 space spacing for Google style.
function GoogleSpaces()
    hi SpecialKey guifg=Red
    :set ts=2 sw=2 tw=79
    :set expandtab softtabstop=2 smarttab
    :set listchars=trail:■,extends:>,precedes:<,tab:❱➝ list
endfunction

" by default, use 4 spaces (PEP-8 style)
:call PyUseSpaces()

:python import os
:python from vimlib.pydev import *
" put VIMSERVER in environment for child python processes to use.
if has("gui_gtk") && has("gui_running")
    :py os.environ["VIMSERVER"] = vim.eval("v:servername")
endif

function Py2()
	let g:flake8_cmd=$HOME . "/bin/flake8-2.7"
	let g:pydoc_cmd = '/usr/bin/pydoc2.7'
    let $PYTHONBIN = "/usr/bin/python2.7"
    python devhelpers.PYTHONBIN = "/usr/bin/python2.7"
  	autocmd BufNewFile            *.py    0r      ~/Templates/Python2.py
endfunction

function Py3()
	let g:flake8_cmd=$HOME . "/bin/flake8-3.6"
	let g:pydoc_cmd = "/usr/local/bin/pydoc3.6"
    let $PYTHONBIN = "/usr/local/bin/python3.6"
    python devhelpers.PYTHONBIN = "/usr/local/bin/python3.6"
  	autocmd BufNewFile            *.py    0r      ~/Templates/Python3.py
endfunction

call Py2()

function! PyClean ()
    normal ma
    :retab
    :%s/\s\+$//eg
    normal 'a
endfunction

let firstline = getline(1)
if firstline =~ 'python2'
    call Py2()
elseif firstline =~ 'python3'
    call Py3()
endif

nmenu Python.Dev.Python\ 2 :call Py2()<CR>
nmenu Python.Dev.Python\ 3 :call Py3()<CR>
nmenu Python.Syntax.Use\ Spaces :call PyUseSpaces()<CR>
nmenu Python.Syntax.No\ Tabs\ (:retab) :%retab<CR>
nmenu Python.Syntax.Clean\ (;cl) :call PyClean()<CR>
nmenu Python.Run.In\ term\ (ru) :update<CR>:python pyterm(vim.current.buffer.name, 0)<CR>
nmenu Python.Run.In\ term\ (interactive)(ri) :update<CR>:python pyterm(vim.current.buffer.name, 1)<CR>
nmenu Python.Run.Interactive\ shell\ (py) :python pyterm()<CR>
nmenu Python.Evaluate\ Line\ (ev) :python print(eval(vim.current.line))<CR>
vmenu Python.Range.Exec\ in\ term\ (et) :python exec_vimrange_in_term(vim.current.range)<CR>
vmenu Python.Range.Eval\ in\ place\ (el) :python vim.current.line = str(eval(vim.current.line))<CR>

let maplocalleader = ';'

" execution/evaluation
nmap <LocalLeader>py :python pyterm()<CR>
nmap <LocalLeader>ru :update<CR>:python pyterm(vim.current.buffer.name, 0)<CR>
nmap <LocalLeader>ri :update<CR>:python pyterm(vim.current.buffer.name, 1)<CR>
nmap <LocalLeader>ev :python print(eval(vim.current.line))<CR>
vmap <LocalLeader>et :python exec_vimrange_in_term(vim.current.range)<CR>
nmap <LocalLeader>el :python vim.current.line = str(eval(vim.current.line))<CR>

" convenient editing macros
nmap <LocalLeader>iv :python insert_viminfo()<CR>
nmap <LocalLeader>ia :python insert__all__()<CR>
nmap <LocalLeader>ed :python keyword_edit()<CR>
nmap <LocalLeader>ei :python import_edit()<CR>
nmap <LocalLeader>ve :python keyword_view()<CR>
vmap <LocalLeader>ed :python visual_edit()<CR>
vmap <LocalLeader>pp :python prettify()<CR>
vmap <LocalLeader>vi :python visual_view()<CR>
nmap <LocalLeader>sp :python keyword_split()<CR>
nmap <F9> :python keyword_split()<CR>
nmap <LocalLeader>he :python keyword_help()<CR>

nmap <LocalLeader>us :call PyUseSpaces()<CR>
nmap <LocalLeader>p2 :call Py2()<CR>
nmap <LocalLeader>p3 :call Py3()<CR>
nmap <LocalLeader>ts :%retab<CR>
vmap <LocalLeader>ts :'<,'>retab<CR>
nmap <LocalLeader>cl :call PyClean()<CR>
