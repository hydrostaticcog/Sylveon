#!/bin/bash
cd /home/Glaceon/Sylveon
./venv/bin/python -m pip -U -r requirements.txt
./bot.py > sylveon.log 2>&1
