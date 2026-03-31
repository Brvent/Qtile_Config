#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return
alias ls='ls --color=auto'
alias grep='grep --color=auto'
PS1='[\u@\h \W]\$ '
alias scrot='scrot "/home/user/Pictures/screenshots/captura_%Y-%m-%d_%H-%M-%S.png"'
alias scrot-s='scrot -s "/home/user/Pictures/screenshots/captura_%Y-%m-%d_%H-%M-%d_%H-%M-%S.png"'

#PATH de teXlive
PATH="/usr/local/texlive/2024/bin/x86_64-linux:$PATH"

export QSYS_ROOTDIR="/home/user/Programs/Quartus/quartus/sopc_builder/bin"
export EDITOR=vim
export PATH="/usr/bin/fortls:$PATH"

#PATH para versiones de python "pyenv"
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"


