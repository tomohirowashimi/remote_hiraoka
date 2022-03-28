# // 20220128 try data back up　→　0212 枚数 R/L 分割
# // 20220227 毎カウント書き込みに変更
# // 20220301 休憩時間考慮　→　0306調整/確認

import threading
import time
import datetime
import tkinter as tk
from dateutil.relativedelta import relativedelta
#import schedule
import pandas as pd
import csv
import sys
import RPi.GPIO as GPIO

class Board():
    def __init__(self):
        self.pin_lh = 5
        self.pin_rh = 22
        self.pin = [self.pin_lh, self.pin_rh]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.myfont = 32
        self.myfont_small = int(self.myfont * 0.5)
        self.myfont_large = int(self.myfont * 1.5)
        self.pad_x = 10
        self.pad_y = 10
        self.fg_label = '#ffffff'
        self.bg_label = '#000000'

        self.file_day = "/home/pi/Documents/monitor/rest_day.csv"
        self.file_night = "/home/pi/Documents/monitor/rest_night.csv"
        self.file_all_indata = '/home/pi/Documents/monitor/indata_all.pkl'

        self.first = True
        self.first_check_lh = True
        self.first_check_rh = True
        now = datetime.datetime.now()

#        self.df_all = pd.read_pickle(self.file_all_indata)
#        self.list_intime = []
        self.list_rest = []
        
        if datetime.time(7, 30) < datetime.datetime.now().time() < datetime.time(19, 30):
            with open(self.file_day, encoding='utf-8', newline='') as f:
                csvreader = csv.reader(f)
                list = [row for row in csvreader]
        else:
            with open(self.file_night, encoding='utf-8', newline='') as f:
                csvreader = csv.reader(f)
                list = [row for row in csvreader]

        for n in range(1, len(list)):
            for m in range(1, 3):
                if list[n][m] == "":
                    rest = now.replace(year=2099, month=1, day=1, hour=8, minute=0)
                else:
                    rest = datetime.datetime.strptime(list[n][m], '%H:%M')
                rest = self.rest_set(rest, now)
                self.list_rest.append(rest)
        self.list_rest.sort() 
        self.restCheckTime = datetime.datetime.now()

#        th_schedule = threading.Thread(target=self.schedule, args=())
#        th_schedule.start()

    def rest_set(self, rest, now):
        rest_base = now.replace(year=1900, month=1, day=1, hour=8, minute=0)
        if rest.year == 2099:
            rest = rest
        elif rest > rest_base:
            rest = rest.replace(year= now.year, month=now.month, day=now.day)
        else:
            rest = rest.replace(year= now.year, month=now.month, day=now.day)
            rest = rest + relativedelta(days=1)   
        return rest

    def in_check(self):
        for i in range(2):
            GPIO.add_event_detect(self.pin[i], GPIO.FALLING, bouncetime=3000)
            GPIO.add_event_callback(self.pin[i], self.process)
                    
    def process(self, pin):
        if self.first == True:
            self.state = False
            
        if pin == self.pin_lh:
            if self.first_check_lh == True:
                self.first_check_lh = False
                self.start_check_lh = 2
                self.startTime_lh = datetime.datetime.now()
                self.before_nowTime = datetime.datetime.now()
                self.result_lh = 1
                self.count_lh = 0
                self.sv_result_lh.set(self.result_lh)
            else:
                if self.start_check_lh == 1:
                    self.start_check_lh = 2
                    self.startTime_lh = datetime.datetime.now()
                    self.before_nowTime = datetime.datetime.now()
                    self.result_lh += 1
                    self.count_lh = 0
                    self.sv_result_lh.set(self.result_lh)
                    self.sv_average_lh.set("")
                    self.sv_new_lh.set("")
                else:
                    self.start_check_rh = 1
                    self.process_lh()
                
        elif pin == self.pin_rh:
            if self.first_check_rh == True:
                self.first_check_rh = False
                self.start_check_rh = 2
                self.startTime_rh = datetime.datetime.now()
                self.before_nowTime = datetime.datetime.now()
                self.result_rh = 1
                self.count_rh = 0
                self.sv_result_rh.set(self.result_rh)
            else:
                if self.start_check_rh == 1:
                    self.start_check_rh = 2
                    self.startTime_rh = datetime.datetime.now()
                    self.before_nowTime = datetime.datetime.now()
                    self.result_rh += 1
                    self.count_rh = 0
                    self.sv_result_rh.set(self.result_rh)
                    self.sv_average_rh.set("")
                    self.sv_new_rh.set("")
                else:
                    self.start_check_lh = 1
                    self.process_rh()

    def process_lh(self):
        lr = "lh"
        self.count_lh += 1
        outcome = self.calculation(self.startTime_lh, self.count_lh, lr)
        self.result_lh += 1
        average = outcome[0]
        new = outcome[1]

        self.sv_result_lh.set(self.result_lh)
        self.sv_average_lh.set(int(average))
        self.sv_new_lh.set(int(new))
    
    def process_rh(self):
        lr = "rh"
        self.count_rh += 1
        outcome = self.calculation(self.startTime_rh, self.count_rh, lr)
        self.result_rh += 1
        average = outcome[0]
        new = outcome[1]

        self.sv_result_rh.set(self.result_rh)
        self.sv_average_rh.set(int(average))
        self.sv_new_rh.set(int(new))

    def calculation(self, startTime, count, lr):
        nowTime = datetime.datetime.now()
        restTime = 0

        for n in range(1, int(len(self.list_rest)/2+1)):
            if self.restCheckTime < self.list_rest[2*n-2]:
                for m in range(2*n-1, len(self.list_rest), 2):
                    if nowTime > self.list_rest[m]:
                        restTime = (self.list_rest[m] - self.list_rest[m-1]).total_seconds()
                        self.restCheckTime = datetime.datetime.now()
                        print(restTime)

        df = pd.read_pickle(self.file_all_indata)     # // 0223 追加　→　0227 見直し
        df = df.append({"lr": lr, "in_time": nowTime, "rest": restTime}, ignore_index=True)
        df.to_pickle(self.file_all_indata)
        
        new = (nowTime - self.before_nowTime).total_seconds()
        self.before_nowTime = nowTime

        adjustTime = 0
        averageSeconds = (nowTime - startTime).total_seconds()
        for n in range(1, int(len(self.list_rest)/2+1)):
            if n == 1:
                if startTime < self.list_rest[2*n-2]:
                    for m in range(2*n-1, len(self.list_rest), 2):
                        if nowTime > self.list_rest[m]:
                            averageSeconds = averageSeconds - (self.list_rest[m] - self.list_rest[m-1]).total_seconds()
            else:
                if self.list_rest[2*n-4] < startTime < self.list_rest[2*n-2]:
                    if startTime < self.list_rest[2*n-3]:
                        adjustTime = (self.list_rest[2*n-3] - startTime).total_seconds()
                    else:
                        adjustTime = 0
                    for m in range(2*n-1, len(self.list_rest), 2):
                        if nowTime > self.list_rest[m]:
                            averageSeconds = averageSeconds - (self.list_rest[m] - self.list_rest[m-1]).total_seconds()
        averageSeconds = averageSeconds - adjustTime
        average = averageSeconds / count

        return (average, new)
        
    def end_button(self):
        for i in range(2):
            GPIO.remove_event_detect(self.pin[i])
        
