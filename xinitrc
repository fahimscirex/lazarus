#!/bin/sh

[[ -f ~/.config/X11/xresources ]] && xrdb -merge ~/.config/X11/xresources
[[ -f ~/.config/X11/xkbmap ]] && setxkbmap ~/.config/X11/xkbmap
[[ -f ~/.config/X11/xprofile ]] && . ~/.config/X11/xprofile
