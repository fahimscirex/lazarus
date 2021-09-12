# load zgenom
source "$HOME/.zgenom/zgenom.zsh"
source "$HOME/.bash_aliases"

# if the init scipt doesn't exist
if ! zgenom saved; then
    echo "Creating a zgenom save"

    zgenom oh-my-zsh

    # plugins
    zgenom loadall <<EOPLUGINS
	zsh-users/zsh-autosuggestions 
	ChrisPenner/copy-pasta
	marzocchi/zsh-notify
	le0me55i/zsh-systemd
	laggardkernel/zsh-thefuck
	nviennot/zsh-vim-plugin
EOPLUGINS

    # omz plugins
    zgenom oh-my-zsh plugins/git
    zgenom oh-my-zsh plugins/sudo
    
    # theme
    zgen load spaceship-prompt/spaceship-prompt spaceship

    # save all to init script
    zgenom save
fi
