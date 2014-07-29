if exists("g:jsdev_loaded")
  finish
endif
:let g:jsdev_loaded = 1

set formatoptions=croql  cinoptions=J1 ai smartindent comments=sr:/*,mb:*,el:*/,b:// 
set ts=4 sw=4 tw=100 expandtab softtabstop=4 smarttab
set listchars=trail:·,extends:>,precedes:<,tab:*# list
set omnifunc=javascriptcomplete#CompleteJS

nmap <LocalLeader>js :update<CR>:call system("xnode " . expand("%"))<CR>

