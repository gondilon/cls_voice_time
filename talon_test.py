import datetime

from talon import Module
mod = Module()

@mod.action_class
class Actions:
    #def find_reverse(): "Begins a reverse search."
    def current_time() ->str:
        "Mangles the input string in the appropriate manner."
        print(datetime.datetime.now().strftime("%H:%M:%S"))
        #return {"current_time": datetime.datetime.now().strftime("%H:%M:%S")}
        return datetime.datetime.now().strftime("%H:%M:%S")


