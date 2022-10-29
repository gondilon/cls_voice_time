current time:
    app.notify(user.current_time())

track {user.case_list}:
     app.notify(user.start_tracking(user.case_list))

stop {user.case_list}:
    user.stop_tracking(user.case_list)