from enum import Enum

userStatus = {} # {int : [ STATUs, telegram.Message ] }
class STATUS(Enum):
    AddName = 1
    SetBeginDate = 2
    SetEndDate = 3
    
addList = {}    # {int : [Name, datetime, datetime]}

def updateDict(name: Enum, userID: int, status: any):
    if status == None:
        if name == DictName.userStatus:
            del userStatus[userID]
        elif name == DictName.addList:
            del addList[userID]

    elif name == DictName.userStatus:
        print(type(status))
        userStatus.update({userID:status})

    elif name == DictName.addList:
        if userID not in addList:
            addList.update({userID:[]})
        addList[userID].append(status)

class DictName(Enum):
    userStatus = 1
    addList = 2
