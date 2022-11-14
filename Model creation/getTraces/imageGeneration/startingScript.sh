#!/bin/bash
Xvfb -ac :99 -screen 0 1280x1024x16 & disown
export DISPLAY=:99
python3 /root/getTraces.py