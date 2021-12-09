#!/usr/bin/env python3
# coding=utf-8
from requests.api import delete
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from Command import *
from dotenv import load_dotenv
from updater import updater

load_dotenv()

# Main function
def main():
    

# 一般指令

    # 開啟與幫助
    updater.dispatcher.add_handler(CommandHandler('start', startbot))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    
    # 新增 (可在 Database.db/Config 中，設定為管理員限定)
    updater.dispatcher.add_handler(CommandHandler('add', add))
    
    # 刪除 (可在 Database.db/Config 中，設定為管理員限定)
    
    # 搜尋
    updater.dispatcher.add_handler(CommandHandler('result', result))
    updater.dispatcher.add_handler(CommandHandler('poll', poll))
    # updater.dispatcher.add_handler(CommandHandler('get', GetData))


# 其他類型回覆

    # 文字
    updater.dispatcher.add_handler(MessageHandler(Filters.text, getText))
    
    # 按鈕
    updater.dispatcher.add_handler(CallbackQueryHandler(callback))


# Bot Start
    print("Bot Server Running...")

    updater.start_polling()
    updater.idle()


# HEAD OF PROGRAM
if __name__ == '__main__':
    main()

