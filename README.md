# cls_voice_time
 Program for voice tracking of time for CLS,


# Installation instructions

1. Download and install Talon voice from [here](https://talonvoice.com/)
2. Download cls_voice_time from [github](https://github.com/gondilon/cls_voice_time)
3. move cls_voice_time files into AppData/Roaming/talon/user folder.
4. copy config.json into the %USERHOME%/Documents folder.
   1. The paths specificed in config.json are relative to the users home directory
   2. case_map_path defines where cases.txt is store.
   3. report_path defines where generated reports will be stored.
5. Create cases.txt at the path listed in config. 
   1. Each case should be  in [case name] [case number] format, one per line. 
   2. The case name is how you will identify the case in a voice command.
   3. example line: "john" 12-1234. User would say "track case John" to start tracking.
6. When cls_voice_time is run form the first time, the "create tables" command must be run to setup the databse.
