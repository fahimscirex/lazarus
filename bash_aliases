# ls
alias l='ls -lh'
alias ll='ls -lah'
alias la='ls -A'
alias lm='ls -m'
alias lr='ls -R'
alias lg='ls -l --group-directories-first'

# git
alias gcl='git clone --depth 1'
alias gi='git init'
alias ga='git add'
alias gc='git commit -m'
alias gp='git push origin master'

alias c="clear"
alias q="exit"
alias hd="hexdump -C"
alias default-apps="clear && ~/.scripts/default-apps/launch && ~/.scripts/default-apps/launch -e"

# pacman
alias pill="sudo powerpill -S"
alias up="sudo pacman -Sy && sudo powerpill -Su && yay"
alias in="yay -S"
alias search="yay -Ss"
alias yayupd="yay -Sy"
alias yayupg="yay -Syu"
alias out="yay -Rcns"
alias orphan="sudo pacman -Qdtq | sudo pacman -Rs -"

alias emergeins="$PRIV emerge -av"
alias emergepv="$PRIV emerge -pv"
alias emergeupd="$PRIV emaint -a sync"
alias emergeupg="$PRIV emerge -av --update --deep --changed-use @world"
alias emergedepc="$PRIV emerge --depclean -av"
alias emergenuse="$PRIV emerge -av --update --newuse --deep @world"
alias emergecuse="$PRIV emerge -av --update --changed-use --deep @world"
alias ecleandist="$PRIV eclean-dist --deep"
alias ecleankern="$PRIV eclean-kernel -n 3"
alias rc-service="$PRIV rc-service"
alias rc-update="$PRIV rc-update"
alias pingoogle="ping 8.8.8.8"
alias trimall="$PRIV fstrim -va"
alias nanosu="$PRIV nano"
alias nvimsu="$PRIV nvim"

# Power
alias off="systemctl poweroff -i"
alias boot="systemctl reboot -i"

# Term paste
alias paste="curl -F 'sprunge=<-' http://sprunge.us"
alias termbin="nc termbin.com 9999 <"

# YouTube-dl
alias ydl="youtube-dl -x --audio-format mp3 --prefer-ffmpeg"
alias yvid="youtube-dl --merge-output-format mp4"

# WGCF
alias won="wg-quick up wgcf-profile"
alias woff="wg-quick down wgcf-profile"
alias wforce="sudo rm -rf wgcf-profile.conf && wgcf generate && sudo rm -rf /etc/wireguard/wgcf-profile.conf && sudo cp wgcf-profile.conf /etc/wireguard"

# Energized
alias eng="sudo sh ~/Downloads/scripts/energized.sh"

# ytfzf
alias yt="ytfzf -s -t -f --preview-side=left"

# Anbox Container
alias anon="sudo systemctl start anbox-container-manager.service"
alias anoff="sudo systemctl stop anbox-container-manager.service"

# Systemd
alias sc="systemctl"
alias scs="systemctl start"
alias scst="systemctl stop"
alias scu="systemctl --user"
alias rank="sc restart rankmirror@{chaotic-,}mirrorlist.service"

# zoxide
alias z="zoxide"
