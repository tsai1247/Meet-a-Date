from typing import Literal
import sqlite3

def RunDB(databaseName: str, command: Literal, parameter = None):
    sql = sqlite3.connect( databaseName )
    cur = sql.cursor()
    if parameter == None:
        cur.execute(command)
    else:
        cur.execute(command, parameter)
    sql.commit()
    ret = None
    if 'select' in command.lower():
        ret = cur.fetchall()
    cur.close()
    sql.close()
    return ret