#        cols = ["lr", "in_time"]
#        df_today = pd.DataFrame(self.list_intime, columns=cols)
#        df = self.df_all.append(df_today)
#        print(df)
#        df.to_pickle(self.file_all_indata)

        self.state_schedule = False
        GPIO.cleanup()
        self.root.destroy()
        print("---end---")
        sys.exit()
        
    def gui(self):
        self.root = tk.Tk()
        self.root.attributes('-zoom', '1')

        self.sv_result_lh = tk.StringVar()
        self.sv_average_lh = tk.StringVar()
        self.sv_new_lh = tk.StringVar()
        self.sv_result_rh = tk.StringVar()
        self.sv_average_rh = tk.StringVar()
        self.sv_new_rh = tk.StringVar()

        title = tk.Label(self.root, text="進捗ボード", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        button_end = tk.Button(self.root, text="終了", command=self.end_button, font=('', self.myfont_small))
        label_lh = tk.Label(self.root, text="LH", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        label_rh = tk.Label(self.root, text="RH", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        label_result = tk.Label(self.root, text="実績（個）", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        label_average = tk.Label(self.root, text="平均（秒）", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        label_new = tk.Label(self.root, text="最新（秒）", font=('', self.myfont), fg=self.fg_label, bg=self.bg_label)
        labelsv_result_lh = tk.Label(self.root, textvariable=self.sv_result_lh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)
        labelsv_average_lh = tk.Label(self.root, textvariable=self.sv_average_lh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)
        labelsv_new_lh = tk.Label(self.root, textvariable=self.sv_new_lh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)
        labelsv_result_rh = tk.Label(self.root, textvariable=self.sv_result_rh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)
        labelsv_average_rh = tk.Label(self.root, textvariable=self.sv_average_rh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)
        labelsv_new_rh = tk.Label(self.root, textvariable=self.sv_new_rh, font=('', self.myfont_large), fg=self.fg_label, bg=self.bg_label)

        title.grid(column=0, row=0, columnspan=2, padx=self.pad_x, pady=self.pad_y)
        button_end.grid(column=2, row=0, padx=self.pad_x, pady=self.pad_y)
        label_lh.grid(column=0, row=1, padx=self.pad_x, pady=self.pad_y)
        label_rh.grid(column=2, row=1, padx=self.pad_x, pady=self.pad_y)
        label_result.grid(column=1, row=2, padx=self.pad_x, pady=self.pad_y)
        label_average.grid(column=1, row=3, padx=self.pad_x, pady=self.pad_y)
        label_new.grid(column=1, row=4, padx=self.pad_x, pady=self.pad_y)
        labelsv_result_lh.grid(column=0, row=2, padx=self.pad_x, pady=self.pad_y)
        labelsv_average_lh.grid(column=0, row=3, padx=self.pad_x, pady=self.pad_y)
        labelsv_new_lh.grid(column=0, row=4, padx=self.pad_x, pady=self.pad_y)
        labelsv_result_rh.grid(column=2, row=2, padx=self.pad_x, pady=self.pad_y)
        labelsv_average_rh.grid(column=2, row=3, padx=self.pad_x, pady=self.pad_y)
        labelsv_new_rh.grid(column=2, row=4, padx=self.pad_x, pady=self.pad_y)

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.configure(bg=self.bg_label)

        self.root.after(100, self.in_check)
        self.root.mainloop()

    def schedule(self):
        schedule.every().day.at("06:00").do(self.end_button)
        schedule.every().day.at("15:53").do(self.end_button)
        
        self.state_schedule = True
        while self.state_schedule:
            schedule.run_pending()
            time.sleep(120)

if __name__ == '__main__':
    board = Board()
    board.gui()
