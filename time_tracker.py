import datetime
import os.path
import sqlite3
from sqlite3 import Error

from talon import Module, Context

mod = Module()
mod.list("case_list", desc="cases defined by user.")


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(db_file)
    except Error as e:
        print(e)
        print(db_file)
    return conn

def get_case_list():

    case_list = {}
    print(os.getcwd())
    with open(os.path.join(os.getcwd(),r"user\cls_voice_time\cases.txt")) as cases:
        lines = cases.readlines()
        for line in lines:
            split_line = line.rstrip().split(" ")
            case_list[split_line[0]] = split_line[1]
            #print("case list",case_list)
    return case_list

ctx_default = Context()
ctx_default.lists["user.case_list"] = get_case_list()
connection_path = os.path.join(os.getcwd(), r"user\cls_voice_time\time_tracking.db")
cases = {}
started=False
start_time = ""
stop_time =""

@mod.action_class
class Actions:

    def start_tracking(case: str) ->str:
        """Starts time tracking on a case"""
        started=True
        start_time = datetime.datetime.now().strftime("%H:%M:%S")
        connection = create_connection(connection_path)
        start_track(connection, case)
        #print(f"started {case} at {start_time}")
        return f"started case {case} at {start_time}"

    def stop_tracking(case: str)->str:
        """Starts time tracking on a case"""
        started=False
        stop_time = datetime.datetime.now().strftime("%H:%M:%S")
        connection = create_connection(connection_path)
        ended = end_track(connection,case)
        #print(f"stopped {case} at {stop_time} which was started at {ended}")
        return f"stopped {case} at {stop_time} which was started at {ended}"

    def db_tables_create() -> str:
        """Starts time tracking on a case"""
        connection = create_connection(connection_path)
        create_db_tables(connection)
        return "tables created."

    def report() -> str:
        """Starts time tracking on a case"""
        #connection = create_connection(connection_path)
        #create_db_tables(connection)
        create_report()
        return "tables created."


def create_report():
    connection = create_connection(connection_path)
    cases_list = get_case_list()
    #print("cases list,",cases_list)
    for case_name, case_num in cases_list.items():
            case_records = get_case_records(connection, case_num)
            if case_records:
                print(datetime.datetime.strptime(case_records[0][2],"%H:%M:%S"))
                print(case_records)
    #with open ("case_report.txt") as case_report:




def get_case_records(connection, case):
    cursor = connection.cursor()
    case_records  = cursor.execute('''select * from time_records where case_num = ?''', [case]).fetchall()
    return case_records

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
    end_time = datetime.datetime.now().strftime("%H:%M:%S")

    try:
        cursor.execute('''update time_tracking set end_time = ? where case_num = ?''', [end_time, case])
        case_record = cursor.execute('''select * from time_tracking where case_num = ?''', [case]).fetchone()
        print(case_record[0])
        cursor.execute('''insert into time_records (case_num, start_time,end_time) values (?,?,?)''', case_record)
        print("added to time records.")
    except Error as e:
        print("case record",e, case)

    try:

        cursor.execute('''delete from time_tracking where case_num = ?''', [case])

    except Error as e:
        print(e)



    connection.commit()
    return case_record[1]
def create_db_tables(connection):
    time_tracking_table = '''create table if not exists time_tracking (
        case_num varchar not null,
        start_time varchar not null,
        end_time varchar
    );'''
    records_table = '''
        create table if not exists time_records (
            record_num integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            case_num varchar not null,
            start_time varchar not null,
            end_time varchar not null
        );
    '''
    try:
        cursor = connection.cursor()
        cursor.execute(time_tracking_table)
        cursor.execute(records_table)
    except Error as e:
        print(e)
    connection.commit()

if __name__ == '__main__':
    connection = create_connection(os.path.join(os.getcwd(),"time_tracking.db"))
    create_db_tables(connection)


