" Vim filetype plugin file
" Language:	Java

" set up 2 space spacing for Google style.
function GoogleJava()
    hi SpecialKey guifg=Red
    :set ts=2 sw=2 tw=99
    :set expandtab softtabstop=2 smarttab
    :set listchars=trail:■,extends:>,precedes:<,tab:❱➝ list
endfunction

:call GoogleJava()

