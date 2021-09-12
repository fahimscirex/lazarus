#!/bin/bash

# Terminate already running bar instances
killall -q polybar

# Wait until the processes have been shut down

polybar -r -c $HOME/.config/polybar/transparent/config bar &

echo "Polybar launched..."
