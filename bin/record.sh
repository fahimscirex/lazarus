#!/bin/bash

ffmpeg \
-f x11grab \
-s 1920x1080 \
-i :0.0 \
-an \
-c:v libvpx \
-b:v 5M \
-crf 25 \
-quality realtime \
-preset slower \
-y ~/Videos/Cheese-:$(date +%F-%I-%M.mkv)
