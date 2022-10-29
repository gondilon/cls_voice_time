import datetime

from talon import Module, Context
mod = Module()
mod.list("case_list", desc="cases defined by user.")

ctx_default = Context()
ctx_default.lists["user.case_list"] = {
    "david": "21",
    "joe": "22",
    "maria": "23"
}


cases = {}
started=False
start_time = ""
stop_time =""

@mod.action_class
class TrackTimeActions:

    def start_tracking(case: str):
        """Starts time tracking on a case"""
        started=True
        start_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"started {case} at {start_time}")

    def stop_tracking(case: str):
        """Starts time tracking on a case"""
        started=False
        stop_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"stopped {case} at {stop_time} which was started at {start_time}")




def load_cases():
    with open ("cases.txt") as cases:
        lines = cases.readlines()
