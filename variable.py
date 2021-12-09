from enum import Enum

availableSymbol = "🔞❎😐✅♥️"

userStatus = {} # {int : [ STATUs, telegram.Message ] }

class STATUS(Enum):
    AddName = 1
    SetBeginDate = 2
    SetEndDate = 3
    Polling = 4
    
addList = {}    # {int : [Name, datetime, datetime]}

currentPoll = {}    # {int : [buttons, dateTime, availableList]}

currentPollInfo = {}

def updateDict(name: Enum, userID: int, status: any):
    if status == None:
        if name == DictName.userStatus:
            del userStatus[userID]
        elif name == DictName.addList:
            del addList[userID]
        elif name == DictName.currentPoll:
            del addList[userID]
        elif name == DictName.currentPollInfo:
            del addList[userID]

    elif name == DictName.userStatus:
        userStatus.update({userID:status})

    elif name == DictName.addList:
        if userID not in addList:
            addList.update({userID:[]})
        addList[userID].append(status)
    elif name == DictName.currentPoll:
        currentPoll.update({userID:status})
    elif name == DictName.currentPollInfo:
        currentPollInfo.update({userID:status})

class DictName(Enum):
    userStatus = 1
    addList = 2
    currentPoll = 3
    currentPollInfo = 4