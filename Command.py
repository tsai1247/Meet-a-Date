from os import name
from typing import Dict
from dosdefence import isDos
from function import GetConfig, Send, getRoomID, getUserID
from newFunction import RunDB
from variable import *
import telegramcalendar, utils, messages


def startbot(update, bot):
    if(isDos(update)): return
    Send(update, "hihi, 我是{0}".format(GetConfig("name")))
    Send(update, "按 /help 取得說明")

def help(update, bot):
    if(isDos(update)): return
    Send(update, GetConfig("helpText"))

def add(update, context):
    userID = getUserID(update)
    message = Send(update, "輸入投票名稱", force=True)
    updateDict(DictName.userStatus, userID, [STATUS.AddName, message])
    
def result(update, context):
    pass

def list(update, context):
    pass

def getText(update, context):
    text = update.message.text
    userID = getUserID(update)
    if userID in userStatus:
        status, message = userStatus[userID]
        print(status, message)
        if status == STATUS.AddName:
            message = Send(update, "請選擇起始日期", reply_markup=telegramcalendar.create_calendar())
            updateDict(DictName.userStatus, userID, [STATUS.SetBeginDate, message])
            updateDict(DictName.addList, userID, text)
        
    pass

def callback(update, context):
    query = update.callback_query
    userID = query.from_user.id
    roomID = query.message.chat_id
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        selected, date = telegramcalendar.process_calendar_selection(update, context, False)
        if selected:
            if userID in userStatus:
                state, message = userStatus[userID]
                if state == STATUS.SetBeginDate:
                    updateDict(DictName.addList, userID, date)
                    telegramcalendar.clearDateButton(query, context)
                    message = Send(update, "請選擇結束日期", reply_markup=telegramcalendar.create_calendar(), chat_id = roomID)
                    updateDict(DictName.userStatus, userID, [STATUS.SetEndDate, message])
                    
                elif state == STATUS.SetEndDate:
                    updateDict(DictName.addList, userID, date)
                    telegramcalendar.clearDateButton(query, context)
                    updateDict(DictName.userStatus, userID, None)

                    name, beginDate, endDate = addList[userID]
                    command = """ INSERT INTO DateList (Name, BeginDate, EndDate) VALUES (?, ?, ?)"""
                    RunDB('Database.db', command, (name, beginDate, endDate))
                    message = Send(update, "{0} 新增成功".format(name), chat_id=roomID)
    pass