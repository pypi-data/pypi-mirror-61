#!/usr/bin/env bash
#
# bash completion file for hello
#
# This script provides completion of:
#  - commands and their options
#
# To enable the completions either:
#  - place this file in /etc/bash_completion.d
#  or
#  - copy this file to e.g. ~/.hello-completion.sh and add the line
#    below to your .bashrc after bash completion features are loaded
#    . ~/.hello-completion.sh
#

_hello()
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="-d --debug -h --help -t --title --version"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _hello hello
