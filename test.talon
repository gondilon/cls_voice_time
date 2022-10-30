current time:
    app.notify(user.current_time())

track case {user.case_list}:
     app.notify(user.start_tracking(user.case_list))

stop case {user.case_list}:
    app.notify(user.stop_tracking(user.case_list))

create tables:
    user.db_tables_create()

create report:
    app.notify(user.report())