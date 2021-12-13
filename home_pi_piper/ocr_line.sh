#!/bin/bash

# -*- coding: utf-8 -*-
source /home/pi/piper/config.txt

input_file="/home/pi/piper/image.jpg"
token=$TOKEN

raspistill -o $input_file -n -t 3000

python3 ./image_preprocessing.py

python3 ./ocr.py

photo_file="/home/pi/piper/output.jpg"

curl -X POST -H "Authorization: Bearer ${token}" -F "message = ラズパイから画像を送ります" -F "imageFile=@${photo_file}" https://notify-api.line.me/api/notify
