
# Telegram Bot Linux Manager
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-blue)
![Python](https://img.shields.io/badge/Python-3.10.12-blue)
![Pip](https://img.shields.io/badge/Pip-22.0.2-blue)
![Telegram bot](https://img.shields.io/badge/Telegram_bot-13.13-blue)
![dotenv](https://img.shields.io/badge/dotenv-blue)
![pyyaml](https://img.shields.io/badge/pyyaml-blue)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
  - [Install Python](#install-python)
  - [Install Pip](#install-pip)
  - [Install Python Libraries](#install-python-libraries)
- [Set Up Source Code](#set-up-source-code)
- [Set Up Service](#set-up-service)
- [Run Service](#run-service)

## Introduction

- Author: Nguyễn Trọng Đại
- Company: CDB-Tech (https://cdb-tech.com)
- License: Free forever

This project provides detailed instructions on how to install and set up a Telegram Bot Manager service on Ubuntu 22.04. This service is written in Python and uses the `python-telegram-bot`, `dotenv`, and `yaml` libraries.

## Installation

### Install Python
Install Python 3.10.12 on Ubuntu 22.04
```sh
# Update package list
sudo apt update

# Install Python 3.10.12
sudo apt install -y python3.10
```

### Install Pip
Install pip, the package manager for Python
```sh
# Install pip for Python 3.10
sudo apt install -y python3-pip

# Check pip version
pip3 --version
# Pip version: 22.0.2
```

### Install Python Libraries
Use pip to install the necessary Python libraries.
```sh
# Install python-telegram-bot
pip3 install python-telegram-bot==13.13

# Install dotenv
pip3 install python-dotenv

# Install PyYAML
pip3 install pyyaml
```

## Set Up Source Code
Install git:
```sh
sudo apt install git -y
```

Create a directory for the source code:
```sh
mkdir /python-app
```

Clone the repository:
```sh
cd /python-app
git clone https://github.com/nguyentrongdai12/Telegram-bot-linux-manager.git
```

Configure the Telegram Bot Token:
```sh
nano /python-app/Telegram-bot-linux-manager/.env
```

Add your Telegram Bot Token:
```ini
BOT_TOKEN=<Your bot token>
HELP_FILE="library/help.txt"
SHELL_CONFIG="library/shell-config.yml"
CHAT_ID=<Your chat ID Group>
```

## Set Up Service
Create a service file for system management and to run the service.
```sh
# Create a new service file
sudo nano /etc/systemd/system/telegram-bot-manager.service
```

Add the following content to the file:

```ini
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=root
WorkingDirectory=/python-app/Telegram-bot-linux-manager
ExecStart=/usr/bin/python3 /python-app/Telegram-bot-linux-manager/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Save and close the file. Then execute the following commands to reload the services and start your service.

```sh
# Reload systemd services
sudo systemctl daemon-reload

# Start the service
sudo systemctl start telegram-bot-manager

# Enable the service to start on boot
sudo systemctl enable telegram-bot-manager
```

## Run Service

After setting up, you can check the status of the service with the command:
```sh
# Run service
sudo systemctl start telegram-bot-manager

# Check status service
sudo systemctl status telegram-bot-manager
```

