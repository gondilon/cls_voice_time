import os.path
import sqlite3
from sqlite3 import Error
import datetime


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn


def start_tracking(connection, case):
    cursor = connection.cursor
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        cursor.execute('''insert into time_tracking (case, start_time) values(?,?);''', case, start_time)
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