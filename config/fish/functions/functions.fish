function c
  clear $argv
end

## Pacman

function in -d "Install ackage"
  yay -S $argv
end

function out -d "Remove ackage"
  yay -Rcns $argv
end

function orphan -d "Remove orphaned package"
  sudo pacman -Qdtq | sudo pacman -Rs - $argv
end

function search -d "Search package"
  yay -Ss $argv
end

## Systemd

function sc
  systemctl $argv
end

function scs
  systemctl start $argv
end

function scr
  systemctl restart $argv
end

function scx
  systemctl stop $argv
end

function scu
  systemctl --user $argv
end

function rank -d "Rank and sort mirrorlist" 
  scr rankmirror@{,chaotic-}mirrorlist.service $argv
end

function off -d "Poweroff system"
  systemctl poweroff -i $argv
end

function boot -d "Reboot system"
  systemctl reboot -i $argv
end

## Termbin

function paste -d "Pastes output to ix.io"
  curl -F 'f:1=<-' ix.io $argv
end

## youtube-dl

function ytv -d "Downloads YouTube video"
  yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' --embed-metadata --embed-thumbnail --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M' $argv
end

function ytm -d "Extracts audio from YouTube"
  yt-dlp --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M' -x --audio-format mp3 --embed-metadata --embed-thumbnail $argv
end

function audiobook -d "Extracts audibook shows to my sdcard path"
  yt-dlp --external-downloader aria2c --external-downloader-args '-c -j 3 -x 3 -s 3 -k 1M' -x --audio-format mp3 --embed-metadata --embed-thumbnail --no-playlist -o /run/media/fahim/AudioPhile/Audiobook/%(title)s.%(ext)s $argv 
end

# Cloudflare Warp
function won
  warp-cli connect $argv
end

function woff
  warp-cli disconnect $argv
end
