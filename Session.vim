vim9script
g:SessionLoad = 1
if &cp | set nocp | endif
var cpo_save: string
cpo_save = &cpo
set cpo&vim
xmap gx <Plug>(open-word-under-cursor)
nmap gx <Plug>(open-word-under-cursor)
xnoremap <Plug>(open-word-under-cursor) <ScriptCmd>vim9.Open(getregion(getpos('v'), getpos('.'), { type: mode() })->join())
nnoremap <Plug>(open-word-under-cursor) <ScriptCmd>vim9.Open(GetWordUnderCursor())
tnoremap <silent> <Plug>(fzf-normal) 
tnoremap <silent> <Plug>(fzf-insert) i
nnoremap <silent> <Plug>(fzf-normal) <Nop>
nnoremap <silent> <Plug>(fzf-insert) i
&cpo = cpo_save
set autoindent
legacy set background=dark
legacy set backupdir=~/.cache/vim/backup//
legacy set clipboard=unnamedplus
legacy set directory=~/.cache/vim/swap//
set fileencodings=ucs-bom,utf-8,default,latin1
set helplang=en
set hidden
set hlsearch
set ignorecase
set incsearch
set laststatus=2
legacy set runtimepath=~/.vim,/usr/share/vim/vimfiles,/usr/share/vim/vim92,/usr/share/vim/vim92/pack/dist/opt/netrw,/usr/share/vim/vimfiles/after,~/.vim/after
set scrolloff=8
set shiftwidth=4
set showmatch
set smartcase
legacy set statusline=%f\ %y\ %m\ %r\ %=%l,%v\ /\ %L\ ||\ %{strftime('%H:%M')}\ 
legacy set suffixes=.bak,~,.o,.info,.swp,.aux,.bbl,.blg,.brf,.cb,.dvi,.idx,.ilg,.ind,.inx,.jpg,.log,.out,.png,.toc
set tabstop=4
legacy set undodir=~/.cache/vim/undo//
set undofile
legacy set wildignore=*.pyc
import autoload '/usr/share/vim/vim92/autoload/dist/ft.vim'
import autoload '/usr/share/vim/vim92/autoload/dist/vim9.vim'
import autoload '/usr/share/vim/vim92/autoload/dist/script.vim'
const so_save: number = &g:so | const siso_save: number = &g:siso | setg so=0 siso=0 | setl so=-1 siso=-1
v:this_session = expand("<sfile>:p")
doautoall SessionLoadPre
var save_splitbelow: bool
var save_splitright: bool
var save_winminheight: number
var save_winminwidth: number
var wipebuf: number = -1
var shortmess_save: string
silent only
silent tabonly
cd ~/Projects/42repo_generale/a_maze_ing
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  wipebuf = bufnr('%')
endif
set shortmess+=aoO
badd +45 a_maze_ing.py
badd +7 src/__init__.py
badd +9 Makefile
badd +1 src/maze/__init__.py
badd +1 src/parser.py
badd +30 src/maze/maze_generator.py
badd +2 config.txt
argglobal
:%argdel
:$argadd a_maze_ing.py
edit a_maze_ing.py
argglobal
balt src/maze/maze_generator.py
setlocal keymap=
setlocal noarabic
setlocal autoindent
legacy setlocal backupcopy=
setlocal balloonexpr=
setlocal nobinary
setlocal nobreakindent
setlocal breakindentopt=
setlocal bufhidden=
setlocal buflisted
setlocal buftype=
setlocal nocindent
legacy setlocal cinkeys=0{,0},0),0],:,!^F,o,O,e
setlocal cinoptions=
setlocal cinscopedecls=public,protected,private
setlocal cinwords=if,else,while,do,for,switch
setlocal colorcolumn=
legacy setlocal comments=b:#,fb:-
legacy setlocal commentstring=#\ %s
setlocal complete=.,w,b,u,t,i
setlocal completefunc=
setlocal completeopt=
setlocal concealcursor=
setlocal conceallevel=0
setlocal nocopyindent
setlocal cryptmethod=
setlocal nocursorbind
setlocal nocursorcolumn
set cursorline
setlocal cursorline
setlocal cursorlineopt=both
legacy setlocal define=^\\s*\\(\\(async\\s\\+\\)\\?def\\|class\\)
setlocal dictionary=
setlocal nodiff
setlocal diffanchors=
setlocal equalprg=
setlocal errorformat=
setlocal eventignorewin=
setlocal expandtab
if &filetype != 'python'
legacy setlocal filetype=python
endif
setlocal fillchars=
setlocal findfunc=
setlocal fixendofline
setlocal foldcolumn=0
setlocal foldenable
setlocal foldexpr=0
setlocal foldignore=#
setlocal foldlevel=4
setlocal foldmarker={{{,}}}
legacy set foldmethod=indent
legacy setlocal foldmethod=indent
setlocal foldminlines=1
setlocal foldnestmax=20
setlocal foldtext=foldtext()
setlocal formatexpr=
setlocal formatlistpat=^\\s*\\d\\+[\\]:.)}\\t\ ]\\s*
legacy setlocal formatoptions=tcq
setlocal formatprg=
setlocal grepformat=
setlocal grepprg=
setlocal iminsert=0
setlocal imsearch=-1
legacy setlocal include=^\\s*\\(from\\|import\\)
legacy setlocal includeexpr=substitute(substitute(substitute(v:fname,b:grandparent_match,b:grandparent_sub,''),b:parent_match,b:parent_sub,''),b:child_match,b:child_sub,'g')
legacy setlocal indentexpr=python#GetIndent(v:lnum)
legacy setlocal indentkeys=0{,0},0),0],:,!^F,o,O,e,<:>,=elif,=except
setlocal noinfercase
legacy setlocal iskeyword=@,48-57,_,192-255
legacy setlocal keywordprg=python3\ -m\ pydoc
setlocal lhistory=10
setlocal nolinebreak
setlocal nolisp
setlocal lispoptions=
setlocal lispwords=
setlocal nolist
setlocal listchars=
setlocal makeencoding=
setlocal makeprg=
setlocal matchpairs=(:),{:},[:]
setlocal modeline
setlocal modifiable
setlocal nrformats=bin,octal,hex
set number
setlocal number
setlocal numberwidth=4
legacy setlocal omnifunc=python3complete#Complete
setlocal path=
setlocal nopreserveindent
setlocal nopreviewwindow
setlocal quoteescape=\\
setlocal noreadonly
setlocal norelativenumber
setlocal norightleft
setlocal rightleftcmd=search
setlocal noscrollbind
setlocal scrolloff=-1
setlocal scrolloffpad=-1
setlocal shiftwidth=4
setlocal noshortname
setlocal showbreak=
setlocal sidescrolloff=-1
setlocal signcolumn=auto
setlocal nosmartindent
setlocal nosmoothscroll
setlocal softtabstop=4
setlocal nospell
setlocal spellcapcheck=[.?!]\\_[\\])'\"\	\ ]\\+
setlocal spellfile=
setlocal spelllang=en
setlocal spelloptions=
legacy setlocal statusline=
setlocal statuslineopt=
legacy setlocal suffixesadd=.py
setlocal swapfile
setlocal synmaxcol=3000
if &syntax != 'python'
legacy setlocal syntax=python
endif
setlocal tabstop=4
legacy setlocal tagcase=
setlocal tagfunc=
setlocal tags=
setlocal termwinkey=
setlocal termwinscroll=10000
setlocal termwinsize=
setlocal textwidth=0
setlocal thesaurus=
setlocal thesaurusfunc=
setlocal undofile
setlocal undolevels=-123456
setlocal varsofttabstop=
setlocal vartabstop=
setlocal virtualedit=
setlocal wincolor=
setlocal nowinfixbuf
setlocal nowinfixheight
setlocal nowinfixwidth
setlocal winhighlight=
setlocal wrap
setlocal wrapmargin=0
:26
sil! normal! zo
:62
sil! normal! zo
{
  var l: number = 45 - ((20 * winheight(0) + 20) / 41)
  if l < 1 | l = 1 | endif
  keepjumps exe ":" .. l
  normal! zt
  keepjumps :45
  normal! 062|
}
tabnext 1
if wipebuf != -1 && len(win_findbuf(wipebuf)) == 0
  silent exe 'bwipe ' .. wipebuf
endif
&winheight = max([1, save_winminheight])
&winwidth = max([20, save_winminwidth])
set shortmess=filnxtToOS
var sx: string = expand("<sfile>:p:r") .. "x.vim"
if filereadable(sx)
  exe "source " .. fnameescape(sx)
endif
&g:so = so_save | &g:siso = siso_save
doautoall SessionLoadPost
unlet g:SessionLoad
# vim: set ft=vim :
