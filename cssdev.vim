if ! has("python3")
  echomsg "*** no Python!"
  finish
endif

if exists("g:cssdev_loaded")
  finish
endif
:let g:cssdev_loaded = 1


set ts=4 sw=4 tw=100 expandtab softtabstop=4 smarttab
set formatoptions=crql cino=(8 ai smartindent
set comments=s1:/*,mb:*,ex:*/,b://
set iskeyword=@,#,48-57,_,^;
set omnifunc=csscomplete#CompleteCSS

