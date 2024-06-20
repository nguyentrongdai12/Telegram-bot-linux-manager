import os
from dotenv import load_dotenv
import yaml
import subprocess
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import re

load_dotenv()
# Lấy mã thông báo API từ biến môi trường
TOKEN = os.getenv("BOT_TOKEN")
CHATID = os.getenv("CHAT_ID")
HELP = os.getenv("HELP_FILE")
SHELL = os.getenv("SHELL_CONFIG")
COMMAND_NAME, COMMAND_SHELL, CONFIRM_DELETE  = range(3)

# Hàm bắt đầu /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome, command basic\n- /help: Show this help message\n- /list_commands: Show the list of configured commands')

# Hàm đọc nội dung của file help.txt
def read_help_content():
    with open(HELP, 'r', encoding='utf-8') as file:
        return file.read()

# Đọc các lệnh từ file YAML
def load_commands():
    with open(SHELL, 'r') as file:
        commands = yaml.safe_load(file)
    return commands

commands = load_commands()

# Hàm phản hồi tin nhắn văn bản
def run(update: Update, context: CallbackContext) -> None:
    matched_command = commands.get(update.message.text.lstrip('/'))
    if matched_command:
        # Thực thi lệnh
        process = subprocess.Popen(matched_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8') + "\n" + stderr.decode('utf-8')
        update.message.reply_text(f'Result:\n{output}')
    else:
        update.message.reply_text("Command not found !!")

# Hàm xử lý lệnh /help
def help_command(update: Update, context: CallbackContext) -> None:
    help_text = read_help_content()
    update.message.reply_text(help_text)

def ls(update: Update, context: CallbackContext) -> None:
    command_list = list(commands.keys())
    if command_list:
        update.message.reply_text("\n".join(command_list))
    else:
        update.message.reply_text("Empty command in config !!")

# Bắt đầu quá trình thêm lệnh mới
def add_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Command Name:')
    return COMMAND_NAME

# Nhận tên lệnh từ người dùng
def get_command_name(update: Update, context: CallbackContext) -> int:
    context.user_data['command_name'] = update.message.text
    update.message.reply_text('Command Detail:')
    return COMMAND_SHELL

# Nhận shell command từ người dùng và lưu vào file YAML
def get_command_shell(update: Update, context: CallbackContext) -> int:
    command_name = context.user_data['command_name']
    command_shell = update.message.text

    commands[command_name] = command_shell
    with open(SHELL, 'w') as file:
        yaml.safe_dump(commands, file)

    update.message.reply_text(f'Command: "{command_name}" added with command shell: "{command_shell}"')
    return ConversationHandler.END

# Hủy quá trình thêm lệnh
def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Cancelled !!.')
    return ConversationHandler.END

def del_command(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Enter command name:')
    return COMMAND_NAME

def confirm_delete(update: Update, context: CallbackContext) -> int:
    command_name = update.message.text
    context.user_data['command_name'] = command_name

    if command_name in commands:
        update.message.reply_text(f'Are you sure delete command name: "{command_name}" (yes/no)')
        return CONFIRM_DELETE
    else:
        update.message.reply_text(f'Command "{command_name}" not found.')
        return ConversationHandler.END

def delete_command(update: Update, context: CallbackContext) -> int:
    if update.message.text.lower() == 'yes':
        command_name = context.user_data['command_name']
        del commands[command_name]
        with open(SHELL, 'w') as file:
            yaml.safe_dump(commands, file)
        update.message.reply_text(f'Delete command "{command_name}" successfully.')
    else:
        update.message.reply_text('Cancelled.')

    return ConversationHandler.END

def restart(update: Update, context: CallbackContext) -> None:
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHATID, text="Restarting ...")
    process = subprocess.Popen('systemctl restart telegram-bot-manager', stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.communicate()

# Thiết lập bot
def main() -> None:
    print("Service is running")
    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHATID, text="Bot started !!!")

    # Tạo Updater và gắn mã thông báo bot
    updater = Updater(TOKEN)

    # Nhận Dispatcher để đăng ký các trình xử lý
    dispatcher = updater.dispatcher

    # Thêm ConversationHandler cho /add_command
    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add_command)],
        states={
            COMMAND_NAME: [MessageHandler(Filters.text & ~Filters.command, get_command_name)],
            COMMAND_SHELL: [MessageHandler(Filters.text & ~Filters.command, get_command_shell)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    del_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('del', del_command)],
        states={
            COMMAND_NAME: [MessageHandler(Filters.text & ~Filters.command, confirm_delete)],
            CONFIRM_DELETE: [MessageHandler(Filters.text & ~Filters.command, delete_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(add_conv_handler)
    dispatcher.add_handler(del_conv_handler)
    # Trình xử lý cho các lệnh /start và /help
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("list", ls))
    dispatcher.add_handler(CommandHandler("restart", restart))

    # Trình xử lý tin nhắn văn bản (lặp lại tin nhắn người dùng)
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.command, run))

    # Bắt đầu bot
    updater.start_polling()

    # Chạy bot cho đến khi người dùng dừng nó
    updater.idle()

if __name__ == '__main__':
    main()

