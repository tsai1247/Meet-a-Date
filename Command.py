from datetime import datetime
from os import curdir
from dosdefence import isDos
from function import GetConfig, Send, SendButton, getRoomID, getUserID
from newFunction import RunDB
from variable import *
import telegramcalendar, utils, messages
from telegram import InlineKeyboardMarkup, InlineKeyboardButton


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
    userID = getUserID(update)
    command = """SELECT Name FROM DateList"""
    data = RunDB('Database.db', command, None)
    nameList = []
    buttons = []
    for i in data:
        nameList.append(i[0])

    for name in nameList:
        buttons.append([InlineKeyboardButton(name, callback_data = "{0};{1};{2};{3};{4}".format("resultName", name, datetime.now(), userID, "") )])
    print(buttons)
    SendButton(update, "現在有的投票：", buttons)
    
    pass

def poll(update, context):
    userID = getUserID(update)
    command = """SELECT Name FROM DateList"""
    data = RunDB('Database.db', command, None)
    nameList = []
    buttons = []
    for i in data:
        nameList.append(i[0])

    for name in nameList:
        buttons.append([InlineKeyboardButton(name, callback_data = "{0};{1};{2};{3};{4}".format("pollName", name, datetime.now(), userID, "") )])
    print(buttons)
    SendButton(update, "現在有的投票：", buttons)

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
    (kind, text, dateTimeStamp, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        selected, date = telegramcalendar.process_calendar_selection(update, context, False)
        if selected:
            if userID in userStatus:
                state, message = userStatus[userID]
                if state == STATUS.SetBeginDate:
                    updateDict(DictName.addList, userID, date)
                    telegramcalendar.clearButton(query, context)
                    message = Send(update, "請選擇結束日期", reply_markup=telegramcalendar.create_calendar(), chat_id = roomID)
                    updateDict(DictName.userStatus, userID, [STATUS.SetEndDate, message])
                    
                elif state == STATUS.SetEndDate:
                    updateDict(DictName.addList, userID, date)
                    telegramcalendar.clearButton(query, context)
                    updateDict(DictName.userStatus, userID, None)

                    name, beginDate, endDate = addList[userID]
                    command = """ INSERT INTO DateList (Name, BeginDate, EndDate) VALUES (?, ?, ?)"""
                    RunDB('Database.db', command, (name, beginDate, endDate))
                    message = Send(update, "{0} 新增成功".format(name), chat_id=roomID)
                elif state == STATUS.Polling:
                    if date < currentPollInfo[userID][0] or date > currentPollInfo[userID][1]:
                        userStatus[userID][1][1].edit_text(text = currentPoll[userID][1].split(" ")[0] + " (不可投票)")
                        return
                    command = """ SELECT Available FROM Data WHERE UserID = ? and Name = ? and Date = ?"""
                    data = RunDB('Database.db', command, (userID, currentPoll[userID][3], date))
                    available = '222'
                    if data != None and len(data) != 0:
                        available = data[0][0]
                    else:
                        command = """INSERT INTO Data (UserID, Name, Date, Available) VALUES(?, ?, ?, ?)"""
                        data = RunDB('Database.db', command, (userID, currentPoll[userID][3], date, available))

                    curDate = date.strftime("%Y-%m-%d")
                    buttons = []
                    script = ["早上", "下午", "晚上"]
                    buttons.append([InlineKeyboardButton(s, callback_data = "{0};{1};{2};{3};{4}".format("ignore", s, datetime.now(), userID, "")) for s in script])
                    buttons.append([InlineKeyboardButton(availableSymbol[int(available[s])], callback_data = "{0};{1};{2};{3};{4}".format("setTime", s, datetime.now(), userID, "")) for s in range(3)])
                    updateDict(DictName.currentPoll, userID, [buttons, str(date), available, currentPoll[userID][3]])

                    userStatus[userID][1][1].edit_text(text = curDate,
                        reply_markup = InlineKeyboardMarkup(currentPoll[userID][0])
                    )
    elif kind == "pollName":
        telegramcalendar.clearButton(query, context)
        command = """SELECT Name, BeginDate, EndDate FROM DateList WHERE Name = '{0}'""".format(text)
        data = RunDB('Database.db', command)
        name, beginDate, endDate = data[0]
        message = Send(update, "投票 {0} (From {1} To {2})".format(name, beginDate.split(" ")[0], endDate.split(" ")[0]), reply_markup=telegramcalendar.create_calendar(), chat_id = userID)
        
        updateDict(DictName.currentPollInfo, userID, [datetime.strptime(beginDate, "%Y-%m-%d %H:%M:%S"), datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")] )

        command = """ SELECT Available FROM Data WHERE UserID = ? and Name = ? and Date = ?"""
        data = RunDB('Database.db', command, (userID, text, beginDate))
        available = '222'
        if data != None and len(data) != 0:
            available = data[0][0]
        else:
            command = """INSERT INTO Data (UserID, Name, Date, Available) VALUES(?, ?, ?, ?)"""
            data = RunDB('Database.db', command, (userID, text, beginDate, available))

        date = beginDate.split(" ")[0]
        buttons = []
        script = ["早上", "下午", "晚上"]
        buttons.append([InlineKeyboardButton(s, callback_data = "{0};{1};{2};{3};{4}".format("ignore", s, datetime.now(), userID, "")) for s in script])
        buttons.append([InlineKeyboardButton(availableSymbol[int(available[s])], callback_data = "{0};{1};{2};{3};{4}".format("setTime", s, datetime.now(), userID, "")) for s in range(3)])
        
        message2 = SendButton(update, date, buttons, chat_id=userID)
        
        updateDict(DictName.currentPoll, userID, [buttons, beginDate, available, text])
        updateDict(DictName.userStatus, userID, [STATUS.Polling, [message, message2]])
    elif kind == "setTime":
        command = """UPDATE Data Set Available = ? where UserID = ? and Name = ? and Date = ?"""

        currentPoll[userID][2] = Increase(currentPoll[userID][2], text, currentPoll[userID][3], currentPoll[userID][1])

        RunDB('Database.db', command, (currentPoll[userID][2], userID, currentPoll[userID][3], currentPoll[userID][1]))
        currentPoll[userID][0][1] = [InlineKeyboardButton(availableSymbol[int(currentPoll[userID][2][s])], callback_data = "{0};{1};{2};{3};{4}".format("setTime", s, datetime.now(), userID, "")) for s in range(3)]
        context.bot.edit_message_text(text = currentPoll[userID][1].split(" ")[0],
                chat_id=query.message.chat_id,
                message_id=query.message.message_id,
                reply_markup = InlineKeyboardMarkup(currentPoll[userID][0])
        )
    elif kind == "resultName":
        telegramcalendar.clearButton(query, context, replaceText="關於投票：\n {0}：".format(text))
        command = """SELECT Date, Time, Result FROM Result WHERE Name == ? and Result > 0 ORDER BY Result DESC LIMIT 5"""
        data = RunDB('Database.db', command, (text))
        print(data)

        count = 0
        for result in data:
            count += 1
            curTime = ""
            if result[1] == 0:
                curTime = "上午"
            elif result[1] == 1:
                curTime = "下午"
            elif result[1] == 2:
                curTime = "晚上"
            Send(update, "{0}.\t{1} {2}\t得到{3}分".format(count, result[0].split(" ")[0], curTime, result[2]), chat_id=userID)
        pass


    else:
        telegramcalendar.clearButton(query, context, replaceText = "按鈕過期")
    pass

def Increase(available, text, name, date):
    index = int(text)
    numAvailable = int(available)
    delta = 1
    if index == 0:
        numAvailable = numAvailable + 100
    if index == 1:
        numAvailable = numAvailable + 10
    if index == 2:
        numAvailable = numAvailable + 1
    available = str(numAvailable)
    for i in range(len(available)):
        if available[i] > '4':
            available = available[:i] + '0' + available[i + 1:]
            delta = -4

    command = """SELECT COUNT(*) FROM Result WHERE Name = ? and Date = ? and Time = ?"""
    data = RunDB('Database.db', command, (name, date, index))[0][0]
    if data == 0:
        command = """INSERT INTO Result (Name, Date, Time, Result) VALUES(?, ?, ?, ?)"""
        RunDB('Database.db', command, (name, date, index, 0))

    command = """UPDATE Result SET Result = Result + ? WHERE Name = ? and Date = ? and Time = ?"""
    RunDB('Database.db', command, (delta, name, date, index))
    
    return available
