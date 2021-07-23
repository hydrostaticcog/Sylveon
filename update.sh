#!/bin/bash
git reset --hard origin/master
sudo chmod +x bot.py
sudo chmod +x start.sh
sudo chmod +x update.sh
sudo systemctl restart sylveon.service
