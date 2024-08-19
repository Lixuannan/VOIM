:command -nargs=1 RunCode !~/.vim/plugged/VOIM/lib/VOIM.py <q-args>

map <F5> :RunCode %<CR>
imap <F5> <esc> :RunCode % <CR>
vmap <F5> <esc> :RunCode % <CR>

