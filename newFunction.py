from typing import Literal
import sqlite3

def RunDB(databaseName: str, command: Literal, parameter: tuple):
    sql = sqlite3.connect( databaseName )
    cur = sql.cursor()
    cur.execute(command, parameter)
    sql.commit()
    ret = None
    if 'selece' in command:
        ret = cur.fetchall()
    cur.close()
    sql.close()
    return ret
