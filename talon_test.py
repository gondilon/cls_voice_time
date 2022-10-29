import datetime
import os

case_list = {}
print(os.getcwd())
with open(r"C:\Users\carlm\AppData\Roaming\talon\user\cls_voice_time\cases.txt") as cases:
    lines = cases.readlines()
    for line in lines:
        split_line = line.rstrip().split(" ")
        case_list[split_line[0]] = split_line[1]
    print("case list",case_list)


