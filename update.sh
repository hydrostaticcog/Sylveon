#!/bin/bash
git fetch
git reset --hard origin/master
./venv/bin/pip install -U -r requirements.txt
sudo chmod +x bot.py
sudo chmod +x start.sh
sudo chmod +x update.sh
sudo systemctl restart sylveon.service
