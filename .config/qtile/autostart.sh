#!/bin/sh

#Spanish keyboard configuration
setxkbmap es &

#background wallpaper (feh dependence)
feh --bg-fill ~/Pictures/wallpapers/australian_water_dragon.jpg &

#system bar icons

udiskie -t & #automounter for removable media bar

nm-applet & #network connection manager bar

pasystray & #volume control bar

cbatticon -u 5 & #battery icon bar

blueman-applet & #BLueetooth connect bar

picom & #terminal-transparence config

parcellite & #clipboard
