#!/usr/bin/env bash

killall -q polybar

echo "---" | tee -a /tmp/polybar1.log
polybar -c $HOME/.config/polybar/neko/config example >> /tmp/polybar1.log 2>&1 &

echo "Bars launched..."
