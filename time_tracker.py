import datetime
import os.path
import sqlite3
from sqlite3 import Error

from talon import Module, Context

mod = Module()
mod.list("case_list", desc="cases defined by user.")
case_list = {}
print(os.getcwd())
with open(os.path.join(os.getcwd(),r"user\cls_voice_time\cases.txt")) as cases:
    lines = cases.readlines()
    for line in lines:
        split_line = line.rstrip().split(" ")
        case_list[split_line[0]] = split_line[1]
        print("case list",case_list)

ctx_default = Context()
ctx_default.lists["user.case_list"] = case_list

cases = {}
started=False
start_time = ""
stop_time =""

@mod.action_class
class TrackTimeActions:

    def start_tracking(case: str) ->str:
        """Starts time tracking on a case"""
        started=True
        start_time = datetime.datetime.now().strftime("%H:%M:%S")
        connection = create_connection(os.path.join(os.getcwd(),r"user\cls_voice_time\time_tracking.db"))
        start_track(connection, case)
        print(f"started {case} at {start_time}")
        return f"started case {case} at {start_time}"

    def stop_tracking(case: str)->str:
        """Starts time tracking on a case"""
        started=False
        stop_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"stopped {case} at {stop_time} which was started at {start_time}")
        return f"stopped {case} at {stop_time} which was started at {start_time}"


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(db_file)
    except Error as e:
        print(e)
        print(db_file)
    return conn


def start_track(connection, case):
    cursor = connection.cursor()
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        cursor.execute('''insert into time_tracking (case_num, start_time) values(?,?);''', [case, start_time])
        print("added new case.", case, start_time)
        connection.commit()
    except Error as e:
        print(e)

def end_track(connection, case):
    cursor = connection.cursor()
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        cursor.execute('''update time_tracking set end_time = ? where case_num = ?''', [case, start_time])
        print("added new case.", case, start_time)
        connection.commit()
    except Error as e:
        print(e)

def create_tables(connection):
    time_tracking_table = '''create table if not exists time_tracking (
        case_num varchar not null,
        start_time varchar not null,
        end_time varchar
    );'''
    try:
        cursor = connection.cursor()
        cursor.execute(time_tracking_table)
    except Error as e:
        print(e)

if __name__ == '__main__':
    connection = create_connection(os.path.join(os.getcwd(),"time_tracking.db"))
    create_tables(connection)


