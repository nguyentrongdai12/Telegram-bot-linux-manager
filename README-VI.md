# Telegram bot linux manager
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-blue)
![Python](https://img.shields.io/badge/Python-3.10.12-blue)
![Pip](https://img.shields.io/badge/Pip-22.0.2-blue)
![Telegram bot](https://img.shields.io/badge/Telegram_bot-13.13-blue)
![dotenv](https://img.shields.io/badge/dotenv-blue)
![pyyaml](https://img.shields.io/badge/pyyaml-blue)

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
  - [Cài đặt Python](#cài-đặt-python)
  - [Cài đặt Pip](#cài-đặt-pip)
  - [Cài đặt Các Thư Viện Python](#cài-đặt-các-thư-viện-python)
- [Thiết lập mã nguồn](#thiết-lập-mã-nguồn)
- [Thiết lập Service](#thiết-lập-service)
- [Chạy Dịch Vụ](#chạy-dịch-vụ)

## Giới thiệu

- Tác giả: Nguyễn Trọng Đại
- Doanh Nghiệp: CDB-Tech (https://cdb-tech.com)
- Bản quyền: Miễn phí

Dự án này cung cấp hướng dẫn chi tiết về cách cài đặt và thiết lập một dịch vụ Telegram-bot-manager trên Ubuntu 22.04. Dịch vụ này được viết bằng Python và sử dụng các thư viện `python-telegram-bot`, `dotenv`, và `yaml`.

## Cài đặt

### Cài đặt Python
Cài đặt Python 3.10.12 trên Ubuntu 22.04
```sh
# Cập nhật danh sách gói
sudo apt update

# Cài đặt Python 3.10.12
sudo apt install -y python3.10
```
### Cài đặt Pip
Cài đặt pip, công cụ quản lý gói cho Python
```sh
# Cài đặt pip cho Python 3.10
sudo apt install -y python3-pip

# Kiểm tra phiên bản pip
pip3 --version
# Phiên bản pip: 22.0.2
```
### Cài đặt Các Thư Viện Python
Sử dụng pip để cài đặt các thư viện Python cần thiết.
```sh
# Cài đặt python-telegram-bot
pip3 install python-telegram-bot==13.13

# Cài đặt dotenv
pip3 install python-dotenv

# Cài đặt PyYAML
pip3 install pyyaml
```

## Thiết lập mã nguồn
Cài đặt git:
```sh
sudo apt install git -y
```
Tạo thư mục chứa mã nguồn:
```sh
mkdir /python-app
```
Tải mã nguồn:
```sh
cd /python-app
git clone https://github.com/nguyentrongdai12/Telegram-bot-linux-manager.git
```
Cấu hình TOKEN Bot Telegram
```sh
nano /python-app/Telegram-bot-linux-manager/.env
```
Thêm Token Bot Telegram của bạn:
```ini
BOT_TOKEN=<Your bot token>
HELP_FILE="library/help.txt"
SHELL_CONFIG="library/shell-config.yml"
```

## Thiết lập Service
Tạo file service để hệ thống quản lý và chạy dịch vụ.
```sh
# Tạo một file service mới
sudo nano /etc/systemd/system/telegram-bot-manager.service
```
Thêm nội dung sau vào file:

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
Lưu và đóng file. Sau đó, thực hiện các lệnh sau để reload các service và khởi động dịch vụ.

```sh
# Reload các dịch vụ systemd
sudo systemctl daemon-reload

# Khởi động dịch vụ
sudo systemctl start telegram-bot-manager

# Kích hoạt dịch vụ để nó tự khởi động cùng hệ thống
sudo systemctl enable telegram-bot-manager
```

## Chạy Dịch Vụ
Sau khi thiết lập, bạn có thể kiểm tra trạng thái của dịch vụ bằng lệnh:
```sh
sudo systemctl status telegram-bot-manager
```
