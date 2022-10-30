import datetime
import json
import math
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
        conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES |
                                                        sqlite3.PARSE_COLNAMES)
        #print(db_file)
    except Error as e:
        print(e)
        print(db_file)
    return conn

def get_case_list():

    case_list = {}
    #print(os.getcwd())
    with open(os.path.join(config["case_map_path"],"cases.txt"),"r") as cases:
        lines = cases.readlines()
        for line in lines:
            split_line = line.rstrip().split(" ")
            case_list[split_line[0]] = split_line[1]
            #print("case list",case_list)
    return case_list

def load_config():
    with open(os.path.join(os.path.expanduser("~"),config.json), "r") as config_file:
        config_data = json.load(config_file)
        return config_data

config = load_config()

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

        start_time = datetime.datetime.now()
        connection = create_connection(connection_path)
        exists = check_existing_track(connection, case)

        #connection = create_connection(connection_path)
        any_tracked = check_any_track(connection)
        if exists:
            return "Case already being tracked."
        elif any_tracked is not None:
            #print("existing case,",any_tracked)
            #connection = create_connection(connection_path)
            end_track(connection, any_tracked[0][0])
            started = start_track(connection, case)
            # print(f"started {case} at {start_time}")
            return f"Closed case {any_tracked[0][0]} {started}"
        else:

            started = start_track(connection, case)
            #print(f"started {case} at {start_time}")
            return started

    def stop_tracking(case: str)->str:
        """Starts time tracking on a case"""
        started=False
        #print("config: ",config)

        stop_time = datetime.datetime.now().strftime("%H:%M:%S")
        connection = create_connection(connection_path)
        exists = check_existing_track(connection, case)
        if exists:
            connection = create_connection(connection_path)
            ended = end_track(connection,case)
            #print(f"stopped {case} at {stop_time} which was started at {ended}")
            return f"stopped {case} at {stop_time} which was started at {ended}"
        else:
            return "Case not being tracked."

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
        return "report created."



def check_any_track(connection):
    cursor = connection.cursor()
    case_records = cursor.execute('''select * from time_tracking''').fetchall()
    #connection.close()
    if case_records:
        return case_records
    else:
        return None

def create_report():
    report_data = {}

    connection = create_connection(connection_path)
    cases_list = get_case_list()
    #print("cases list,",cases_list)
    for case_name, case_num in cases_list.items():
        case_report = {
            "case_number": case_num,
            "time": "",
        }
        case_records = get_case_records(connection, case_num)
        if case_records:
            for case in case_records:
                if case[-1] == 1:
                    continue
                else:
                    time_diff = time_difference(case[2], case[3])
                    if case[1] in report_data.keys():
                        report_data[case[1]]["time"] += time_diff
                    else:
                        case_report["time"] = time_diff
                        report_data[case[1]] = case_report
                    change_reported_state(connection, case[1])

    #print(report_data)

    with open(os.path.join(os.path.expanduser("~"),config["report_path"],f"{datetime.date.today()}_case_report.txt"), "w") as case_report:
        lines = []
        today = datetime.date.today()
        lines.append(today.strftime("%b %d %Y")+"\n")
        for case, data in report_data.items():
            line = f"Case: {case}, Time: {data['time']} Minutes.\n"
            lines.append(line)
        case_report.writelines(lines)
    return "created report."

def change_reported_state(connection,case):
    cursor = connection.cursor()
    stmt = '''update time_records set reported=1 where case_num = ?'''
    cursor.execute(stmt, [case])
    connection.commit()

def time_difference(start_time, end_time):
    difference = int(round((end_time-start_time).total_seconds()/60))
    unit_diff = math.ceil(difference/6)
    #print(unit_diff)
    return 6*unit_diff

def check_existing_track(connection, case):
    cursor = connection.cursor()
    case_records = cursor.execute('''select * from time_tracking where case_num = ?''', [case]).fetchall()
    #connection.close()
    if case_records:

        return True
    else:
        return False

def get_case_records(connection, case):
    cursor = connection.cursor()
    case_records  = cursor.execute('''select * from time_records where case_num = ?''', [case]).fetchall()
    return case_records

def start_track(connection, case):
    cursor = connection.cursor()
    start_time = datetime.datetime.now()
    try:
        cursor.execute('''insert into time_tracking (case_num, start_time) values(?,?);''', [case, start_time])
        print("added new case.", case, start_time.strftime('%H:%M:%S'))
        connection.commit()
    except Error as e:
        print(e)
    return f"started case {case} at {start_time.strftime('%H:%M:%S')}"

def end_track(connection, case):
    cursor = connection.cursor()
    end_time = datetime.datetime.now()

    try:
        cursor.execute('''update time_tracking set end_time = ? where case_num = ?''', [end_time, case])
        case_record = cursor.execute('''select * from time_tracking where case_num = ?''', [case]).fetchone()
        print(case_record[0])
        cursor.execute('''insert into time_records (case_num, start_time,end_time) values (?,?,?)''', case_record)
        print("added to time records.")
    except Error as e:
        print("case record",e, case)
        return e

    try:
        cursor.execute('''delete from time_tracking where case_num = ?''', [case])

    except Error as e:
        print(e)
        return e

    connection.commit()
    return case_record[1].strftime('%H:%M:%S')

def create_db_tables(connection):
    time_tracking_table = '''create table if not exists time_tracking (
        case_num varchar not null,
        start_time timestamp not null,
        end_time timestamp
    );'''
    records_table = '''
        create table if not exists time_records (
            record_num integer PRIMARY KEY AUTOINCREMENT NOT NULL,
            case_num varchar not null,
            start_time timestamp not null,
            end_time timestamp not null
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
    connection = create_connection(os.path.join(os.getcwd(), "time_tracking.db"))
    create_db_tables(connection)


